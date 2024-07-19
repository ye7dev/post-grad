# 180. Consecutive Numbers

Tags: Intermediate
Date: July 14, 2024

- lag 함수 복습
    - 파라미터로 음수가 들어갈 수는 없다
    - 괄호 주의
- 걸린 코너 케이스들
    - 3행 이상으로 연속되는 숫자의 경우 → `DISTINCT` 사용
    - 나란한 행에서도 id가 1차이 나지 않는 경우 → num 뿐만 아니라 id 차이도 체크

```sql
# Write your MySQL query statement below
WITH num_show AS
    (SELECT LAG(num, 1) OVER (ORDER BY id) AS prev, 
            num AS cur, 
            LEAD(num, 1) OVER (ORDER BY id) AS next,
            LAG(id, 1) OVER (ORDER BY id) AS id_prev, 
            id AS id_cur, 
            LEAD(id, 1) OVER (ORDER BY id) AS id_next     
    FROM Logs)

SELECT DISTINCT cur AS ConsecutiveNums
FROM num_show
WHERE prev = cur AND cur = next and id_prev + 1 = id_cur and id_cur + 1 = id_next;
```

- solution
    - `id is an autoincrement column.`
        - 정렬할 필요가 없다는 뜻
    - from에서 같은 table을 연속으로 3번 - alias - 다르게 해서 불러온다
        
        ```sql
        SELECT DISTINCT
            l1.Num AS ConsecutiveNums
        FROM
            Logs l1, # prev
            Logs l2, # cur
            Logs l3 # next 
        WHERE
        		# id 체크: prev = cur - 1 , cur = next - 1
            l1.Id = l2.Id - 1 AND l2.Id = l3.Id - 1
            # num 확인: prev = cur = next
            AND l1.Num = l2.Num AND l2.Num = l3.Num
        ;
        ```