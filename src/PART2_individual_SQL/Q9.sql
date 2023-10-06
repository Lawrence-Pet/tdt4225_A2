/*
# Question 9: Find the top 15 users who have gained the most altitude meters
*/

/*This removes all trackpoints with -777*/
WITH trackpoint_a_cleaner AS( 

    SELECT TrackPoint.*, t2.user_id
    FROM TrackPoint
    JOIN Activity as t2
    ON TrackPoint.activity_id = t2.activity_id
    WHERE altitude != -777
)

SELECT 
    A.user_id,  
    SUM((B.altitude) - (A.altitude) * 0.3048) as altitude_gain
FROM  trackpoint_a_cleaner AS A
JOIN trackpoint_a_cleaner AS B 
    ON(A.trackpoint_id = B.trackpoint_id-1)
WHERE A.activity_id = B.activity_id 
    AND (B.altitude - A.altitude) > 0
GROUP BY user_id
ORDER BY altitude_gain DESC
LIMIT 15;