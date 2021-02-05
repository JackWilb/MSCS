import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd

## Q1.1
# Generate data
df1 = np.array(range(1,201))

# Create plot
fig1 = plt.figure()
ax1 = fig1.add_axes([0,0,1,1])
bp = ax1.boxplot(df1)
plt.show()


## Q1.2
# Generate data
df2 = np.array([random.random() for x in range(0, 10000)])

# Create plot
fig2,ax2 = plt.subplots(1,1)

ax2.hist(df2, bins = 20)
ax2.set_title("histogram of 10,000 random numbers")
ax2.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax2.set_xlabel('Random Value')
ax2.set_ylabel('Occurrences')
plt.show()