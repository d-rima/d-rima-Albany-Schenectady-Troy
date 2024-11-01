import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load both Excel files
file_leisure = 'albany-statistics\\leisure-hospitality.xlsx'
file_professional = 'albany-statistics\\professional-business.xlsx'

# Load data and skip rows to reach actual headers
leisure_data = pd.read_excel(file_leisure, skiprows=12)
professional_data = pd.read_excel(file_professional, skiprows=12)

# Convert each file from wide format to long format with 'Date' and 'Employment Level' columns
leisure_data = pd.melt(leisure_data, id_vars=['Year'], var_name='Month', value_name='Leisure & Hospitality')
professional_data = pd.melt(professional_data, id_vars=['Year'], var_name='Month', value_name='Professional & Business')

# Combine 'Year' and 'Month' columns to create a datetime column
leisure_data['Date'] = pd.to_datetime(leisure_data['Year'].astype(str) + leisure_data['Month'], format='%Y%b')
professional_data['Date'] = pd.to_datetime(professional_data['Year'].astype(str) + professional_data['Month'], format='%Y%b')

# Keep only the 'Date' and relevant employment columns
leisure_data = leisure_data[['Date', 'Leisure & Hospitality']]
professional_data = professional_data[['Date', 'Professional & Business']]

# Merge both datasets on the 'Date' column for continuous time series plotting
combined_data = pd.merge(leisure_data, professional_data, on='Date', how='inner').sort_values(by='Date')

# Plot both series with monthly data, displaying only the year on x-axis labels
plt.figure(figsize=(12, 8))
plt.plot(combined_data['Date'], combined_data['Leisure & Hospitality'], label='Leisure & Hospitality', color='blue')
plt.plot(combined_data['Date'], combined_data['Professional & Business'], label='Professional & Business', color='green')

# Set plot titles and labels
plt.title("Comparison of Employment Trends: Leisure & Hospitality vs. Professional & Business")
plt.xlabel("Year")
plt.ylabel("Employment Level (in Thousands)")
plt.legend()
plt.grid(True)

# Customize x-axis to display only January of each year
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
plt.show()
