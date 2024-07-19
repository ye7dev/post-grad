# 1141. User Activity for the Past 30 Days I

Tags: Easy
Date: July 11, 2024

- AC 코드
    
    ```sql
    SELECT activity_date AS day, COUNT(DISTINCT user_id) AS active_users
    FROM Activity 
    GROUP BY activity_date
    HAVING activity_date BETWEEN '2019-06-28' AND '2019-07-27';
    ```
    
    - group by에 날짜랑 user_id를 다 넣으면 index 칼럼이 두 개인 셈이라, aggregation을 더 어떻게 해야 하는지 안 보인다
        
        → 날짜만 넣어서 그룹으로 묶은 다음, unique user_id를 세는 게 맞다 
        
    - 날짜를 가지고 between을 쓸 때는 string 형식으로 주면 된다. 그리고 AND를 꼭 줘야 한다