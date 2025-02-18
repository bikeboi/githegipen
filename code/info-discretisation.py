"""Code for the info-theory blog post about discretisation"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('ticks')


n_points = 10000
alpha = np.linspace(0, 1,)[1:-1]

cond_ent = (1/2) * np.log2(alpha - alpha**2)
mi = 0 - cond_ent

alpha_tend = np.linspace(1e-1, 1, 1_000_000, endpoint=False)
h_Y_B = np.log2(1 - alpha_tend)
plt.plot(alpha_tend, h_Y_B)
plt.xlabel('$\\alpha$')
plt.ylabel('$\\log(1-\\alpha)$')

plt.savefig('log_tend.png', dpi=300)

plt.show()

"""
ax1 = plt.gca()
ax1.plot(alpha, cond_ent, color='red')
ax1.set_xlabel('$\\alpha$')
ax1.set_ylabel('Conditional Entropy', color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.plot(alpha, mi, color='blue')
ax2.set_ylabel('Mutual Information', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

plt.savefig('continous_partition_condent_mi.png', dpi=300)

plt.show()
"""