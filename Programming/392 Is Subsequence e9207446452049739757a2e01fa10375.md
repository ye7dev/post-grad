# 392. Is Subsequence

Status: done, in progress
Theme: Two pointers
Created time: November 16, 2023 5:39 PM
Last edited time: November 16, 2023 5:44 PM

- 머리 식히기 2
- 코드
    
    ```python
    class Solution:
        def isSubsequence(self, s: str, t: str) -> bool:
            i, j = 0, 0
            while i < len(s) and j < len(t):
                if s[i] == t[j]:
                    i += 1
                    j += 1
                else:
                    j += 1 
            if i == len(s):
                return True 
            else:
                return False
    ```