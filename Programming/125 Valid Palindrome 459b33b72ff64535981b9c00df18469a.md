# 125. Valid Palindrome

Status: done, in progress
Theme: Two pointers
Created time: November 16, 2023 5:22 PM
Last edited time: November 16, 2023 5:38 PM

- 머리 식힐 겸 easy 문제
- string.isalnum() 이라는 method가 있더라
- 코드
    
    ```python
    class Solution:
        def isPalindrome(self, s: str) -> bool:
            n = len(s)
            i, j = 0, n-1
            while i < j:
                if s[i].isalnum() and s[j].isalnum():
                    if s[i].lower() == s[j].lower(): 
                        i += 1 
                        j -= 1 
                    else:
                        return False
                elif s[i].isalnum():
                    j -= 1 
                elif s[j].isalnum():
                    i += 1
                else: # both not alphanumeric
                    i += 1
                    j -= 1
            return True
    ```