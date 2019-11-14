USE tennis_data;

SELECT winner_name, sum(winner_rank_points), date_format(tourney_date + interval 30 day, '%Y-%m-%d') as 'time_logged'
FROM tennis
GROUP BY  time_logged, winner_name
HAVING winner_name like '%rog%fed%'
ORDER BY time_logged
LIMIT 10;

SELECT winner_name, winner_rank_points, tourney_date, date_format(tourney_date + interval 30 day, '%Y-%m-%d') as 'time_logged'
FROM tennis

HAVING winner_name like '%rog%fed%'
ORDER BY tourney_date
LIMIT 10;