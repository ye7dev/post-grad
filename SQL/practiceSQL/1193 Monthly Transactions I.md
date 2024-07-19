# 1193. Monthly Transactions I

Tags: Intermediate
Date: June 28, 2024

- AC 코드
    
    ```sql
    SELECT DATE_FORMAT(trans_date, '%Y-%m') AS month, country, count(*) AS trans_count, SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count, SUM(amount) AS trans_total_amount, SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
    FROM Transactions 
    GROUP BY DATE_FORMAT(trans_date, '%Y-%m'), country;
    ```
    
- mySQL에는 yearmonth 함수는 없고 DATE_FORMAT만 있다.
    - 내가 헷갈렸던 건 yearweek 함수
- DATE_FORMAT 사용법
- GROUP BY에서도 연월로 묶으려면 저렇게 꼭 해야 하는가?
    - select에서 사용한 alias month를 그대로 쓸 수 있다는데 헷갈리니까 그냥 하자
- `SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END)` 잘 썼음
    - then 뒤에 칼럼 값을 쓸 수 있다는 사실을 배움
    - 조금 더 깔끔하게 쓰고 싶다면 `IF(state = 'approved', amount, 0)` 이런 식으로 쓸 수 있음
        - `IF(expression, true_value, false_value)`
        - CASE WHEN 보다 쬐끔 빠르다