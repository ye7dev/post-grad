# 91. Decode Ways

Status: done, in progress
Theme: DP
Created time: November 21, 2023 10:47 PM
Last edited time: November 21, 2023 11:10 PM

🌸와우 처음으로 미디엄 한번에 풀었다

- 코드
    
    ```python
    class Solution:
        def numDecodings(self, s: str) -> int:
            dp = [0] * (len(s)+1)
            dp[0] = 1 
            if int(s[0]) != 0:
                dp[1] = 1
            for i in range(2, len(s)+1):
                if 10 <= int(s[i-2:i]) <= 26:
                    dp[i] += dp[i-2]
                if 1 <= int(s[i-1:i]) <= 9:
                    dp[i] += dp[i-1]
    
            return dp[-1]
    ```