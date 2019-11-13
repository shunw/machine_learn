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
#             winner_name as player_name, tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date, winner_hand as player_hand, winner_age as player_age, winner_ht as player_ht, winner_rank_points as player_rank_points
#             FROM tennis
#         UNION
#             SELECT DISTINCT
#             loser_name as player_name, tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date, loser_hand as player_hand, loser_age as player_age, loser_ht as player_ht, loser_rank_points as player_rank_points
#             FROM tennis
#     ''')

# # get the tourney and its round information
# cursor.execute('''
#         CREATE TABLE tourney_r_inf
#         SELECT round, 
#             @r:=CASE WHEN  @id <> tourney_id THEN 1 ELSE @r:= @r+1 END as round_count,
#             @id:= tourney_id as t_id
#         FROM(
#             SELECT tourney_id, round, COUNT(round) as total
#             FROM tennis
#             GROUP BY round, tourney_id
#             ORDER BY tourney_id, total desc
            
#             ) totals, (SELECT @r:= 0, @id:=NULL)round_count;
#         ''')

# # tables = cursor.fetchall() 

# # know the player win and lose information in a tourney
# cursor.execute('''
#     CREATE TABLE win_info
#         SELECT ten.winner_name, MAX(tny.round_count) as winner_max_round, ten.tourney_id
#         FROM tennis as ten
#         LEFT JOIN tourney_r_inf as tny
#         ON ten.tourney_id = tny.t_id and ten.round = tny.round
#         GROUP BY ten.winner_name, ten.tourney_id;

#     ''')

# cursor.execute('''
#     CREATE TABLE lose_info
#         SELECT 
#             loser_name, COUNT(*) as loser_count, tourney_id
#         FROM tennis
#         GROUP BY tourney_id, loser_name
#         order by loser_count desc

#     ''')

# # get the tourney and it's round qty
# cursor.execute('''
#     CREATE TABLE tourney_r_total
#         SELECT t_id as tourney_id, MAX(round_count) as round_total
#         FROM tourney_r_inf 
#         GROUP BY t_id;

#     ''')


# create the table, player and his win/ lose count in a tourney
cursor.execute('''
CREATE TABLE player_wl_tourney
    SELECT player_name, add_final.tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date, 
        CASE WHEN final_winner_name is NULL THEN 0
        ELSE 1 END as final_winner, 
    r_t.round_total, w.winner_max_round, 
    CASE WHEN w.winner_max_round is NULL THEN 0
        ELSE w.winner_max_round / r_t.round_total * 100 END as win_percent, 
    player_hand, player_age, player_ht, player_rank_points

    FROM(
    SELECT p.*, f.final_winner_name 
    FROM player_info as p
    LEFT JOIN final_win_info as f
    ON f.final_winner_name = p.player_name and f.tourney_id = p.tourney_id
    ) as add_final
    
    LEFT JOIN win_info as w
    ON w.winner_name = add_final.player_name and w.tourney_id = add_final.tourney_id
    
    LEFT JOIN tourney_r_total as r_t
    ON r_t.tourney_id = add_final.tourney_id
    
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
