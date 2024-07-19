# 62. Unique Paths

Status: done
Theme: DP
Created time: November 12, 2023 7:02 PM
Last edited time: November 12, 2023 7:08 PM

- 코드
    
    ```python
    class Solution:
        def uniquePaths(self, m: int, n: int) -> int:
            dp = [[0 for _ in range(n)] for _ in range(m)]
            dp[0][0] = 1
            for i in range(1, m):
                dp[i][0] = 1 
            for j in range(1, n):
                dp[0][j] = 1 
            
            for i in range(1, m):
                for j in range(1, n):
                    dp[i][j] = dp[i-1][j] + dp[i][j-1]
            
            return dp[-1][-1]
    ```