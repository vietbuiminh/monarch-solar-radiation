import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

start_date, start_month = 11, 6
end_date, end_month = 11, 6
year = 2023

start_timestamp = pd.Timestamp(year=year, month=start_month, day=start_date)
end_timestamp = pd.Timestamp(
    year=year, month=end_month, day=end_date, hour=23, minute=59, second=59)
print(end_timestamp)

rows_per_day = 480  # this is what we would like to be constant for everyday
# this function is use for the case of a day that does not have
# 480 data points and it will pad that to make it into 480


def pad_array(arr, target_shape):
    padded_arr = np.full((target_shape,), np.nan)
    arr_shape = arr.shape[0]
    # # print(arr['time'], arr_shape, target_shape)
    # if arr_shape > target_shape:
    #     print("UGH", arr_shape)
    #     # Truncate the array if it is larger than the target shape
    #     arr = arr[:target_shape]
    #     arr_shape = target_shape
    padded_arr[:arr_shape] = arr
    return padded_arr


data1 = pd.read_csv("image_data.csv")
data2 = pd.read_csv("image_data2.csv")
data3 = pd.read_csv("image_data3.csv")
data4 = pd.read_csv("image_data4.csv")
data5 = pd.read_csv("image_data5.csv")
data6 = pd.read_csv("image_data6.csv")
# data7 = pd.read_csv("image_data7.csv")
# print(data7)
# data = data7
data = pd.concat([data1, data2, data3, data4, data5, data6])

data['time'] = pd.to_datetime(data["time"])
data = data.sort_values(by='time')
print(data['time'])
# Filter the subset for a specific day
subset = data[(data['time'] >= start_timestamp)
              & (data['time'] <= end_timestamp)]
print(subset)
# Extract unique dates from the DataFrame
unique_dates = subset['time'].dt.date.unique()
print(f'unique day={unique_dates}')
day = subset['time'].dt.day
hour = subset['time'].dt.hour
minute = subset['time'].dt.minute
blue = subset['b']
green = subset['g']
red = subset['r']

unique_days = len(unique_dates)
print(unique_days)
blue_padded = pad_array(blue, (rows_per_day * unique_days))
green_padded = pad_array(green, (rows_per_day * unique_days))
red_padded = pad_array(red, (rows_per_day * unique_days))


# Replace NaN values with 0 for blue and green channels, and 1 for the red channel
blue_padded[np.isnan(blue_padded)] = 0
green_padded[np.isnan(green_padded)] = 0
red_padded[np.isnan(red_padded)] = 255

# display only blue value
# green_padded[:] = 0
# red_padded[:] = 0

# Reshape the 'blue' array to match the grid dimensions
blue = blue_padded.reshape(rows_per_day, unique_days, order="F") / 255.0
green = green_padded.reshape(
    rows_per_day, unique_days, order="F") / 255.0
red = red_padded.reshape(rows_per_day, unique_days, order="F") / 255.0

rgb = np.stack((red, green, blue), axis=-1)

xgrid = np.arange(unique_days + 1)
ygrid = np.arange(rows_per_day + 1)
# Extract unique hours from the DataFrame
unique_hours = subset['time'].dt.hour.unique()
print(unique_hours)

# Create a list of timestamps for the y-axis based on unique hours
# timestamps = pd.date_range(
#     start='00:00', periods=24, freq='H')


# Plot the data
fig, ax = plt.subplots(figsize=(2, 6))
ax.pcolormesh(xgrid, ygrid, rgb, shading='auto')
ax.set_frame_on(False)
# Set the y-axis labels to the timestamps
# ax.set_yticks(np.linspace(0, rows_per_day, len(timestamps)))
# ax.set_yticklabels(timestamps.strftime('%H:%M'))  # Format as HH:MM
spacing = 10
ax.set_xticks(np.arange(len(unique_dates)))
ax.set_xticklabels(unique_dates, rotation=45, ha='right')
# for index, label in enumerate(ax.xaxis.get_ticklabels()):
#     if index % spacing != 0 and index != 7:
#         label.set_visible(False)
# plt.yticks(np.arange(0, 24, 1))
# Format the y-axis labels
# ax.yaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.savefig("zoomInJune10.pdf", format="pdf", bbox_inches="tight")

plt.show()
