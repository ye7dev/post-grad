# 596. Classes More Than 5 Students

Tags: Easy
Date: July 12, 2024

```sql
SELECT class
FROM Courses
GROUP BY class
HAVING COUNT(student) >= 5;
```