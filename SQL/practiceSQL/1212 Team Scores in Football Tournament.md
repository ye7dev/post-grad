# 1212. Team Scores in Football Tournament

Tags: Medium

- 문제 이해
    - 팀별 점수 계산
        - 승: 3점, 무:1점, 패: 0점
    - 정렬
        - 점수 내림차순, 팀id 오름차순
- 해결 과정
    - 매치 당 host가 얻는 점수, guest가 얻는 점수 칼럼 생성
        - CTE로 설정해두고, host id랑 host score 칼럼만 들고 와서 합계
        - CTE 다시 불러와서 guest id랑 guest score 칼럼만 들고 와서 합계
    - 각 팀이 host 일 때 guest 일 때의 점수를 합쳐서 (union all) 팀별 점수 구함
    - 정렬 기준에 맞게 정렬
- AC 코드
    
    ```sql
    WITH scores AS (
    SELECT host_team, guest_team, 
        CASE WHEN host_goals > guest_goals THEN 3
            WHEN host_goals = guest_goals THEN 1
            WHEN host_goals < guest_goals THEN 0
            ELSE NULL
            END AS host_score, 
        CASE WHEN host_goals < guest_goals THEN 3
            WHEN host_goals = guest_goals THEN 1
            WHEN host_goals > guest_goals THEN 0
            ELSE NULL
            END AS guest_score
    FROM Matches)
    
    SELECT t.team_id, t.team_name, IFNULL(sum(derived.num_points), 0) AS num_points
    FROM Teams t
        LEFT JOIN 
        ((SELECT host_team AS team_id, sum(host_score) AS num_points
        FROM scores
        GROUP BY host_team)
        UNION ALL
        (SELECT guest_team AS team_id, sum(guest_score) AS num_points
        FROM scores
        GROUP BY guest_team)) AS derived
        ON t.team_id = derived.team_id
    GROUP BY t.team_id
    ORDER BY num_points DESC, t.team_id ASC;
    ```
    
- 헷갈렸던 부분
    - union all vs. union
        - 팀별 host일 때의 합산 점수 테이블과 guest일 때의 합산 점수 테이블을 합치는 상황이라 team_id랑 num_points가 모두 같은 상황이 상길 수 있음
        - 이 경우 union으로만 하면 점수 합계 시 오답
    - CASE WHEN THEN ELSE END 에서 ELSE 일 때 어떤 값 가져가야 하는지도 체크해야 함
- solution
    
    ```sql
    # Write your MySQL query statement below
    SELECT team_id,team_name,
    SUM(CASE WHEN team_id=host_team AND host_goals>guest_goals THEN 3
             WHEN team_id=guest_team AND guest_goals>host_goals THEN 3
             WHEN team_id=host_team AND host_goals=guest_goals THEN 1
             WHEN team_id=guest_team AND guest_goals=host_goals THEN 1 ELSE 0 END) as num_points
    FROM Teams
    LEFT JOIN Matches
    ON team_id=host_team OR team_id=guest_team
    GROUP BY team_id
    ORDER BY num_points DESC, team_id ASC;
    ```
    
    - CTE 안 만들고 바로 CASE 문에다가 그룹핑해서 SUM aggregation
    - 대신 team_id가 guest 일 때, host 일 때 두 경우모두 살펴봄
        - host team으로 이길 때
        - guest team으로 이길 때
        - host team으로 비길 때
        - guest team으로 비길 때
        - 지는 경우는 점수 추가 없으니까 조건문에 안들어감
    - team 정보에다가 Matches 정보 left join
        - team_id가 host이거나 guest이거나 둘 중에 하나만 만족해도 해당 행을 teams에 가져다가 붙이도록