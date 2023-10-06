/*
* Question 10: Find the users that have traveled the longest total distance in one day for each transportation mode.
* INCLUDES ACTIVITES THAT CROSSES MULTIPLE DATES BUT ONLY TAKES INTO ACCOUNT TRACKPOINTS IN THE SAME DAY. 
* HOWEVER RETURNS MULTIPLE USERS SINCE THEY HAVE SAME MAX
*/
WITH transport_same_day AS (
    SELECT 
        user_id, 
        activity_id, 
        transportation_mode 
    FROM 
        Activity 
    WHERE 
        transportation_mode != 'NULL' 
), 

joined AS (
    SELECT 
        lon, 
        lat,
        date_time, 
        trackpoint_id,
        transport_same_day.user_id,
        transport_same_day.transportation_mode 
    FROM 
        TrackPoint 
    JOIN 
        transport_same_day 
    ON 
        TrackPoint.activity_id = transport_same_day.activity_id

),

distances_per_day AS (
    SELECT 
        SUM(SQRT(POW(A.lon-B.lon, 2)+POW(A.lat-B.lat, 2))*111139) as distance_in_meters, 
        A.user_id as user_id, 
        A.transportation_mode AS transportation_mode,
        DATE(A.date_time) AS date_date
    FROM joined A
    JOIN joined B ON (A.trackpoint_id = B.trackpoint_id -1)
    WHERE DATE(A.date_time) = DATE(B.date_time)
    GROUP BY date_date, user_id, transportation_mode

),

sumarized_by_day_tm AS(
SELECT 
    user_id, 
    SUM(distance_in_meters) AS total_daily_distance, 
    transportation_mode,
    date_date 
FROM distances_per_day
GROUP BY user_id, date_date, transportation_mode
)
SELECT A.user_id, A.transportation_mode, A.total_daily_distance, A.date_date
FROM (
    SELECT 
        MAX(total_daily_distance) as max_daily,
        transportation_mode 
    FROM 
        sumarized_by_day_tm 
    GROUP BY
        transportation_mode
        ) AS B
JOIN sumarized_by_day_tm AS A
    ON B.transportation_mode = A.transportation_mode
WHERE A.transportation_mode = B.transportation_mode AND A.total_daily_distance = B.max_daily
;

