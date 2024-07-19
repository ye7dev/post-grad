# 1934. Confirmation Rate

Tags: Easy
Date: June 26, 2024

```sql
SELECT s.user_id, round(SUM(CASE WHEN c.action='confirmed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS confirmation_rate
FROM Signups s  
    LEFT JOIN Confirmations c
    ON c.user_id = s.user_id
GROUP BY s.user_id;
```

- s.user_id로 해야 c에 없는 모든 id에 대해 다 구할 수 있다
    - left join을 쓴다는 건 left table의 모든 행에 대해 right table 칼럼의 정보를 가져온다는 거고, 설사 정보가 없으면 left table의 행에서 null을 감수하겠다는 것
    - 6의 경우 s.user_id에는 있지만, c.user_id에는 없기 때문에 group by, select를 백날 c.user_id로 해봤자 무쓸모
- 분자, 분모를 분리해서 구하면 6 같은 경우는 c에 없는 id도 s에는 있기 때문에 분모값이 최소 1이 나와서 분수를 구할 수 있음
    
    ![Untitled](1934%20Confirmation%20Rate%206b5ea44f5f5b4459b691ad99cd9eb7cd/Untitled.png)