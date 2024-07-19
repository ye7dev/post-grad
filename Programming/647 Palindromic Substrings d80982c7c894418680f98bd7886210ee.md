# 647.Palindromic Substrings

Status: done, in progress
Theme: DP
Created time: February 21, 2024 11:44 AM
Last edited time: February 22, 2024 6:02 PM

- 문제 이해
    - palindromic substring 개수를 구해라
    - 동일한 char도 자리가 다르면 별도의 substring으로 생각
        - 예) Input: s = "aaa"
            - Output: 6
            - Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".
- 과정
    - substring 길이랑 헷갈린다
- AC 코드
    - Bottom-up(🪇🐢)
        
        ```python
        class Solution:
            def countSubstrings(self, s: str) -> int:
                n = len(s)
                # dp[i][j]: # of p.s in string[i:j+1]
                # return: dp[0][n-1] -> string[0:n]
                dp = [[0] * n for _ in range(n)] 
        
                # base case: single char
                for i in range(n):
                    dp[i][i] = 1 
                total = n
        
                # recurrence relation
                for i in range(n-1, -1, -1): 
                    for j in range(i+1, n): # i=n-1 -> j=n -> skip for loop 
                        if s[i] == s[j]:
                            if j == i+1 or dp[i+1][j-1]:
                                dp[i][j] += 1
                        total += dp[i][j]
                
                return total
        ```