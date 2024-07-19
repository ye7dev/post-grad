# 20. Valid Parentheses

Status: done, in progress
Theme: stack
Created time: November 16, 2023 5:53 PM
Last edited time: November 16, 2023 6:00 PM

- 머리 식히기 4
- 조건 분기를 잘해야…
    - 사전에 없는 값이 나오면 stack에 넣어야 하고
    - 사전에 있는 데 stack top이랑 다르면 stack에 넣어야 하고
    - stack에 원소가 아무것도 없어도 넣어야 하고 …
    
    → 결국 pop 할 때 빼고는 무조건 넣어줘야 하는데 pop 하는 조건이 무려 3개나 중첩되었던 것이다…
    
- 코드
    
    ```python
    class Solution:
        def isValid(self, s: str) -> bool:
            stack = []
            n = len(s)
            paren_dict = {}
            paren_dict[')'] = '('
            paren_dict[']'] = '['
            paren_dict['}'] = '{'
    
            for i in range(len(s)):
                if s[i] in paren_dict and stack and stack[-1] == paren_dict[s[i]]:
                    stack.pop()
                else:
                    stack.append(s[i])
            
            if stack: return False
            else: return True
    ```