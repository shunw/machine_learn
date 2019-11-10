import csv
import MySQLdb as mysql
import re
import os

csv_data = csv.reader(open('TENNISDB.csv', encoding ='utf-8'))

# this is to get the title list name
n = 0
for row in csv_data:
    list_title = row
    break

list_title = ['item_id', 'tourney_id', 'tourney_name', 'surface', 'draw_size', 'tourney_level', 'tourney_date', 'match_id', 'winner_id', 'winner_seed', 'winner_entry', 'winner_name', 'winner_hand', 'winner_ht', 'winner_ioc', 'winner_age', 'winner_rank', 'winner_rank_points', 'loser_id', 'loser_seed', 'loser_entry', 'loser_name', 'loser_hand', 'loser_ht', 'loser_ioc', 'loser_age', 'loser_rank', 'loser_rank_points', 'score', 'best_of', 'round', 'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']

sql_type_dict = {'string': 'VARCHAR(50)', 'int': 'INTEGER', 'date': 'DATETIME', 'float': 'DECIMAL(8, 3)'}

item_type_dict = {'string': ['tourney_id', 'tourney_name', 'surface', 'tourney_level', 'winner_entry', 'winner_name', 'winner_hand', 'winner_ioc', 'loser_entry', 'loser_name', 'loser_hand', 'loser_ioc', 'score', 'round'], 

    'int': ['item_id', 'draw_size', 'match_id', 'winner_id', 'winner_seed', 'winner_rank', 'winner_rank_points', 'loser_id', 'loser_seed', 'loser_rank', 'loser_rank_points', 'best_of', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced'], 

    'float': ['winner_ht', 'winner_age', 'loser_ht', 'loser_age', 'minutes'],

    'date': ['tourney_date']}
def get_type(name, item_type_dict, sql_type_dict): 
    for k, v in item_type_dict.items(): 
        if name in v: 
            return (sql_type_dict[k])

sql_title_dict = {}

for i in list_title: 
    
    sql_title_dict[i] = name_type = get_type(i, item_type_dict, sql_type_dict)



sqluser = os.environ['sqluser']
sqlpwd = os.environ['sqlpwd']
sqlhost = os.environ['sqlhost']

# # create database
# mydb = mysql.connect(host = sqlhost, user = sqluser, passwd = sqlpwd)
# mycreate = mydb.cursor()
# mycreate.execute('CREATE DATABASE tennis_data')

db1 = mysql.connect(host = sqlhost, user = sqluser, passwd = sqlpwd, db = 'tennis_data')

cursor = db1.cursor()

# # create tennis_data db
# sql = 'CREATE DATABASE IF NOT EXISTS tennis_data'
# cursor.execute(sql)

# # create tennis_data table framework
# sql_command_text = ''
# start_command = 'CREATE TABLE tennis ('
# end_command = ');'

# sql_command_text = start_command

# for i in list_title: 
#     if i == 'item_id': 
#         sql_command_text += i + ' ' + sql_title_dict[i] + ' NOT NULL, '
#     else:
#         sql_command_text += i + ' ' + sql_title_dict[i] + ', '
# sql_command_text = sql_command_text[:-2]
# sql_command_text += end_command
# # print (sql_command_text)
# cursor.execute(sql_command_text)

# insert data into the table
def sql_micro_entry(data_list):
    # add the '' in the space and - data
    new_list = list()
    for ind, i in enumerate(data_list): 
        if not i: 
            new_list.append('NULL')
        elif get_type(list_title[ind], item_type_dict, sql_type_dict) == 'VARCHAR(50)': 
            if "'" in i:
                i = i.replace("'", '')
            new_list.append("'" + i + "'")
        else: 
            new_list.append(i)
    return new_list


for line in csv_data:
    
    sql_insert_value = 'INSERT INTO tennis VALUES ('+ ', '.join(sql_micro_entry(line)) + ');'
    cursor.execute(sql_insert_value)
    

    

# cursor.execute('use tennis_data;')
# cursor.execute('show tables;')
# cursor.execute('SHOW COLUMNS FROM tennis')
# cursor.execute('DELETE FROM tennis')
# cursor.execute('select * from tennis')
# cursor.execute('SELECT COUNT(*) FROM tennis')
# tables = cursor.fetchall()   
# print (tables)



# print ('aaa')
db1.commit()
db1.close()

# print (list_title)

