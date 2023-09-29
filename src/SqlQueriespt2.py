queries = [
    # Question 1: Count users, activities, and trackpoints
    "SELECT COUNT(*) FROM users",
    "SELECT COUNT(*) FROM activities",
    "SELECT COUNT(*) FROM trackpoints",

    # Question 2: Average, maximum, and minimum trackpoints per user
    "SELECT AVG(trackpoint_count), MAX(trackpoint_count), MIN(trackpoint_count) FROM (SELECT user_id, COUNT(*) AS trackpoint_count FROM trackpoints GROUP BY user_id) AS subquery",

    # Question 3: Top 15 users with the highest number of activities
    "SELECT user_id, COUNT(*) AS activity_count FROM activities GROUP BY user_id ORDER BY activity_count DESC LIMIT 15",

    # Question 4: Users who have taken a bus
    "SELECT DISTINCT user_id FROM activities WHERE transportation_mode='bus'",

    # Question 5: Top 10 users by the number of different transportation modes
    "SELECT user_id, COUNT(DISTINCT transportation_mode) AS mode_count FROM activities GROUP BY user_id ORDER BY mode_count DESC LIMIT 10",

    # Question 6: Activities that are registered multiple times
    "SELECT activity_id FROM activities GROUP BY activity_id HAVING COUNT(activity_id) > 1",

    # Question 7a: Users who started an activity one day and ended the next day
    "SELECT user_id, MIN(start_time) AS start_time, MAX(end_time) AS end_time FROM activities GROUP BY user_id HAVING DATE(start_time) != DATE(end_time)",

    # Question 7b: List transportation mode, user id, and duration for these activities (query based on results of Question 7a)

    # Question 8: Number of users close in time and space (define the query based on your data schema)

    # Question 9: Top 15 users who gained the most altitude meters
    "SELECT user_id, SUM(altitude_gain) AS total_altitude_gain FROM activities GROUP BY user_id ORDER BY total_altitude_gain DESC LIMIT 15"
]
