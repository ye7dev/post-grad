# 1633. Percentage of Users Attended a Contest

Tags: Easy
Date: June 27, 2024

- AC 코드
    
    ```sql
    SELECT r.contest_id, round(count(u.user_id)/ (SELECT count(*) FROM Users) * 100, 2) AS percentage
    FROM Register r
        LEFT JOIN Users u 
        ON r.user_id = u.user_id
    GROUP BY r.contest_id
    ORDER BY percentage desc, r.contest_id;
    ```
    

c.f. round 함수 밖에서 * 100을 해버리면 0.66 * 100 = 66 이런 식이라 소수점 이하 두 자리가 사라지게 된다. 따라서 round 함수가기 전에 100을 해서 66.66666… → 반올림해서 66.67로 해야 올바른 답이 나온다.