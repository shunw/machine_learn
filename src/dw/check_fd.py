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
this is to check the scatter for one field
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
    WHERE surface = 'Hard' and winner_name like '%rog%fed%' and tourney_date between '2016-01-01' and '2018-12-31'

    '''

df1 = pd.read_sql_query(sql = sql_commnd, con=db1)

sql_commnd = '''

    SELECT loser_name as 'player_name', tourney_date, tourney_id, l_1stWon/l_1stIn as '1st_in_per', 0 as 'w_or_l'
    FROM tennis
    WHERE surface = 'Hard' and winner_name like '%rog%fed%' and tourney_date between '2016-01-01' and '2018-12-31'


    ORDER BY tourney_date

    '''

df2 = pd.read_sql_query(sql = sql_commnd, con=db1)

db1.close()

ax1 = df1.plot(x = 'tourney_date', y = '1st_in_per', c = 'DarkBlue', style = '.', alpha = .5)
ax2 = df2.plot(x = 'tourney_date', y = '1st_in_per', c = 'Red', style = 'x', ax = ax1)
plt.savefig('check_df.png')