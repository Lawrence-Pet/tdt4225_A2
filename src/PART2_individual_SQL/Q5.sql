/*
# Question 5: List the top 10 users by their amount of different transportation modes
*/
SELECT user_id, COUNT(DISTINCT transportation_mode) AS mode_count
FROM Activity
GROUP BY user_id
ORDER BY mode_count DESC
LIMIT 10