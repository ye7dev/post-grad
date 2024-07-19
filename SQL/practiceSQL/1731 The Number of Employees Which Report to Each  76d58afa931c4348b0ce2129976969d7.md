# 1731. The Number of Employees Which Report to Each Employee

Tags: Easy
Date: July 13, 2024

```sql
SELECT e1.employee_id AS employee_id, e1.name, COUNT(e2.employee_id) AS reports_count, ROUND(AVG(e2.age)) AS average_age
FROM Employees e1
    INNER JOIN Employees e2
    ON e1.employee_id = e2.reports_to
GROUP BY e1.employee_id
ORDER BY e1.employee_id;
```

- 그룹으로 묶이는 대상은 e1.employee_id이고, 그 안에서 세야 할 것은 e2.employee_id임을 잘 구분했음!
- ROUND 함수에서 두번째 파라미터 안 주면 정수만 남음. 반올림