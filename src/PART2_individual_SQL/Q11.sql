/*
* 11. Find all users who have invalid activities, and the number of invalid activities per user
*/

WITH invalid_act AS(
    SELECT *
    FROM(

        SELECT 
            A.activity_id,
            A.trackpoint_id as track_id_A,
            B.trackpoint_id as track_id_B,
            TIMESTAMPDIFF(SECOND, A.date_time, B.date_time) as sec_dif
        FROM TrackPoint A
        JOIN TrackPoint B
        ON (A.trackpoint_id = B.trackpoint_id -1)
        WHERE A.activity_id = B.activity_id
    ) as dif_table
    WHERE sec_dif > 300 /* 5 minutes */
),

dist_acts AS (
SELECT DISTINCT activity_id
FROM invalid_act
)

SELECT 
    Activity.user_id, 
    COUNT(dist_acts.activity_id) as N_invalid_activities
FROM dist_acts
JOIN Activity
ON Activity.activity_id = dist_acts.activity_id
GROUP BY user_id
;