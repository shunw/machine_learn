USE tennis_data;

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
    
    LIMIT 10 ;

