#!/usr/bin/python3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data for the plot
data = {
    "Queue Type": [
        "CBS High\nPriority Queue", 
        "CBS DoS High\nPriority Queue", 
        "CBS DoS Low\nPriority Queue"
    ],
    "Throughput (Mb/s)": [7.833, 4.786, 7.965],
    "Error": [0.1749317327, 0.524767378, 0.1288625452],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set Seaborn style
sns.set(style="whitegrid")

# Create the horizontal bar plot
plt.figure(figsize=(10, 6))
barplot = sns.barplot(
    y="Queue Type", 
    x="Throughput (Mb/s)", 
    data=df, 
    palette=["gold", "red", "chocolate"], 
    ci=None
)

# Add error bars
for index, row in df.iterrows():
    plt.errorbar(
        row["Throughput (Mb/s)"], index, 
        xerr=row["Error"], 
        fmt='none', 
        color='black', 
        capsize=5
    )

# Annotate the bars with their values (position adjusted higher)
for index, row in df.iterrows():
    plt.text(
        row["Throughput (Mb/s)"] + 0.1, 
        index - 0.1,  # Adjusted position slightly higher
        f'{row["Throughput (Mb/s)"]}', 
        color="black", 
        va="center", 
        fontsize=12
    )

# Label axes and title
plt.xlabel("Throughput (Mb/s)", fontsize=16)
plt.ylabel("", fontsize=14)  # Restored y-axis label

# Adjust x-axis limit and set ticks for every integer value between 0 and 10
plt.xlim(0, 9)
plt.xticks(range(0, 9, 1))  # Add ticks from 0 to 10 with step of 1
plt.yticks(fontsize=16)

plt.tight_layout()
# Show the plot
plt.show()

