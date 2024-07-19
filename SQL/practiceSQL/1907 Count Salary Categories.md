# 1907. Count Salary Categories

Tags: Intermediate
Date: July 15, 2024

- CASE 절에서 WHEN 여러 개 나와도 콤마 필요 없다
- Solution
    - 각 Case 별로 세서 union 한다
    
    ```sql
    SELECT 
        'Low Salary' AS category,
        SUM(CASE WHEN income < 20000 THEN 1 ELSE 0 END) AS accounts_count
    FROM 
        Accounts
        
    UNION
    
    SELECT  
        'Average Salary' category,
        SUM(CASE WHEN income >= 20000 AND income <= 50000 THEN 1 ELSE 0 END) 
        AS accounts_count
    FROM 
        Accounts
    
    UNION
    
    SELECT 
        'High Salary' category,
        SUM(CASE WHEN income > 50000 THEN 1 ELSE 0 END) AS accounts_count
    FROM 
        Accounts
    ```
    
- Trial
    - CTE에 없는 카테고리를 넣어줄 방법이 없다
    
    ```sql
    # Write your MySQL query statement below
    WITH income_check AS 
        (SELECT account_id, 
                CASE WHEN income < 20000 THEN 'Low Salary'
                    WHEN income BETWEEN 20000 AND 50000 THEN 'Average Salary'
                    ELSE 'High Salary'
                    END
                AS 'category'
        FROM Accounts)
    
    SELECT category, count(account_id) AS accounts_count
    FROM income_check
    GROUP BY category
    ```