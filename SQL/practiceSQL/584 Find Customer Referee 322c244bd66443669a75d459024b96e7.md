# 584. Find Customer Referee

Tags: Easy
Date: June 20, 2024

```sql
SELECT name
FROM Customer
WHERE referee_id != 2 or referee_id is null; 
```

- referee_id가 null 인 행도 포함했어야 하는 점