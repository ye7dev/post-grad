# 550. Game Play Analysis IV

Tags: Intermediate
Date: July 10, 2024

- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    WITH first_login AS
        (SELECT player_id, min(event_date) as first_date
        FROM Activity
        GROUP BY player_id)
    SELECT round(AVG(fr), 2) AS fraction
    FROM 
        (
        SELECT a.player_id, SUM(IF(DATEDIFF(a.event_date, first_date) = 1, 1, 0)) AS fr
        FROM Activity a
            INNER JOIN first_login
            ON a.player_id = first_login.player_id
        GROUP BY a.player_id) AS derived; 
    ```
    
    - 이 코드 짜면서 복습한 점
        - CTE 다음에 본 쿼리 짤 때는 comma 절대 안 붙인다
        - CASE WHEN THEN ELSE 보다 IF가 깔끔하긴 하다
        - Derived table (FROM 뒤의 서브 쿼리에서 나온 테이블)에는 alias를 꼭 넣어줘야 한다
- 생각 안나서 괴로웠던 점들
    - lag 함수 (문제에 적합하지는 않다)
        - 이건 바로 위의 행과의 비교하는 함수(물론 정렬한 뒤에)
        - [[**197. Rising Temperature**](https://leetcode.com/problems/rising-temperature/description/?envType=study-plan-v2&envId=top-sql-50)](197%20Rising%20Temperature%201352d8779c9c44438cb6ad16082abd46.md) 이 문제와 비슷함
            - `LAG(recordDate, 1) OVER (ORDER BY (recordDate))`
        - 정렬 기준 두 칼럼 줄 수 있음. 콤마로 연결
        - 그러나…
            
            ```sql
            WITH prev_date AS
                (SELECT player_id, event_date, LAG(event_date, 1) OVER (ORDER BY player_id, event_date) AS prev_date
                FROM Activity
                GROUP BY player_id)
            SELECT *
            FROM prev_date;
            ```
            
            - `group by player_id` 를 없애면 이렇게 나오는데, group by를 하면 event_date가 애초에 하나만 남게 되어서
                
                ![Untitled](550%20Game%20Play%20Analysis%20IV%209b60cd7f2a3447baad571d97357ac5a2/Untitled.png)
                
            - 이런 오답이 나온다. 왜냐면 group by를 select보다 먼저 하기 때문에!
                
                ![Untitled](550%20Game%20Play%20Analysis%20IV%209b60cd7f2a3447baad571d97357ac5a2/Untitled%201.png)
                
- Editorial
    - **Approach 1: Subqueries and multi-value use of the `IN` comparison operator**
        
        ```sql
        SELECT 
        ROUND(
        	# 분자: WHERE로 행 필터링 후 player_id 칼럼이 null이 아닌 행의 개수
        	COUNT(A1.player_id) 
        	/ 
        	# 분모: 전체 player_id 개수 세기 
        	SELECT COUNT(DISTNCT A3.player_id) FROM Activity A3), 
        	2) AS fraction
        FROM Activity A1 
        WHERE 
        			# multi-value comparison
        			(A1.player_id, DATE_SUB(A1.event_date, INTERVAL 1 DAY)) 
        			IN 
        			# id별 first login 날짜 구하기 
        			(SELECT A2.player_id, MIN(A2.event_Date)
        			FROM Activity A2
        			GROUP BY A2.player_id);
        ```
        
        - 서로 다른 테이블에서 count를 구한 다음 나눠줄 수 있음
        - FROM → WHERE → SELECT 이기 때문에 A1에는 WHERE 절 조건 만족하는 row만 남아 있게 됨
        - WHERE 절 조건: 여러 칼럼 값으로 구성된 tuple이 subquery로 구성된 결과에 있는지 IN으로 확인
            - `DATE_SUB(date, INTERVAL \value \unit)`
                - 주어진 날짜에서 지정한 간격을 빼는 데 사용
                - INTERVAL 시간 단위를 지정하는 키워드
                - ⭐️ date 다음에 콤마 반드시 필요하다!
    - **Approach 2: CTEs and `INNER JOIN`**
        - 선형적 접근 가능
            1. 각 player별 first login date를 구한다(unique player 명수도 같이 구해짐)
            2. 1.바로 다음 날에도 로그인한 player의 명수를 구한다 
            3. 2.를 1의 명수로 나눠서 구한 뒤 반올림한다 
        
        ```sql
        # 1.
        WITH first_login AS (
        	SELECT A.player_id, MIN(event_date) AS login_date
        	FROM Activity A 
        	GROUP BY A.player_id)
        
        # 두번째 CTE 정의에 콤마는 반드시 필요하지만 WITH는 필요 없다
        , second_login AS (
        	SELECT COUNT(A.player_id) AS num_logins
        	FROM first_login F 
        		INNER JOIN Activity A 
        		ON F.player_id = A.player_id 
        				AND F.login_date = DATE_SUB(A.event_date, INTERVAL 1 DAY)
        	)
        	
        # 메인 쿼리
        SELECT 
        	ROUND(
        		(SELECT S.num_logins FROM second_login S)
        		/ (SELECT count(F.player_id) FROM first_login F)
        		, 2) AS fraction;
        ```