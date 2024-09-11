import pandas as pd
import duckdb
import matplotlib.pyplot as plt

start_date, start_month = 8, 6
end_date, end_month = 30, 6
start_hour, end_hour = 6, 17  # using standard time

# Converting UTC time from logs to Central US Time
pyro_data = pd.read_csv('combined_logs.csv')
pyro_data['Time [UTC]'] = pd.to_datetime(pyro_data['Time [UTC]'])
pyro_data['Time [UTC]'] = pyro_data['Time [UTC]'].dt.tz_localize('UTC')
pyro_data['time'] = pyro_data['Time [UTC]'].dt.tz_convert(
    'America/Chicago')

# Concat data from the image blue value
data1 = pd.read_csv("image_data.csv")
data2 = pd.read_csv("image_data2.csv")
data3 = pd.read_csv("image_data3.csv")
sky_data = pd.concat([data1, data2, data3])
sky_data['time'] = pd.to_datetime(sky_data["time"])
sky_data['time'] = sky_data['time'].dt.tz_localize('America/Chicago')

sky_data = sky_data.sort_values(by='time')

subset_pyro = pyro_data[(pyro_data['time'].dt.day >= start_date)
                        & (pyro_data['time'].dt.day <= end_date) & (pyro_data['time'].dt.month >= start_month)
                        & (pyro_data['time'].dt.month <= end_month) & (pyro_data['time'].dt.hour >= start_hour)
                        & (pyro_data['time'].dt.hour <= end_hour)]
subset_sky = sky_data[(sky_data['time'].dt.day >= start_date)
                      & (sky_data['time'].dt.day <= end_date) & (sky_data['time'].dt.month >= start_month)
                      & (sky_data['time'].dt.month <= end_month) & (sky_data['time'].dt.hour >= start_hour)
                      & (sky_data['time'].dt.hour <= end_hour)]
filtered_pyro = duckdb.query(
    'SELECT "time", " Pyro [uV]" FROM subset_pyro').to_df()
filtered_sky = duckdb.query('SELECT "time", "b" FROM subset_sky').to_df()

filtered_pyro.set_index('time', inplace=True)
filtered_sky.set_index('time', inplace=True)

filtered_pyro = filtered_pyro.resample('15min').mean()
filtered_sky = filtered_sky.resample('15min').mean()

data_combined = pd.merge_asof(
    filtered_pyro, filtered_sky, on='time', direction='nearest')

# Print the DataFrame in a nice format
print("First few rows of the combined data:")
print(data_combined.head())

print("\nLast few rows of the combined data:")
print(data_combined.tail())

t_fract = data_combined['time'].astype(str)
t_fract = (t_fract.str[11:13])
t_fract = t_fract.astype(int)

Y = data_combined[[' Pyro [uV]']]
X = data_combined.drop(columns=[' Pyro [uV]'])

color = t_fract

fig, ax = plt.subplots()
fig, ax = plt.subplots()
scatter = ax.scatter(
    data_combined[' Pyro [uV]'], data_combined['b'], c=color, alpha=1, s=2)
cbar = fig.colorbar(scatter, ax=ax, orientation='horizontal')
cbar.set_label('Hour of Day', fontweight='bold')
ax.set_xlabel(' Pyro [uV]', fontweight='bold')
ax.set_ylabel('Blue Value', fontweight='bold')
plt.show()
