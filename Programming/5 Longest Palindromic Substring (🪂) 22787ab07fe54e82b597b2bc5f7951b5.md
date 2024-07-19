# 5. Longest Palindromic Substring (🪂)

Status: done, in progress, incomplete, with help, 🏋️‍♀️
Theme: DP, On Strings
Created time: January 26, 2024 7:07 PM
Last edited time: January 27, 2024 7:32 PM

- Trial
    - Brute Force 84/142
        
        ```python
        class Solution:
            def longestPalindrome(self, s: str) -> str:
                n = len(s)
                if n == 1:
                    return s
                
                def check_palindrome(string):
                    if string[::-1] == string:
                        return True
                    return False
                
                for start in range(n-1): # 0->n-2
                    for length in range(n-1, 0, -1): # n-1 -> 1
                        end = start + length
                        # 0 + n-1 = n-1 -> 0:n -> n
                        # n-2 + 1 = n-1 -> n-2:n -> 2
                        if check_palindrome(s[start:end+1]):
                            print(start, end)
                            return s[start:end+1]
                return s[0]
        ```
        
    - DP 예제 1/2
        - i, j indexing 하는 부분이 여전히 헷갈린다
        
        ```python
        class Solution:
            def longestPalindrome(self, s: str) -> str:
                n = len(s)
                dp = [[False] * n for _ in range(n)]
                # state dp[i][j] -> inclusive bounds(i, j)
        
                # base case - length 1
                for i in range(n):
                    dp[i][i] = True 
                # base case - length 2
                for i in range(n-1): # 0->n-2
                    if s[i] == s[i+1]: # 1->n-1
                        dp[i][i+1] = True 
                # recurrence case
                long_pal = ""
                for diff in range(2, n): # n-1 - 0 = n-1
                    for i in range(n-diff): 
                        if s[i] == s[i+diff] and dp[i+1][i+diff-1]:
                            dp[i][i+diff] = True 
                            if len(long_pal) < diff:
                                long_pal = s[i:i+diff+1]
                return long_pal
        ```
        
    - long pal이 base case에서도 나오게끔 변경 → 118/142
        
        ```python
        class Solution:
            def longestPalindrome(self, s: str) -> str:
                n = len(s)
                dp = [[False] * n for _ in range(n)]
                # state dp[i][j] -> inclusive bounds(i, j)
                long_pal = ""
                # base case - length 1
                for i in range(n):
                    dp[i][i] = True 
                    if len(long_pal) < 1:
                        long_pal = s[i]
                # base case - length 2
                for i in range(n-1): # 0->n-2
                    if s[i] == s[i+1]: # 1->n-1
                        dp[i][i+1] = True 
                        if len(long_pal) < 2:
                            long_pal = s[i:i+2]
                # recurrence case
                for diff in range(2, n): # n-1 - 0 = n-1
                    for i in range(n-diff): 
                        if s[i] == s[i+diff] and dp[i+1][i+diff-1]:
                            dp[i][i+diff] = True 
                            if len(long_pal) < diff:
                                long_pal = s[i:i+diff+1]
                return long_pal
        ```
        
- AC 코드
    - Brute Force - index, length 주의
        
        ```python
        class Solution:
            def longestPalindrome(self, s: str) -> str:
                def check(i, j):
                    left = i
                    right = j-1
        
                    while left < right:
                        if s[left] != s[right]:
                            return False
        								# 아래 부분 까먹으면 무한 루프 돈다 
                        left += 1
                        right -= 1
                    return True 
        
                n = len(s)
                if n == 1:
                    return s
                
                for length in range(n, 0, -1):
                    # how much start can go further? n-length
                    for start in range(n-length+1):
                        if check(start, start+length):
                            return s[start:start+length]
                return ""
        ```
        
        - 모든 길이에 대해 start는 0에서 시작. 그럼 어디서 끝나나?
            - 맨 마지막 원소 index n-1
            - last_start … n-1 의 길이가 length가 되어야 함
                - n-1-start + 1 = length → n-start = length
                - last_start = n-length
            - last_start … n-1의 길이가 length
                - s[last_start:n]
                - n-1 = start + length -1
                - n = start + length
                
                → s[last_start: last_start + length] 의 길이가 length  
                
    - DP - diff + 1 은 length다
        
        ```python
        class Solution:
            def longestPalindrome(self, s: str) -> str:
                n = len(s)
                dp = [[False] * n for _ in range(n)]
                # state dp[i][j] -> inclusive bounds(i, j)
                # base case - length 1
                long_pal = ""
                for i in range(n):
                    dp[i][i] = True 
                    if len(long_pal) < 1:
                        long_pal = s[i]
                # base case - length 2
                for i in range(n-1): # 0->n-2
                    if s[i] == s[i+1]: # 1->n-1
                        dp[i][i+1] = True 
                        if len(long_pal) < 2:
                            long_pal = s[i:i+2]
                # recurrence case
                for diff in range(2, n): # n-1 - 0 = n-1
                    for i in range(n-diff): 
                        if s[i] == s[i+diff] and dp[i+1][i+diff-1]:
                            dp[i][i+diff] = True 
                            if len(long_pal) < diff + 1:
                                long_pal = s[i:i+diff+1]
                return long_pal
        ```
        
    - DP - keep tracking index version
        
        ```python
        class Solution:
            def longestPalindrome(self, s: str) -> str:
                n = len(s)
                dp = [[False] * n for _ in range(n)]
                # state dp[i][j] -> inclusive bounds(i, j)
                # base case - length 1
                ans = [0, 0] # inclusive bounds
                for i in range(n):
                    dp[i][i] = True 
                # base case - length 2
                for i in range(n-1): # 0->n-2
                    if s[i] == s[i+1]: # 1->n-1
                        dp[i][i+1] = True 
                        ans = [i, i+1]
                # recurrence case
                for diff in range(2, n): # n-1 - 0 = n-1
                    for i in range(n-diff): 
                        if s[i] == s[i+diff] and dp[i+1][i+diff-1]:
                            dp[i][i+diff] = True 
                            ans = [i, i+diff]
                return s[ans[0]:ans[1]+1]
        ```
        
- Editorial
    - **Approach 1: Check All Substrings**
        - Intuition
            - two pointers
            - 서로에게 향하는 방향으로 pointer 이동 시키면서, 두 pointer에 위치한 문자가 일치하는지 확인
            - 두 pointer가 한 곳에서 만나면 palindrome
            - 가장 긴 substring부터 도는 것이 유리 - 문제에서 Longest palindrome을 요구하고 있으니까. 처음 만나는 palindrome이 Longest.
        - Algorithm
            1. substring이 palindrome인지 판별해주는 helper method 정의 
                - parameter: start index i, end index j (exclusive)
                - substring in question : s[i:j] → last char: s[j-1]
                - two pointer 선언
                    - left = i, right = j-1
                    - left < right 조건 만족하는 동안 아래의 작업 수행 (stop condition: left == right or left > right)
                        - 두 pointer에 해당하는 char가 일치하지 않으면 그 즉시 return False
                        - 일치하면 left, right를 서로를 향해 하나씩 전진 시킴
                - while loop 다 지나오면 전체 범위에 대해 두 pointer에 해당하는 char가 모두 일치한다는 것이므로 return True
            2. outer for loop: `length` 
                - len(s) → 1 (inclusive)
                - 현재 우리가 고려하는 substring의 길이 의미
            3. inner for loop: `start`
                - 0 → len(s) - length (inclusive)
                    - range stop 값은 len(s) - length + 1
                - 현재 우리가 고려하는 substring의 시작점 의미
                - 헷갈리는 for loop
                    - length 길이의 자를 0부터 시작해서 한번씩 대본다고 생각
                    
                    | length | start | start + length |
                    | --- | --- | --- |
                    | 7 | 0 | 7 |
                    | 6 | 0 | 6 |
                    | 6 | 1 | 7 |
                    | 5 | 0 | 5 |
                    | 5 | 1 | 6 |
                    | 5 | 2 | 7 |
            4. inner for loop: `s[start: start+length]` 
                - 1에서 정의한 함수 활용해서 해당 substring이 palindrome인지 체크
    - **Approach 2: Dynamic Programming**
        - Intuition
            - inclusive bounds i, j (s[i:j+1]) 가 palindrome 일 때, s[i-1] == s[j+1] 이면 s[i-1:j+2]도 palindrome - constant time work
            - 이 로직의 순서를 반대로 뒤집으면 s[i] == s[j] 이고 inclusive bounds (i+1, j-1) 의 substring이 palindrome이면, substring (i, j)도 palindrome
            - 홀수 길이의 substring의 경우
                - length 1의 모든 substring은 palindrome → 길이 3의 substring이 palindrome인지 check 가능
                    - j - i = 2 인 모든 i, j pair를 체크하면 된다
                    - brute force에서도 확인했듯이 inclusive bound의 차 + 1 = 해당 구간 substring 길이
                - 길이 3의 palindrome 확인하고 나면, 길이 5, 7 등의 substring에 대해서도 palindrome 여부 확인 가능
            - 짝수 길이의 substring의 경우
                - 길이 2의 경우: 그 둘이 같은 문자면 palindrome
                - 길이 2의 substring을 찾고 나면, 4, 6 등의 길이에 대해서도 찾을 수 있다
            - dp table
                - size: n * n
                - state `dp[i][j]`
                    - inclusive bounds i, j가 palindrome인지 여부를 저장
                - initial cell value: true for all the substrings of length 1
                    - dp[i][i] = True
                - length 2 substrings
                    - s[i] == s[i+1] → dp[i][i+1] true
            - recurrence relation
                - iterate over all i, j pairs
                - 처음에는 j-i = 2부터 시작해서 3, 4, …
                    - 길이가 짧은 substring부터 확인하기 때문에 새롭게 확인되는 palindrome 마다 역대 최장 palindrome이 됨
                - 체크하는 조건
                    
                    1) current char이 일치하는지 s[i] == s[j]
                    
                    2) 그 사이의 substring이 palindrome 인지 dp[i+1][j-1] 
                    
        - 알고리즘
            1. dp table 초기화
            2. `ans` 초기화 [0, 0]
                - inclusive bounds of the answer
            3. base case I 
                - dp[i][i]  = True
            4. base case II
                - dp[i][i+1]
                - ans update - [i, i+1]
            5. recurrence case 
                - outer loop - diff range: 2 → n (exclusive)
                    - j - i 값을 의미
                - inner loop - i range: 0 → n-diff (exclusive)
                    - j = i + diff
                    - s[i] == s[j] && dp[i+1][j-1] 이면 dp[i][j] = True