import numpy as np
import random

# np.random.seed(42)

# def make_sample(sample_size):
#     # Usually this probabiliy is not known. Setting it here for simulation purposes.
#     pA = 0.55
#     return np.random.binomial(
#         n = sample_size,
#         p = pA)

# #10 mil, 52% A, 48% B, 100 times of sample sizes 20, 100, 400
# sm = [make_sample(20) > 10 for i in range(100)]
# md = [make_sample(100) > 50 for i in range(100)]
# lg = [make_sample(400) > 200 for i in range(100)]

# print(sum(sm) / 100)
# print(sum(md) / 100)
# print(sum(lg) / 100)

# ninety_1000 = []
# for i in range(1000):
#     n = 180
#     ninety_1000.append(sum([make_sample(n) > n/2 for i in range(1000)]) / 1000)
# print(sum(ninety_1000) / 1000)


bias = 5500000
total = 10000000
ten_mil_test = ([1] * bias) + ([0] * (total - bias))

total = 0
for i in range(100):
    total += 1 if sum(random.sample(ten_mil_test, 20)) > 10 else 0

print(total / 100)

total = 0
for i in range(100):
    total += 1 if sum(random.sample(ten_mil_test, 100)) > 50 else 0

print(total / 100)

total = 0
for i in range(100):
    total += 1 if sum(random.sample(ten_mil_test, 400)) > 200 else 0

total = 0
for i in range(100):
    total += 1 if sum(random.sample(ten_mil_test, 400)) > 200 else 0

print(total / 100)

total = 0
for i in range(100):
    total += 1 if sum(random.sample(ten_mil_test, 180)) > 180/2 else 0

print(total / 100) 
