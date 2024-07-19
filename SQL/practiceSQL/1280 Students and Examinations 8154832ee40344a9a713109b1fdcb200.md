# 1280. Students and Examinations

Tags: Easy
Date: June 25, 2024

- Trial
    
    ```sql
    # Write your MySQL query statement below
    SELECT s.student_id, s.student_name, sub.subject_name, count(*) as attended_exams
    FROM Students s 
        INNER JOIN Examinations e
        ON s.student_id = e.student_id 
        INNER JOIN Subjects sub
        ON e.subject_name = sub.subject_name
    GROUP BY e.student_id, sub.subject_name;
    ```
    
- cross join 사용
    - join key 필요 없음
    - cartesian product → 모든 조합
- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    SELECT s.student_id, s.student_name, sub.subject_name, count(e.subject_name) attended_exams
    FROM Students s 
        CROSS JOIN Subjects sub
        LEFT JOIN Examinations e
        ON s.student_id = e.student_id and sub.subject_name = e.subject_name
    GROUP BY s.student_id, sub.subject_name
    ORDER BY s.student_id, sub.subject_name;
    ```
    
    1. cross join으로 학생 x 과목 모든 조합을 만들어둔다 
        - 원래 Students table에서 학생 한 명당 하나의 행이었는데
        - cartesian product 하면서 학생 한 명 당 과목 수 만큼의 행이 생기게 됨
    2. left join으로 examination에서의 칼럼을 데리고 온다 
        - why left join?
            - inner join 했을 때 전체 행수
                
                ![Untitled](1280%20Students%20and%20Examinations%208154832ee40344a9a713109b1fdcb200/Untitled.png)
                
            - left join 했을 때 전체 행수
                
                ![Untitled](1280%20Students%20and%20Examinations%208154832ee40344a9a713109b1fdcb200/Untitled%201.png)
                
        - [join 조건](1280%20Students%20and%20Examinations%208154832ee40344a9a713109b1fdcb200.md)  중 둘 중에 하나라도 만족하지 않으면, Examinations 테이블에서 가져오는 컬럼들은 모두 NULL이 됩니다.
            - 쿼리
                
                ```sql
                SELECT e.student_id, e.subject_name
                FROM Students s 
                    CROSS JOIN Subjects sub
                    LEFT JOIN Examinations e
                    ON s.student_id = e.student_id and sub.subject_name = e.subject_name
                ```
                
            - 결과
                
                ![Untitled](1280%20Students%20and%20Examinations%208154832ee40344a9a713109b1fdcb200/Untitled%202.png)
                
        - LEFT JOIN을 하면 해당 학생이 해당 과목 시험을 본 기록이 없다고 하더라도, 학생 id와 과목 이름에 시험 기록 관련 칼럼은 NULL로 되어 있는 행이 존재
        - INNER JOIN을 하면 시험 본 기록이 없는 학생-과목 조합 행은 아예 제외된다
    3. 모든 학생과 모든 과목 조합에 대해 시험 응시 횟수를 구해야 하기 때문에, e 테이블이 아닌 s와 sub 테이블의 칼럼을 기준으로 그룹화를 한다 
        - 만약 여기서 e.student_id나 e.subject_name을 기준으로 그룹화하는 경우, null값이 있는 행들이 하나로 묶이게 될 것
    4. count
        - **COUNT(*)**: 모든 행을 셉니다. NULL 값을 포함한 행도 계산합니다.
        - **COUNT(column_name)**: NULL이 아닌 값만 셉니다.
        - 여기서는 e table의 칼럼 값 중 null이 아닌 값만 세도록 했기 때문에, null이 있는 값은 0으로 나와서 원래 구하려던 값으로 나온다.