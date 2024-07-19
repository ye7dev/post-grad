# 2707. Extra Characters in a String

Status: done, in progress
Theme: DP
Created time: February 14, 2024 2:58 PM
Last edited time: February 14, 2024 3:36 PM

- 문제 이해
    
    input string s를 하나(통째로 다쓰거나) 이상의 substring으로 쪼개서(non-overlapping), 각 substring이 given dictionary에 모두 있도록 한다 
    
    근데 단어를 최대한 쪼개서도 남는 char이 몇몇 있을 건데 최소 숫자를 return 해라 - 없음 말구
    
- AC 코드
    - Bottom-up(🐢🪇)
        
        ```python
        class Solution:
            def minExtraChar(self, s: str, dictionary: List[str]) -> int:
                n = len(s)
                dp = [i for i in range(n+1)]
                # dp[i]: min extra char numbers left over considering breaking s[:i]
                # dp[0] : s[:0] = 0
                # dp[n] : s[:n] = n-1
                for i in range(1, n+1):
                    for j in range(i):
                        if s[j:i] in dictionary:
                            dp[i] = min(dp[i], dp[j])
                        else:
                            dp[i] = min(dp[i], dp[j] + i-j)
                        
                return dp[n]
        ```
        
    - Editorial Bottom-up
        
        ```python
        class Solution:
            def minExtraChar(self, s: str, dictionary: List[str]) -> int:
                n = len(s)
                dp = [0 for _ in range(n+1)]
                # dp[i]: min extra char numbers left over considering breaking s[i:]
                # dp[0] : s[0:]. ans
                # dp[n] : s[n:n]. base case. zero (empty string)
                for i in range(n-1, -1, -1):
                    dp[i] = 1 + dp[i+1]
                    for j in range(i, n):
                        if s[i:j+1] in dictionary:
                            dp[i] = min(dp[i], dp[j+1])
                        
                return dp[0]
        ```