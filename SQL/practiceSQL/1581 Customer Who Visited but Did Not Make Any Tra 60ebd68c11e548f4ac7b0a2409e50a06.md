# 1581. Customer Who Visited but Did Not Make Any Transactions

Tags: Easy
Date: June 24, 2024

- AC 코드
    
    ```sql
    SELECT v.customer_id as customer_id, count(*) as count_no_trans
    FROM Visits v 
        WHERE NOT EXISTS (SELECT 1 
                        FROM Transactions t 
                        WHERE v.visit_id = t.visit_id)  
    GROUP BY v.customer_id;
    ```
    
- 또 다른 솔루션들
    - left join 한 뒤, left가 null인 값만 가져온다
        - not exists 쓰는 게 더 빠르긴 함
        
        ```sql
        SELECT v.customer_id as customer_id, count(*) as count_no_trans
        FROM Visits v 
            LEFT JOIN Transactions t 
            ON v.visit_id = t.visit_id 
        WHERE t.transaction_id IS NULL
        GROUP BY v.customer_id;
        ```
        
        - left join이기 때문에 transaction에서 칼럼을 붙여온 Visits 테이블에 Null 값이 발생할 것
        - null이 발생할 수 있는 칼럼은 transaction_id
        - group by 빼먹으면 전체 count가 되어서 답이 틀리게 되니 주의
    - exists 안 하고 그냥 valid visit_id 리스트를 다 들고 와서, 거기 없는 행의 customer_id만 return
        
        ```sql
        # Write your MySQL query statement below
        SELECT v.customer_id as customer_id, count(*) as count_no_trans
        FROM Visits v 
        WHERE v.visit_id not in (SELECT visit_id FROM Transactions)
        GROUP BY v.customer_id
        ```