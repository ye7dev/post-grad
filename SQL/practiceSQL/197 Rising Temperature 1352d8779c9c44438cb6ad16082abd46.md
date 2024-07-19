# 197. Rising Temperature

Tags: Easy
Date: June 24, 2024

- Trial: 13/14
    
    ```sql
    SELECT w2.id
    FROM Weather w1 
        INNER JOIN Weather w2
        ON w1.recordDate+1 = w2.recordDate
    WHERE w1.temperature < w2.temperature;
    ```
    
- Solution1: join + datediff
    1. self join 해서 Cartesian product 만든다 
    2. datediff 함수 사용해서 연속한 날짜에 대해서만 pair를 남기도록 함 
        - join condition: `ON DATEDIFF(w1.recordDate, w2.recordDate) = 1`
    3. 두번째 날이 더 높은 날만 남긴다 
    
    ```sql
    SELECT w1.id
    FROM Weather w1 
        INNER JOIN Weather w2
        ON DATEDIFF(w1.recordDate, w2.recordDate) = 1
    WHERE w1.temperature > w2.temperature;
    ```
    
    - `datediff(enddate, startdate)` = difference
    - datediff에서 w1의 날짜가 enddate이므로 뒤쪽 날짜가 더 큰 쪽으로 필터링
    - 오답 체크
        - 왜 join 조건으로 ON w1.recordDate+1 = w2.recordDate는 안되는가?
            - MySQL은 DATE 형식의 필드에 수치 연산을 직접 지원하지 않음?
            - SELECT date('2024-06-24') + 1의 결과가 INT 타입인 이유는 MySQL에서 DATE 타입에 숫자를 더하면 내부적으로 DATE 타입이 INT 타입으로 변환되어 계산되기 때문입니다.
            - MySQL은 날짜를 기본적으로 YYYYMMDD 형식의 정수로 간주하여 더하기 연산을 수행합니다. 따라서 date('2024-06-24') + 1은 20240624 + 1로 간주되어 결과는 20240625가 되며, 이는 정수로 취급됩니다.
- Solution2: lag function
    - lag 함수 복습
        - `LAG (expression, offset, (default)) OVER ( [PARTITION BY partition_expression] ORDER BY sort_expression)`
            - 이렇게 단순하게 들어갈 수도 있음 
             `LAG(temperature, 1) OVER (ORDER BY recordDate)`
    - CTE 복습
        - 쿼리 내에서 공통적으로 사용할 수 있는 임시 테이블 형태의 표현식
            - 책에서 예시
                
                ```sql
                with actors_s as
                	(select actor_id, first_name, last_name
                    from actor
                    where last_name like 'S%')**, # 콤마 있음** 
                    
                  actors_s_pg as 
                	(select s.actor_id, s.first_name, s.last_name, f.film_id, f.title
                    from actors_s s 
                			inner join film_actor fa
                      on s.actor_id = fa.actor_id
                      inner join film f
                      on f.film_id = fa.film_id
                		where f.rating = 'PG')**, # 콤마 있음** 
                		
                ```
                
                - 여기서 콤마가 있는 건 CTE를 여러 개 만들어야 해서 그런 것
        - CTE와 메인 쿼리는 쉼표로 구분하지 않고 이어서 작성해야 함
    - AC 코드
        
        ```sql
        WITH previousData AS
            (
                SELECT id, recordDate, LAG(recordDate, 1) OVER (ORDER BY (recordDate)) AS prevDate,
                        temperature, LAG(temperature, 1) OVER (ORDER BY (recordDate)) AS prevTemp
                FROM Weather 
            )
            SELECT id
            FROM previousData
            WHERE prevTemp < temperature AND recordDate = DATE_ADD(prevDate, INTERVAL 1 DAY);
        ```
        
        - 조건만 DATEDIFF로 바꿔도 통과
            
            ```sql
            # Write your MySQL query statement below
            WITH previousData AS
                (
                    SELECT id, recordDate, LAG(recordDate, 1) OVER (ORDER BY (recordDate)) AS prevDate,
                            temperature, LAG(temperature, 1) OVER (ORDER BY (recordDate)) AS prevTemp
                    FROM Weather 
                )
                SELECT id
                FROM previousData
                WHERE prevTemp < temperature AND DATEDIFF(recordDate, prevDate) = 1;
            ```
            
        - 주의 할 점
            1. CTE와 메인 쿼리 사이에는 콤마가 없다 
            2. LAG 함수는 바보라서 현재 상태에서 몇 번째 떨어진 행을 가져올 것인지만 할 수 있다. 
                - 그래서 LAG 함수 전에 over 하위 절에서 날짜 기준으로 정렬을 해야 하는 것.
                - 온도도 아무 생각 없이 온도로 정렬하면 안된다! 날짜 기준으로 정렬해야 함 ⭐️
                - 추가 조건 `AND recordDate = DATE_ADD(prevDate, INTERVAL 1 DAY);` 이 필요한 것도 마찬가지 이유
                    - 행으로 하나만 떨어져 있어도, 날짜가 하루 차이난다는 보람이 없기 때문에
                    - 해당 조건을 다시 한번 더 확인해줘야 한다.
            3. `DATE_ADD(기준 날짜, 간격)` 함수
                - DATEDIFF와 다르게 underbar가 있다
                - 특정 날짜에 지정한 간격을 추가한 결과를 반환