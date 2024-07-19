# 1378. Replace Employee ID With The Unique Identifier

Tags: Easy
Date: June 21, 2024

```sql
SELECT e2.unique_id, e1.name
FROM Employees e1
    left join EmployeeUNI e2
    on e1.id = e2.id;
```

- left join, right join 방향 복습
    - left, right 키워드는 데이터에 null이 있을 수 있는 table을 서버에 알려주는 역할
    - 문제에서 If a user does not have a unique ID replace just show `null`. 라고 했기 때문에 left로 들어가야 맞음