import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Step 1: Generate 30 random integers and add them to an array
#np.random.seed(0)  # For reproducibility
data = np.random.randint(1, 101, size=30)  # Random integers between 1 and 100
#data = [100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]

# Step 2: Calculate mean, average, and standard deviation
mean = np.mean(data)
std_dev = np.std(data)

# Step 3: Show a bar chart of these integers
plt.figure(figsize=(12, 6))
plt.bar(range(len(data)), data, alpha=0.7, color='blue', label='Data')

# Step 4: Show average, mean, and std lines on the bar chart
plt.axhline(mean, color='red', linestyle='-', linewidth=2, label=f'Mean: {mean:.2f}')
plt.axhline(mean + std_dev, color='green', linestyle='--', linewidth=2, label=f'Std Dev: {mean + std_dev:.2f}')
plt.axhline(mean - std_dev, color='green', linestyle='--', linewidth=2)

# Adding labels and legend
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Bar Chart of Random Integers with Mean and Std Dev Lines')
plt.legend()

# Save the plot as an image file
plt.savefig('bar_chart.png')

# Display the plot image using Pillow
img = Image.open('bar_chart.png')
img.show()
