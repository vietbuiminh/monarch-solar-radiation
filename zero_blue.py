import pandas as pd
import duckdb
import matplotlib.pyplot as plt

# Converting UTC time from logs to Central US Time
zero_data = pd.read_csv('zero_reading_time.csv')
zero_data['time'] = pd.to_datetime(zero_data['time'])
zero_data['time'] = zero_data['time'].dt.tz_convert('America/Chicago')
# print(zero_data)
# Concat data from the image blue value
data1 = pd.read_csv("image_data.csv")
data2 = pd.read_csv("image_data2.csv")
data3 = pd.read_csv("image_data3.csv")
data4 = pd.read_csv("image_data4.csv")
data5 = pd.read_csv("image_data5.csv")
data6 = pd.read_csv("image_data6.csv")
sky_data = pd.concat([data1, data2, data3, data4, data5, data6])
sky_data['time'] = pd.to_datetime(sky_data["time"])
sky_data['time'] = sky_data['time'].dt.tz_localize('America/Chicago')
sky_data.drop(columns=['filename'], inplace=True)
sky_data = sky_data.sort_values(by='time')
# print(sky_data)


zero_data.set_index('time', inplace=True)
sky_data.set_index('time', inplace=True)
zero_data_resampled = zero_data.resample('10min').mean()
sky_data_resampled = sky_data.resample('10min').mean()

# Merge the data on the 'time' index to get the overlapping subset
data_combined = pd.merge(
    zero_data, sky_data, left_index=True, right_index=True, how='inner')

# Reset the index to bring 'time' back as a column
data_combined.reset_index(inplace=True)
data_combined['r'] = data_combined['r'] / 255.0
data_combined['g'] = data_combined['g'] / 255.0
data_combined['b'] = data_combined['b'] / 255.0

colors = data_combined[['r', 'g', 'b']].values
print(data_combined)


plt.figure(figsize=(10, 6))
plt.scatter(data_combined['time'], data_combined['b'],
            marker='D', linestyle='-', color=colors, s=100)
plt.xlabel('Time', fontweight='bold')
plt.ylabel('Blue Value', fontweight='bold')
plt.title('Time vs Blue Value', fontweight='bold')
plt.grid(True)
plt.tight_layout()
plt.show()
