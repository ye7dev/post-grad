# 1068. Product Sales Analysis I

Tags: Easy
Date: June 24, 2024

```sql
# Write your MySQL query statement below
SELECT p.product_name, s.year, s.price
FROM Sales s
    INNER JOIN Product p 
    ON s.product_id = p.product_id; 
```