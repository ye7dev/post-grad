# 2356. Number of Unique Subjects Taught by Each Teacher

Tags: Easy
Date: July 11, 2024

```sql
SELECT teacher_id, count(distinct subject_id) AS cnt
FROM Teacher
GROUP BY teacher_id;
```

- distinct는 칼럼 이름 앞에 쓴다!