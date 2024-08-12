# 175. Combine Two Tables

Tags: Easy

- 문제 이해
    - person table에 있는 모든 사람에 대해 이름, 성, state
        - 사람 id가 주소 테이블에 없으면 null
- AC 코드
    
    ```sql
    SELECT p.firstName, p.lastName, a.city, a.state
    FROM Person p
        LEFT JOIN Address a
        ON p.personId = a.personId;
    ```