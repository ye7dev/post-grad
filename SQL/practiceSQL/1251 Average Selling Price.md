# 1251. Average Selling Price

Tags: Easy
Date: June 27, 2024

- 한 product_id에 대해 가격 정보가 여러 개인 경우
    
    ![Untitled](1251%20Average%20Selling%20Price%208b172544ffdc42499b199dbbbbaf98a5/Untitled.png)
    
    - LEFT JOIN 쓰면 범위에 안 맞는 행까지 matching 해서 준다
        
        ![Untitled](1251%20Average%20Selling%20Price%208b172544ffdc42499b199dbbbbaf98a5/Untitled%201.png)
        
    - INNER JOIN 해야 맞는 범위의 가격만 가져다준다
        
        ![Untitled](1251%20Average%20Selling%20Price%208b172544ffdc42499b199dbbbbaf98a5/Untitled%202.png)
        
        - 근데 이러면 구매 기록이 없는 product_id 3에 대한 행 정보가 없다
- AC 코드
    
    ```sql
    SELECT p.product_id, (CASE WHEN sum(u.units) IS NULL THEN 0 ELSE round(sum(p.price * u.units)/ sum(u.units), 2) END) AS average_price 
    FROM Prices p
        LEFT JOIN UnitsSold u
        ON u.purchase_date BETWEEN p.start_date AND p.end_date AND u.product_id = p.product_id 
    GROUP BY p.product_id;
    ```
    
    - range 안에 있는지 체크할 때는 `BETWEEN ~ AND ~`
    - prices에 모든 product_id가 있기 때문에 설사 구매 기록(table u)에 없더라도 모든 아이디를 기준으로 평균 가격이 나올 수 있도록 LEFT JOIN을 사용하고, 왼쪽 table을 Prices로 만든다
    - 구매 기록이 없는 상품의 경우 join된 u 테이블의 칼럼에서 units 값 ( 사실은 다른 칼럼 값도) None으로 나온다
        - 이 점을 이용해서 CASE WHEN으로 평균 가격이 0 나올 수 있도록 예외 처리
- 다른 solutions
    - CASE WHEN 대신 `IFNULL` 사용하면 수식 더 깔끔
        - IFNULL(null값을 확인할 조건(칼럼, 수식 등), null 값인 경우 주게 될 값)
        - 우리 문제에서는 두번째 인자가 0으로 들어감