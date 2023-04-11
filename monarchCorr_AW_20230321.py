#! /usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

#  Reading in log file
df = pd.read_csv('Log00002.csv')

# Removing battery level, roll, pitch, K&Z Temp, and NA row that was added as a buffer.
df = df.iloc[: ,3:]
df = df.drop(columns=[" Bat [V]", " R_u [deg]", " P_u [deg]"])
df = df.iloc[: ,:-2]
#print(df)

# Seaborn Hearmap
#sns.heatmap(df.corr());
#plt.show()

#dfCorr = (df.corr())
#dfCorr.to_excel('test.xlsx', sheet_name='sheet1', index=True)

# 6 columns
cols = [' UVA_u', ' UVB_u', ' White_u', ' Vis_u [lx]', ' IR_S_u',
       ' IR_M_u']
       
Y = df[[' Pyro [uV]']]
X = df.drop(columns=[' Pyro [uV]'])
#(X_train, X_test, y_train, y_test) = train_test_split(X, Y, train_size = 0.8)

regr = linear_model.LinearRegression()
regr.fit(X, Y) 

y_hats2 = regr.predict(X)
df['y_hats'] = y_hats2

# Plot colors of points based on time stamp
# Assuming everything in order
t_fract = df.index / df.index.max()
#color = 1 - (t_fract * 0.8 + 0.1)


fig = plt.figure(figsize=(8,10))
i=0
for col in cols:
    i += 1
    ax = plt.subplot(3, 2, i)
    scatter = ax.scatter( df[' Pyro [uV]'], df[col], c=t_fract, alpha=0.1 )
    #ax.plot( df['y_hats'], df[col], 'ko', color = 'red', alpha=0.2)
    ax.set_xlabel(' Pyro [uV]', fontweight='bold')
    ax.set_ylabel(col, fontweight='bold')
    fig.colorbar(scatter, location='bottom')
    
plt.tight_layout()
plt.show()

