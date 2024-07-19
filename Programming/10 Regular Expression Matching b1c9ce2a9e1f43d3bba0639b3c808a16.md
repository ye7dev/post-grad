# 10. Regular Expression Matching

Status: in progress
Theme: DP
Created time: November 2, 2023 5:40 PM
Last edited time: November 2, 2023 11:54 PM

- 문제 이해
    
    pattern이 더 긴건 상관없나? → 그렇다 
    
    중요한 점은 *를 사용해서 중복된 문자를 지우고 그 다음 글자부터 다시 또 같아야…
    
    .*이면 어떤 char이 몇 개나 와도 상관없다는 듯? 
    
    dp table을 꼭 써야할까? 안쓰고 해보자 
    
- 내힘으로는 여기까지
    
    ```python
    class Solution:
        def isMatch(self, s: str, p: str) -> bool:
            m, n = len(s), len(p)
            i, j = 0, 0
            prev = None
            while j < n and i < m:
                if p[j] == '*':
                    if prev == '.': return True 
                    if prev is None: return False 
                    while prev == s[i]:
                        i += 1 
                        if i == m: return True
                    j += 1 
                    prev = p[j]
                else:
                    if p[j] == s[i]:
                        i += 1  
                    prev = p[j]    
                    j += 1
                    
            if i == m:
                return True
            return False
    ```
    
- 남의 아이디어
    - Recursion
        - *가 없으면 왼→오 1:1 매칭 체크
            
            1) pattern이 남아 있는지 - 다 썼으면 text도 다썼는지 
            
            2) text가 남아 있는지 - 남아 있으면 pattern이랑 지금 당면한 글자가 매칭인지
            
            3) 앞으로의 것들도 recursive call
            
            4) 현재와 미래가 모두 True라면 최종 return 값도 True 
            
            ```python
            def match(text, pattern):
                # run out of pattern & text -> True 
                # some chars in text not covered -> False
                if len(pattern) == 0:
                    return True if len(text) == 0 else False 
                # checked pattern empty but not check text empty yet 
                # check text empty and if pattern is matching or versatile
                if len(text) != 0 and pattern[0] in {text[0], '.'}:
                    first_match = True 
                else:
                    first_match = False 
                # both current matching and matching afterwards -> True 
                # if one them fails -> False 
                return first_match and match(text[1:], pattern[1:])
            ```
            
        - remind: suffix - starting from a given position and extending to the end of the text.(’llo’ from ‘hello’)
        - *가 있으면 s의 suffix들이 pattern의 나머지 부분과 일치하는지 체크해야 함 → recursive
        - *는 패턴의 최소 두번째 자리부터 올 수 있음. 왜냐면 바로 앞에 오는 char의 반복이기 때문에
            - *은 바로 앞에 오는 문자가 0번부터 n번까지 반복되는 경우를 커버
                - 바로 앞에 오는 문자가 0번 = “” 아무것도 없는 경우
                    - pattern에서 바로 앞에 오는 문자 + 뒤에오는 * 가 모두 없는 경우와 마찬가지임
                    - 예) text: aab vs. pattern: c*a*b
                        
                        → c*a*b에서 c를 0번 반복하면 ‘a*b’와 마찬가지 = pattern[2:]
                        
                    
                    ```python
                    isMatch(text, pattern[2:])
                    ```
                    
                - n번 반복
                    - * 앞에 오는 문자와 text가 일치하면 text는 하나 소진시키고 pattern은 그대로
                    - 예) text: aaaab vs. pattern: a*b
                        
                        → a == a → text: aaab → a == a → text: aab → a == a → text: ab →a ==a → text: b → isMatch(text=b, pattern[2:]=b) → True 
                        
                    
                    ```python
                    first_match and isMatch(text[1:], pattern))
                    ```
                    
        - 전체 코드
            
            ```python
            def isMatch(text, pattern):
            		# pattern empty -> text empty (True), text left (False)
                if not pattern:
                    return not text
            		
            		# text not empty and matches the first char 
                first_match = bool(text) and pattern[0] in {text[0], '.'}
            
                if len(pattern) >= 2 and pattern[1] == '*':
            				# zero of preciding or repetition
                    return (isMatch(text, pattern[2:]) or
                            first_match and isMatch(text[1:], pattern))
            		# no *
                else:
                    return first_match and isMatch(text[1:], pattern[1:])
            ```
            
    - top-down
        
        ```python
        def isMatch(text, pattern):
            memo = {} # key: index pair, value: bool (match or not)
            def dp(i, j):
                if (i, j) not in memo:
                    if j == len(pattern): # pattern ran out
        								# text ran out -> True / text left -> False
                        ans = i == len(text)
                    else:
        								# check first char 
                        first_match = i < len(text) and pattern[j] in {text[i], '.'}
                        # star exists
        								if j+1 < len(pattern) and pattern[j+1] == '*':
        										# j+2 : skipping preceding & star 
        										# i+1 : first char from text crossed off with repetition
                            ans = dp(i, j+2) or first_match and dp(i+1, j)
        								# star not exists
                        else:
                            ans = first_match and dp(i+1, j+1)
        						# save intermediate result for the future
                    memo[i, j] = ans
        				# if value exists just return
                return memo[i, j]
        
            return dp(0, 0)
        ```
        
    - bottom-up
        - base case tricky
            - 0번째 row : empty text
                
                →  char*인 상태에서 char를 0번 반복한 뒤 내가 바로 그 다음에 오는 char인 경우 
                
                - 바로 앞에 오는 문자가 0번 = “” 아무것도 없는 경우
                    - pattern에서 바로 앞에 오는 문자 + 뒤에오는 * 가 모두 없는 경우와 마찬가지임
                    - 예) text: aab vs. pattern: c*a*b
                        
                        → c*a*b에서 c를 0번 반복하면 ‘a*b’와 마찬가지 = pattern[2:]
                        
        
        ```python
        def isMatch(text, pattern):
            m, n = len(text), len(pattern)
        		# row: text, col: pattern
            dp = [[False] * (n + 1) for _ in range(m + 1)]
        
            dp[0][0] = True # empty text, empty pattern 
        		# base case: empty text -> c*a*b에서 나는 a이면 True
            for j in range(1, n+1):
                if pattern[j-1] == '*': # 현재 substring에서 마지막 letter
        						# j == 1이면, j-2는 -1
        						# 같은 row의 가장 오른쪽 cell -> 아직 계산 안한 곳이라서 무조건 False됨
        						# 생각해보면 j=1이면 j-1은 0. 0번째에 '*'가 오면 False가 오는 게 맞음 
                    dp[0][j] = dp[0][j-2] **# (앞부분) + (뒷부분: pre + *)**
        						**# 뒷부분은 pre를 0번 반복한다고 하면 True이기 때문에 앞부분 여하에 따라 달라짐** 
        		
        		# transition
            for i in range(1, m + 1): # s[:1](첫글자) ~ s[:m+1](text 전체)
                for j in range(1, n + 1): # p[:1](첫글자) ~ p[:n+1](text 전체)
        						# 현재 substring에서 마지막 글자가 같거나 pattern 마지막 글자가 무적이거나
        						# substring에서 앞부분은 이미 확인된 상태라서 마지막 글자만 보면 됨 
                    if pattern[j-1] == text[i-1] or pattern[j-1] == '.':
                        dp[i][j] = dp[i-1][j-1]
        						# pattern substring 마지막 글자가 '*'이면 
                    elif pattern[j-1] == '*':
        								# '*' 앞에 글자를 0번 사용하는 경우 -> (앞부분) 매칭 여부에 따라 결정
        								# '*' 앞에 글자로 text 하나 매칭하는지 확인 
        								# -> pattern은 substring 마지막에서 두번째랑 text substring 마지막 글자가 matching 되는지 확인 
        								# -> matching이면 앞부분 여하에 따라 이번 cell 값이 결정됨 
        								# -> 혹은 pattern substring 마지막에서 두번째가 만능이어도 앞부분 여하에 따라 결정 
                        dp[i][j] = dp[i][j-2] or (dp[i-1][j] if text[i-1] == pattern[j-2] or pattern[j-2] == '.' else False)
        		# end 
            return dp[m][n]
        ```