# 1965. Employees With Missing Information

- 문제 이해
    
    name이나 salary 정보가 없는 모든 직원의 id를 오름차순으로 
    
- [x]  두 테이블에 있는 같은 이름의 칼럼을 어떻게 하나로 합치지 → 수직적 결합. UNION
- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    SELECT e.employee_id 
    FROM Employees e
    WHERE e.employee_id NOT IN (SELECT Salaries.employee_id FROM Salaries)
    UNION 
    SELECT s.employee_id 
    FROM Salaries s
    WHERE s.employee_id NOT IN (SELECT Employees.employee_id FROM Employees)
    ORDER BY 1 ASC
    ```