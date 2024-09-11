import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

start_date = 7
end_date = 19
rows_per_day = 480  # this is what we would like to be constant for everyday
# this function is use for the case of a day that does not have
# 480 data points and it will pad that to make it into 480


def pad_array(arr, target_shape):
    padded_arr = np.full(target_shape, np.nan)
    arr_shape = arr.shape[0]
    padded_arr[:arr_shape] = arr
    return padded_arr


data1 = pd.read_csv("image_data.csv")
data2 = pd.read_csv("image_data2.csv")

data = pd.concat([data1, data2])

data['time'] = pd.to_datetime(data["time"])
data = data.sort_values(by='time')

# Filter the subset for a specific day
subset = data[(data['time'].dt.day >= start_date)
              & (data['time'].dt.day <= end_date)]
# Extract unique dates from the DataFrame
unique_dates = subset['time'].dt.date.unique()
day = subset['time'].dt.day
hour = subset['time'].dt.hour
minute = subset['time'].dt.minute
blue = subset['b']
green = subset['g']
red = subset['r']

unique_days = len(day.unique())
blue_padded = pad_array(blue, (rows_per_day * unique_days,))
green_padded = pad_array(green, (rows_per_day * unique_days,))
red_padded = pad_array(red, (rows_per_day * unique_days,))


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
unique_hours = subset['time'].dt.floor('h').unique()

# Create a list of timestamps for the y-axis based on unique hours
# timestamps = pd.date_range(
#     start='00:00', periods=24, freq='H')


# Plot the data
fig, ax = plt.subplots()
ax.pcolormesh(xgrid, ygrid, rgb, shading='auto')
ax.set_frame_on(False)
# Set the y-axis labels to the timestamps
# ax.set_yticks(np.linspace(0, rows_per_day, len(timestamps)))
# ax.set_yticklabels(timestamps.strftime('%H:%M'))  # Format as HH:MM
ax.set_xticks(np.arange(len(unique_dates)))
ax.set_xticklabels(unique_dates, rotation=45, ha='right')
# Format the y-axis labels
# ax.yaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.show()
