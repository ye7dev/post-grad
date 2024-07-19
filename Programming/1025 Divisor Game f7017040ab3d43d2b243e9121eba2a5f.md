# 1025. Divisor Game

Status: done, in progress
Theme: DP
Created time: November 28, 2023 11:30 PM
Last edited time: November 29, 2023 12:45 AM

- 쿨다운 easy
- easy인데 생각보다 오래 걸림 [[**486. Predict the Winner**](https://leetcode.com/problems/predict-the-winner/description/)](486%20Predict%20the%20Winner%20c85e69d4dfad4741bb95f1dc6cfe4e6b.md) 랑 비슷한 방식으로 풀었다
- n=1이면 항상 진다는 게 base case
- 코드
    - DP, top-down 🪇
    
    ```python
    class Solution:
        def divisorGame(self, n: int) -> bool:
            memo = {}
            memo[1] = False
            def recur(num):
                if num in memo:
                    return memo[num]
                for i in range(1, num):
                    if num % i == 0 and not recur(num-i):
                        memo[num] = True 
                        return True 
                memo[num] = False
                return False
            return recur(n)
    ```
    
    - DP, bottom-up
        - top-down 에서처럼 들어오는 모든 n에 대해서 그보다 앞에 있는 숫자들과도 체크해야 함
    
    ```python
    class Solution:
        def divisorGame(self, n: int) -> bool:
            dp = [False] * (n+1)
            for i in range(2, n+1):
                for j in range(1, i):
                    if i % j == 0 and not dp[i-j]:
                        dp[i] = True 
            return dp[n]
    ```