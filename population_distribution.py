import matplotlib.pyplot as plt
import pandas as pd

# Data preparation
age_groups = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
albany_schenectady_troy = [9.9, 12.2, 14.2, 12.6, 12, 13.2, 12.9, 8.7, 4.3]
us = [11.4, 12.9, 13.3, 13.7, 12.4, 12.4, 12, 7.9, 3.9]

# Create a DataFrame for plotting
data = pd.DataFrame({
    'Age Group': age_groups,
    'Albany-Schenectady-Troy (%)': albany_schenectady_troy,
    'US (%)': us
})

# Plot for Albany-Schenectady-Troy
plt.figure(figsize=(10, 6))
plt.bar(data['Age Group'], data['Albany-Schenectady-Troy (%)'], color='skyblue')
plt.title("Age Distribution in Albany-Schenectady-Troy")
plt.xlabel("Age Group")
plt.ylabel("Percentage (%)")
plt.ylim(0, 16)
plt.show()

# Plot for US
plt.figure(figsize=(10, 6))
plt.bar(data['Age Group'], data['US (%)'], color='salmon')
plt.title("Age Distribution in the US")
plt.xlabel("Age Group")
plt.ylabel("Percentage (%)")
plt.ylim(0, 16)
plt.show()
