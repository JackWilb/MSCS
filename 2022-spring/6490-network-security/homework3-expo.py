# m^d mod n
def expo(m, d, n):
  # make sure m is in range of [0, n-1]
  m = m % n
  
  result = 1
  while d > 0:

    # If odd, multiply result by m
    if(d & 1 == 1):
      result = (result * m) % n
    
    # Even by here so bitshift and square
    d = d >> 1
    m = (m ** 2) % n
  
  return result

print(expo(0,0,1))