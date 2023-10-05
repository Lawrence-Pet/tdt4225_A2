from DbConnector import DbConnector
from pet_log import get_logger
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


# Question 9: Find the top 15 users who have gained the most altitude meters
top_15_users_altitude_gain_query = """
SELECT user_id, SUM(altitude) AS total_altitude_gain
FROM TrackPoint
GROUP BY user_id
ORDER BY total_altitude_gain DESC
LIMIT 15
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