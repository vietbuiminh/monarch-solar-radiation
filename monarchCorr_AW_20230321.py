#! /usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
# import seaborn as sns
from sklearn import linear_model
from sklearn.model_selection import train_test_split
# import statsmodels.api as sm
import duckdb

#  Reading in log file
df = pd.read_csv('Logs/Log00020.csv')

# remove the extra spacing infront of the heading of the columns
df.columns = df.columns.str.replace(r'^\s+', '', regex=True)
df['White_u'] = df['White_u'].astype('int')
df['Pyro [uV]'] = df['Pyro [uV]'].astype('int')
df['IR_M_u'] = df['IR_M_u'].astype('float')

print(df['White_u'])

df = duckdb.query("SELECT  *  FROM df WHERE White_u < 65535").to_df()
weird_date = duckdb.query(
    'SELECT "Time [UTC]", "Pyro [uV]", "IR_M_u" FROM df WHERE ((IR_M_u < 1.5 AND IR_M_u > 0.5) AND ("Pyro [uV]" < 8000 AND "Pyro [uV]" > 2000))').to_df()
print(weird_date)
another_weird_date = duckdb.query(
    'SELECT "Time [UTC]", "Pyro [uV]", "IR_M_u" FROM df WHERE ((IR_M_u < 1.56 AND IR_M_u > 0.13) AND ("Pyro [uV]" < 250 AND "Pyro [uV]" > -67))').to_df()
print(another_weird_date)
# Removing battery level, roll, pitch, K&Z Temp, and NA row that was added as a buffer.
t_fract = df['Time [UTC]']
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
        red_region = ax.scatter(
            weird_date['Pyro [uV]'], weird_date[col], c='r', alpha=1, s=2)
        blue_region = ax.scatter(
            another_weird_date['Pyro [uV]'], another_weird_date[col], c='b', alpha=1, s=2)
    # ax.plot( df['y_hats'], df[col], 'ko', color = 'red', alpha=0.05)
    ax.set_xlabel('Pyro [uV]', fontweight='bold')
    ax.set_ylabel(col, fontweight='bold')
    fig.colorbar(scatter, location='bottom')

plt.tight_layout()
plt.show()
