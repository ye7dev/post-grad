# 64. Minimum Path Sum(🪂)

Status: done, in progress
Theme: DP
Created time: January 12, 2024 5:17 PM
Last edited time: January 12, 2024 8:16 PM

- Process
    - greedy로 풀어도 되는 거 아닌가? 모르겠다 암튼 직전 칸과 이번 칸의 관계만 생각해서 풀어보자
- AC 코드 - bottom up (⚡️)
    
    ```python
    class Solution:
        def minPathSum(self, grid: List[List[int]]) -> int:
            m, n = len(grid), len(grid[0])
            '''
            # array
            dp = [[0] * n for _ in range(m)]
            # base case
            for i in range(m):
                dp[i][0] = grid[i][0]
            for j in range(n):
                dp[0][j] = grid[0][j]
            '''
            # recurrence relation
            for i in range(m):
                for j in range(n):
                    if i == 0 and j == 0:
                        continue
                    if i == 0:
                        grid[i][j] += grid[i][j-1]
                    elif j == 0:
                        grid[i][j] += grid[i-1][j]
                    else:
                        grid[i][j] += min(grid[i-1][j], grid[i][j-1])
            return grid[-1][-1]
    ```