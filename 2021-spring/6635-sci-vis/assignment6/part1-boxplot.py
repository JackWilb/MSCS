import matplotlib.pyplot as plt
import random
import numpy as np

## Q1.1
# Generate data
df1_1 = np.array([random.random() for x in range(0, 10000)])

# Create plot
fig1_1,ax1_1 = plt.subplots()

ax1_1.boxplot(df1_1)
ax1_1.set_title("Boxplot for 10000 random numbers")
ax1_1.set_xticks([])
ax1_1.set_yticks([0, .2, .4, .6, .8, 1])
ax1_1.set_ylabel('Values')
plt.show()
