# 576. Out of Boundary Paths

Status: done, in progress
Theme: DP
Created time: February 26, 2024 6:05 PM
Last edited time: February 26, 2024 7:03 PM

- 과정
    - visited를 두어야 하나 말아야 하나?
        - visited 안 쓰면 무한재귀호출
        - 예제 보면 중복이 허용 되는 걸 알수 있다
    - start cell에서의 거리-이동 횟수-가 max_move 미만이면서
    - 값이 out of boundary인 방법의 횟수를 찾아야 함
- Trial
    - Top-bottom: 예제 1
        
        ```python
        class Solution:
            def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
                mod = 10 ** 9 + 7
                memo = {}
        
                def recur(r, c, num_move):
                    # check memo:
                    if (r, c) in memo:
                        return memo[(r, c)]
                    # check base case
                    if num_move > maxMove:
                        return 0 
                    if r < 0 or r >= m:
                        return 1
                    if c < 0 or c >= n:
                        return 1
                    # recurrence relation
                    directions =[(1, 0), (0, 1), (-1, 0), (0, -1)]
                    cnt = 0
                    for d in directions:
                        cnt = (cnt + recur(r+d[0], c+d[1], num_move+1)) % mod
                    memo[(r, c)] = cnt
                    return memo[(r, c)]
                
                return recur(startRow, startColumn, 0)
        ```
        
    - Top-bottom: state 변수 3개로 둠
- AC 코드
    - Top-down
        
        ```python
        class Solution:
            def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
                mod = 10 ** 9 + 7
                memo = {}
        
                def recur(r, c, num_move):
                    # check memo:
                    state = (r, c, num_move)
                    if state in memo:
                        return memo[state]
                    # check base case 
                    if r < 0 or r >= m:
                        return 1
                    if c < 0 or c >= n:
                        return 1
                    if num_move == 0:
                        return 0
                    # recurrence relation
                    directions =[(1, 0), (0, 1), (-1, 0), (0, -1)]
                    cnt = 0
                    for d in directions:
                        cnt = (cnt + recur(r+d[0], c+d[1], num_move-1)) % mod
                    memo[state] = cnt
                    return memo[state]
                
                return recur(startRow, startColumn, maxMove)
        ```