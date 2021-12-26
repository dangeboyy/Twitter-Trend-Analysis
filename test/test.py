import numpy as np
import matplotlib.pyplot as plt

positive = [20,43,76,123,9,4,75,65,16,56]
negative = [12,45,23,43,65,23,87,23,65,45]
neutral = [23,43,54,23,34,12,54,65,34,65]

data = [positive,
negative,
neutral]

X = np.arange(10)
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.00, data[0], color = 'b', width = 0.25)
ax.bar(X + 0.25, data[1], color = 'g', width = 0.25)
ax.bar(X + 0.50, data[2], color = 'r', width = 0.25)
plt.show()