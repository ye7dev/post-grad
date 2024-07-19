# 940. Distinct Subsequences II

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP
Created time: February 5, 2024 3:52 PM
Last edited time: February 5, 2024 5:34 PM

[[**1987. Number of Unique Good Subsequences**](https://leetcode.com/problems/number-of-unique-good-subsequences/description/)](1987%20Number%20of%20Unique%20Good%20Subsequences%204b64619c993a4a7bae70d8d21ed28df2.md) 연관 문제

- Progress
    - string s의 distinct non-empty subsequence 개수를 구하라
    - len(s) ≤ 2000
    - 이미 만들어진 단어 set이랑, 현재 index에서의 distinct subseq 개수랑 따로 자료 구조를 운용해야 맞는 거겠지?
    - last letter랑 같은 경우 다른 경우를 봐야 하나?
    - s = ‘aaa’에서 aa(0,1)이랑 aa(1,2)랑 같은 거라고 얘기하려면 단어 set을 어디 만들어 두나?
- Editorial
    - **Approach 1: Dynamic Programming**
        - Intuition
            - 먼저 empty까지 포함해서 가능한 모든 subsequence를 찾은 뒤 → 거기서 empty subsequence만 뺀다
            - a typical idea: dp[k]
                - s[0]부터 s[k] (k inclusive, s[0:k+1])까지의 substring을 고려할 때 distinct subseqs 개수를 tracking
                - 예) s = ‘abcx’
                    
                    → dp[k] = dp[k-1] * 2 
                    
                    - 기존 dp[k-1]개
                    - x는 앞의 어떤 문자랑도 겹치지 않으므로, dp[k-1]개 각각에 x를 뒤에 붙여서(char 등장 순서는 유지해야 하므로) 만들어진 string도 모두 unique
                    
                    ![Untitled](Untitled%2020.png)
                    
                - 예2) s = ‘abab’
                    - dp[0] = 2 → ("", "a")
                    - dp[1] = 4 → ("", "a") + (""+b, "a"+b)
                    - dp[2] = 7
                        
                        ("", "a", "b", "aa", "ab", "ba", "aba")
                        
                        - 여기도 사실은 dp[-1] = “”라고 치면 dp[1] * 2 - dp[-1] = 4 * 2 -1 = 7로 볼 수 있음
                    - dp[3] = 12
                        
                        ("", "a", "b", "aa", "ab", "ba", "bb", "aab", "aba", "abb", "bab", "abab")
                        
                    - dp[3]를 잘 뜯어보면
                        - dp[2]가 우선 그대로 들어 있고
                            - dp[2] = ("", "a", "b", "aa", "ab", "ba", "aba")
                        - second_part = ("b", "aa", "ab", "ba", "aba")에다가 각각 ‘b’를 붙인 구성이 추가되어 있다
                            - (bb, aab, abb, bab, abab)
                        - second part는 dp[2]에서 (””, “a”)를 제외한 것 - 왜냐면 여기다 ‘b’를 붙이면 (b, ab)가 되는데 얘네는 이미 second part에 존재하기 때문에 중복 count가 되기 때문에
                        - current letter b는 s[3]. 같은 letter가 가장 최근에 나온 자리는 s[1] = b
                            - dp[1]을 계산할 때 dp[0] = (””, “a”)에 이미 b가 하나씩 붙어서 나왔음
                            - dp[3]을 계산할 때 dp[0]에 s[3] = b를 붙인 결과는 dp[0]에 s[1] = b를 붙인 결과와 동일
                            - 따라서 중복된 이 부분은 빼줘야 한다
                        - 재귀식 정리하면 `dp[k] = dp[k-1] * 2 - dp[last[s[k]]`
                            - k = 3 → s[3] = b
                            - last[s[k]] = last[s[3]] = last[b] = 1
                            - dp[1] = 2
                            - dp[3] = dp[2] * 2 -2 = 14-2 = 12
                            
                        
                        ![Untitled](Untitled%2021.png)
                        
- AC 코드
    
    ```python
    class Solution:
        def distinctSubseqII(self, s: str) -> int:
            mod = 10 ** 9 + 7
            n = len(s)
            dp = [0] * (n + 1)
            dp[0] = 1  # Base case: dp[0] = ""
            last_seen = {chr(x): -1 for x in range(97, 123)}  # Initialize last seen for all lowercase letters
    
            for i in range(n):
                dp[i + 1] = (2 * dp[i]) % mod  # Apply modulo after doubling
                if last_seen[s[i]] != -1:  # If char is repeated
                    dp[i + 1] = (dp[i + 1] - dp[last_seen[s[i]]]) % mod  # Apply modulo after subtraction
                
                last_seen[s[i]] = i  # Update the last seen index for the current char
    
            # Adjust the final answer for the empty subsequence, then apply modulo to ensure it's positive
            return (dp[n] - 1 + mod) % mod
    ```
    
- Trial
    - Bottom-up
        
        ```python
        class Solution:
            def distinctSubseqII(self, s: str) -> int:
                mod = 10 ** 9 + 7
                n = len(s)
                dp = [0] * (n+1)
                # base case : dp[0] = ""
                dp[0] = 1
                # dp[i]: # of distinct subsequences considering s[:i]
                char_set = {chr(x):-1 for x in range(97, 123)}
                for i in range(1, n+1): # last letter from s[:i]: s[i-1]
                    if char_set[s[i-1]] < 0: # new letter
                        dp[i] = 2 * dp[i-1]
                        char_set[s[i-1]] = i-1
                    else:
                        dp[i] = 2 * dp[i-1] - dp[char_set[s[i-1]]-1]
                return dp[-1]-1
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def distinctSubseqII(self, s: str) -> int:
                mod = 10 ** 9 + 7
                n = len(s)
                dp = [0] * (n+1)
                # base case : dp[0] = ""
                dp[0] = 1
                # dp[i]: # of distinct subsequences considering s[:i]
                last_seen = {chr(x):-1 for x in range(97, 123)}
                for i in range(n):
                    dp[i+1] = 2 * dp[i]
                    if last_seen[s[i]] != -1: # repeated char 
                        dp[i+1] -= dp[last_seen[s[i]]]
                        
                    last_seen[s[i]] = i
                return dp[n]-1
        ```