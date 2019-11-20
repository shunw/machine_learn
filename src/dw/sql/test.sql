USE tennis_data;

select count(*) from(
SELECT loser_name, l_ace, 'a'

FROM tennis) as b
;