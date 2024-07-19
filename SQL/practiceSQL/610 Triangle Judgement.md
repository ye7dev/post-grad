# 610. Triangle Judgement

Tags: Easy
Date: July 14, 2024

```sql
SELECT x, y, z, IF(x+y > z AND x+z>y AND y+z > x, 'Yes', 'No') As triangle
FROM Triangle;
```

- [x]  SELECT는 행마다 한 줄씩 실행되는 거 맞는지
    - 맞으면 x,y,z 칼럼 각각에서 값 가져오는 거니까 문제 없음
- 세 변이 삼각형 형성하는지 확인하려면 아래의 조건 만족해야 함 (chat gpt한테 물어봄)
    - 아무 두 변의 합이 무조건 남은 한 변의 길이보다 커야 한다