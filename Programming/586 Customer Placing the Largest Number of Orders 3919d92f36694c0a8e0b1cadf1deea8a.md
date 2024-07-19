# 586. Customer Placing the Largest Number of Orders

- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    SELECT o.customer_number
    FROM Orders AS o
    GROUP BY o.customer_number
    ORDER BY COUNT(*) DESC
    LIMIT 1 
    ```