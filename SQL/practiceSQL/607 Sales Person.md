# 607. Sales Person

Tags: Easy

- 문제 이해
    - red라는 이름의 회사와 관련된 주문을 하나도 하지 않은 판매원의 이름을 찾아라
- 해결 과정
    - Trial1
        - red라는 이름이 들어간 회사 id를 찾는다
        - Order에서 해당 주문건은 거른다
            
            <aside>
            ☝ 이렇게 하면 안된다. Pam이라는 직원이 red 회사에 주문했지만, 그건만 없어지고, Pam의 다른 회사 주문건은 그대로 남기 때문
            
            </aside>
            
        - 그룹바이해서 unique 회사원 id만 남긴다
        - 회사원 테이블이랑 조인해서 이름을 가져온다
    - Orders에서 red 구매 기록이 있는 판매원 아이디 리스트를 얻은 뒤
    - SalesPerson에서 left join 해서 필터링한다 → null이면 정답 레코드
- 헷갈렸던 점
    - left join도
        - LEFT JOIN된 테이블에서 여러 행이 일치할 경우, FROM 절의 행이 각각의 일치하는 행과 조합되어 여러 번 반복됩니다.
    - CTE는 하나의 테이블처럼 사용되지만, 이를 참조하려면 테이블 자체로 조인하거나 서브쿼리처럼 사용하는 방식이 필요합니다.
    - 특정 칼럼 값이 null인지 확인할 때는 등호를 쓰면 안되고, `IS NULL` 을 무조건 사용해야 한다
- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    WITH team_red AS
    (SELECT sales_id
    FROM Orders o
        INNER JOIN Company c
        ON o.com_id = c.com_id
    WHERE c.name = 'RED')
    
    SELECT name
    FROM SalesPerson s
        LEFT JOIN team_red r 
        ON s.sales_id = r.sales_id
    WHERE r.sales_id IS NULL;
    ```
    
- Editorial
    
    ```sql
    SELECT
        s.name
    FROM
        salesperson s
    WHERE
        s.sales_id NOT IN (SELECT
                o.sales_id
            FROM
                orders o
                    LEFT JOIN
                company c ON o.com_id = c.com_id
            WHERE
                c.name = 'RED')
    ;
    ```
    
    - CTE 안 쓰고 where 절에 서브 쿼리 박음
    - `NOT IN`을 사용