# 1070. Product Sales Analysis III

Tags: Intermediate
Date: July 12, 2024

```sql
# Write your MySQL query statement below
WITH first_year AS 
    (SELECT product_id, MIN(year) AS min_year
    FROM Sales
    GROUP BY product_id)

SELECT p.product_id, first_year.min_year AS first_year, s.quantity, s.price
FROM Product p
    INNER JOIN first_year 
    ON p.product_id = first_year.product_id
    INNER JOIN Sales s
    ON p.product_id = s.product_id AND first_year.min_year = s.year;
```