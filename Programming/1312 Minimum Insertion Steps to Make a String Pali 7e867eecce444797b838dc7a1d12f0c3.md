# 1312. Minimum Insertion Steps to Make a String Palindrome

Status: done, in progress
Theme: DP, Longest Common Subsequence
Created time: January 22, 2024 4:57 PM
Last edited time: January 22, 2024 5:17 PM

- Process
    - 왠지 input string과 그걸 뒤집은 것 사이의 LCS 길이를 구해서 지향점 길이에서 빼면 될 것 같은데
    - 지향점은 어떻게 구함? → 그치 지향점이 아니라 주어진 string 길이에서 빼면 될 듯
- AC 코드 🪇
    
    ```python
    class Solution:
        def minInsertions(self, s: str) -> int:
            reverse_s = s[::-1]
    
            def get_lcs(text1, text2):
                m, n = len(text1), len(text2)
                dp = [[0] * (n+1) for _ in range(m+1)]
    
                # base case - auto covered - text1[:0] vs. text2[:j]
                # iteration
                ## state dp[i][j]: text1[:i] vs. text2[:j]
                for i in range(m-1, -1, -1):
                    for j in range(n-1, -1, -1):
                        if text1[i] == text2[j]:
                            dp[i][j] = 1 + dp[i+1][j+1]
                        else:
                            dp[i][j] = max(dp[i+1][j], dp[i][j+1])
                
                return dp[0][0]
        
            len_lcs = get_lcs(s, reverse_s)
            return len(s) - len_lcs
    ```