import pandas as pd
import duckdb
import matplotlib.pyplot as plt

start_date, start_month = 8, 6
end_date, end_month = 28, 8
start_hour, end_hour = 6, 17  # using standard time

start_timestamp = pd.Timestamp(
    year=2023, month=start_month, day=start_date).tz_localize('America/Chicago')
end_timestamp = pd.Timestamp(
    year=2023, month=end_month, day=end_date, hour=23, minute=59, second=59).tz_localize('America/Chicago')
print(end_timestamp)

# Converting UTC time from logs to Central US Time
pyro_data = pd.read_csv('../processed_data/combined_logs.csv')
pyro_data['Time [UTC]'] = pd.to_datetime(pyro_data['Time [UTC]'])
pyro_data['Time [UTC]'] = pyro_data['Time [UTC]'].dt.tz_localize('UTC')
pyro_data['time'] = pyro_data['Time [UTC]'].dt.tz_convert(
    'America/Chicago')

# Concat data from the image blue value
data1 = pd.read_csv("../processed_data/image_data.csv")
data2 = pd.read_csv("../processed_data/image_data2.csv")
data3 = pd.read_csv("../processed_data/image_data3.csv")
data4 = pd.read_csv("../processed_data/image_data4.csv")
data5 = pd.read_csv("../processed_data/image_data5.csv")
data6 = pd.read_csv("../processed_data/image_data6.csv")
sky_data = pd.concat([data1, data2, data3, data4, data5, data6])
sky_data['time'] = pd.to_datetime(sky_data["time"])
sky_data['time'] = sky_data['time'].dt.tz_localize('America/Chicago')

sky_data = sky_data.sort_values(by='time')

subset_pyro = pyro_data[(pyro_data['time'] >= start_timestamp)
                        & (pyro_data['time'] <= end_timestamp)
                        & (pyro_data['time'].dt.hour >= start_hour)
                        & (pyro_data['time'].dt.hour <= end_hour)]
subset_sky = sky_data[(sky_data['time'] >= start_timestamp)
                      & (sky_data['time'] <= end_timestamp)
                      & (sky_data['time'].dt.hour >= start_hour)
                      & (sky_data['time'].dt.hour <= end_hour)]
filtered_pyro = duckdb.query(
    'SELECT "time", " Pyro [uV]" FROM subset_pyro').to_df()
filtered_sky = duckdb.query(
    'SELECT "time", "b", "g", "r" FROM subset_sky').to_df()

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

fig = plt.figure(figsize=(8, 6))
i = 0
ls = ["b", "g", "r"]
for item in ls:
    i += 1
    ax = plt.subplot(2, 2, i)
    scatter = ax.scatter(
        data_combined[' Pyro [uV]'], data_combined[item], c=color, alpha=1, s=2)
    cbar = fig.colorbar(scatter, ax=ax, orientation='horizontal')
    cbar.set_label('Hour of Day', fontweight='bold')
    ax.set_xlabel(' Pyro [uV]', fontweight='bold')
    ax.set_ylabel(f'{item} Value', fontweight='bold')

plt.show()
