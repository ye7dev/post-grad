# 120. Triangle

Status: done
Theme: DP
Created time: November 12, 2023 10:52 PM
Last edited time: November 13, 2023 11:02 AM

- dp table을 삼각형 크기랑 같게 만들어서 해결 → 근데 남의 풀이 보니까 dp table 따로 안 만들고 그냥 바로 삼각형에다가 덮어쓰기해서 triangle[0][0] 하는 방법도 있는 듯
- 코드
    
    ```python
    class Solution:
        def minimumTotal(self, triangle: List[List[int]]) -> int:
            n = len(triangle)
            dp = [[None] * i for i in range(1, n+1)]
            dp[-1] = triangle[-1]
            for r in range(n-2, -1, -1):
                for c in range(r+1): 
                    dp[r][c] = triangle[r][c] + min(dp[r+1][c], dp[r+1][c+1])
            return dp[0][0]
    ```