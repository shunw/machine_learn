import csv
import MySQLdb as mysql
import re
import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

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
    SELECT win_percent, tourney_date 
    FROM player_wl_tourney
    WHERE lower(player_name) like '%raf%nad%' and tourney_date between '2017-01-01 00:00:00' and '2017-12-31 23:59:00' 
    ORDER BY tourney_date
    '''

df = pd.read_sql_query(sql = sql_commnd, con=db1)

# cursor.execute('show columns in player_info')
# tables = cursor.fetchall()
# print (tables)


winner_name = 'winner_name'
tourney_name = 'tourney_name'
tourney_date = 'tourney_date'
tourney_id = 'tourney_id'
player_name = 'player_name'
surface = 'surface'
draw_size = 'draw_size'
loser_count = 'loser_count'
win_percent = 'win_percent'

db1.close()

plt.scatter(df[tourney_date], df[win_percent])
plt.savefig('pic_output.png')