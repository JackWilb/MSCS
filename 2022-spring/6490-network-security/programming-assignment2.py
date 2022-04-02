import socket
import threading
import secrets
import pickle
import hmac
import hashlib
import base64
from OpenSSL import crypto
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

import random
PORT = random.randint(8080, 60000)

# Make 256 bit nonce
def make_nonce():
  return secrets.randbits(256)

def make_encrypted_nonce(cert, nonce):
  pub_key = cert.get_pubkey().to_cryptography_key()
  nonce_bytes = nonce.to_bytes(32, 'little')

  encrypted_nonce = pub_key.encrypt(
    nonce_bytes,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

  return encrypted_nonce

def decrypt_nonce(encrypted_nonce, key):
  priv_key = key.to_cryptography_key()

  return int.from_bytes(priv_key.decrypt(
    encrypted_nonce,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  ), "little")

def sign_with_private(input, key):
  priv_key = key.to_cryptography_key()
  return priv_key.sign(
    input,
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
  )

def verify_with_public(input, message, cert):
  pub_key = cert.get_pubkey().to_cryptography_key()
  return pub_key.verify(
    input,
    message,
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
  ) == None

def aes_encrypt(data, key):
  return Fernet(base64.urlsafe_b64encode(key)).encrypt(data)

def aes_decrypt(cypher, key):
  return Fernet(base64.urlsafe_b64encode(key)).decrypt(cypher)

# Encodes message for sending to socket
def message_encode(message_dict):
  return pickle.dumps(message_dict)

# Decodes message received on socket
def message_decode(message_bytes):
  return pickle.loads(message_bytes)

def certIsValid(cert):
  cert_store = crypto.X509Store()
  cert_store.add_cert(cert)
  store_ctx = crypto.X509StoreContext(cert_store, cert)
  verification_status = store_ctx.verify_certificate()
  return verification_status == None

def generate_hmac(all_messages, secret, source):
  combined_bytes = b''

  for message in all_messages:
    combined_bytes += pickle.dumps(message)

  combined_bytes += source.encode()

  output_hmac = hmac.new(secret.to_bytes(32, "little"), combined_bytes, hashlib.sha1)
  return output_hmac.digest()

def hmacs_match(hmac1, hmac2):
  return hmac1 == hmac2

def generate_key(shared_secret):
    pwd = shared_secret
    salt = secrets.token_bytes(16)

    key_func = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=10 ** 6
    )

    key = key_func.derive(shared_secret.to_bytes(32, "little"))
    return key

def get_two_keys(shared_secret):
  k1 = generate_key(shared_secret)
  k2 = generate_key(shared_secret)
  return k1, k2



def threaded(fn):
  def wrapper(*args, **kwargs):
    threading.Thread(target=fn, args=args, kwargs=kwargs).start()
  return wrapper

class Node():
  def __init__(self, name):
    self.name = name
    self.all_messages = []

    # Create the socket for each node, a unix file
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if self.name == "Bob":
      # Get cert for Bob
      with open("programming-assignment2-B.crt") as f:
        self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

      with open("programming-assignment2-B.key") as f:
        self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())

      self.sock.bind(("localhost", PORT))
      self.sock.listen()
    else:
      # Get cert for Alice
      with open("programming-assignment2-A.crt") as f:
        self.cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

      with open("programming-assignment2-A.key") as f:
        self.key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())

      self.sock.connect(("localhost", PORT))

  @threaded
  def server_start(self):
    print("starting", self.name)

    while True:
      ##### START HANDSHAKE

      # Receive message 1 (cypher and Alice's nonce)
      conn, addr = self.sock.accept()
      message = message_decode(conn.recv(1024))
      chosen_cypher = message

      if chosen_cypher == "AES":
        print("Got client hello, server accepts cypher")
      else:
        print("Got client hello, server rejects cypher")
        print(chosen_cypher)
        return

      self.all_messages.append(message)



      # Send message 2
      message = crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert)
      conn.send(message_encode(message))
      self.all_messages.append(message)



      # Receive message 3
      message = message_decode(conn.recv(4096))
      client_cert = crypto.load_certificate(crypto.FILETYPE_PEM, message[0])
      if certIsValid(client_cert):
        print("Server received valid certificate")
      else:
        print("Server received invalid certificate")
        return

      RA = decrypt_nonce(message[1], self.key)
      self.all_messages.append(message)



      # Send message 4
      RB = make_nonce()
      encrypted_RB = make_encrypted_nonce(client_cert, RB)
      message = encrypted_RB
      conn.send(message_encode(message))
      self.all_messages.append(message)

      shared_secret = RA ^ RB

      print()
      print(f"server: {RA}, {RB}")
      print(f"server shared secret: {shared_secret}")



      # Receive message 5
      message = conn.recv(2048)
      received_hmac = message



      # Send message 6
      client_hmac = generate_hmac(self.all_messages, shared_secret, 'CLIENT')
      server_hmac = generate_hmac(self.all_messages, shared_secret, 'SERVER')
      message = server_hmac
      conn.send(message)

      # Check client hmac vs hmac
      if hmacs_match(client_hmac, received_hmac):
        print("server: Successfully authenticated")
      else:
        print("server: Failed to authenticated, HMAC didn't match")


      ##### HANDSHAKE DONE
      ##### START KEY EXCHANGE

      server_auth_key, server_encrypt_key = get_two_keys(shared_secret)

      # Receive message 1
      message = message_decode(conn.recv(4096))
      unencrypted_message = [aes_decrypt(x, shared_secret.to_bytes(32, "little")) for x in message]

      client_auth_key_verified = verify_with_public(unencrypted_message[2], unencrypted_message[0], client_cert)
      client_encrypt_key_verified = verify_with_public(unencrypted_message[3], unencrypted_message[1], client_cert)

      if client_auth_key_verified and client_encrypt_key_verified:
        print("client verified after key exchange")
      else:
        print("client not verified after key exchange")
        return

      client_auth_key = unencrypted_message[0]
      client_encrypt_key = unencrypted_message[1]



      # Send message 2
      server_auth_key, server_encrypt_key = get_two_keys(shared_secret)
      KB_priv_encrypted_keys = [sign_with_private(x, self.key) for x in [unencrypted_message[0], unencrypted_message[1]]]

      unencrypted_message = [server_auth_key, server_encrypt_key, *KB_priv_encrypted_keys]
      message = [aes_encrypt(x, shared_secret.to_bytes(32, "little")) for x in unencrypted_message]
      conn.send(message_encode(message))



      ##### KEY EXCHANGE DONE
      ##### START DATA TRANSFER

      # Receive message 1
      message = message_decode(conn.recv(4096))
      unencrypted_message = [aes_decrypt(x, server_encrypt_key) for x in message]
      filename = unencrypted_message[0]
      verified = Fernet(base64.b64encode(client_auth_key)).decrypt(unencrypted_message[1]) == filename

      if not verified:
        print("signature mismatch, message 1")

      

      # Send message 2
      with open(filename.decode(), 'rb') as f:
        message = aes_encrypt(f.read(), client_encrypt_key)
        conn.send(message)

      while True:
        data = conn.recv(1024)
        print(data)

        if data == b'':
          self.sock.close()
          return

  @threaded
  def client_start(self):
    print("starting", self.name)

    ##### START HANDSHAKE

    # Send message 1
    chosen_cypher = "AES" 
    message = chosen_cypher
    self.sock.send(message_encode(message))
    self.all_messages.append(message)



    # Receive message 2
    message = message_decode(self.sock.recv(2048))
    server_cert = crypto.load_certificate(crypto.FILETYPE_PEM, message)
    if certIsValid(server_cert):
      print("Client received valid certificate")
    else:
      print("Client received invalid certificate")
      return
    self.all_messages.append(message)



    # Send message 3
    client_cert = crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert)
    RA = make_nonce()
    encrypted_RA = make_encrypted_nonce(server_cert, RA)
    message = [client_cert, encrypted_RA]
    self.sock.send(message_encode(message))
    self.all_messages.append(message)



    # Receive message 4
    message = message_decode(self.sock.recv(4096))
    RB = decrypt_nonce(message, self.key)
    self.all_messages.append(message)

    shared_secret = RA ^ RB

    print()
    print(f"client: {RA}, {RB}")
    print(f"client shared secret: {shared_secret}")


    # Send message 5
    client_hmac = generate_hmac(self.all_messages, shared_secret, 'CLIENT')
    server_hmac = generate_hmac(self.all_messages, shared_secret, 'SERVER')
    message = client_hmac
    self.sock.send(message)



    # Receive message 6
    message = self.sock.recv(2048)
    received_hmac = message


    # Check server hmac vs hmac
    if hmacs_match(server_hmac, received_hmac):
      print("client: Successfully authenticated")
    else:
      print("client: Failed to authenticated, HMAC didn't match")


    ##### HANDSHAKE DONE
    ##### START KEY EXCHANGE

    # Send message 1
    client_auth_key, client_encrypt_key = get_two_keys(shared_secret)
    KA_priv_encrypted_keys = [sign_with_private(x, self.key) for x in [client_auth_key, client_encrypt_key]]
    
    unencrypted_message = [client_auth_key, client_encrypt_key, *KA_priv_encrypted_keys]
    message = [aes_encrypt(x, shared_secret.to_bytes(32, "little")) for x in unencrypted_message]
    self.sock.send(message_encode(message))



    # Receive message 2
    message = message_decode(self.sock.recv(4096))
    unencrypted_message = [aes_decrypt(x, shared_secret.to_bytes(32, "little")) for x in message]

    server_auth_key, server_encrypt_key = unencrypted_message[0], unencrypted_message[1]

    client_auth_key_verified = verify_with_public(unencrypted_message[2], client_auth_key, server_cert)
    client_encrypt_key_verified = verify_with_public(unencrypted_message[3], client_encrypt_key, server_cert)

    if client_auth_key_verified and client_encrypt_key_verified:
      print("server verified after key exchange")
    else:
      print("server not verified after key exchange")
      return



    ##### KEY EXCHANGE DONE
    ##### START DATA TRANSFER

    # Send message 1
    filename = "programming-assignment2-50KB.txt".encode()
    signed_filename = Fernet(base64.b64encode(client_auth_key)).encrypt(filename)
    unencrypted_message = [filename, signed_filename]
    message = [aes_encrypt(x, server_encrypt_key) for x in unencrypted_message]
    self.sock.send(message_encode(message))



    # Receive message 2
    message = self.sock.recv(1024 * 1024 * 1024 * 8)
    file_data = aes_decrypt(message, client_encrypt_key)
    
    with open("programming-assignment2-received-data.txt", "wb") as f:
      f.write(file_data) 



    # Send end message to server and close socket
    self.sock.send(b"")
    self.sock.close()




    



# Driver program
bob = Node("Bob")
alice = Node("Alice")

bob.server_start()
alice.client_start()
