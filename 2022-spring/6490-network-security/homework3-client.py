import socket
expo = __import__('homework3-expo')

g = 1907
p = 784313
Sa = 160031

HOST = 'localhost'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  Sa_g = expo.expo(g, Sa, p)
  print(f'Client, Alice, sending {Sa_g}')
  s.sendall(Sa_g.to_bytes(Sa_g.bit_length(), 'big'))

  data = s.recv(1024)
  Sb_g = int.from_bytes(data, 'big')
  print(f'Client, Alice, received {Sb_g}')

  SaSb_g = expo.expo(Sb_g, Sa, p)
  print(f'Client, Alice, computes key as {SaSb_g}')