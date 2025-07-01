import matplotlib.pyplot as plt

values = [
    1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 1, 1, 4, 3, 1, 1, 2, 3, 2, 4,
    4, 3, 4, 3, 3, 4, 3, 4, 3, 2, 1, 2, 3, 4, 4, 2, 2, 3, 4, 2,
    2, 3, 3, 4, 3, 4, 3, 2, 2, 1, 1, 3, 2, 3, 3, 4, 3, 4, 5,
    4, 3, 3, 4, 3, 2, 4, 4, 3, 2, 2, 3, 2, 2, 3, 2,
    4, 3, 2, 3, 4
]

# Feedback indices
indices = list(range(1, len(values) + 1))

# Plot both line plot and histogram in one figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5))

# Line plot
ax1.plot(indices, values, marker='o', linestyle='-')
ax1.set_title('Feedback Values')
ax1.set_xlabel('Feedback Index')
ax1.set_ylabel('Feedback Value')
ax1.grid(False)

# Histogram
ax2.hist(values, bins=range(1, 7), align='left', edgecolor='black')
ax2.set_title('Histogram of Feedback Values')
ax2.set_xlabel('Feedback Value')
ax2.set_ylabel('Counts')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("figures/feedback_plot.png")
plt.show()
