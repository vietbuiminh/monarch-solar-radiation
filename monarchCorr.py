import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

#  Reading in log file
df = pd.read_csv('Log00001.csv')

# Removing battery level, roll, pitch, K&Z Temp, and NA row that was added as a buffer.
df = df.iloc[: ,3:]
df = df.drop(columns=[" Bat [V]", " R_u [deg]", " P_u [deg]"])
df = df.iloc[: ,:-2]
print(df)

# Seaborn Hearmap
#sns.heatmap(df.corr());
#plt.show()

# 6 columns
cols = [' UVA_u', ' UVB_u', ' White_u', ' Vis_u [lx]', ' IR_S_u',
       ' IR_M_u']
       

plt.figure(figsize=(8,10))
i=0
for col in cols:
    i += 1
    ax = plt.subplot(3, 2, i)
    ax.plot( df[' Pyro [uV]'], df[col], 'ko' )
    ax.set_xlabel(' Pyro [uV]', fontweight='bold')
    ax.set_ylabel(col, fontweight='bold')
    
plt.tight_layout()
plt.show()