# 1164. Product Price at a Given Date

Tags: Intermediate
Date: July 15, 2024
review?: Yes

- Approach
    - 8/16 이후에 첫 변화 → default 값인 10.
    - 8/16 이전에 마지막 변화 → max(change_date)에서의 price
    - 8/16 이전에도 변화하고, 이후에도 변화 → ?
- Solution ⭐️
    - Sol1. `UNION All` 사용
        
        ```sql
        # 8/16 이후에 첫 변화 -> default 가격 10
        SELECT
          product_id, 10 AS price
        FROM
          Products
        GROUP BY
          product_id
        HAVING
          MIN(change_date) > '2019-08-16'
        
        # 위의 부분은 최소가 이미 8/16 이후기 때문에 8/16 이전 변화 기록은 없음 
        # 따라서 아랫 부분의 subquery where절 조건에 해당하는 행은 존재하지 않음
        # 따라서 위아래 중복되는 행은 없음. 성능 때문에 사용하는 것 뿐   
        UNION ALL
        
        # 8/16 이전의 변화 중에 가장 늦은 변화 당시의 가격
        SELECT
          product_id, new_price AS price
        FROM
          Products
        WHERE
        # multiple value check in subquery
          (product_id, change_date) IN 
          (SELECT product_id, MAX(change_date)
            FROM Products
            WHERE change_date <= '2019-08-16'
            GROUP BY product_id)
        ```
        
    - Sol2. `JOIN, LEFT JOIN, IFNULL` 사용
        
        ```sql
        SELECT
          UniqueProductId.product_id,
          IFNULL(LastChangedPrice.new_price, 10) AS price
        FROM
        	# unique product id 
          (
            SELECT DISTINCT
              product_id
            FROM
              Products
          ) AS UniqueProductIds
          # product id만 있는 왼쪽 테이블에 product_id 맞춰서 LastChangedPrice 테이블 LEFT JOIN 
          LEFT JOIN (
            SELECT
              Products.product_id,
              new_price
            FROM
              Products
              # derived table (LastChangedDate) join 
              JOIN (
        	      # 8/16 넘지 않으면서 가격 변경한 마지막 날짜 
                SELECT
                  product_id,
                  MAX(change_date) AS change_date
                FROM
                  Products
                WHERE
                  change_date <= "2019-08-16"
                GROUP BY
                  product_id
        	      ) AS LastChangedDate USING (product_id, change_date)
            GROUP BY # 중복 행 제거의 의미가 강한듯 
              product_id
              
          ) AS LastChangedPrice USING (product_id) 
        ```
        
        1. id 별로 8월 16일 넘지 않으면서 가격 변경한 마지막 날짜를 구해둔다 
            - subquery → derived table “LastChangedDate”
        2. 1과 Products 테이블을 INNER JOIN 한다 
            - USING (product_id, change_date)
                - 두 테이블에 모두 같은 이름의 열이 존재
            - 이 때 change_date는 사실 두 테이블에서 담고 있는 내용이 다르다
                - Products: 진짜 변경한 날짜
                - LastChangedDate: 16일 안 넘는 최신 변경 날짜
                - 두 칼럼의 값이 일치하는 행만 남음 (INNER JOIN이기 때문에)
            
            → product_id, 그 때 가격, 16일 안넘는 최신 변경 날짜 두 개의 칼럼만 존재 
            
        3. pid 기준으로 그룹화 
            - 아마도 중복 행 제거를 위해서…? 사실 왜 있는지 모르겠음
            - 여기까지 한 테이블을 LastChangedPridce라고 명명
        4. unique product id만 구해서 UniqueProductIds table 준비
        5. 3와 4를 product_id 행 기준으로 LEFT JOIN 한다 
            - 3에만 있는 product_id가 4에 없는 행에 대해서는 4의 칼럼들 값이 모두 NULL
        6. 왼쪽 테이블(UniqueProductIds)에서 product_id를 가져오고, 오른쪽 테이블의 new_price 칼럼 값이 null인 행에 대해서는 10을 넣어준다 
            - 오른쪽 테이블 new_price 칼럼 값이 0인 이유는 16일 안넘는 최신 변경 날짜가 없는 product_id이기 때문에
                - 최초 변경 날짜가 16일을 넘거나, 아님 초기 가격에서 변화가 아예 없는 경우
- IN 뒤에 올 수 있는 것들 - IN 앞에 여러 값이 묶인 튜플이 올 때
    - **값 목록**: IN (value1, value2, value3, ...)
    - **서브쿼리**: IN (SELECT column FROM table WHERE condition)
        - 서브쿼리의 결과의 각 행과 비교한다
    - **튜플 비교**: IN (SELECT column1, column2 FROM table WHERE condition)
- UNION ALL vs. UNION
    - **UNION ALL**: 중복을 포함하여 모든 행을 결합합니다.
    - **UNION**: 중복을 제거하고 고유한 행만 결합합니다.
    - 이 문제에서 왜 union all을 쓰느냐? 중복은 없지만 성능 때문에
        - We know there are no duplicated tuples when we union the two separated tables because we get one field using `GROUP BY` for each query.
        - Thus, it would be better to use `UNION ALL` instead of `UNION`for performance.
- IFNULL(expression, replacement)
    - expression 값이 null이면 replacement 값을 넣는다
- USING(col)
    - 두 테이블 간에 공통으로 존재하는 열을 기준으로 조인을 수행할 때 사용
    - ON이랑 비슷한데 두 테이블에서 열 이름이 같을 때
        - 열 이름 전후로 괄호 필수