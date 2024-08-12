# 1607. Sellers With No Sales

Tags: Easy

- 문제 이해
    - 2020년에 아무것도 못 판매한 상인의 이름 을 오름차순으로
- 문제 접근
    - 2020년 주문건만 where로 거른다
    - seller table이랑 결합해서 이름으로 그룹바이 한 다음에 sum 때린다
    - 0인 행만 남긴다
- 질문
    - Customer 테이블은 왜 있는거지?
- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    WITH 2020_orders AS
        (SELECT *
        FROM Orders
        WHERE year(sale_date) = 2020)
    
    SELECT s.seller_name 
    FROM Seller s
        LEFT JOIN 2020_orders o
        ON s.seller_id = o.seller_id
    GROUP BY s.seller_id
    HAVING count(order_id) = 0
    ORDER BY s.seller_name;
    ```
    
    - 간단하게 이 조건 사용해도 됨 
    `WHERE o.seller_id IS NULL`