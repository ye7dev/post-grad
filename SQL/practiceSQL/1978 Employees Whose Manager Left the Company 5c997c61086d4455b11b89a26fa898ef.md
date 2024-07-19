# 1978. Employees Whose Manager Left the Company

Tags: Easy
Date: July 16, 2024

```sql
SELECT employee_id
FROM Employees
WHERE manager_id NOT IN (SELECT employee_id FROM Employees) AND salary < 30000
ORDER BY employee_id;
```