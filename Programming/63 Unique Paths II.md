# 63. Unique Paths II

Status: done
Theme: DP
Created time: November 12, 2023 10:50 PM
Last edited time: November 12, 2023 10:52 PM

- 코드
    
    ```python
    class Solution:
        def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
            if obstacleGrid[0][0] == 1: return 0 
            m, n = len(obstacleGrid), len(obstacleGrid[0])
            dp = [[0]*n for _ in range(m)]
            dp[0][0] = 1
    
            for i in range(1, m):
                if dp[i-1][0] != 0 and obstacleGrid[i][0] != 1:
                    dp[i][0] = 1
            for j in range(1, n):
                if dp[0][j-1] != 0 and obstacleGrid[0][j] != 1:
                    dp[0][j] = 1
    
            for i in range(1, m):
                for j in range(1, n):
                    if obstacleGrid[i][j] != 1:
                            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
            return dp[-1][-1]
    ```
    
- base case dp[0][0] 설정 주의