#!/usr/bin/python3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Time array
time = np.linspace(0, 1000, 1000)

# Normal clock progresses linearly
normal_clock = time * 1

# Clock under attack
clock_under_attack = time.copy()
clock_under_attack[:500] = time[:500]  # Matches normal clock until 500 seconds
clock_under_attack[500:700] = 300 + (100 * (time[500:700] - 500) / 100)  # Rises linearly from 300 to 500
clock_under_attack[700] = 300  # Instant vertical drop to 300
clock_under_attack[701:900] = 300 + (100 * (time[701:900] - 700) / 100)  # Rises linearly from 300 to 500
clock_under_attack[900] = 300  # Instant vertical drop to 300
clock_under_attack[901:1000] = 300 + (100 * (time[901:1000] - 900) / 100)  # Rises linearly from 300 to 500

# Set Seaborn style
sns.set(style="whitegrid")

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(time, clock_under_attack, label="Fake master clock", color="red", linewidth=2)  # Changed color to red
plt.plot(time, normal_clock, label="Normal clock", color="teal", linestyle="--", linewidth=2)

# Add labels, legend, and title
plt.xlabel("Time (s)", fontsize=16)
plt.ylabel("Time from start of the attack (s)", fontsize=16)
plt.legend(fontsize=16)

# Show the plot
plt.tight_layout()
plt.show()

