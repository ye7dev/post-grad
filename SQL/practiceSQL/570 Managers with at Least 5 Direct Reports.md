# 570. Managers with at Least 5 Direct Reports

Tags: Easy
Date: June 26, 2024

```sql
SELECT e2.name
FROM Employee e1 
    INNER JOIN Employee e2
    ON e1.managerId = e2.id 
GROUP BY e2.Id
HAVING count(*) >= 5; 
```

- [x]  left join 하면 안되는 이유
    - LEFT JOIN을 사용하는 경우, 왼쪽 테이블의 조인 키 값이 NULL인 경우에도 결과에 포함
        - 하지만 오른쪽 테이블에서 해당하는 행을 찾을 수 없기 때문에 오른쪽 테이블의 모든 열 값은 NULL
    - john 은 상사가 없어서 상사 id가 null → e2에서 가져오는 모든 칼럼 값이 null
        - group by id로 하면 null 그룹이 생긴다
        - 상사가 없는 행이 5개 이상이면 having 조건 만족하므로 null이 name으로 등장 → 오답
- [x]  e1.name과 e2.name의 차이
    - 같은 이유로 e1.name에는 null이 있고, e2.name에는 null이 없다