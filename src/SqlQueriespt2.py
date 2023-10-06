from DbConnector import DbConnector
from pet_log import get_logger
import math
logger = get_logger('SQL PART2')
# Question 1: How many users, activities, and trackpoints are there in the dataset
count_users_query = "SELECT COUNT(*) FROM User"
count_activities_query = "SELECT COUNT(*) FROM Activity"
count_trackpoints_query = "SELECT COUNT(*) FROM TrackPoint"

# Question 2: Find the average, maximum, and minimum number of trackpoints per user
trackpoints_stats_query = """
SELECT
    AVG(trackpoint_count) AS average_trackpoints,
    MAX(trackpoint_count) AS maximum_trackpoints,
    MIN(trackpoint_count) AS minimum_trackpoints
FROM (
    SELECT
        a.user_id,
        COUNT(t.id) AS trackpoint_count
    FROM Activity a
    INNER JOIN TrackPoint t ON a.id = t.activity_id
    GROUP BY a.user_id
) subquery
"""

# Question 3: Find the top 15 users with the highest number of activities
top_users_activities_query = """
SELECT user_id, COUNT(*) AS activity_count
FROM Activity
GROUP BY user_id
ORDER BY activity_count DESC
LIMIT 15
"""

# Question 4: Find all users who have taken a bus
bus_users_query = "SELECT DISTINCT user_id FROM Activity WHERE transportation_mode='bus'"

# Question 5: List the top 10 users by their amount of different transportation modes
top_10_users_modes_query = """
SELECT user_id, COUNT(DISTINCT transportation_mode) AS mode_count
FROM Activity
GROUP BY user_id
ORDER BY mode_count DESC
LIMIT 10
"""

# Question 6: Find activities that are registered multiple times
duplicate_activities_query = """
SELECT activity_id
FROM Activity
GROUP BY activity_id
HAVING COUNT(activity_id) > 1
"""

# Question 7a: Find the number of users that have started an activity in one day and ended the activity the next day
users_start_end_next_day_query = """
SELECT user_id, MIN(start_date_time) AS start_time, MAX(end_date_time) AS end_time
FROM Activity
GROUP BY user_id
HAVING DATE(start_date_time) != DATE(end_date_time)
"""

# Question 7b: List the transportation mode, user id, and duration for these activities
# use the 'users_start_end_next_day_query' result to join with Activity and calculate duration

# Question 8: Find the number of users which have been close to each other in time and space
users_close_in_time_and_space_query = """
SELECT 
    user_id1,
    user_id2,
    T1.tr_activity_id AS activity_id1,
    T2.tr_activity_id AS activity_id2,
    T1.tr_date_time AS date_time1,
    T2.tr_date_time AS date_time2,
    T1.lat AS lat1,
    T1.lon AS lon1,
    T2.lat AS lat2,
    T2.lon AS lon2


WITH close_time (user_id1, user_id2, activity_id1, activity_id2) AS (
    SELECT DISTINCT A1.user_id AS user1, A2.user_id AS user2, A1.activity_id AS activity_id1, A2.activity_id AS activity_id2
    FROM Activity AS A1
    INNER JOIN Activity AS A2 ON A1.user_id <> A2.user_id
        AND (ABS(TIMESTAMPDIFF(SECOND, A1.start_date_time, A2.start_date_time)) <= 30
            OR ABS(TIMESTAMPDIFF(SECOND, A1.end_date_time, A2.end_date_time)) <= 30
            OR A1.start_date_time BETWEEN A2.start_date_time AND A2.end_date_time
            OR A1.end_date_time BETWEEN A2.start_date_time AND A2.end_date_time)
        AND A1.user_id < A2.user_id
        AND A1.user_id < 050
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
INTO OUTFILE '/var/lib/mysql-files/output.txt';
"""

# Question 9: Find the top 15 users who have gained the most altitude meters
top_15_users_altitude_gain_query = """
SELECT user_id, TrackPoint.activity_id AS activity_id, 
    (MAX(altitude) - MIN(altitude)) * 0.3048 AS altitude_gain
FROM TrackPoint
INNER JOIN Activity ON TrackPoint.activity_id = Activity.activity_id
WHERE altitude != -777
GROUP BY user_id, TrackPoint.activity_id
ORDER BY altitude_gain DESC
LIMIT 15;
"""

# 10. Find the users that have traveled the longest total distance in one day for each transportation mode.
query_10 = """
SELECT user_id, transportation_mode, MAX(total_distance) AS max_distance
FROM (
    SELECT 
        user_id,
        transportation_mode,
        DATE(date_time) AS travel_date,
        SUM(distance) AS total_distance
    FROM TrackPoint
    INNER JOIN Activity ON TrackPoint.activity_id = Activity.activity_id
    GROUP BY user_id, transportation_mode, travel_date
) AS user_mode_distance
GROUP BY user_id, transportation_mode;
"""

# 11. Find all users who have invalid activities, and the number of invalid activities per user.
# An invalid activity is defined as an activity with consecutive trackpoints where the timestamps deviate with at least 5 minutes.
query_11 = """
SELECT user_id, COUNT(*) AS num_invalid_activities
FROM (
    SELECT 
        A.user_id,
        TP.date_time,
        LAG(TP.date_time) OVER (PARTITION BY A.user_id, A.activity_id ORDER BY TP.date_time) AS prev_timestamp
    FROM TrackPoint TP
    INNER JOIN Activity A ON TP.activity_id = A.activity_id
) AS timestamp_diff
WHERE TIMESTAMPDIFF(MINUTE, prev_timestamp, date_time) >= 5
GROUP BY user_id;
"""

# 12. Find all users who have registered transportation_mode and their most used transportation_mode.
# The answer should be on format (user_id, most_used_transportation_mode) sorted on user_id.
# Some users may have the same number of activities tagged with e.g. walk and car.
# In this case, it is up to you to decide which transportation mode to include in your answer (choose one).
# Do not count the rows where the mode is null.
query_12 = """
SELECT user_id, MAX(transportation_mode) AS most_used_transportation_mode
FROM Activity
WHERE transportation_mode IS NOT NULL
GROUP BY user_id;
"""


def query_to_db(db_connector: DbConnector, query = None):
    
    if query != None:
        try:
            #db_connector.cursor.execute(query)
            logger.debug(f"Executing: {query}")
            results=[]
            for result in db_connector.cursor.execute(query, multi=True):
                if result.with_rows:
                    results.append(result.fetchall())
                    print(result.fetchall())
                else:
                    print("Number of rows affected by statement '{}': {}".format(
                    result.statement, result.rowcount))
            return True, results
        except Exception as e:
            logger.error(f"Error executing query '{query}':\n {e}")
            return False, None
        
    logger.error("No query was passed.")
    return False, None

def calculate_lon_lat_distance(lon1, lon2, lat1, lat2):
    dist_x = abs(lon1-lon2)
    dist_y = abs(lat1-lat2)
    total = math.sqrt(dist_x**2 + dist_y**2)
    return total