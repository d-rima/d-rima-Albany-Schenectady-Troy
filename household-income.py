import pandas as pd
import matplotlib.pyplot as plt

# Load the spreadsheet and skip irrelevant rows
file_path = 'albany-statistics\\household-income.xlsx'  # Update path as needed for your environment
data = pd.read_excel(file_path, skiprows=2)

# Renaming columns, excluding the extra column
data.columns = ['Income Bracket', 'United States', 'Albany-Schenectady-Troy, NY', 
                'Chicago-Naperville-Elgin, IL-IN-WI', 'Providence-Warwick, RI-MA', 
                'Scranton--Wilkes-Barre, PA', 'Worcester, MA-CT', 'Indianapolis-Carmel-Muncie, IN', 'Remove']
data = data.drop(columns=['Remove', 'United States'])  # Drop the extra and 'United States' column

# Removing any rows where 'Income Bracket' is NaN (if any)
data = data.dropna(subset=['Income Bracket'])

# Convert income counts to percentages for each column
data.set_index('Income Bracket', inplace=True)
data = data.apply(lambda x: (x / x.sum()) * 100)

# Plotting the percentage data with Albany-Schenectady-Troy as the baseline
plt.figure(figsize=(12, 8))
for column in data.columns:
    if column == 'Albany-Schenectady-Troy, NY':
        data[column].plot(kind='line', linewidth=0, marker='o', label=column)
    else:
        data[column].plot(kind='line', linestyle='', alpha=0.7, marker='x', label=column)

plt.title('Household Income Distribution Comparison by MSA')
plt.xlabel('Income Bracket')
plt.ylabel('Percentage of Households')
plt.xticks(rotation=45, ha='right')
plt.xticks(ticks=range(len(data.index)), labels=data.index, rotation=45, ha='right')  # Ensure all income brackets are shown
plt.legend(title='MSA', loc='upper left')
plt.tight_layout()
plt.show()
