state = [x for x in range(256, 0, -1)]
x = 0
y = 0
def rc4init(key):
  j = 0
  k = 0

  for i in range(256):
    t = state[i]
    k += (ord(key[j]) + t)
    k = k % 256
    state[i] = state[k]
    state[k] = t
    j = (j + 1) % len(key)

  x = 0
  y = 0

  return x, y


def rc4step(x, y, get, keystream):
  y += state[++x]
  y = y % 256
  t = state[y]
  state[y] = state[x]
  state[x] = t;

  if get:
    return keystream.append(state[(state[x] + state[y]) % 256])
  return x, y

x,y = rc4init("qwert")

# Skip 512 octets
for i in range(512):
  x, y = rc4step(x, y, False, [])

# encode and print string
keystream = []
plaintext = "This class is cool."

for a in plaintext:
  rc4step(x, y, True, keystream)

# xor the keystream with the plaintext and print
for pos in range(len(plaintext)):
  print(hex(ord(plaintext[pos]) ^ keystream[pos])[2:], end=",")

print()
