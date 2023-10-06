WITH close_time (user_id1, user_id2, activity_id1, activity_id2) AS (
    SELECT DISTINCT A1.user_id AS user1, A2.user_id AS user2, A1.activity_id AS activity_id1, A2.activity_id AS activity_id2
    FROM Activity AS A1
    INNER JOIN Activity AS A2 ON A1.user_id <> A2.user_id
        AND (ABS(TIMESTAMPDIFF(SECOND, A1.start_date_time, A2.start_date_time)) <= 30
            OR ABS(TIMESTAMPDIFF(SECOND, A1.end_date_time, A2.end_date_time)) <= 30
            OR A1.start_date_time BETWEEN A2.start_date_time AND A2.end_date_time
            OR A1.end_date_time BETWEEN A2.start_date_time AND A2.end_date_time)
        AND A1.user_id < A2.user_id
),
trackpoints (tr_activity_id, lat, lon, tr_date_time) AS (
    SELECT activity_id, lat, lon, date_time
    FROM TrackPoint
)
SELECT COUNT(DISTINCT user_id1) AS number_of_users
    FROM close_time
INNER JOIN trackpoints AS T1 ON activity_id1 = T1.tr_activity_id
INNER JOIN trackpoints AS T2 ON activity_id2 = T2.tr_activity_id
AND ST_Distance_Sphere(
        POINT(T1.lon, T1.lat),
        POINT(T2.lon, T2.lat)
        ) <= 50