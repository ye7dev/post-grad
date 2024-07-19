# 139. Word Break (🪂)

Status: done, in progress
Theme: DP
Created time: January 8, 2024 2:52 PM
Last edited time: January 8, 2024 4:55 PM

- 문제 이해
    - input: string s, wordDict
    - output: bool.
        - s가 wordDict에 있는 단어들로 쪼개질 수 있으면 True
    - 사전에 있는 단어는 몇 번이고 다시 쓰일 수 있음
- Trial
    - Top-down 예제 통과 + 37/46 TLE
        - avail option을 다 돌고 나서도 답을 못 얻으면, False가 해당 state에 대한 답이므로 이 또한 memoization을 꼭 해줘야 한다
        
        ```python
        class Solution:
            def wordBreak(self, s: str, wordDict: List[str]) -> bool:
                memo = {}
                # function
                def recur(i):
                    # base case
                    if i < 0:
                        return True 
                    # check memoization
                    if i in memo:
                        return memo[i]
                    # iteration of the recurrent relation 
                    for w in wordDict:
                        w_len = len(w)
                        # first condition
                        if s[i+1-w_len:i+1] == w:
                            if recur(i-w_len):
                                memo[i] = True
                                return memo[i]
                    # 요기서 memoization만 해도 통과
        						return False
        		
                return recur(len(s)-1)
        ```
        
- AC 코드
    - Bottom-up(⚡️)
        
        ```python
        class Solution:
            def wordBreak(self, s: str, wordDict: List[str]) -> bool:
                # array
                dp = [False] * len(s)
                
                # iteration
                for i in range(len(s)):
                    # iteration of the recurrence relation?
                    for w in wordDict:
                        w_len = len(w)
                        # i+1 - x = w_len -> x = i+1-w_len
                        # first condition
                        if s[i+1-w_len:i+1] != w:
                            continue
        								# second condition/ base case
                        if i-w_len == -1:
                            dp[i] = True 
        								# second condition/ recurrent relation
                        if i-w_len >=0 and not dp[i-w_len]:
                            continue 
                        dp[i] = True
        								break
                
                return dp[-1]
        ```
        
    - Top-down (⚡️)
        
        ```python
        class Solution:
            def wordBreak(self, s: str, wordDict: List[str]) -> bool:
                memo = {}
                # function
                def recur(i):
                    # base case
                    if i == -1:
                        return True 
                    # check memoization
                    if i in memo:
                        return memo[i]
                    # iteration of the recurrent relation 
                    for w in wordDict:
                        w_len = len(w)
                        # first condition
                        if s[i+1-w_len:i+1] == w:
                            # second condition
                            if i+1-w_len == 0: # no previous letter
                                memo[i] = True
                                return memo[i]
                            elif i+1-w_len > 0: # true for previous letter
                                if recur(i-w_len):
                                    memo[i]=True
                                    return memo[i]
                            # i+1-w_len < 0 -> continue
                    memo[i] = False
                    return False
        
                return recur(len(s)-1)
        ```