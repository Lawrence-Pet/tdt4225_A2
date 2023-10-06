/*
*## Question 6: Find activities that are registered multiple times
*/
SELECT activity_id
FROM Activity
GROUP BY activity_id
HAVING COUNT(activity_id) > 1

