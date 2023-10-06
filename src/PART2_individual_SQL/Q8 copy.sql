WITH close_time (user_id1, user_id2, activity_id1, activity_id2) AS (
    SELECT DISTINCT A1.user_id AS user1, A2.user_id AS user2, A1.activity_id AS activity_id1, A2.activity_id AS activity_id2
    FROM Activity AS A1
    INNER JOIN Activity AS A2 
    ON A1.user_id <> A2.user_id
        AND (ABS(TIMESTAMPDIFF(SECOND, A1.start_date_time, A2.end_date_time)) <= 30
            OR ABS(TIMESTAMPDIFF(SECOND, A1.end_date_time, A2.start_date_time)) <= 30
            OR A1.start_date_time BETWEEN A2.start_date_time AND A2.end_date_time
            OR A1.end_date_time BETWEEN A2.start_date_time AND A2.end_date_time)
        AND A1.user_id < A2.user_id
),

filter_trackpoints AS(
    SELECT * 
    FROM TrackPoint
    WHERE activity_id IN (
        SELECT DISTINCT activity_id1 FROM close_time
        UNION
        SELECT DISTINCT activity_id2 FROM close_time)
),

t1 as (
    SELECT ft.*, ct.user_id1 as user_id
    FROM close_time AS ct
    JOIN filter_trackpoints AS ft
    ON (ct.activity_id1 = ft.activity_id)
),

t2 AS(
    SELECT ft.*, ct.user_id2 as user_id
    FROM close_time AS ct
    JOIN filter_trackpoints AS ft
    ON (ct.activity_id2 = ft.activity_id)
),

trackpoints AS (
    SELECT 
        t2.user_id as id_2, 
        t2.activity_id as activity_id2,
        t2.lon as lon2,
        t2.lat as lat2,
        t2.date_time as date_time2,
        t1.user_id as id_1, 
        t1.activity_id as activity_id1,
        t1.lon as lon1,
        t1.lat as lat1,
        t1.date_time as date_time1,
        ABS(TIMESTAMPDIFF(SECOND, t1.date_time, t2.date_time)) as temporal_diff_secs,
        ST_Distance_Sphere(POINT(t1.lon, t1.lat),POINT(t2.lon, t2.lat)) as spatial_dif   
    FROM t1
    JOIN t2
    ON(
        t1.activity_id <> t2.activity_id
        AND ABS(TIMESTAMPDIFF(SECOND, t1.date_time, t2.date_time)) < 30
        AND ST_Distance_Sphere(POINT(t1.lon, t1.lat),POINT(t2.lon, t2.lat)) <= (50 / 111139) /*converting 50 meter to decimal coordinate*/
        AND t1.activity_id < t2.activity_id
    )
)

SELECT COUNT(DISTINCT id_1) as n_users FROM trackpoints;