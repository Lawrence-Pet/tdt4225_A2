/*
* Question 10: Find the users that have traveled the longest total distance in one day for each transportation mode.
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
        AND DATE(start_date_time) = DATE(end_date_time)
), 

joined AS (
    SELECT 
        lon, 
        lat,
        date_time, 
        transport_same_day.activity_id,
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
        A.activity_id as activity_id, 
        A.user_id as user_id, 
        A.transportation_mode AS transportation_mode,
        DATE(A.date_time) AS date_date
    FROM joined A
    JOIN joined B ON (A.trackpoint_id = B.trackpoint_id -1)
    GROUP BY DATE(date_time), activity_id
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
select user_id, transportation_mode, total_daily_distance, date_date
from sumarized_by_day_tm
where (total_daily_distance, transportation_mode) in(SELECT MAX(total_daily_distance),transportation_mode 
                                                        from sumarized_by_day_tm 
                                                         group by transportation_mode)
;

