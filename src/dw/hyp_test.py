import csv
import MySQLdb as mysql
import re
import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import scipy.stats as st

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns
'''
purpose: to check some factor impact the win/ lose result
'''

start_time = time.time()
sqluser = os.environ['sqluser']
sqlpwd = os.environ['sqlpwd']
sqlhost = os.environ['sqlhost']
db1 = mysql.connect(host = sqlhost, user = sqluser, passwd = sqlpwd, db = 'tennis_data')

cursor = db1.cursor()


sql_commnd = '''
    SELECT winner_name as 'player_name', tourney_date, tourney_id, w_1stWon/w_1stIn as '1st_in_per', 1 as 'w_or_l'
    FROM tennis
    WHERE surface = 'Hard' and winner_name like '%rog%fed%'
    '''

df_los = pd.read_sql_query(sql = sql_commnd, con=db1)

sql_commnd = '''
    SELECT loser_name as 'player_name', tourney_date, tourney_id, l_1stWon/l_1stIn as '1st_in_per', 0 as 'w_or_l'
    FROM tennis
    WHERE surface = 'Hard' and loser_name like '%rog%fed%'
    '''

df_win = pd.read_sql_query(sql = sql_commnd, con=db1)

db1.close()
cp_col = '1st_in_per'
# cp_col = 'ace%'

ax = df_win[cp_col].plot.hist(bins = 20,color = 'b', alpha = .5)
ax.axvline(x = df_win[cp_col].mean(), color = 'b', linestyle = '--')
ax = df_los[cp_col].plot.hist(bins = 20, color = 'r', alpha = .5)
ax.axvline(x = df_los[cp_col].mean(), color = 'r', linestyle = '--')


plt.savefig('ace_hist.png')

def hyp_cp_mean(h0_mean, h0_std, h0_n, h1_mean, h1_std, h1_n):
    '''
    this is to compare the mean, with different std
    '''
    z_value = (h0_mean - h1_mean)/ (((h1_std **2)/h1_n + (h0_std**2)/h0_n) ** .5)
    print (z_value)
    z_p = st.norm.cdf(z_value)
    return z_p

h0_mean = df_win[cp_col].mean()
h0_std = df_win[cp_col].std()
h0_n = len(df_win[cp_col])
print (h0_mean, h0_std, h0_n)

h1_mean = df_los[cp_col].mean()
h1_std = df_los[cp_col].std()
h1_n = len(df_los[cp_col])
print (h1_mean, h1_std, h1_n)

z_p = hyp_cp_mean(h0_mean, h0_std, h0_n, h1_mean, h1_std, h1_n)
print (z_p)
# print (df_win['ace%'].mean(), df_win['ace%'].std())
# print (df_los['ace%'].mean(), df_los['ace%'].std())