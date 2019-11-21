USE tennis_data;

select count(*) from(
SELECT loser_name, tourney_id, l_ace, 'a'
FROM tennis
UNION
SELECT winner_name, tourney_id, w_ace, 'b'
FROM tennis
) as b
;

SELECT loser_name as 'player_name', tourney_date, tourney_id, l_ace as 'ace', 1 as 'w_or_l'
FROM tennis
WHERE loser_name like '%rog%fed%'
-- ORDER BY tourney_date
UNION
SELECT winner_name as 'player_name', tourney_date, tourney_id, w_ace as 'ace', 0 as 'w_or_l'
FROM tennis
WHERE winner_name like '%rog%fed%'
ORDER BY tourney_date
LIMIT 10;