"""Draws the Sprint 1 burndown chart and saves it as burndown.png.

Run:  python burndown.py
Numbers match the 'Sprint 1 Progress' table in user_stories.md.
"""

import matplotlib.pyplot as plt
import numpy as np

TOTAL_POINTS = 30
days = np.arange(0, 11)  # day 0 to day 10

# Ideal line: equal work every day, straight from 30 down to 0
ideal = np.linspace(TOTAL_POINTS, 0, len(days))

# Actual story points left at the end of each day
actual = [30, 30, 27, 25, 20, 17, 17, 12, 8, 3, 0]

plt.figure(figsize=(9, 5))
plt.plot(days, ideal, '--', color='gray', label='Ideal')
plt.plot(days, actual, 'o-', color='#8e1b1b', linewidth=2, label='Actual')

for d, pts in zip(days, actual):
    plt.annotate(str(pts), (d, pts), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=9)

plt.annotate('Researching blood\ncompatibility rules', xy=(6, 17), xytext=(6.8, 23),
             arrowprops={'arrowstyle': '->'}, fontsize=9)

plt.title('Sprint 1 Burndown Chart: Blood Donor Finder')
plt.xlabel('Sprint Day')
plt.ylabel('Story Points Remaining')
plt.xticks(days)
plt.ylim(0, TOTAL_POINTS + 4)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('burndown.png', dpi=150)
print('Saved burndown.png')
