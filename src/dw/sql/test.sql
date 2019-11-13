USE tennis_data;

SELECT round, 
    @r:=CASE WHEN  @id <> tourney_id THEN 1 ELSE @r:= @r+1 END as round_count,
    @id:= tourney_id as t_id
FROM(
    SELECT tourney_id, round, COUNT(round) as total
    FROM tennis
    GROUP BY round, tourney_id
    HAVING tourney_id in ('2018-M020', '2018-0451', '2018-M001', '2016-0605', '2007-615')
    ORDER BY tourney_id, total desc
    LIMIT 20
    ) totals, (SELECT @r:= 0, @id:=NULL)round_count;