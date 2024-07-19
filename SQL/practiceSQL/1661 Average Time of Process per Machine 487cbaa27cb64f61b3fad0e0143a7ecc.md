# 1661. Average Time of Process per Machine

Tags: Easy
Date: June 25, 2024

- 문제 이해
    - 기계마다 같은 수의 process 돌림
    - 각 기계 별로 하나의 process를 끝내는데 걸리는 시간의 평균을 구하라
        - 기계 하나에 대해 하나의 process를 끝내는데 걸리는 시간을 구할 수 있음
        - 다 더해서 process 개수로 나누면 됨
- AC 코드
    
    ```sql
    SELECT a1.machine_id, round(avg(a2.timestamp - a1.timestamp), 3) processing_time
    FROM Activity a1
        INNER JOIN Activity a2
        ON a1.machine_id = a2.machine_id and a1.process_id = a2.process_id
    WHERE a1.activity_type = 'start' and a2.activity_type = 'end'
    GROUP BY a1.machine_id;
    
    ```
    
- 모르겠는 점
    - [x]  group by 조건이 하나만 들어가야 답이 나오게 되는 메커니즘
        - group by 전까지 하면 (round, avg도 제외) 같은 기계에 대해 프로세스별 소요 시간이 나온다
            
            ![Untitled](1661%20Average%20Time%20of%20Process%20per%20Machine%20487cbaa27cb64f61b3fad0e0143a7ecc/Untitled.png)
            
        - 여기서 machine_id 기준으로 묶어서 평균 내면 하나의 기계 기준 (프로세스별 소요 시간 합) / (프로세스 개수)가 나와서 원하는 답이 나온다.
    - [x]  where 조건을 저렇게 줘도 되나?
    - [x]  where 조건이랑 join on 조건이랑 작동 메커니즘? 차이
        - chatGPT 설명
            - **ON 절에서 조인 조건으로 필터링:**
                - **조인 시점**: ON 절에서 조건을 사용하면 두 테이블을 조인하는 단계에서 조건을 적용합니다.
                - **동작 방식**: 데이터베이스는 먼저 두 테이블을 조인하면서 ON 절에 지정된 조건을 만족하는 행들만 선택합니다. 조인 조건이 충족되지 않는 행은 조인 결과에 포함되지 않습니다.
                - **효율성**: 이 방식은 조인을 수행할 때 이미 불필요한 행들을 제외하기 때문에, 전체적으로 처리해야 할 데이터 양이 줄어듭니다. 이는 특히 큰 테이블을 조인할 때 성능 향상에 도움이 됩니다.
            - **WHERE 절에서 필터링:**
                - **조인 후 시점**: WHERE 절에서 조건을 사용하면 모든 조인 결과에 대해 필터링을 적용합니다.
                - **동작 방식**: 데이터베이스는 두 테이블을 조인한 후, 조인 결과에서 WHERE 절에 지정된 조건을 만족하는 행들만 선택합니다. 조인 조건을 만족하지 않는 행도 일단 조인 결과에 포함된 후, WHERE 절에서 필터링됩니다.
                - **효율성**: 이 방식은 조인 후에 불필요한 행들을 제외하므로, 조인 결과가 큰 경우에는 성능이 떨어질 수 있습니다.
        - where 조건을 join 조건으로 보내도 정답은 나온다
            
            ```sql
            # Write your MySQL query statement below
            SELECT a1.machine_id, round(avg(a2.timestamp - a1.timestamp), 3) processing_time
            FROM Activity a1
                INNER JOIN Activity a2
                ON a1.machine_id = a2.machine_id and a1.process_id = a2.process_id and a1.activity_type = 'start' and a2.activity_type = 'end'
            GROUP BY a1.machine_id;
            ```
            
- 또 다른 솔루션 - CASE WHEN (훨씬 느리다)
    
    ```sql
    SELECT 
        machine_id,
        ROUND(SUM(CASE WHEN activity_type='start' THEN timestamp*-1 ELSE timestamp END)*1.0
        / (SELECT COUNT(DISTINCT process_id)),3) AS processing_time
    FROM 
        Activity
    GROUP BY machine_id
    ```
    
    - 테이블 조인은 없고, 문제 그대로 구해서 나누기
        - 분자
            - 결국 프로세스별 소요 시간의 합은 프로세스1 종료 - 프로세스1 시작 + 프로세스2 종료 - 프로세스2 시작 … 이렇게 번갈아가면서 +-로 더해진다
            - CASE WHEN 써서 번갈아 더하기 실행
                - CASE WHEN 복습
                    
                    ```sql
                    CASE
                        WHEN condition1 THEN result1
                        WHEN condition2 THEN result2
                        ...
                        ELSE resultN
                    END
                    ```
                    
                - start time은 음수 곱해져서 더해지고, 아닌 경우는 원래 값 그대로 들어간다