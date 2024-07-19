# 1729. Find Followers Count

Tags: Easy
Date: July 12, 2024

```sql
SELECT user_id, COUNT(DISTINCT follower_id) AS followers_count
FROM Followers
GROUP BY user_id;
```