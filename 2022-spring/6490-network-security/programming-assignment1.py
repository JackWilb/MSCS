import socket
import threading
import json
import uuid
import os
import base64
import ast
import pickle
from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.padding import PKCS7

# Makes 8 byte = 64 bit key
def make_key():
  return os.urandom(8)

def make_nonce():
  return uuid.uuid4().int & (1<<64)-1

# Encodes message for sending to socket
def message_encode(message_dict):
  return pickle.dumps(message_dict)

# Decodes message received on socket
def message_decode(message_bytes):
  return pickle.loads(message_bytes)

# Sends JSON message to a socket.
# Keep retrying if there is a problem (e.g. the owner of the socket isn't accepting)
def send_message(message, to):
  sent = False
  while not sent:
    try:         
      with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(f"{to}.sock")
        s.send(message_encode(message))
      sent = True
    except:
      pass

# Triple DES encryption with ECB
def encrypt(message, key):
  # Encode the string/list in bytes
  plaintext = message

  # Add necessary padding
  padder = PKCS7(64).padder()
  padded_plaintext = padder.update(plaintext) + padder.finalize()

  # Encrypt the blocks
  encryptor = Cipher(TripleDES(key), ENCRYPTION_MODE).encryptor()
  ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

  return ciphertext

def decrypt(ciphertext, key):
  # Make the decryption class
  decryptor = Cipher(TripleDES(key), ENCRYPTION_MODE).decryptor()

  # Decrypt the message
  padded_message = decryptor.update(ciphertext) + decryptor.finalize()

  # Remove the padding
  unpadder = PKCS7(64).unpadder()
  message = unpadder.update(padded_message) + unpadder.finalize()

  return message

# Helper function to send blank messages to all so they quit their while loops
def shutdown():
  send_message({}, "Alice")
  send_message({}, "Bob")
  send_message({}, "KDC")

# Wrapper to make each person a thread so they can run in parallel
def threaded(fn):
  def wrapper(*args, **kwargs):
    threading.Thread(target=fn, args=args, kwargs=kwargs).start()
  return wrapper

# Make some global objects for keys so that the may be shared between clients and KDC
KA = make_key()
KB = make_key()
KAB = make_key()

TRUDY_REPLAY_PAYLOAD = None

class Node():
  def __init__(self, name):
    # Set name and get the keys that the client would have
    self.name = name
    self.running = False

    if self.name == "Alice":
      self.KA = KA
    elif self.name == "Bob":
      self.KB = KB
    elif self.name == "KDC":
      self.KA = KA
      self.KB = KB
      self.KAB = KAB

    # Create the socket for each node, a unix file
    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.sock.bind(f"{self.name}.sock")
    self.sock.listen()

  # Here is the thread that allows the nodes to run in parallel
  @threaded
  def start(self, intruder = False):
    self.running = True
    global TRUDY_REPLAY_PAYLOAD
    print(f"Starting {self.name}")

    if not intruder:
      # Set USING_NB true
      USING_NB = True
    else:
      # SET USING_NB false
      USING_NB = False


    # Kick off the exchange when alice starts
    if self.name == "Alice":
      if not intruder:
        # Message 1: "I want to talk to you"
        send_message({"1": ["Alice", "Bob"]}, "Bob")
      else:
        print('here')
        # Start Trudy's replay attack
        self.first_message = True
        send_message({"5": TRUDY_REPLAY_PAYLOAD}, "KDC")

    # Start point for Bob and KDC.
    # Loop to wait for messages
    while True:
      conn, addr = self.sock.accept()
      data = conn.recv(1024)

      # Decode the python bytes message back to JSON
      message_dict = message_decode(data)
      print(message_dict)

      # if the dict received is empty, close the socket and terminate
      if len(message_dict.keys()) == 0:
        self.running = False
        break

      if "1" in message_dict.keys():
        # If we're not the intended recipient, raise an error
        if self.name != message_dict["1"][1]:
          raise Exception("I'm not the intended recipient, breaking.")

        # Else if we are the recipient, respond to the sender with an encoded nonce.
        # Keep track of the nonce we send so we can verify later
        self.most_recent_nonce = make_nonce()
        payload = encrypt(self.most_recent_nonce.to_bytes(8, 'big'), self.KB)

        # Send the encrypted nonce to Alice
        send_message({"2": payload}, "Alice")
      
      elif "2" in message_dict.keys():
        # Keep track of the nonce we send so we can verify later
        self.most_recent_nonce = make_nonce()
        N1 = self.most_recent_nonce

        # Get Bob's encrypted nonce
        KB_NB = message_dict["2"]

        send_message(
          {"3": [N1, ["Alice", "Bob"], KB_NB]},
          "KDC"
        )

      elif "3" in message_dict.keys():
        # Get the required piece for message 4 from message 3
        if USING_NB:
          NB = decrypt(message_dict["3"][2], self.KB)

        N1 = message_dict["3"][0]

        # Encrypt the ticket with Bob's key and the entire payload with Alice's key
        if USING_NB:
          ticket = [encrypt(self.KAB, self.KB), encrypt("Alice".encode("ascii"), self.KB), encrypt(NB, self.KB)]
        else:
          ticket = [encrypt(self.KAB, self.KB), encrypt("Alice".encode("ascii"), self.KB)]
        payload = [encrypt(N1.to_bytes(8, 'big'), self.KA), encrypt("Bob".encode("ascii"), self.KA), encrypt(self.KAB, self.KA), list(map(lambda x: encrypt(x, self.KA), ticket))]

        send_message({"4": payload}, "Alice")

      elif "4" in message_dict.keys():
        # Get the data from the message
        decrypted_data = list(map(lambda x: decrypt(x, self.KA), message_dict["4"][:3]))
        N1 = int.from_bytes(decrypted_data[0], "big")
        who = decrypted_data[1].decode("ascii")
        self.KAB = decrypted_data[2]

        decrypted_data = list(map(lambda x: decrypt(x, self.KA), message_dict["4"][3]))
        ticket = decrypted_data

        # Check that N1 matches
        if N1 != self.most_recent_nonce:
          raise Exception("Integrity issue, N1 mismatch")

        # Check that who matches
        if who != "Bob":
          raise Exception("Shared key is not to Bob")

        # Make N2 and encrypt
        self.most_recent_nonce = make_nonce()
        N2 = self.most_recent_nonce
        KAB_N2 = encrypt(self.most_recent_nonce.to_bytes(8, "big"), self.KAB)

        # Save ticket for Trudy later
        if not TRUDY_REPLAY_PAYLOAD:
          TRUDY_REPLAY_PAYLOAD = [ticket, KAB_N2]

        payload = [ticket, KAB_N2]
        send_message({"5": payload}, "Bob")

      elif "5" in message_dict.keys():
        # Decrypt ticket to get KAB and N2
        ticket = list(map(lambda x: decrypt(x, self.KB), message_dict["5"][0]))

        # Check ticket is valid by checking Nb
        if USING_NB and int.from_bytes(ticket[2], "big") != self.most_recent_nonce:
          raise Exception("NB mismatch, breaking")

        # If ticket is valid, set KAB
        self.KAB = ticket[0]

        # Use KAB to get N2
        N2 = int.from_bytes(decrypt(message_dict["5"][1], self.KAB), "big")

        # Generate N3
        if hasattr(self, "most_recent_nonce"):
          self.oldN3 = self.most_recent_nonce
        self.most_recent_nonce = make_nonce()
        N3 = self.most_recent_nonce

        payload = [encrypt(int(N2 - 1).to_bytes(8, "big"), self.KAB), encrypt(N3.to_bytes(8, "big"), self.KAB)]
        send_message({"6": payload}, "Alice")

      elif "6" in message_dict.keys():
        if not intruder:
          # Decrypt message and get N2-1 and N3
          decrypted_data = list(map(lambda x: decrypt(x, self.KAB), message_dict["6"]))
          N2_1 = int.from_bytes(decrypted_data[0], "big")
          N3 = int.from_bytes(decrypted_data[1], "big")

          # Check N2 - 1 is what we expect
          if N2_1 != self.most_recent_nonce - 1:
            raise Exception("Bob didn't send N2 - 1, breaking")

          payload = encrypt(int(N3 - 1).to_bytes(8, "big"), self.KAB)
          send_message({"7": payload}, "Bob")

        # Trudy's replay
        else:
          if self.first_message:
            self.first_message = False
            encrypt_KAB_N3 = message_dict["6"][1]

            ticket = TRUDY_REPLAY_PAYLOAD[0]

            send_message({"5": [ticket, encrypt_KAB_N3]}, "Bob")
          
          else: 
            encrypt_KAB_N3_1 = message_dict["6"][0]

            send_message({"7": encrypt_KAB_N3_1}, "Bob")

      elif "7" in message_dict.keys():
        # Get N3 - 1
        N3_1 = int.from_bytes(decrypt(message_dict["7"], self.KAB), "big")

        # Add check for old N3, happens when Bob makes 2 connections (replay), we want the first n3
        if N3_1 != self.oldN3 - 1:
          print("Trudy successfully tricked Bob")

        # Check that N3 - 1 is what we expect
        elif N3_1 != self.most_recent_nonce - 1:
          raise Exception("Alice didn't send N3 - 1, breaking")

        # If all successful, we've got to the end of the protocol with a shared key
        # Quit for now
        print("Got to the end of the message chain")
        shutdown()

# Initialize the 3 nodes
alice = Node("Alice")
bob = Node("Bob")
kdc = Node("KDC")

# Start the extended protocol
print()
print("Extended Needham-Schroeder ECB")
ENCRYPTION_MODE = modes.ECB()
alice.start()
bob.start()
kdc.start()

# Wait until all parties have stopped running
while alice.running or bob.running or kdc.running:
  continue

print()
print("TRUDY_REPLAY_PAYLOAD", TRUDY_REPLAY_PAYLOAD)
# Start the original protocol ECB
ENCRYPTION_MODE = modes.ECB()
print("Original Needham-Schroeder ECB")
alice.start(True) #Alice here is trudy...
bob.start(True)
kdc.start(True)

# Wait until all parties have stopped running
while alice.running or bob.running or kdc.running:
  continue

print()
# Start the original protocol CBC
ENCRYPTION_MODE = modes.CBC(make_key())
print("Original Needham-Schroeder CBC")
alice.start(True)
bob.start(True)
kdc.start(True)
