# 620. Not Boring Movies

Tags: Easy
Date: June 26, 2024

```sql
SELECT id, movie, description, rating
FROM Cinema
WHERE id % 2 = 1 and description != 'boring'
ORDER BY rating desc;
```