import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('combined_logs.csv', low_memory=False)

# remove extra spacing
df.columns = df.columns.str.replace(r'^\s+', '', regex=True)

# make sure to convert all the data into numbers
df['White_u'] = df['White_u'].fillna(0)
df['White_u'] = df['White_u'].astype('float').round().astype('int')
df['Pyro [uV]'] = df['Pyro [uV]'].astype('float').round().astype('int')
df['IR_M_u'] = df['IR_M_u'].astype('float')
df['IR_S_u'] = df['IR_S_u'].astype('float')
df['Vis_u [lx]'] = df['Vis_u [lx]'].astype('float')

# localize UTC to Central US Time
df['Time [UTC]'] = pd.to_datetime(df["Time [UTC]"])
df['Time [UTC]'] = df['Time [UTC]'].dt.tz_localize('UTC')
df['Time [Central]'] = df['Time [UTC]'].dt.tz_convert(
    'America/Chicago')

print(df)


def getData(inputyear, inputmonth, inputday, starthour, endhour):
    start_timestamp = pd.Timestamp(
        year=inputyear, month=inputmonth, day=inputday, hour=starthour, minute=0, second=0).tz_localize('America/Chicago')
    end_timestamp = pd.Timestamp(year=inputyear, month=inputmonth, day=inputday,
                                 hour=endhour, minute=59, second=59).tz_localize('America/Chicago')
    data = df[(df['Time [Central]'] >= start_timestamp)
              &
              (df['Time [Central]'] <= end_timestamp)]
    data.loc[:, 'time'] = data['Time [Central]'].dt.time
    data = data[['Time [Central]', 'time', 'IR_S_u',
                 'IR_M_u', 'Vis_u [lx]', 'Pyro [uV]']]
    data = data.set_index('time')
    print('Data inside the funcitonb')
    print(data)
    return data


# get Data here
sunny_data = getData(2023, 6, 11, 12, 16).reset_index()
print('Sunny Data')
print(sunny_data)
ratios = ['r1', 'r2', 'normalized Pyro [uV]']
# r1 = IR_s/Vis
sunny_data['r1'] = (sunny_data['IR_S_u']/max(sunny_data['IR_S_u'])) / \
    (sunny_data['Vis_u [lx]']/max(sunny_data['Vis_u [lx]']))
# r2 = IR_m/Vis
sunny_data['r1'] = (sunny_data['IR_M_u']/max(sunny_data['IR_M_u'])) / \
    (sunny_data['Vis_u [lx]']/max(sunny_data['Vis_u [lx]']))


sunny_data['normalized Pyro [uV]'] = sunny_data['Pyro [uV]'] / \
    max(sunny_data['Pyro [uV]'])
print('Ratio')
print(sunny_data['r1'])
X = sunny_data['Time [Central]']
fig, ax = plt.subplots(figsize=(12, 8))

for r in ratios:
    Y = sunny_data[r]
    ax.plot(X, Y, label=f'{r}')

ax.set_xlabel('Time')
ax.set_ylabel('ratio (normalized)')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
