# 931. Minimum Falling Path Sum(🪂)

Status: done, in progress
Theme: DP
Created time: January 12, 2024 8:16 PM
Last edited time: January 12, 2024 8:31 PM

- AC 코드(🪇, ⚡️)
    
    ```python
    class Solution:
        def minFallingPathSum(self, matrix: List[List[int]]) -> int:
            m, n = len(matrix), len(matrix[0])
            # array
            dp = [[0] * n for _ in range(m)]
            # base case
            for j in range(n):
                dp[0][j] = matrix[0][j]
            # recurrence relation
            for i in range(1, m):
                for j in range(n):
                    dp[i][j] = matrix[i][j]
                    add_min = dp[i-1][j]
                    if j-1 >= 0:
                        add_min = min(dp[i-1][j-1], add_min)
                    if j+1 < n:
                        add_min = min(dp[i-1][j+1], add_min)
                    dp[i][j] += add_min
            return min(dp[m-1])
    ```