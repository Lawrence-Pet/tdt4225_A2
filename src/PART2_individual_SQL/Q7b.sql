/*
## Question 7b: List the transportation mode, user id, and duration for these activities
*/

WITH difference_seconds AS (
    SELECT user_id, transportation_mode, TIMESTAMPDIFF(SECOND, start_date_time, end_date_time) AS seconds
    FROM Activity
    WHERE DATE(start_date_time) != DATE(end_date_time)
),

diff_clock AS (
    SELECT 
        user_id, 
        transportation_mode,
        seconds, 
        MOD(seconds, 60) AS seconds_p,
        MOD(seconds, 60*60) AS minutes_p,
        MOD(seconds, 60*60*24) AS hours_p
    FROM
        difference_seconds
) 

SELECT
    user_id,
    transportation_mode,
    CONCAT(
        FLOOR(seconds / 3600 / 24), ' days ',
        FLOOR(hours_p / 3600), ' hours ',
        FLOOR(minutes_p / 60), ' minutes ',
        seconds_p, ' seconds '
    ) AS duration
FROM diff_clock;