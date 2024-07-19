# 1211. Queries Quality and Percentage

Tags: Easy
Date: June 28, 2024

- AC 코드
    
    ```sql
    SELECT query_name, round(avg(rating/position), 2) AS quality, 
            round((SUM(CASE WHEN rating < 3 THEN 1 ELSE 0 END)) / count(*) * 100 , 2) AS poor_query_percentage
    FROM Queries
    GROUP BY query_name
    HAVING query_name IS NOT NULL;
    ```
    
- group by 한 칼럼 값이 null인 경우를 걸러야 하는 경우 having을 꼭 쓴다!