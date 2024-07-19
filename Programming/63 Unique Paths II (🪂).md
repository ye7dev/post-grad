# 63. Unique Paths II (🪂)

Status: done, in progress
Theme: DP
Created time: January 12, 2024 5:06 PM
Last edited time: January 12, 2024 5:16 PM

- AC 코드
    - base case 주의
        - 장애물이 없을 때만 1이고, 장애물이 있으면 0임. 그리고 어디로든 갈 수 없으니까 그대로 return 0 때려 버려야 함
    
    ```python
    class Solution:
        def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
            m, n = len(obstacleGrid), len(obstacleGrid[0])
            # edge case
            if obstacleGrid[0][0] == 1:
                return 0
            # array
            dp = [[0] * n for _ in range(m)]
            
            # base case
            dp[0][0] = 1
    
            # recurrence relation
            for i in range(m):
                for j in range(n):
                    if i == 0 and j == 0:
                        continue
                    if obstacleGrid[i][j] == 1:
                        continue
                    if i == 0:
                        dp[i][j] = dp[i][j-1]
                    elif j == 0:
                        dp[i][j] = dp[i-1][j]
                    else:
                        dp[i][j] = dp[i][j-1] + dp[i-1][j]
    
            return dp[-1][-1]
    ```