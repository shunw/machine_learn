USE tennis_data;

-- select count(*) from(
-- SELECT loser_name, tourney_id, l_ace, 'a'
-- FROM tennis
-- UNION
-- SELECT winner_name, tourney_id, w_ace, 'b'
-- FROM tennis
-- ) as b
-- ;

-- SELECT loser_name as 'player_name', tourney_date, tourney_id, l_ace/(l_1stWon + l_2ndWon + w_svpt - w_1stWon - w_2ndWon) as 'ace%', 0 as 'w_or_l'
-- FROM tennis
-- WHERE loser_name like '%rog%fed%'
-- LIMIT 10;

-- SELECT winner_name as 'player_name', tourney_date, tourney_id, w_ace/(w_1stWon + w_2ndWon + l_svpt - l_1stWon - l_2ndWon) as 'ace%', 1 as 'w_or_l'
-- FROM tennis
-- WHERE winner_name like '%rog%fed%'

-- LIMIT 10;

-- SELECT loser_name as 'player_name', tourney_date, tourney_id, l_1stWon/l_1stIn as '1st_in_per', 0 as 'w_or_l'
-- FROM tennis
-- WHERE loser_name like '%rog%fed%'
-- LIMIT 10;

-- select count(*) from (
-- SELECT winner_name as 'player_name', tourney_date, tourney_id, w_1stWon/w_1stIn as '1st_in_per', 1 as 'w_or_l'
-- FROM tennis
-- WHERE surface = 'Hard' and winner_name like '%rog%fed%' and tourney_date between '2016-01-01' and '2018-12-31'

-- UNION 

-- SELECT loser_name as 'player_name', tourney_date, tourney_id, l_1stWon/l_1stIn as '1st_in_per', 0 as 'w_or_l'
-- FROM tennis
-- WHERE surface = 'Hard' and winner_name like '%rog%fed%'


-- ORDER BY tourney_date
-- ) as b;

-- select count(*) from (
-- SELECT winner_name as 'player_name', tourney_date, tourney_id, w_1stWon/w_1stIn as '1st_in_per', 1 as 'w_or_l'
-- FROM tennis
-- WHERE winner_name like '%rog%fed%' and tourney_date between '2016-01-01' and '2018-12-31'
-- ORDER BY tourney_date
-- LIMIT 10;
-- ) as b;

-- select count(*) from (
-- SELECT loser_name as 'player_name', tourney_date, tourney_id, l_1stWon/l_1stIn as '1st_in_per', 0 as 'w_or_l'
-- FROM tennis
-- WHERE surface = 'Hard' and loser_name like '%rog%fed%'
-- ) as b;

-- select count(*) from (
-- SELECT winner_name as 'player_name', tourney_date, tourney_id, w_1stWon/w_1stIn as '1st_in_per', 1 as 'w_or_l'
-- FROM tennis
-- WHERE surface = 'Grass'and winner_name like '%rog%fed%'
-- ) as c;

-- SELECT player_name, tourney_date, tourney_id, tourney_name, avg(1w_sp) as avg_1w_sp, avg(t_sp) as avg_t_sp, avg(t_rp) as avg_t_rp
-- FROM (
-- SELECT winner_name as player_name, loser_name as opponent_name, 1 as w_or_l,tourney_date, tourney_id, tourney_name, w_1stIn/w_svpt as 1in_sp, w_1stWon/w_1stIn as 1w_sp, w_2ndWon/(w_svpt - w_df - w_1stIn) as 2w_sp, (l_1stIn - l_1stWon)/l_1stIn as 1w_rp, (l_svpt - l_df - l_1stIn - l_2ndWon)/(l_svpt - l_df - l_1stIn) as 2w_rp, (w_1stWon + w_2ndWon)/w_svpt as t_sp, (l_svpt - l_1stIn - l_2ndWon)/l_svpt as t_rp
-- FROM tennis
-- WHERE winner_name like '%rog%fed%'

-- UNION

-- SELECT loser_name as player_name, winner_name as opponent_name, 0 as w_or_l, tourney_date, tourney_id, tourney_name, l_1stIn/l_svpt as 1in_sp, l_1stWon/l_1stIn as 1w_sp, l_2ndWon/(l_svpt - l_df - l_1stIn) as 2w_sp, (w_1stIn - w_1stWon)/w_1stIn as 1w_rp, (w_svpt - w_df - w_1stIn - w_2ndWon)/(w_svpt - w_df - w_1stIn) as 2w_rp, (l_1stWon + l_2ndWon)/l_svpt as t_sp, (w_svpt - w_1stIn - w_2ndWon)/w_svpt as t_rp
-- FROM tennis
-- WHERE loser_name like '%rog%fed%'

-- ) as b
-- GROUP BY player_name, tourney_date, tourney_id, tourney_name
-- LIMIT 10
-- ;



SELECT p.*, pcal.avg_1w_sp, pcal.avg_t_rp, pcal.avg_t_sp
FROM player_match_stat as p
LEFT JOIN player_match_stat_cal as pcal
ON p.player_name = pcal.player_name and p.tourney_id = pcal.tourney_id
LIMIT 10;
-- select *
-- from tennis 
-- where w_svpt = 0 and w_svpt is not NULL
-- limit 10;


-- 1in_sp: 一发进球率
-- 1w_sp: 一发赢球率
-- 2w_sp: 二发赢球率
-- 1w_rp: 一发回球率
-- 2w_rp: 二发回球率
-- t_sp: 发球局赢率
-- t_rp: 回球局赢率