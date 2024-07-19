# 1174. Immediate Food Delivery II

Tags: Intermediate
Date: June 28, 2024

- Trial
    
    ```sql
    SELECT customer_id, count(distinct customer_id) 
    FROM Delivery
    GROUP BY customer_id
    HAVING min(order_date) = min(customer_pref_delivery_date)
    ```
    
- 여기서 2까지는 구할 수 있는데 2/4를 어떻게 해야 할지?
- 🐢 Solution 1 (where 절에서 tuple filtering, select 절에서 avg)
    
    ```sql
    Select 
        round(avg(order_date = customer_pref_delivery_date)*100, 2) as immediate_percentage
    from Delivery
    where (customer_id, order_date) in (
      Select customer_id, min(order_date) 
      from Delivery
      group by customer_id
    );
    ```
    
    1. filtering이 서로 다른 위치와 차원에서 이루어져야 
        1. 날짜가 최소 날짜인가 → 모든 고객에 대해 다 구해야 → where 절에서 날짜만 필터링 적용 
        2. 최소 날짜가 선호 날짜와 같은가 → 아닌 고객이 있을 수도 있음 → SELECT 에서 조건으로 정수 결과가 나오게끔 
    2. 전체 count가 분모로 오는 경우는 avg 함수 사용이 가능한지 확인해본다 
        - 내 trial에서는 그룹화를 customer_id 하나 당 하기 때문에, 그 안에서 avg 구하는 건 의미가 없다
        - 그룹이 전체로 되어 있어야 - 포함 구문에 group by절이 없어야 - 전체 count가 avg의 분모로 들어간다
    3. subquery를 where에 넣는다 
        - customer_id 당 order_date 최소 값을 구하기 위해
    4. where 절에서 두 칼럼을 tuple로 묶어서 IN을 쓸 수 있다 
        - IN 연산자 뒤에는 특정 값의 목록이나 서브쿼리가 올 수 있다
        - IN 연산자 양쪽의 튜플은 동일한 크기여야
    
    +. having으로 그룹화 이후의 조건을 다루는 경우, 비교 대상(예를 들어 등호 기준으로 좌우에 오는 값들)도 aggregated 수치여야 한다. 
    
- ⚡️ Solution 2 (CTE 사용해서 최소 날짜 필터링, select 절에서 avg)
    
    ```sql
    WITH min_date 
        AS (SELECT customer_id as cid, min(order_date) as min_order_date, min(customer_pref_delivery_date) as pref_date
            FROM Delivery
            GROUP BY customer_id)
    SELECT round(avg(order_date = customer_pref_delivery_date) * 100, 2) AS immediate_percentage
    FROM Delivery
        INNER JOIN min_date md 
        ON customer_id = cid and order_date = min_order_date;
    ```