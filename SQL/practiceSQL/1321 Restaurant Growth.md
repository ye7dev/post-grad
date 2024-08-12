# 1321. Restaurant Growth

Tags: Review

- 문제 이해
    - 매일 최소 한 명의 손님있음
    - 현재 날짜에 6일을 더한 7일 짜리 window 안에서 손님이 얼마나 지불하는지 moving average를 구해라
        - 소수 둘째 자리까지 반올림
    - 방문 날짜 기준으로 오름 차순
- window 함수 복습
    - 윈도우 함수 OVER (order by col partition by col) AS  …
    - [예제](https://www.notion.so/16-dd200389011e4e70a9f62b9cc40e318a?pvs=21)
        - 3주치 롤링 평균 계산
            1. group by로 aggregation 먼저 
                - 같은 주끼리 amount 더한다 sum(amount)
            2. select 넘어 와서 윈도우 설정 
                1. 기준 칼럼으로 정렬 
                2. 정렬된 상태에서 윈도우 크기 설정 
                    - 현재 row 기준 하나 앞, 하나 뒤 총 3개를 기준으로 잡음
                3. 설정된 윈도우 안에서 window function 수행
                    - 연달아 있는 3개 행의 avg(주별 합계 금액)
- 결론 - 함수2(함수1(col)) OVER … 이런 상황이면
    - 괄호는 안쪽에서부터 풀어나간다
    - group by는 select에 선행한다
    - 함수1이 aggregation - collapsing function
    - OVER 뒤의 구문 처리
        1. partition 현재 상태에서 파티션 분할
        2. 하나의 파티션 내에서 주어진 기준 칼럼에 따라 정렬 
        3. 하나의 파티션 내에서 (있다면) 윈도우 프레임 설정 
        4. 윈도우 프레임에서 윈도우 함수(함수2) 실행 
- Trial
    
    ```sql
    # Write your MySQL query statement below
    SELECT *
    FROM (
        SELECT visited_on, 
        sum(sum(amount)) OVER (ORDER BY visited_on ROWS BETWEEN CURRENT ROW AND 6 FOLLOWING) AS amount, 
        round(avg(sum(amount)) OVER (ORDER BY visited_on ROWS BETWEEN CURRENT ROW AND 6 FOLLOWING), 2) AS average_amount
        FROM Customer
        GROUP BY visited_on
        ORDER BY visited_on) AS derived
    WHERE DATE_SUB(visited_on, INTERVAL 6 DAY) >= (SELECT min(visited_on) FROM Customer);
    ```
    
    - 날짜는 맞는데 이러면 날짜 앞이 아니라 뒤의 날짜를 가지고 수치를 구하게 됨
    - 근데 ROWS BETWEEN에서 PRECEDING을 쓰면 범위에 null 있다고 에러남
- solution
    
    ```sql
    # Write your MySQL query statement below
    SELECT *
    FROM (
        SELECT visited_on, 
        sum(sum(amount)) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount, 
        round(avg(sum(amount)) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS average_amount
        FROM Customer
        GROUP BY visited_on
        ORDER BY visited_on) AS derived
    WHERE DATE_SUB(visited_on, INTERVAL 6 DAY) >= (SELECT min(visited_on) FROM Customer);
    ```
    
    - ROWS BETWEEN 사용이 미숙해서 그랬던 것
    - 논리적으로 preceding 날짜는 current 보다 앞이니까 코드 쓸 때도 앞에 써줘야 한다