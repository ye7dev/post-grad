# 626. Exchange Seats

Tags: Intermediate
Date: July 16, 2024
review?: Yes

- Lag 함수 복습
    - 괄호 위치 주의
    - `LAG(col, interval) OVER (ORDER BY col2)`

```sql
WITH neighbors AS
    (SELECT id, student, lag(student, 1) OVER (ORDER BY id) AS prev,
            lead(student, 1) OVER (ORDER BY id) AS next
    FROM Seat)

SELECT id, IFNULL(IF(id % 2 = 0, prev, next), student) AS student
FROM neighbors
```

- [x]  solution 확인
- Solution
    
    ```sql
    SELECT
        (CASE
            WHEN MOD(id, 2) != 0 AND counts != id THEN id + 1
            WHEN MOD(id, 2) != 0 AND counts = id THEN id
            ELSE id - 1
        END) AS id,
        student
    FROM
        seat,
        (SELECT
            COUNT(*) AS counts
        FROM
            seat) AS seat_counts
    ORDER BY id ASC; 
    ```
    
    - CTE 없이 대신 derived table 추가로 FROM에서 불러옴
        - 전체 학생 수(좌석 수)를 알기 위해
        - `counts` 는 숫자 하나고, SELECT 문에 쓰였다.
            - 사실은 seat_counts.counts가 되는게 맞는데 그냥 생략하고 쓴듯
            - 왜냐면 seat table에는 counts라는 칼럼이 없으니까
    - prev, cur, next 다 확인하는 대신 조건으로 분기
        - id가 홀수고 마지막이 아닌 경우
            - 바로 아래 바꿀 대상이 있으므로 id+1
        - id가 홀수고 마지막인 경우
            - 그냥 그대로
        - id가 짝수인 경우
            - 문제에서 짝수는 마지막이더라도 swap이 되도록 함. 당연하지 바꿀 짝이 바로 위에 있는데
                - If the number of students is odd, the id of the last student is not swapped.
    - [x]  id가 바뀌는 건 알겠는데 student는 자동으로 바뀌나?
        - 마지막에 있는 ORDER BY id ASC를 하면서 바뀐다
            - 그 이름이 새롭게 있어야 할 자리 번호를 id에 부여한다 (id swap)
            - id 기준으로 정렬하면 student가 있어야 할 자리에 있게 된다
        - seat 테이블 약식 예제
            - 원래 테이블
                
                ![Untitled](626%20Exchange%20Seats%200b426d4bac4a47c1ba0acc03c3fd30f7/Untitled.png)
                
            - order by 절 빼고 실행하면
                
                ![Untitled](626%20Exchange%20Seats%200b426d4bac4a47c1ba0acc03c3fd30f7/Untitled%201.png)
                
                - id만 바뀌어 있다
            - Order by 절 추가하면
                
                ![Untitled](626%20Exchange%20Seats%200b426d4bac4a47c1ba0acc03c3fd30f7/Untitled%202.png)
                
                - 이름도 같이 재정렬된다