# 1407. Top Travellers

- [x]  ORDER BY 기준 칼럼 두 개 이상 쓰는 법
- [x]  join 해서 Null 값 나온 경우 0으로 고치기
- [x]  동명이인의 경우 그룹바이 조건 두 개 넣어주기
- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    SELECT u.name, COALESCE(SUM(r.distance), 0) AS travelled_distance
    FROM Users AS u
    LEFT JOIN Rides AS r ON u.id = r.user_id
    GROUP BY u.id, u.name
    ORDER BY SUM(r.distance) DESC, u.name ASC ;
    
    ```