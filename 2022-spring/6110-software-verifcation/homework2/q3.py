def bubblesort(arr):
  j = 0
  t = -10000

  while (t != arr[0]):
    t = arr[0]
    
    for j in range(1, len(arr)):
      print(arr[j-1], arr[j], arr[j-1] > arr[j], arr)
      if arr[j-1] > arr[j]:
        t = arr[j-1]
        arr[j-1] = arr[j]
        arr[j] = t

    print()

  return arr

print(bubblesort([1, 1, 0, 0]))
