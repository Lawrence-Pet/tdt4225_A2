/*
* ## Question 7a: Find the number of users that have started an activity in one day and ended the activity the next day
*/
WITH result AS (
    SELECT user_id
    FROM Activity
    WHERE DATE(start_date_time) != DATE(end_date_time)
)
SELECT DISTINCT user_id FROM result
;