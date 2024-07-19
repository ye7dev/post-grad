# 931. Minimum Falling Path Sum

Status: done
Theme: DP
Created time: November 13, 2023 11:02 AM
Last edited time: November 13, 2023 11:14 AM

- [[**120. Triangle**](https://leetcode.com/problems/triangle/description/?envType=study-plan-v2&envId=dynamic-programming)](120%20Triangle%2057d5748273414694b351f63c5619c320.md) 과 거의 비슷. 맨 처음, 맨 마지막 column만 주의하면 됐음
- 코드
    
    ```python
    class Solution:
        def minFallingPathSum(self, matrix: List[List[int]]) -> int:
            n = len(matrix)
            dp = [[0] * n for _ in range(n)]
    
            dp[0] = matrix[0]
    
            for i in range(1, n):
                for j in range(n):
                    if j == 0:
                        dp[i][j] = min(dp[i-1][j], dp[i-1][j+1]) + matrix[i][j]
                    elif j == n-1:
                        dp[i][j] = min(dp[i-1][j], dp[i-1][j-1]) + matrix[i][j]
                    else:
                        dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]) + matrix[i][j]
            return min(dp[-1])
    ```