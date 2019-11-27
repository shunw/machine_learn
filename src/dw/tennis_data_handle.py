import csv
import MySQLdb as mysql
import re
import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns
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
    SELECT p.*, pcal.avg_1w_sp, pcal.avg_t_rp, pcal.avg_t_sp
    FROM player_match_stat as p
    LEFT JOIN player_match_stat_cal as pcal
    ON p.player_name = pcal.player_name and p.tourney_id = pcal.tourney_id

    '''

df_cal = pd.read_sql_query(sql = sql_commnd, con=db1)


db1.close()


winner_name = 'winner_name'
tourney_name = 'tourney_name'
tourney_date = 'tourney_date'
tourney_id = 'tourney_id'
player_name = 'player_name'
opponent_name = 'opponent_name'
surface = 'surface'
draw_size = 'draw_size'
loser_count = 'loser_count'
win_percent = 'win_percent'
rolling_score_180 = 'rolling_score_180'
wt_win_percent = 'wt_win_percent'
scaled_period_score = 'scaled_period_score'
level_weight = 'level_weight'
player_hand = 'player_hand'
player_age = 'player_age'
player_ht ='player_ht'
player_rank_points = 'player_rank_points'

# this part is calculate the mean on wt_win_percent from current back to some period
def get_rolling_amount(grp, freq, col_mean): 
    return grp.rolling(freq, on=tourney_date)[col_mean].mean()

df_cal['avg_t_sp_365'] = np.transpose(df_cal.groupby(player_name, as_index = False, group_keys = False).apply(get_rolling_amount, '365D', 'avg_t_sp'))

df_cal_chose = df_cal.loc[(df_cal[player_name] == 'Roger Federer') & (df_cal[opponent_name] == 'Novak Djokovic')]

print (df_cal_chose.head())



#================= ABOVE IS CONSTRUCT DATAFRAME =====================

# nes_col = list([win_percent, player_name, tourney_id, surface, draw_size, level_weight, player_hand, player_age, player_ht, player_rank_points, scaled_period_score])
# cat_cols = list([player_name, tourney_id, surface, player_hand])
# y_col = win_percent

# # this is to convert all the category into float/ int
# df_short = df[nes_col]
# df_one_hot = pd.get_dummies(df_short, prefix = cat_cols)

# X, y = df_one_hot.iloc[:, 1:].values, df_one_hot.iloc[:, 0].values
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3, stratify = y, random_state = 0)

# sc = StandardScaler()
# X_train_std = sc.fit_transform(X_train)
# X_test_std = sc.transform(X_test)

#================= ABOVE IS SPLIT TRAIN/ TEST DATA =====================

# pair_cols = [scaled_period_score, player_age, player_ht]
# # sns.pairplot(df_short[pair_cols], size = 2.5)
# # plt.scatter(y = df_short[win_percent], x = df_short[player_hand])
# # plt.tight_layout()
# # plt.savefig('player_hand.png')
# # plt.savefig('pairplt.png')

# cm = np.corrcoef(df_short[pair_cols].values.T)
# # sns.set(font_scale = 1.5)
# hm = sns.heatmap(cm, cbar = True, annot = True, square = True, fmt = '.2f', annot_kws = {'size': 15}, yticklabels = pair_cols, xticklabels = pair_cols)
# # hm.set_ylim(0, 10)
# plt.savefig('heatmap.png', bbox_inches='tight')

#================= ABOVE IS TO CHECK PAIRPLOT =====================

# cov_mat = np.cov(X_train_std.T)
# def check_symm(mat):
#     '''
#     check mat is symmetric
#     '''
#     m, n = mat.shape
#     for i in range(m):
#         for j in range(n):
#             if mat[i, j] != mat[j, i]: 
#                 print ('not sym')
#                 print ('the row is {}; the col is {}'.format(i, j))
#                 break
# # check_symm(cov_mat)

# eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)

# # plot the eigen_vals scree plot
# tot = sum(eigen_vals)
# var_exp = list([(i/tot) for i in sorted(eigen_vals, reverse = True)])
# cum_var_exp = np.cumsum(var_exp)
# df_var_exp = pd.DataFrame({'var_exp':var_exp, 'cum_var':cum_var_exp})
# print (df_var_exp.head())
# plt.bar(range(1, 331), var_exp, alpha = .5, align = 'center', label = 'invidivual explained variance')
# plt.step(range(1, 331), cum_var_exp, where = 'mid', label = 'cumulative explained variace')
# plt.ylabel('Explained variace ratio')
# plt.xlabel('Principal component index')
# plt.legend(loc = 'best')
# plt.savefig('tennis_pca.png')

#================= ABOVE IS PCA PART =====================

# # this is to make the scatter plot to check the relationship
# fig, axes = plt.subplots(1, 1)
# axes.scatter(df.loc[df[player_name] == 'Rafael Nadal', scaled_period_score], df.loc[df[player_name] == 'Rafael Nadal', win_percent], c = 'navy')

# axes.scatter(df.loc[df[player_name] == 'Roger Federer', scaled_period_score], df.loc[df[player_name] == 'Roger Federer', win_percent], c = 'red')
# plt.savefig('pic_output.png')