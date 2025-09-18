#Data loader (task №2)

import pandas as pd

url='https://drive.google.com/uc?id=1dTauyYXM4FfCyeFgc6jAS9XtkjTdfsVt'

df=pd.read_csv(url)

print(df.head())

#saving the dataset (for offline access)

import os

script_dir = str(os.path.dirname(__file__))
print('SCRIPT DIRECTORY:',script_dir)
files_dir = script_dir + '\\data\\'

if not os.path.exists(files_dir):
    os.makedirs(files_dir)

df.to_csv(files_dir+'dataset.csv',index=False)
