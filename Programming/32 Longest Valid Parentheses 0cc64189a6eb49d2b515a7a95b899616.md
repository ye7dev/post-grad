# 32. Longest Valid Parentheses

Status: in progress, 🏋️‍♀️
Theme: DP
Created time: February 26, 2024 10:55 PM
Last edited time: February 27, 2024 2:12 PM

- Trial
    - brute-force : 80/231
        - 불연속 valid 쌍을 한꺼번에 count 한다는 단점
        
        ```python
        class Solution:
            def longestValidParentheses(self, s: str) -> int:
                n = len(s)
                if n == 0:
                    return 0
                left, right = 0, 0
                ans = 0
                for i in range(n):
                    if s[i] == ")":
                        if left > 0:
                            left -= 1
                            ans += 1 
                        else:
                            right += 1
                    else: # "("
                        left += 1 
                return ans * 2
        ```
        
    - brute-force: 156/231
        - max_len 추가했음
        
        ```python
        class Solution:
            def longestValidParentheses(self, s: str) -> int:
                n = len(s)
                if n == 0:
                    return 0
                left, right = 0, 0
                max_len, ans = 0, 0
                for i in range(n):
                    if s[i] == ")":
                        if left > 0:
                            left -= 1
                            ans += 1 
                        else:
                            right += 1
                            ans = 0
                    else: # "("
                        left += 1 
                    max_len = max(ans, max_len)
                return max_len * 2
        ```
        
    - brute-force: 228/231 (TLE)
        
        ```python
        class Solution:
            def longestValidParentheses(self, s: str) -> int:
                n = len(s)
                if n == 0:
                    return 0
        
                def check_substring(substr):
                    stack = []
                    ans = 0
                    for i in range(len(substr)):
                        if substr[i] == '(':
                            stack.append('(')
                        else:
                            if not stack:
                                return 0 
                            stack.pop()
                            ans += 1 
                    if stack:
                        return 0
                    return ans * 2
                    
                ans = 0
                for i in range(n):
                    end = i+2
                    while end <= n:
                        substring = s[i:end]
                        valid_len = check_substring(substring)
                        ans = max(valid_len, ans)
                        end += 2 
                return ans 
        ```
        
- 과정
    - 연속이라고 하면 right 개수보다 Left 개수가 먼저 는다
    - 근데 right 개수가 먼저는다? 그건 불연속. 그때는 max ans 취하고 다시 시작
    - 불연속인 경우를 어떻게 알지?
        - 확실히 알 수 있는 경우는 ())인데…
        - "()(()”의 경우…
- Editorial
    - **Approach 1: Brute Force**
        - every possible non-empty 짝수 길이의 substring 체크
        - valid 여부 파악하기 위해서는 stack 사용
            - ‘(’ 만날 때마다 push
            - ‘)’ 만날 때마다 Pop ‘(’
            - ‘)’ 만났는데 Pop 할 ‘(’가 없거나, substring 다 돌고 나서 stack에 원소가 남아 있으면 → 해당 substring은 invalid
            - every possible substring
            
    - **Approach 2: Using Dynamic Programming**
        - dp[i]: i에서 끝나는 longest valid substring의 length
        - valid substring은 무조건 )으로 끝나야 함
            
            → (로 끝나는 substring 자리는 무조건 0 
            
            - dp 초기값이므로 그대로 둔다
        - check every two consecutive chars
            1. s[i] = ‘)’ 이고, s[i-1] = ‘(’인지 (→ ….`()` ) 모양새 
                - dp[i] = dp[i-2] + 2
            2. s[i] = ‘)’ 이고, s[i-1] = ‘)’ 인지 (→ ….`))` ) 모양새 
                - x→dp[i-1]→i
                - dp[i-1]의 마지막은 s[i-1] = `)`
                - dp[i-1]의 처음은 s[x+1]
                    - x+1~i-1까지 구간에서 둘 다 inclusive 일 때 길이가 dp[i-1]이 나오려면
                    - i-1-(x+1)+1 = dp[i-1]
                        - i-1-x-1+1 = i-1-x = dp[i-1]
                        
                        → x = i-1-dp[i-1]
                        
                - x가 `(`여야 s[i] `)` 가 닫힐 수 있음
                    
                    ⇒ x = i-1-dp[i-1]이 `(` 인지 확인 
                    
                    - 맞으면 dp[i]는 …x-1 → `x → dp[i-1] → i`
                        1. x 이전 구간의 dp state는 dp[x-1] = dp[i-2-dp[i-1]]
                        2. dp[i-1]에 두 개 더 늘어난 값 = dp[i-1]+2
                        
                        ⇒ dp[i] = dp[i-2-dp[i-1]] + dp[i-1] + 2
                        
                    
- AC 코드
    
    ```python
    class Solution:
        def longestValidParentheses(self, s: str) -> int:
            n = len(s)
            if n == 0 or n == 1:
                return 0
            dp = [0] * n
    
            # base case
            # dp[0] = 0
            if s[0] == '(' and s[1] == ')':
                dp[1] = 2
            
            for i in range(2, n):
                if s[i] == ')':
                    if s[i-1] == '(':
                        dp[i] = dp[i-2] + 2 
                    else: # )) 
                        if i-dp[i-1] > 0:
                            left_edge = s[i-1-dp[i-1]]
                            if left_edge == '(':
                                front = dp[i-2-dp[i-1]]
                                dp[i] = front + dp[i-1] + 2
            return max(dp)
            
    ```