#! /usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
# import seaborn as sns
from sklearn import linear_model
from sklearn.model_selection import train_test_split
# import statsmodels.api as sm
import duckdb
import timezone

import glob
import os

directory_path = 'raw/Logs'
files = glob.glob(os.path.join(directory_path, '*.txt'))

df = pd.read_csv('combined_logs.csv')

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
df['White_u'] = df['White_u'].astype('float').round().astype('int')
df['Pyro [uV]'] = df['Pyro [uV]'].astype('float').round().astype('int')
df['IR_M_u'] = df['IR_M_u'].astype('float')

print(df['White_u'])

df['Time [UTC]'] = pd.to_datetime(df["Time [UTC]"])
df = df[(df['Time [UTC]'].dt.hour >= 9) & (df['Time [UTC]'].dt.hour <= 17)]
df = duckdb.query("SELECT  *  FROM df WHERE White_u < 65535").to_df()
weird_date = duckdb.query(
    'SELECT "Time [UTC]", "Pyro [uV]", "IR_M_u" FROM df WHERE ((IR_M_u < 1.5 AND IR_M_u > 0.5) AND ("Pyro [uV]" < 8000 AND "Pyro [uV]" > 2000))').to_df()
print(weird_date)
another_weird_date = duckdb.query(
    'SELECT "Time [UTC]", "Pyro [uV]", "IR_M_u" FROM df WHERE ((IR_M_u < 1.56 AND IR_M_u > 0.13) AND ("Pyro [uV]" < 250 AND "Pyro [uV]" > -67))').to_df()
print(another_weird_date)
# Removing battery level, roll, pitch, K&Z Temp, and NA row that was added as a buffer.
t_fract = df['Time [UTC]'].astype(str)
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

Y = df[['Pyro [uV]']]
X = df.drop(columns=['Pyro [uV]'])

# color = 1 - (t_fract * 0.8 + 0.1)
color = t_fract

fig = plt.figure(figsize=(8, 10))
i = 0
for col in cols:
    i += 1
    ax = plt.subplot(3, 2, i)
    scatter = ax.scatter(df['Pyro [uV]'], df[col], c=t_fract, alpha=0.05, s=2)
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
