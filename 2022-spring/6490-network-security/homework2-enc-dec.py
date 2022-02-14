import sys
import random
random.seed(999)

# Quit if not 8 chars
if (len(sys.argv) != 10):
  print("wrong num of args: .py encrypt/decrypt a b c d e f g h")
  exit(1)

# Get input chars
input = [ord(x) for x in sys.argv[2:10]]
print("input:", [chr(c) for c in input])

# Get key
key = [ord(x) for x in "secretos"]

# Substitution tables
subst = [list(range(256))] * 8
for i in range(8): 
  random.shuffle(subst[i])

# encrypt
if sys.argv[1] == "encrypt":
  for a in range(16):
    for i in range(len(input)):
      # xor
      input[i] = input[i] ^ key[i]
      # substitute
      input[i] = subst[i][input[i]]
      # permute
      leftmost_bit = (input[i] >> 7)
      right_bits = ((input[i] << 1) % (1 << 8))
      input[i] = right_bits | leftmost_bit

    print(input)


# Decrypt
elif sys.argv[1] == "decrypt":
  for a in range(16):
    for i in range(len(input)):
      # permute
      rightmost_bit = (input[i] & 1) << 7
      left_bits = (input[i]) >> 1
      input[i] = rightmost_bit | left_bits
      # substitute
      input[i] = subst[i].index(input[i])
      # xor
      input[i] = input[i] ^ key[i]

    print(input)
      
else:
  print("must encrypt or decrypt")
  exit(1)

input = [chr(c) for c in input]
print("output: ", " ".join(input))


