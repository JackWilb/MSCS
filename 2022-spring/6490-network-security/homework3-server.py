import socket
expo = __import__('homework3-expo')

g = 1907
p = 784313
Sb = 12077

HOST = 'localhost'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()

  while True:
    conn, addr = s.accept()
    with conn:
      while True:
        data = conn.recv(1024)
        if not data:
          break

        Sa_g = int.from_bytes(data, 'big')
        print(f'Server, Bob, received {Sa_g}')

        Sb_g = expo.expo(g, Sb, p)
        print(f'Server, Bob, sending {Sb_g}')
        conn.sendall(Sb_g.to_bytes(Sb_g.bit_length(), 'big'))

        SaSb_g = expo.expo(Sa_g, Sb, p)
        print(f'Server, Bob, computes key as {SaSb_g}')
