# 1112. Highest Grade For Each Student

Tags: Medium

- 문제 이해
    - 각 학생별로 가장 높은 성적을 거둔 과목과 점수를 구하라
        - 동점일 때는 과목 id가 작은 것으로
    - 최종 결과 정렬은 학생 id 기준으로
- AC 코드
    
    ```sql
    SELECT student_id, course_id, grade
    FROM (
        SELECT *, RANK() OVER (PARTITION BY student_id ORDER BY grade DESC, course_id ASC) AS score_rank
        FROM Enrollments) AS derived
    WHERE score_rank = 1; 
    ```
    
    - 헷갈렸던 점
        - ORDER BY 에서 기준이 여러 개인 경우
            - 두 칼럼은 콤마로 연결
            - 오름차순 내림차순이 다른 경우 각각 써준다. 특히 ASC도
        - rank over 뒤에서 PARTITION BY가 ORDER BY 보다 앞에 온다