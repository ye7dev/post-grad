# 1398. Customers Who Bought Products A and B but Not C

Tags: Medium
review?: yes

- Trial
    
    ```sql
    SELECT c.customer_id, c.customer_name
    FROM (
        SELECT customer_id, GROUP_CONCAT(product_name) AS prods
        FROM Orders
        GROUP BY customer_id) AS derived
        INNER JOIN Customers c
        ON derived.customer_id = c.customer_id
    WHERE prods LIKE '%A%' AND prods LIKE '%B%' AND prods NOT LIKE '%C%';
    ```
    
    - A, B, C 존재 여부를 확인하는 더 효율적인 라인 필요
- Solution
    
    ```sql
    SELECT c.customer_id, customer_name
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    HAVING SUM(product_name='A') > 0
        AND SUM(product_name='B') > 0
        AND SUM(product_name='C') = 0
    ORDER BY c.customer_id;
    ```
    
    - customer_id로 묶어 놓고
        - - 개별 행이 그룹화 되긴 했으나 하나로 collapse된 상태는 아닌 가봄? -
        - 각 그룹 내에서 HAVING 뒤에 있는 조건 실행
        - 같은 id를 가진 행들 중에서 조건 만족하는 행수를 더했을 때 1 이상 나오는지, 아님 0인지 확인
    - 훨씬 빠르긴 하다