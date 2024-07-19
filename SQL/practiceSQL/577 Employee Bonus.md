# 577. Employee Bonus

Tags: Easy
Date: June 25, 2024

```sql
SELECT e.name, b.bonus
FROM Employee e
    LEFT JOIN Bonus b
    ON e.empId = b.empId
WHERE b.bonus IS NULL or b.bonus < 1000;
```

- [x]  other solutions? same as mine
- is null도 별도의 조건으로 빼줘야 하는 점!