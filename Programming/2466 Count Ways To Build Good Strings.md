# 2466. Count Ways To Build Good Strings

Status: done, in progress
Theme: DP
Created time: November 21, 2023 3:51 PM
Last edited time: November 21, 2023 10:44 PM

한번 update 할 때 변화되는 모양새가 두 개로 분기됨

- 과정
    
    90%는 맞았는데 initialization이 틀렸다 아쉽
    
    ```python
    class Solution:
        def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
            dp = [0] * (high+1)
            dp[zero] += 1
            dp[one] += 1 
            for i in range(high+1):
                if i-zero >= 0:
                    dp[i] += dp[i-zero]
                if i-one >= 0:
                    dp[i] += dp[i-one]
    
            if low == high:
                return dp[high] % (10^9+7)
            else:
                return (dp[low]+dp[high]) % (10^9+7)
    ```
    
- 코드
    
    ```python
    from collections import defaultdict
    class Solution:
        def countGoodStrings(self, low: int, high: int, zero: int, one: int) -> int:
            dp = [0] * (high+1)
            dp[0] = 1
            for i in range(1, high+1):
                if i-zero >= 0:
                    dp[i] += dp[i-zero]
                if i-one >= 0:
                    dp[i] += dp[i-one]
    
            if low == high:
                return dp[high] % (10**9+7)
            else:
                return (sum(dp[low:high+1])) % (10**9+7)
    ```