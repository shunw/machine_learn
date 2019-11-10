USE tennis_data
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