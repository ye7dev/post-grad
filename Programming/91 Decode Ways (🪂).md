# 91. Decode Ways (🪂)

Status: done, in progress, with help
Theme: DP
Created time: January 10, 2024 4:17 PM
Last edited time: January 11, 2024 6:17 PM

- Process
    - mapping 자체는 정해져있음. 대문자인데 mapping value 역시 숫자를 string화 한 것임에 주의
    - input은 숫자 뭉치의 string
        - 이걸 어디서 끊을지 정해서 문자로 다시 바꿔야 함
    - 현재 위치에 split을 넣냐 안 넣냐가 중요한 결정
        - split을 넣으면 다뤄야할 문제의 input이 줄어듦
            - split 기준 오른쪽 답
        - split을 안 넣으면
            - 그 덩어리 대로 어떤 문자로 전환할 수 있는지를 봐야 할 듯
    - base case
        - empty string “”을 쪼개는 방법은 1개인데 - do nothing
        - 여기에 mapping 되는 문자는 없다
        - 아님 0이 아닌 한 자리 수에 대해서는 모두 1로 채워두는 게 base case?
    - "226” - 홀수가 문제인 것 같다
        - 22, 6
            - 2, 2, 6
            - 22, 6
            
            → 2개로 카운트 
            
        - 2, 26
            - 2, 2, 6
            - 2, 26
            
            → 2개로 카운트 
            
        - 두 경우에서 2, 2, 6은 중복이 됨
        - 중복으로 들어가는 데 어떻게 하야 하쥐
    
- Trial
    - 예제 2/3. Top-down
        
        ```python
        import string
        class Solution:
            def numDecodings(self, s: str) -> int:
                n = len(s)
                # prepare mapping
                mapping = {}
                capitals = string.ascii_uppercase
                for i in range(1, 27):
                    mapping[str(i)] = capitals[i-1]
                
                memo = {}
                # function: # of distinctive way to make s[start:end+1]
                def recur(start, end):
                    # base case: 
                    if start == end: # solo '0' cannot survive
                        if s[start:end+1] == '0':
                            return 0 
                        else: # one digit -> one letter
                            return 1
                    if start > end:
                        return 0
        
                    # check memo
                    if (start, end) in memo:
                        return memo[(start, end)]
        
                    num_ways = 0
                    # recurrence relation
                    if s[end] in mapping:
                        num_ways += recur(start, end-1)
                    if s[start] in mapping:
                        num_ways += recur(start+1, end)
                    memo[(start, end)] = num_ways
        
                    return memo[(start, end)] 
        
                return recur(0, n-1)
        ```
        
- AC 코드
    - Top-down
        
        ```python
        import string
        class Solution:
            def numDecodings(self, s: str) -> int:
                n = len(s)
                # prepare mapping
                mapping = {}
                capitals = string.ascii_uppercase
                for i in range(1, 27):
                    mapping[str(i)] = capitals[i-1]
                
                memo = {}
                # function: # of distinctive way to make s[i:len(s)]
                def recur(i):
                    # base case : empty string
                    ## you can make an empty string by doing nothing 
                    ## you have cleared out all the letters
                    ## you made all the way out to the end
                    if i == len(s):
                        return 1
                    ## invalid - starting with '0'  -> move on 
                    if s[i] == '0':
                        return 0
                    # check memo
                    if i in memo:
                        return memo[i]
                    # recurrence relation
                    ## option 1: clearing out one digit
                    one_digit = recur(i+1)
                    ## option 2: clearing out two digits 
                    two_digit = 0
                    if i < len(s)-1 and int(s[i:i+2]) < 27:
                        two_digit = recur(i+2)
                    memo[i] = one_digit + two_digit
                    return memo[i]
        
                return recur(0)
        ```
        
    - Bottom-up
        - dp[i]를 s[:i+1]을 만드는 개수로 했는데 그렇게 하면 301 같은 건 절대 0이 나올 수 없어서 애먹음
        - 반대로 한다는 걸 깨닫고 풀리기 시작
        
        ```python
        class Solution:
            def numDecodings(self, s: str) -> int:
                # edge case - length 1 
                if s[0] == '0':
                    return 0
                if len(s) == 1:
                    return 1 
        
                # array
                n = len(s)
                dp = [0] * n
        
                # base case
                if s[n-1] != '0': # solo
                    dp[n-1] += 1
        
                if s[n-2] != '0':
                    if 10 <= int(s[n-2:]) <= 26: # duo
                        dp[n-2] += 1
                    # two solo case now depend on the latter one 
                    dp[n-2] += dp[n-1]
        
                # iteration
                for i in range(n-3, -1, -1): # i+2 <= n -> i <= n-2
                    if s[i] == '0': 
                        continue
                    if 10 <= int(s[i:i+2]) <= 26: # duo
                        dp[i] += dp[i+2] # n-3+2 = n-1 (base case)
                    # two solo case now depend on the latter one 
                    dp[i] += dp[i+1]          
                return dp[0] # dp[i]: # of making up s[i:]
        ```
        
    - Editorial Bottom-up
        - empty string에 대해 늘 decoding 방법이 있다고 설정 → dp size도 n+1로
        - state 정의도 다름
            - dp[i]: substring s[:i]을 decode 하는 방식의 개수
            - current string도 s[i]가 아니고 s[i-1]
        
        ```python
        class Solution:
            def numDecodings(self, s: str) -> int:
                # Array to store the subproblem results
                dp = [0 for _ in range(len(s) + 1)]
        
                dp[0] = 1
                # Ways to decode a string of size 1 is 1. Unless the string is '0'.
                # '0' doesn't have a single digit decode.
                dp[1] = 0 if s[0] == '0' else 1
        
                for i in range(2, len(dp)):
        
                    # Check if successful single digit decode is possible.
                    if s[i - 1] != '0':
                        dp[i] = dp[i - 1]
        
                    # Check if successful two digit decode is possible.
                    two_digit = int(s[i - 2 : i])
                    if two_digit >= 10 and two_digit <= 26:
                        dp[i] += dp[i - 2]
                        
                return dp[len(s)]
        ```
        
    - Neat Bottom-up (⚡️)
        
        ```python
        class Solution:
            def numDecodings(self, s: str) -> int:
                n = len(s)
                # edge case
                if n == 1:
                    if s[0] == '0': return 0
                    else: return 1 
                
                dp = [0] * (n+1)
                # base case
                dp[0] = 1 # empty string can be always decode (...)
                dp[1] = 1 if s[0] != '0' else 0
        
                # iteration
                for i in range(2, n+1): # 2~n
                    # one digit
                    if s[i-1] != '0': # 1~n-1
                        dp[i] += dp[i-1]
                    # two digit (independent of one digit)
                    ## cur idx: i-1 & already calculated results are on the left side of it
                    ## two digit : i-2, i-1
                    if 10 <= int(s[i-2:i]) <= 26:
                        dp[i] += dp[i-2]
                return dp[-1]
        ```
        
    - 오기 Bottom-up
        - 알쏭달쏭 base case 인 empty string always decodes를 없애기 위해
        - dp[i]: substring s[:i+1]을 decode 하는 방법 → dp size는 n
        - iteration은 i=2부터 가능한데, dp[1]의 base case 설정하는 게 좀 까다로움
        
        ```python
        class Solution:
            def numDecodings(self, s: str) -> int:
                n = len(s)
                # edge case
                if n == 1:
                    if s[0] == '0': return 0
                    else: return 1 
                
                dp = [0] * n
                # base case
                dp[0] = 1 if s[0] != '0' else 0
        
                if 10 <= int(s[:2]) <= 26: # duo
                    dp[1] += 1
                if s[0] != '0' and s[1] != '0': # solo
                    dp[1] += 1
        
                # iteration
                for i in range(2, n): # 2~n-1
                    # one digit
                    if s[i] != '0': 
                        dp[i] += dp[i-1]
                    # two digit (independent of one digit)
                    ## cur idx: i & already calculated results are on the left side of it
                    ## two digit : i-1, i
                    if 10 <= int(s[i-1:i+1]) <= 26:
                        dp[i] += dp[i-2]
                return dp[-1]
        ```