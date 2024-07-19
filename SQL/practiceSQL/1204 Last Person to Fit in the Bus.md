# 1204. Last Person to Fit in the Bus

Tags: Intermediate
Date: July 15, 2024

```sql
SELECT person_name
FROM (
    SELECT person_name, turn, IF(SUM(Weight) OVER (ORDER BY turn) > 1000, 'yes', 'no') AS over_limit
    FROM Queue) AS weight_check
WHERE over_limit = 'no'
ORDER BY turn DESC
LIMIT 1;
```

- ORDER BY 기준으로 삼으려는 칼럼이 테이블 안에 있어야 함
- `LIMIT`
    - 자체에는 reverse 기능이 없지만, ORDER BY 에서 DESC 하면 된다