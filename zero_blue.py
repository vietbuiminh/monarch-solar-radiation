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
sky_data['r'] = sky_data['r'] / 255.0
sky_data['g'] = sky_data['g'] / 255.0
sky_data['b'] = sky_data['b'] / 255.0

sky_data = sky_data.sort_values(by='time')
graph_sky_data = duckdb.query(
    "SELECT * FROM sky_data WHERE time < '2023-07-04 10:15:00-05:00'").to_df()
# print(sky_data)
zero_data.set_index('time', inplace=True)
sky_data.set_index('time', inplace=True)
# Merge the data on the 'time' index to get the overlapping subset
data_combined = pd.merge(
    zero_data, sky_data, left_index=True, right_index=True, how='inner')
# Reset the index to bring 'time' back as a column
data_combined.reset_index(inplace=True)

colors = data_combined[['r', 'g', 'b']].values
full_data_colors = graph_sky_data[['r', 'g', 'b']].values
print(data_combined)

print(graph_sky_data)

fig, ax1 = plt.subplots()
ax1.scatter(graph_sky_data['time'], graph_sky_data['b'],
            marker='D', linestyle='-', color=full_data_colors, s=80)
# ax1.tick_params(axis='y')

ax2 = ax1.twinx()
ax2.scatter(data_combined['time'], data_combined['b'],
            marker='D', linestyle='-', color='white', s=100, edgecolor='white', linewidth=10)
# ax2.tick_params(axis='y')
ax3 = ax1.twinx()
ax3.scatter(data_combined['time'], data_combined['b'],
            marker='D', linestyle='-', color=colors, s=100, edgecolor='black', linewidth=1)


# fig.x_label('Time', fontweight='bold')
# fig.y_label('Blue Value', fontweight='bold')
# fig.title('Time vs Blue Value', fontweight='bold')
# fig.grid(True)
a, b = 0.3, 0.8
ax1.set_ylim(a, b)
ax2.set_ylim(a, b)
ax3.set_ylim(a, b)

fig.tight_layout()
plt.show()
