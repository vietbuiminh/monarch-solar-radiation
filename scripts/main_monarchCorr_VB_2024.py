#! /usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
# import seaborn as sns
# from sklearn import linear_model
# from sklearn.model_selection import train_test_split
# import statsmodels.api as sm
import duckdb
# import timezone

import glob
import os

directory_path = 'raw/Logs'
files = glob.glob(os.path.join(directory_path, '*.txt'))

# df = pd.read_csv('newsys_log.csv')
df = pd.read_csv('combined_logs.csv')


start_date, start_month = 14, 6
end_date, end_month = 14, 6
year = 2023

start_timestamp = pd.Timestamp(
    year=year, month=start_month, day=start_date).tz_localize('America/Chicago')
end_timestamp = pd.Timestamp(
    year=year, month=end_month, day=end_date, hour=23, minute=59, second=59).tz_localize('America/Chicago')

print(end_timestamp)
# print(df)
# uncomment all of this for the first time run. otherwise using the combined_log.csv


# def getting_file_no(file_path):
#     file_name = os.path.basename(file_path)
#     file_no = int(file_name[3:-4])
#     return file_no


# files.sort(key=getting_file_no)
# start_file_no = 21
# end_file_no = 180
# desired_order = ['Time [UTC]',
#                  ' PresOB [mBar]',
#                  ' RH_OB [%]',
#                  ' TempOB [C]',
#                  ' Temp RTC [C]',
#                  ' Bat [V]',
#                  ' Pyro [uV]',
#                  ' R_u [deg]',
#                  ' P_u [deg]',
#                  ' UVA_u',
#                  ' UVB_u',
#                  ' White_u',
#                  ' Vis_u [lx]',
#                  ' IR_S_u',
#                  ' IR_M_u',
#                  ' PyroT_u [C]',
#                  '']
# for file_path in files:
#     if getting_file_no(file_path) < start_file_no or getting_file_no(file_path) >= end_file_no:
#         continue
#     else:
#         print(f'Reading file: {file_path}')
#         with open(file_path, 'r') as file:
#             skipped_line = file.readline().strip()
#             if not skipped_line:
#                 print(f'Skipping empty file: {file_path}')
#                 continue
#             column_head = ""
#             if skipped_line[0:2] == '20':
#                 print(
#                     f'File {file_path} has no heading, applying manual heading')
#                 column_head = "Time [UTC], PresOB [mBar], RH_OB [%], TempOB [C], Temp RTC [C], Bat [V], Pyro [uV], R_u [deg], P_u [deg], UVA_u, UVB_u, White_u, Vis_u [lx], IR_S_u, IR_M_u, PyroT_u [C],".strip()
#                 column_head = column_head.split(',')
#                 df_temp = pd.DataFrame([skipped_line.split(',')
#                                         for line in skipped_line], columns=column_names)
#                 df_temp = df_temp[desired_order]
#                 df_combined = pd.concat([df, df_temp])
#                 df_combined.reset_index(drop=True, inplace=True)
#                 df = df_combined
#             else:
#                 column_head = file.readline().strip()
#                 column_names = column_head.split(',')
#             for i in range(len(column_names)):
#                 if column_names[i] == " Kipp and Zonen Voltage [uV]":
#                     column_names[i] = ' Pyro [uV]'
#             lines = file.readlines()
#             df_temp = pd.DataFrame([line.strip().split(',')
#                                    for line in lines], columns=column_names)
#             df_temp = df_temp[desired_order]
#             # print(df_temp['Time [UTC]'])
#             df_combined = pd.concat([df, df_temp])
#             df_combined.reset_index(drop=True, inplace=True)
#             df = df_combined
#             # csv_file_path = file_path.replace('.txt', '.csv')
#             # df_combined.to_csv(csv_file_path, index=False)
#             # print(f'Saved to CSV: {csv_file_path}')

#             # break

#         # break
# csv_file_path = 'combined_logs.csv'
# df.to_csv(csv_file_path, index=False)
# print(f'Saved combined data to CSV: {csv_file_path}')

# remove the extra spacing infront of the heading of the columns
df.columns = df.columns.str.replace(r'^\s+', '', regex=True)
print(df['White_u'])
df['White_u'] = df['White_u'].fillna(0)
df['White_u'] = df['White_u'].astype('float').round().astype('int')
df['Pyro [uV]'] = df['Pyro [uV]'].astype('float').round().astype('int')
df['IR_M_u'] = df['IR_M_u'].astype('float')

# print(df['White_u'])

df['Time [UTC]'] = pd.to_datetime(df["Time [UTC]"])
df['Time [UTC]'] = df['Time [UTC]'].dt.tz_localize('UTC')
df['time'] = df['Time [UTC]'].dt.tz_convert(
    'America/Chicago')

df = df[(df['time'] >= start_timestamp)
        & (df['time'] <= end_timestamp)]

# filter, you can comment this line to view the full data
# df = df[(df['time'].dt.hour >= 6) & (df['time'].dt.hour <= 10)]
# df = duckdb.query("SELECT  *  FROM df WHERE White_u < 60000").to_df()
# print(df['Time [UTC]'])
weird_date = duckdb.query(
    'SELECT "time", "Pyro [uV]", "IR_M_u" FROM df WHERE ((IR_M_u < 1.5 AND IR_M_u > 0.5) AND ("Pyro [uV]" < 8000 AND "Pyro [uV]" > 2000))').to_df()
# print(weird_date)
another_weird_date = duckdb.query(
    'SELECT "time", "Pyro [uV]", "IR_M_u" FROM df WHERE ((IR_M_u < 1.56 AND IR_M_u > 0.13) AND ("Pyro [uV]" < 250 AND "Pyro [uV]" > -67))').to_df()
# print(another_weird_date)
inves_zero = duckdb.query(
    'SELECT "time", "Pyro [uV]", "IR_S_u" FROM df WHERE (IR_S_u <= 0)').to_df()
print(inves_zero)
csv_file_path = 'inves_zero.csv'
inves_zero.to_csv(csv_file_path, index=False)
# Extract the date and hour from the 'time' column
inves_zero['date'] = inves_zero['time'].dt.date
inves_zero['hour'] = inves_zero['time'].dt.hour

# Group the data by date and hour and count the number of entries for each group
grouped_data = inves_zero.groupby(
    ['date', 'hour']).size().reset_index(name='count')

# Pivot the data to have hours as columns and dates as rows
pivot_data = grouped_data.pivot(
    index='date', columns='hour', values='count').fillna(0)

# Plot the bar graph for each date
# pivot_data.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
# plt.xlabel('Date', fontweight='bold')
# plt.ylabel('Total Count', fontweight='bold')
# plt.title('Total Count by Hour and Date', fontweight='bold')
# plt.legend(title='Hour of the Day', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.title('Total Count by Hour of the Day', fontweight='bold')
# plt.xticks(range(0, 24))  # Ensure all hours are shown on the x-axis
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show()
# print("This is the first line")
# print(df['time'])

# -------------------------------------------
# sunny_start_timestamp = pd.Timestamp(
#     year=2023, month=6, day=8).tz_localize('America/Chicago')
# sunny_end_timestamp = pd.Timestamp(
#     year=2023, month=6, day=8, hour=23, minute=59, second=59).tz_localize('America/Chicago')
# sunny_data = df[(df['time'] >= sunny_start_timestamp)
#                 & (df['time'] <= sunny_end_timestamp)]

# cloudy_start_timestamp = pd.Timestamp(
#     year=2023, month=6, day=7).tz_localize('America/Chicago')
# cloudy_end_timestamp = pd.Timestamp(
#     year=2023, month=6, day=7, hour=23, minute=59, second=59).tz_localize('America/Chicago')
# cloudy_data = df[(df['time'] >= cloudy_start_timestamp)
#                  & (df['time'] <= cloudy_end_timestamp)]

# smoke_start_timestamp = pd.Timestamp(
#     year=2023, month=6, day=14).tz_localize('America/Chicago')
# smoke_end_timestamp = pd.Timestamp(
#     year=2023, month=6, day=14, hour=23, minute=59, second=59).tz_localize('America/Chicago')
# smoke_data = df[(df['time'] >= smoke_start_timestamp)
#                 & (df['time'] <= smoke_end_timestamp)]

# let store all of them inside files
# sunny_data.to_csv('sunny_data.csv', index=False)
# cloudy_data.to_csv('cloudy_data.csv', index=False)
# smoke_data.to_csv('smoke_data.csv', index=False)

# Let take a comparison between:
# - sunny and cloudy day
# print(f"sunny data : {sunny_data}")
# print(f"cloudy data: {cloudy_data}")
# ratio_sunny_over_cloudy = (sunny_data["IR_S_u"]/cloudy_data["IR_S_u"])
# print(f"ratio IR_SW: {ratio_sunny_over_cloudy}")
# - sunny and Jun 14
# - cloudy and Jun 14
# graph where it is the abs(ratio difference) on time scale from 0 to 23:59:59
# -------------------------------------------


# UVB_u = df['UVB_u']  # use this normalize and compare with all other sensors


# df['IR_S_u_sim'] = df['IR_S_u'].apply(lambda x: 0 if x <= 0.0 else 1)
# print(df['IR_S_u_sim'])
# df['PyroT_u [C]'] = df['PyroT_u [C]'].astype(float)
# temperature = df['PyroT_u [C]']
# humidity = df['RH_OB [%]']
# print(temperature)
# IR_sim = df['IR_S_u_sim']
# IR_s = df['IR_S_u']
# IR_m = df['IR_M_u']
# White = df['White_u']
# Vis = df['Vis_u [lx]']

# figIR, ax1 = plt.subplots()
# l1 = ax1.scatter(UVB_u, IR_s, c='deepskyblue',
#                  alpha=0.6, edgecolor='none')
# ax1.set_xlabel('UVB', fontweight='bold')
# ax1.set_xticklabels(ax1.get_xticks(), rotation=45, ha='right')
# ax1.set_ylabel('IR_Short', fontweight='bold')
# ax1.tick_params(axis='y')
# ax2 = ax1.twinx()
# ax2.set_ylabel('IR_Mid', fontweight='bold')
# l2 = ax2.scatter(UVB_u, IR_m, c='yellowgreen',
#                  alpha=0.6, edgecolor='none')
# ax2.tick_params(axis='y')
# figIR.suptitle(
#     f"Ultra-violet B vs Infrared on {start_month}-{start_date}-{year}", fontweight='bold')
# plt.legend([l1, l2], ['IR Short', 'IR Mid'], loc='lower right')

# figVis, ax1 = plt.subplots()
# l1 = ax1.scatter(UVB_u, White, c='blue', alpha=0.6, edgecolor='none')
# ax1.set_xlabel('UVB', fontweight='bold')
# ax1.set_xticklabels(ax1.get_xticks(), rotation=45, ha='right')
# ax1.set_ylabel('White Broadband', fontweight='bold', c='blue')
# ax1.tick_params(axis='y')
# ax2 = ax1.twinx()
# ax2.set_ylabel('White Filtered', fontweight='bold', c='violet')
# l2 = ax2.scatter(UVB_u, Vis, c='violet', alpha=0.6, edgecolor='none')
# ax2.tick_params(axis='y')
# figVis.suptitle(
#     f"Ultra-violet B vs White Broadband & White Filtered(Vis) on {start_month}-{start_date}-{year}", fontweight='bold')
# plt.legend([l1, l2], ['White Broadband',
#            'White Filtered(Vis)'], loc='lower right')

# figIRVis, ax1 = plt.subplots()
# l1 = ax1.scatter(Vis, IR_s, c='deepskyblue',
#                  alpha=0.6, edgecolor='none')
# ax1.set_xlabel('White Filtered', fontweight='bold')
# ax1.set_xticklabels(ax1.get_xticks(), rotation=45, ha='right')
# ax1.set_ylabel('IR_Short', fontweight='bold')
# ax1.tick_params(axis='y')
# ax2 = ax1.twinx()
# ax2.set_ylabel('IR_Mid', fontweight='bold')
# l2 = ax2.scatter(Vis, IR_m, c='yellowgreen',
#                  alpha=0.6, edgecolor='none')
# ax2.tick_params(axis='y')
# figIRVis.suptitle(
#     f"White Filtered vs Infrared on {start_month}-{start_date}-{year}", fontweight='bold')
# plt.legend([l1, l2], ['IR Short', 'IR Mid'], loc='upper left')

# fig, ax1 = plt.subplots()
# error_occured = duckdb.query("SELECT time FROM df WHERE IR_S_u == 0").to_df()
# csv_file_path = 'zero_reading_time.csv'
# error_occured.to_csv(csv_file_path, indexs=False)
# print(f'Saved combined data to CSV: {csv_file_path}')

# print(error_occured)
# ax1.plot(df['time'], IR_sim, c='r')
# ax1.set_xlabel('Time', fontweight='bold')
# ax1.set_ylabel('IR Short Wave Reading (0/1)', fontweight='bold')
# ax1.tick_params(axis='y', labelcolor='r')

# ax1.plot(df['time'], humidity, c='r')
# ax1.plot(df['time'], IR_s, c='r')
# ax1.set_xlabel('Time', fontweight='bold')
# # ax1.set_ylabel('Humidity', fontweight='bold')
# ax1.set_ylabel('IR_SW', fontweight='bold')
# ax1.tick_params(axis='y', labelcolor='r')
# ax1.set_title('Temperature vs. Simplified IR Readings thru Time',
#               fontweight='bold')
# ax1.grid(True)

# ax2 = ax1.twinx()
# ax2.set_ylabel('Temperature')
# ax2.scatter(df['time'], temperature, c='b', s=1)
# ax2.tick_params(axis='y', labelcolor='tab:blue')

# ax3 = ax1.twinx()
# ax3.set_ylabel('IR Short Wave Reading', fontweight='bold')
# ax3.scatter(df['time'], IR_s, c='green', s=1)
# ax3.tick_params(axis='y', labelcolor='tab:green')

# fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()
# Extract time and battery voltage columns
time = df['time']
cols = ['UVA_u', 'UVB_u', 'White_u', 'Vis_u [lx]', 'IR_S_u', 'Pyro [uV]']

# Normalize the data
df[cols] = df[cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

plt.figure(figsize=(12, 8))

for col in cols:
    plt.plot(time, df[col], label=col)

plt.xlabel('Time', fontweight='bold')
plt.ylabel('Normalized Sensor Readings on 06/14/2023', fontweight='bold')
plt.title('Normalized Sensor Readings vs Time', fontweight='bold')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

# Label the axes
# plt.xlabel('Time', fontweight='bold')
# plt.ylabel('Battery Voltage', fontweight='bold', color="g")
# plt.twinx().set_ylabel('Temperature OB [C]', fontweight='bold', color="b")

# # Add a title
# plt.title('Battery Voltage and Temperature OB vs Time', fontweight='bold')

# # Add a legend
# plt.legend()

# Display the plot
plt.show()

# Removing battery level, roll, pitch, K&Z Temp, and NA row that was added as a buffer.
t_fract = df['time'].astype(str)
t_fract = (t_fract.str[11:13])
t_fract = t_fract.astype(int)

# Zenith Angle
# h = (t - 12) / 12

df = df.iloc[:, 2:]
df = df.drop(columns=["Bat [V]", "R_u [deg]", "P_u [deg]"])
df = df.iloc[:, :-2]

# print(df)

# Seaborn Hearmap
# sns.heatmap(df.corr());
# plt.show()

# dfCorr = (df.corr())
# dfCorr.to_excel('test.xlsx', sheet_name='sheet1', index=True)

# 6 columns
cols = ['UVA_u', 'UVB_u', 'White_u', 'Vis_u [lx]', 'IR_S_u',
        'IR_M_u']
Y_extra = df[['PyroT_u [C]']]
Y = df[['Pyro [uV]']]
X = df.drop(columns=['Pyro [uV]'])

# color = 1 - (t_fract * 0.8 + 0.1)
color = t_fract

fig = plt.figure(figsize=(8, 10))
i = 0
for col in cols:
    i += 1
    ax = plt.subplot(3, 2, i)
    scatter = ax.scatter(df['Pyro [uV]'], df[col], c=t_fract, alpha=0.5, s=2)
    if col == "IR_M_u":
        # red region was detected on 1 day UTC 2023/06/12 23:06:06 - 2023/06/12 23:52:24 blue sky
        # nothing can be seems out of the ordinary just from the looking at photos
        red_region = ax.scatter(
            weird_date['Pyro [uV]'], weird_date[col], c='r', alpha=1, s=2)

        # blue region was detected on 1 day UTC 2023/06/14 02:03:00 - 2023/06/14 07:39:00 clear dark sky with stars
        # I wonder if the infared detect the wavelength from the stars?
        # Double checked the Aurora past activity and none was detected on that day
        # Jupiter is highly visible on that day
        # Checked the spectrum of Infrared of Jupiter https://articles.adsabs.harvard.edu//full/1966ApJ...143..949D/0000950.000.html
        # the question is, how do I check the corelation
        blue_region = ax.scatter(
            another_weird_date['Pyro [uV]'], another_weird_date[col], c='b', alpha=1, s=2)
    # ax.plot( df['y_hats'], df[col], 'ko', color = 'red', alpha=0.05)
    ax.set_xlabel('Pyro [uV]', fontweight='bold')
    ax.set_ylabel(col, fontweight='bold')
    fig.colorbar(scatter, location='bottom')

plt.tight_layout()
plt.show()
