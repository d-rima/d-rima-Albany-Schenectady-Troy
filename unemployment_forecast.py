# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Step 1: Load and inspect the data
unemployment_data = pd.read_excel('albany-statistics\\unemployment.xlsx', skiprows=8, header=1)
unemployment_data = unemployment_data.dropna(axis=1, how='all')
unemployment_data.columns = ['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
unemployment_data = unemployment_data[unemployment_data['Year'].astype(str).str.isnumeric()]

# Step 2: Transform data into a long format with DateTime index
unemployment_long = pd.melt(
    unemployment_data, id_vars=['Year'], var_name='Month', value_name='Unemployment Rate'
)
unemployment_long['Unemployment Rate'] = pd.to_numeric(unemployment_long['Unemployment Rate'], errors='coerce')
unemployment_long = unemployment_long.dropna()
unemployment_long['Date'] = pd.to_datetime(unemployment_long['Year'].astype(str) + unemployment_long['Month'], format='%Y%b')
unemployment_long = unemployment_long.sort_values(by='Date').set_index('Date')

# Step 3: Visualize the unemployment rate time series
plt.figure(figsize=(12, 6))
plt.plot(unemployment_long.index, unemployment_long['Unemployment Rate'], marker='o')
plt.title('Unemployment Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate')
plt.grid(True)
plt.show()

# Step 4: Check for stationarity with ADF test
adf_result = adfuller(unemployment_long['Unemployment Rate'])
print(f'ADF Statistic: {adf_result[0]}')
print(f'p-value: {adf_result[1]}')
print('Critical Values:', adf_result[4])

# Step 5: Plot ACF and PACF to identify potential SARIMA parameters
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
plot_acf(unemployment_long['Unemployment Rate'], lags=24, ax=axes[0])
axes[0].set_title('ACF Plot')
plot_pacf(unemployment_long['Unemployment Rate'], lags=24, ax=axes[1])
axes[1].set_title('PACF Plot')
plt.show()

# Step 6: Fit the SARIMA model
sarima_model = SARIMAX(
    unemployment_long['Unemployment Rate'],
    order=(1, 0, 1), 
    seasonal_order=(1, 0, 1, 12), 
    enforce_stationarity=False, 
    enforce_invertibility=False
)
sarima_result = sarima_model.fit(disp=False)
print(sarima_result.summary())

# Step 7: Forecast the next 12 months
forecast_steps = 12
forecast = sarima_result.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=unemployment_long.index[-1] + pd.DateOffset(1), periods=forecast_steps, freq='M')
forecast_mean = forecast.predicted_mean
conf_int = forecast.conf_int()

# Plot the historical data and forecast
plt.figure(figsize=(12, 6))
plt.plot(unemployment_long.index, unemployment_long['Unemployment Rate'], label='Observed', marker='o')
plt.plot(forecast_index, forecast_mean, label='Forecast', marker='o', linestyle='--')
plt.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='gray', alpha=0.3)
plt.title('Unemployment Rate Forecast (Next 12 Months)')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate')
plt.legend()
plt.grid(True)
plt.show()

# Step 8: Zoomed-in forecast for the next 12 months
plt.figure(figsize=(10, 5))
plt.plot(forecast_index, forecast_mean, label='Forecast', marker='o', color='blue', linestyle='--')
plt.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='blue', alpha=0.2)
plt.title('Zoomed-In Unemployment Rate Forecast (Next 12 Months)')
plt.xlabel('Month')
plt.ylabel('Forecasted Unemployment Rate')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Step 9: Display forecast values with confidence intervals in a table format
forecast_df = pd.DataFrame({
    'Date': forecast_index,
    'Forecasted Unemployment Rate': forecast_mean,
    'Lower CI': conf_int.iloc[:, 0],
    'Upper CI': conf_int.iloc[:, 1]
})

print(forecast_df)

# Optional: Save forecast results to Excel
forecast_df.to_excel('forecasted_unemployment.xlsx', index=False)
