# 256. Paint House

Status: done, in progress
Theme: DP
Created time: January 14, 2024 11:15 AM
Last edited time: January 14, 2024 11:27 AM

- Process
    - greedy…?
    - 3일 때 1, 2 2일 때 1, 3, 1일 때 2, 3을 얻는 방법은? → 그냥 조건문 씀
- AC 코드 (🪇⚡️)
    
    ```python
    class Solution:
        def minCost(self, costs: List[List[int]]) -> int:
            n = len(costs)
            # state: dp[i][c] - min cum painting cost until coloring ith house with color c 
            
            # array
            dp = costs.copy()
    
            # base case: first house cost is same as costs
            ## automatically covered
            for i in range(1, n):
                for c in range(3):
                    if c == 0:
                        dp[i][c] += min(dp[i-1][c+1], dp[i-1][c+2])
                    elif c == 1:
                        dp[i][c] += min(dp[i-1][c-1], dp[i-1][c+1])
                    else:
                        dp[i][c] += min(dp[i-1][c-2], dp[i-1][c-1])
            return min(dp[-1])
    ```