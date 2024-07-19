# 595. Big Countries

Tags: Easy
Date: June 20, 2024

```sql
SELECT name, population, area
FROM World
WHERE area >= 3000000 or population >= 25000000;
```