# 1407. Top Travellers

Tags: Easy

- 문제 이해
    - 여행 거리를 내림차순으로
    - 두 명 이상이 같은 거리를 여행했으면 이름 오름차순으로
- 해결 과정
    - group by sum을 먼저 하고 join을 하려 했는데, 그럼 null이 있는 행이 나온다
    - `IFNULL(colname, 대체값)` 으로 해결
- AC 코드
    
    ```sql
    WITH sum_dist AS
        (SELECT user_id, sum(distance) AS dist
        FROM Rides
        GROUP BY user_id)
    
    SELECT u.name, IFNULL(s.dist, 0) AS travelled_distance
    FROM Users u
        LEFT JOIN sum_dist s
        ON u.id = s.user_id
    ORDER BY s.dist DESC, u.name ASC;
    ```
    
    - CTE 안 쓰고 그냥 IFNULL 안에 sum(distance) 바로 집어 넣고, GROUP BY 문을 main query에 추가해도 답 나옴