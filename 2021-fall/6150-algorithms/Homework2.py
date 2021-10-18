def fibonacci(k):
    if k == 0 or k == 1:
        return 1
    else:
        return fibonacci(k - 1) + fibonacci(k - 2)

import timeit

start = timeit.default_timer()
fibonacci(45)
stop1 = timeit.default_timer()
fibonacci(50)
stop2 = timeit.default_timer()
fibonacci(55)
stop3 = timeit.default_timer()

print('Fibonacci 45: ', stop1 - start)
print('Fibonacci 50: ', stop2 - stop1)
print('Fibonacci 55: ', stop3 - stop2)


