/*
* Question 12: Find all users who have registered transportation_mode and their most used transportation_mode. 
**  The answer should be on format (user_id, most_used_transportation_mode) sorted on user_id.
**  Some users may have the same number of activities tagged with e.g. walk and car. In this case it is up to you to decide which transportation mode to include in your answer (choose one).
**  Do not count the rows where the mode is null.
*/

WITH transport_modes AS (
    SELECT 
        user_id, 
        activity_id, 
        transportation_mode 
    FROM 
        Activity 
    WHERE 
        transportation_mode != 'NULL' 
), 

counted_tm AS (
    SELECT 
        user_id, 
        COUNT(*) AS n_used, 
        transportation_mode
    FROM 
        transport_modes
    GROUP BY 
        transportation_mode, user_id
)

SELECT 
    DISTINCT A.user_id, 
    A.n_used AS max_count,
    A.transportation_mode
FROM 
    counted_tm AS A
JOIN (
    SELECT 
        user_id, 
        MAX(n_used) AS max_n_used
    FROM 
        counted_tm
    GROUP BY 
        user_id
) AS B
ON 
    A.user_id = B.user_id 
    AND A.n_used = B.max_n_used
;

