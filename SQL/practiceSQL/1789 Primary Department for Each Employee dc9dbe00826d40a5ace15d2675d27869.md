# 1789. Primary Department for Each Employee

Tags: Easy
Date: July 14, 2024

```sql
# Write your MySQL query statement below
WITH only_dep AS
    (SELECT employee_id
    FROM Employee
    GROUP BY employee_id
    HAVING COUNT(department_id) = 1)

SELECT e1.employee_id, e1.department_id
FROM Employee e1
    LEFT JOIN only_dep
    ON e1.employee_id = only_dep.employee_id
WHERE primary_flag = 'Y' OR only_dep.employee_id IS NOT NULL;
```

- [x]  solution 체크
- Sol1. union 사용
    
    ```sql
    -- Retrieving employees with primary_flag set to 'Y'
    SELECT 
      employee_id, 
      department_id 
    FROM 
      Employee 
    WHERE 
      primary_flag = 'Y' 
      
    UNION 
    
    -- Retrieving employees that appear exactly once in the Employee table
    SELECT 
      employee_id, 
      department_id 
    FROM 
      Employee 
    GROUP BY 
      employee_id 
    HAVING 
      COUNT(employee_id) = 1;
    ```
    
- Sol2. subquery & window 함수 사용
    - derived table: EmployeeParition
        - window 함수 사용
    
    ```sql
    SELECT 
      employee_id, 
      department_id 
    FROM 
      (
        SELECT 
          *, 
          # 각 eid가 table에서 몇 번씩 나타나는지 
          COUNT(employee_id) OVER(PARTITION BY employee_id) AS EmployeeCount
        FROM 
          Employee
      ) EmployeePartition 
    WHERE 
      EmployeeCount = 1 # eid가 table에서 한번만 나타남 = 소속된 부서가 하나라는 뜻
      OR primary_flag = 'Y';
    ```
    
- window 함수 복습
    - 데이터의 특정 범위 내에서 계산을 수행.
    - OVER() 절을 사용하여 윈도우를 정의
        - PARTITION BY와 ORDER BY를 포함
            - group by vs. partition by
                - GROUP BY는 데이터를 그룹화하여 각 그룹의 집계 결과만 반환
                - PARTITION BY는 윈도우 함수와 함께 사용되어 데이터를 논리적으로 분할하고, 원본 데이터의 모든 행을 유지한 채로 각 행에 대해 계산된 값을 추가