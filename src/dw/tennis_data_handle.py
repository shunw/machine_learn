import csv
import MySQLdb as mysql
import re
import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn import preprocessing

'''
purpose: select query to get the main table and check the data
'''

start_time = time.time()
sqluser = os.environ['sqluser']
sqlpwd = os.environ['sqlpwd']
sqlhost = os.environ['sqlhost']
db1 = mysql.connect(host = sqlhost, user = sqluser, passwd = sqlpwd, db = 'tennis_data')

cursor = db1.cursor()


sql_commnd = '''
    SELECT *, win_percent * level_weight as wt_win_percent
    FROM player_wl_tourney
    WHERE (lower(player_name) like '%raf%nad%' or lower(player_name) like '%rog%fed%') and tourney_date between '2015-01-01 00:00:00' and '2017-12-31 23:59:00' 
    ORDER BY player_name, tourney_date
    '''
# 
df = pd.read_sql_query(sql = sql_commnd, con=db1)

db1.close()


winner_name = 'winner_name'
tourney_name = 'tourney_name'
tourney_date = 'tourney_date'
tourney_id = 'tourney_id'
player_name = 'player_name'
surface = 'surface'
draw_size = 'draw_size'
loser_count = 'loser_count'
win_percent = 'win_percent'
rolling_score_180 = 'rolling_score_180'
wt_win_percent = 'wt_win_percent'



# print (df.shape)
def get_rolling_amount(grp, freq): 
    return grp.rolling(freq, on='tourney_date')['wt_win_percent'].mean()

df['rolling_score_180'] = np.transpose(df.groupby('player_name', as_index = False, group_keys = False).apply(get_rolling_amount, '180D'))
# print (df.head())

df['scaled_xxx'] = (df[wt_win_percent] - df[wt_win_percent].min())/ (df[wt_win_percent].max() - df[wt_win_percent].min())
# print (df.head())
fig, axes = plt.subplots(1, 1)
axes.scatter(df.loc[df[player_name] == 'Rafael Nadal', 'scaled_xxx'], df.loc[df[player_name] == 'Rafael Nadal', win_percent], c = 'navy')



axes.scatter(df.loc[df[player_name] == 'Roger Federer', 'scaled_xxx'], df.loc[df[player_name] == 'Roger Federer', win_percent], c = 'red')
plt.savefig('pic_output.png')

# # print (df.loc[df[player_name] == 'Rafael Nadal', tourney_date])