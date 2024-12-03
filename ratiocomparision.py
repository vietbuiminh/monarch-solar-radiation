import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from scipy.ndimage import gaussian_filter

df = pd.read_csv('combined_logs.csv')

# remove extra spacing
df.columns = df.columns.str.replace(r'^\s+', '', regex=True)

# make sure to convert all the data into numbers
df['White_u'] = df['White_u'].fillna(0)
df['White_u'] = df['White_u'].astype('float').round().astype('int')
df['Pyro [uV]'] = df['Pyro [uV]'].astype('float').round().astype('int')
df['IR_M_u'] = df['IR_M_u'].astype('float')
df['IR_S_u'] = df['IR_S_u'].astype('float')

# localize UTC to Central US Time
df['Time [UTC]'] = pd.to_datetime(df["Time [UTC]"])
df['Time [UTC]'] = df['Time [UTC]'].dt.tz_localize('UTC')
df['Time [Central]'] = df['Time [UTC]'].dt.tz_convert(
    'America/Chicago')


def getData(inputyear, inputmonth, inputday, starthour, endhour):
    start_timestamp = pd.Timestamp(
        year=inputyear, month=inputmonth, day=inputday, hour=starthour, minute=0, second=0).tz_localize('America/Chicago')
    end_timestamp = pd.Timestamp(year=inputyear, month=inputmonth, day=inputday,
                                 hour=endhour, minute=59, second=59).tz_localize('America/Chicago')
    data = df[(df['Time [Central]'] >= start_timestamp)
              & (df['Time [Central]'] <= end_timestamp)]
    data.loc[:, 'time'] = data['Time [Central]'].dt.time
    data = data[['Time [Central]', 'time', 'IR_S_u',
                 'IR_M_u', 'UVA_u', 'UVB_u', 'Vis_u [lx]']].reset_index(drop=True)
    data = data.set_index('time')
    return data


sunny_data = getData(2023, 6, 11, 11, 16)
cloudy_data = getData(2023, 6, 10, 11, 16)
rainny_data = getData(2023, 6, 18, 11, 16)
smoke_data = getData(2023, 6, 14, 11, 16)
# Merge the data on 'time' columns
merged_data = pd.concat([sunny_data, cloudy_data, rainny_data, smoke_data], axis=1, keys=[
                        'Sunny', 'Cloudy', 'Rainy', 'Smoke']).reset_index()
merged_data['time'] = pd.to_datetime(merged_data['time'], format='%H:%M:%S')
merged_data = merged_data.set_index('time')

# Resample the merged data to 30-minute intervals and calculate the mean
resampled_data = merged_data.resample('10min').mean()
# Calculate the ratio of IR_S_u and IR_M_u for different weather conditions
conditions = ['Cloudy', 'Rainy', 'Smoke']

# r1 = IR_S / IR_S_Sunny
# r2 = IR_M / IR_M_Sunny
for condition in conditions:
    resampled_data[(f'{condition}_Ratio', f'r1')
                   ] = resampled_data[condition]['IR_S_u'] / resampled_data['Sunny']['IR_S_u']
    resampled_data[(f'{condition}_Ratio', f'r2')
                   ] = resampled_data[condition]['IR_M_u'] / resampled_data['Sunny']['IR_M_u']
    # resampled_data[('Ratio', f'IR_S_{condition}/UVA_Sunny')
    #                ] = resampled_data[condition]['IR_M_u'] / resampled_data['Sunny']['UVA_u']
    # resampled_data[('Ratio', f'Vis_{condition}/UVA_Sunny')
    #                ] = resampled_data[condition]['Vis_u [lx]'] / resampled_data['Sunny']['UVA_u']

print(resampled_data)

X = resampled_data.index.strftime('%H:%M:%S')
# colors = ['red', 'green', 'blue', 'yellow']
fig, ax = plt.subplots(figsize=(12, 8))
# ax.set_prop_cycle(color=colors)
for condition in conditions:
    Y1 = resampled_data[f'{condition}_Ratio']['r1']
    Y2 = resampled_data[f'{condition}_Ratio']['r2']
    color1 = ax._get_lines.get_next_color()
    color2 = ax._get_lines.get_next_color()
    polygon = ax.fill_between(X, Y1, Y2, lw=0, color='none')
    ylim = ax.get_ylim()
    verts = np.vstack([p.vertices for p in polygon.get_paths()])
    ymin, ymax = verts[:, 1].min(), verts[:, 1].max()
    gradient_data = np.array([np.interp(np.linspace(ymin, ymax, 200), [y1i, y2i], np.arange(2))
                              for y1i, y2i in zip(Y1, Y2)]).T
    blurred_gradient_data = gaussian_filter(gradient_data, sigma=1)
    cm1 = LinearSegmentedColormap.from_list(
        'Temperature Map', [color1, color2])
    gradient = ax.imshow(blurred_gradient_data,
                         cmap=cm1, aspect='auto', origin='lower', extent=[X.min(), X.max(), ymin, ymax], alpha=0.1)
    gradient.set_clip_path(polygon.get_paths()[
                           0], transform=ax.transData)
    ax.set_ylim(ylim)
    ax.plot(X, Y1,
            label=f'IR_S_{condition} / IR_S_Sunny', color=color1, marker='o')
    ax.plot(X, Y2,
            label=f'IR_M_{condition} / IR_M_Sunny', color=color2, marker='o')

ax.set_title(
    'Ratios of Various IRs Conditions (Cloudy, Rainy, Smoke) over IRs in Sunny Conditions')
ax.set_xlabel('Time')
ax.set_ylabel('Ratio')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
