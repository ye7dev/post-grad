# 64. Minimum Path Sum

Status: done
Theme: DP
Created time: November 12, 2023 7:09 PM
Last edited time: November 12, 2023 7:22 PM

- base case 때문에 헷갈림
    - first row, first column 이더라도 [0][0] 아니고는 누적으로 값을 가져야 함
        - dp[i-1][0] + grid[i][0] 이런 식으로
- 코드
    
    ```python
    class Solution:
        def minPathSum(self, grid: List[List[int]]) -> int:
            m, n = len(grid), len(grid[0])
            dp = [[0]*n for _ in range(m)]
            dp[0][0] = grid[0][0]
            for i in range(1, m):
                dp[i][0] = dp[i-1][0] + grid[i][0]
            for j in range(1, n):
                dp[0][j] = dp[0][j-1] + grid[0][j]
            
            for i in range(1, m):
                for j in range(1, n):
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
        
            return dp[-1][-1]
    ```