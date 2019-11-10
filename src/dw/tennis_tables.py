import csv
import MySQLdb as mysql
import re
import os
import pandas as pd
import numpy as np

'''
purpose: to create the related tables and get final query data
'''

sqluser = os.environ['sqluser']
sqlpwd = os.environ['sqlpwd']
sqlhost = os.environ['sqlhost']
db1 = mysql.connect(host = sqlhost, user = sqluser, passwd = sqlpwd, db = 'tennis_data')

cursor = db1.cursor()

# # known the final winner for each tourney
# cursor.execute('''
#     CREATE TABLE final_win_info
#         SELECT winner_name as final_winner_name, tourney_id
#         FROM tennis
#         WHERE round = 'F'
#     ''')

# # tables = cursor.fetchall() 

# # get all the players attend which tourney
# cursor.execute('''
#     CREATE TABLE player_info
#         SELECT DISTINCT
#             winner_name as player_name, tourney_id, tourney_name, surface, draw_size, tourney_date
#             FROM tennis
#         UNION
#             SELECT DISTINCT
#             loser_name as player_name, tourney_id, tourney_name, surface, draw_size, tourney_date
#             FROM tennis
#     ''')
 
# # tables = cursor.fetchall() 

# # know the player win and lose information in a tourney
# cursor.execute('''
#     CREATE TABLE win_info
#         SELECT 
#             winner_name, COUNT(*) as winner_count, tourney_id
#         FROM tennis
#         GROUP BY tourney_id, winner_name

#     ''')

# cursor.execute('''
#     CREATE TABLE lose_info
#         SELECT 
#             loser_name, COUNT(*) as loser_count, tourney_id
#         FROM tennis
#         GROUP BY tourney_id, loser_name
#         order by loser_count desc

#     ''')

# create the table, player and his win/ lose count in a tourney
cursor.execute('''
CREATE TABLE player_wl_tourney
    SELECT player_name, add_final.tourney_id, tourney_name, surface, draw_size, tourney_date, 
        CASE WHEN final_winner_name is NULL THEN 0
        ELSE 1 END as final_winner, 
    l.loser_count, w.winner_count, 
    CASE WHEN l.loser_count is NULL THEN 100
        WHEN w.winner_count is NULL THEN 0
        ELSE w.winner_count / (w.winner_count + l.loser_count) * 100 END as win_percent

    FROM(
    SELECT p.*, f.final_winner_name 
    FROM player_info as p
    LEFT JOIN final_win_info as f
    ON f.final_winner_name = p.player_name and f.tourney_id = p.tourney_id
    ) as add_final
    
    LEFT JOIN lose_info as l
    ON l.loser_name = add_final.player_name and l.tourney_id = add_final.tourney_id

    LEFT JOIN win_info as w
    ON w.winner_name = add_final.player_name and w.tourney_id = add_final.tourney_id
    
    ORDER BY final_winner_name DESC
    ''')

# cursor.execute('DROP TABLE final_win_info')

# cursor.execute('select * from lose_info;')
# cursor.execute('show tables;')
# cursor.execute('show columns in player_info;')

# tables = cursor.fetchall()   

# print (tables)
db1.commit()
db1.close()

# list_title = ['item_id', 'tourney_id', 'tourney_name', 'surface', 'draw_size', 'tourney_level', 'tourney_date', 'match_id', 'winner_id', 'winner_seed', 'winner_entry', 'winner_name', 'winner_hand', 'winner_ht', 'winner_ioc', 'winner_age', 'winner_rank', 'winner_rank_points', 'loser_id', 'loser_seed', 'loser_entry', 'loser_name', 'loser_hand', 'loser_ht', 'loser_ioc', 'loser_age', 'loser_rank', 'loser_rank_points', 'score', 'best_of', 'round', 'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']

# nonselected_title = ['tourney_name', 'surface', 'draw_size', 'tourney_level', 'tourney_date', 'winner_id', 'winner_seed', 'winner_entry', 'winner_hand', 'winner_ht', 'winner_ioc', 'winner_age', 'winner_rank', 'winner_rank_points', 'loser_id', 'loser_seed', 'loser_entry', 'loser_hand', 'loser_ht', 'loser_ioc', 'loser_age', 'loser_rank', 'loser_rank_points']

# winner_name = 'winner_name'
# tourney_name = 'tourney_name'
# tourney_date = 'tourney_date'
# tourney_id = 'tourney_id'
# # final_w_list = [winner_name, tourney_name, tourney_id, tourney_date] # for the query [final winner for each tourney]
# # player_name_list = ['player_name', tourney_id] # player list 
# df = pd.DataFrame(tables, columns = ['player_name', 'win_count', 'loser_count', 'tourney_id', 'win_per'])  
# print (df)
