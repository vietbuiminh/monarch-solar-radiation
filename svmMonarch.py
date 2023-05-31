#! /usr/bin/python3

import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

#  Reading in log file
df1 = pd.read_csv('Logs/Log00007.csv') 
df2 = pd.read_csv('Logs/Log00008.csv')
df3 = pd.read_csv('Logs/Log00002.csv')
df4 = pd.read_csv('Logs/Log00004.csv')
frames = [df1, df2, df3, df4]
df = pd.concat(frames)

t_fract = df['Time [UTC]']
t_fract = (t_fract.str[11:13])
t_fract = t_fract.astype(int)
# + t_fract.str[14:16]


# Removing battery level, roll, pitch, K&Z Temp, and NA row that was added as a buffer.
df = df.iloc[: ,2:]
df = df.drop(columns=[" Bat [V]", " R_u [deg]", " P_u [deg]"])
df = df.iloc[: ,:-2]

#dfCorr = (df.corr())
#dfCorr.to_excel('test.xlsx', sheet_name='sheet1', index=True)

# 6 columns
cols = [' UVA_u', ' UVB_u', ' White_u', ' Vis_u [lx]', ' IR_S_u',
       ' IR_M_u']

y = df[[' Pyro [uV]']]
X = df.drop(columns=[' Pyro [uV]'])
(X_train, X_test, y_train, y_test) = train_test_split(X, y, train_size = 0.3)


# Keris Model
model = Sequential()
model.add(Dense(12, input_shape=(9,), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=150, batch_size=10)
score = model.evaluate(X_test, y_test, verbose=0)

print(score)
print("Done")