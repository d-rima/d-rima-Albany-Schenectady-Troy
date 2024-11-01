import pandas as pd
import matplotlib.pyplot as plt

# Load Albany and US unemployment data, skipping rows that may contain headers or irrelevant information
albany_file_path = 'albany-statistics\\5-year-unemployment-albany.xls'
us_file_path = 'albany-statistics\\5-year-unemployment-us.xls'

# Load data, skipping rows that are headers or metadata (adjust skiprows if necessary)
albany_data = pd.read_excel(albany_file_path, skiprows=1, usecols=[0, 1], names=['Date', 'Unemployment Rate'])
us_data = pd.read_excel(us_file_path, skiprows=1, usecols=[0, 1], names=['Date', 'Unemployment Rate'])

# Drop any rows where Date or Unemployment Rate is NaN (if there are extra rows with irrelevant data)
albany_data.dropna(subset=['Date', 'Unemployment Rate'], inplace=True)
us_data.dropna(subset=['Date', 'Unemployment Rate'], inplace=True)

# Convert 'Date' column to datetime format for accurate plotting
albany_data['Date'] = pd.to_datetime(albany_data['Date'], errors='coerce')
us_data['Date'] = pd.to_datetime(us_data['Date'], errors='coerce')

# Drop rows with invalid dates (if any)
albany_data.dropna(subset=['Date'], inplace=True)
us_data.dropna(subset=['Date'], inplace=True)

# Plotting the comparison line graph
plt.figure(figsize=(12, 8))

# Plot Albany unemployment data
plt.plot(albany_data['Date'], albany_data['Unemployment Rate'], label='Albany-Schenectady-Troy, NY', marker='o')

# Plot US unemployment data
plt.plot(us_data['Date'], us_data['Unemployment Rate'], label='United States', marker='x')

# Adding titles and labels
plt.title('5-Year Unemployment Rate Comparison: Albany-Schenectady-Troy, NY vs United States')
plt.xlabel('Year')
plt.ylabel('Unemployment Rate (%)')
plt.xticks(rotation=45)
plt.legend(title='Region')
plt.tight_layout()

# Show the plot
plt.show()
