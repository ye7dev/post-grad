# Sales Person

- [x]  foreign key
- 문제 이해
    - Orders table
        - com_id : foreign from Company table
        - sales_id: foreign from SalesPerson table
        - 둘 다 다른 테이블의 primary key임
    - Company
        - name column value ≠ RED
    - SalesPerson
        - name
- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    SELECT name
    FROM SalesPerson
    WHERE sales_id NOT IN (SELECT sales_id FROM Orders 
                        WHERE com_id = (SELECT com_id FROM Company
                                        WHERE name = 'RED'))
    ```