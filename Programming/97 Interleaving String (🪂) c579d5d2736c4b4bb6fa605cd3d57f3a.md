# 97. Interleaving String (🪂)

Status: done, in progress
Theme: DP
Created time: January 16, 2024 5:10 PM
Last edited time: January 17, 2024 2:37 PM

- Progress
    - A **substring** is a contiguous non-empty sequence of characters within a string.
    - 늘 s와 t의 길이는 1차이거나 같거나겠지?
    - 이러저러한 조합을 다 해봤을 때 둘다 empty string이 되면 True인듯
    - 두 string을 남김없이 다써야 하나?
        - 아니다
        - a, b,  ⇒ a 일 때는 false다
    - x[0:] = all, x[:0] = empty
    - len(s1) = n. len(s[1:]) = n-1, len(s[2:]) = n-2
        
        → len(s[i:]) = n - i 
        
        - s[x:] = n - 2 → x = 2
    - len(s1[i:]) + len(s2[j:]) = n-i+ m- j = n+m - (i+j)
        - j = m → n + m - i - m = n-i
- Trial
    - Bottom-up
        - 예제 3/5
            - base case를 어떻게 해야 할지 모르겠음
                - top-down에서 그대로 가져와서 나름 index로 조정했는데, 뭔가 순차적으로 뒤에서부터 몇 개가 일치하면 True이런식이 좀 잘못된 것 같음. 왜냐면 각 스트링에서 지그재그로 한 문자씩 가져갈 수 있기 때문에.
            
            ```python
            class Solution:
                def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
                    n, m, sum_len = len(s1), len(s2), len(s3)
                    if n + m != sum_len:
                        return False
                    
                    # array
                    ## state dp[i][j] - is s1[i:] + s2[j:] = s3[i+j:]?
                    dp = [[-1] * (m+1) for _ in range(n+1)]
                    # base case
                    dp[n][m] = True # empty substrings can make empty substring
                    for i in range(n):
                        if s1[i:] == s3[(n - i):]:
                            dp[i][m] = True 
                        else:
                            dp[i][m] = False
                    for j in range(m):
                        if s2[j:] == s3[(m - j):]:
                            dp[n][j] = True
                        else:
                            dp[n][j] = False   
            
                    # iteration
                    k = sum_len-1
                    for i in range(m-1, -1, -1):
                        for j in range(n-1, -1, -1):
                            if s1[i] == s3[k] and dp[i+1][j]:
                                dp[i][j] = True
                            if s2[j] == s3[k] and dp[i][j+1]:
                                dp[i][j] = True
                            if dp[i][j] is True:
                                k -= 1 
                            else:
                                dp[i][j] = False
                    
                    return dp[0][0]
            ```
            
- AC 코드
    - 갖가지 상황을 다 집어넣은 top-down
        
        ```python
        class Solution:
            def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
                memo = {}
                n, m = len(s1), len(s2)
                third_len = len(s3)
                # function
                def recur(first_idx, second_idx, third_idx):
                    # base case
                    if third_idx == -1:
                        if first_idx == -1 and second_idx == -1:
                            return True
                        else:
                            return False
                    if first_idx == -1 and second_idx == -1:
                        return False
                    # check memoized
                    if (first_idx, second_idx) in memo:
                        return memo[(first_idx, second_idx)]
                    # recurrence relation
                    first_trial, second_trial = False, False
                    if first_idx > -1 and s1[first_idx] == s3[third_idx]:
                        first_trial = recur(first_idx-1, second_idx, third_idx-1)
                    if second_idx > -1 and s2[second_idx] == s3[third_idx]:
                        second_trial = recur(first_idx, second_idx-1, third_idx-1)
                    if first_trial or second_trial:
                        memo[(first_idx, second_idx)] = True
                    else:
                        memo[(first_idx, second_idx)] = False
                    return memo[(first_idx, second_idx)] 
        
                return recur(n-1, m-1, third_len-1)
        ```
        
    - 좀 더 간결한 top-down from editorial
        - 0에서 시작해서 어느 한 쪽이 마지막 index에 도달하면
            - 남은 한쪽의 현재 위치부터 끝까지의 substring이 s3의 현재 위치부터 끝까지의 substring과 동일한지만 체크
                
                ```python
                # base case
                if i == len(s1):
                    return s2[j:] == s3[k:]
                if j == len(s2):
                    return s1[i:] == s3[k:]
                ```
                
            - 만약 두 쪽다 모두 소진한 상태면, s3도 다 소진했는지의 여부에 따라 결정될 것
                - string[last_idx + 1:] = empty
        - memo로 저장되는 값이 bool이고, i j가 모두 index이기 때문에 이 경우는 memo를 사전 대신 2차원 matrix, 값은 -1 (아직 아무것도 처리 되지 않았다는 뜻)로 초기화하는 것이 좋아보임
        - 또 edge case로는 두 substring을 s3에 모두 소진해야 하기 때문에, s1, s2 길이의 합이 s3의 길이와 다르면 그대로 return False 하면 여러 케이스를 간결하게 걸러낼 수 있다
        
        ```python
        class Solution:
            def is_Interleave(self, s1, i, s2, j, s3, k, memo):
                if i == len(s1):
                    return s2[j:] == s3[k:]
                if j == len(s2):
                    return s1[i:] == s3[k:]
                if memo[i][j] >= 0:
                    return memo[i][j] == 1
        
                ans = ((s3[k] == s1[i] and self.is_Interleave(s1, i + 1, s2, j, s3, k + 1, memo)) or
                       (s3[k] == s2[j] and self.is_Interleave(s1, i, s2, j + 1, s3, k + 1, memo)))
                
                memo[i][j] = 1 if ans else 0
                return ans
        
            def isInterleave(self, s1, s2, s3):
                if len(s1) + len(s2) != len(s3):
                    return False
        
                memo = [[-1 for _ in range(len(s2))] for _ in range(len(s1))]
                return self.is_Interleave(s1, 0, s2, 0, s3, 0, memo)
        ```
        
    - base case 따로 뺀 bottom-up
        
        ```python
        class Solution:
            def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
                m, n, sum_len = len(s1), len(s2), len(s3)
                if n + m != sum_len:
                    return False
                
                # array
                ## state dp[i][j] - is s1[:i] + s2[:j] = s3[:i+j-1]?
                dp = [[False] * (n+1) for _ in range(m+1)]
                # base case
                dp[0][0] = True # empty substrings can make empty substring
                for i in range(m): # 0~m-1
                    if s1[i] == s3[i] and dp[i][0]:
                        dp[i+1][0] = True # 1~m
                for j in range(n): # 0~n-1 
                    if s2[j] == s3[j] and dp[0][j]:
                        dp[0][j+1] = True # 1~n
                # recurrence relation
                for i in range(1, m+1): # 1~m
                    for j in range(1, n+1): # 1~n
                        if s1[i-1] == s3[i+j-1] and dp[i-1][j]: # 0~m-1
                            dp[i][j] = True # 1~m
                        if s2[j-1] == s3[i+j-1] and dp[i][j-1]: # 0~n-1
                            dp[i][j] = True # 1~n
        
                return dp[m][n]
        ```
        
    - index 확실히 교통정리한 bottom-up
        
        ```python
        class Solution:
            def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
                m, n, res_len = len(s1), len(s2), len(s3)
                if m + n != res_len:
                    return False 
                
                # array
                '''
                - state definition
                    dp[i][j] : s1[:i] & s2[:j] => s3[:i+j-1]? 
                - prefix valid index range
                    s1[:i] -> s1[0], s1[1], ..., s1[i-1] -> valid i : 1~m
                    s1[:0] -> "", s1[:m] -> s1
                - original problem
                    s1 & s2 => s3? 
                    s1[:m] & s[:n] => s3[:m+n]
                    s1[:m] = s1[0], ... s1[m-1] -> len(s1[:m]) = m
                    s2[:n] = s2[0], ... s2[n-1] -> len(s2[:n]) = n
                    s3[:m+n] = s3[0], ... s3[m+n-1] -> len(s3[:m+n]) = m+n-1 
                '''  
                dp = [[False] * (n+1) for _ in range(m+1)]
                
                # base case: two empty strings can make one empty string
                ## s1[:0] = "" & s2[:0] = "" -> "" 
                dp[0][0] = True 
                # edge of the matrix: dp[0][j], dp[i][0]
                for i in range(1, m+1):
                    if s1[i-1] == s3[i-1]: # last element of s1[:i]. 0 <= i-1 < m
                        dp[i][0] = True # dp[1][0] ~ dp[m][0]
                    else:
                        break
                for j in range(1, n+1):
                    if s2[j-1] == s3[j-1]: # 0 <= j-1 < n
                        dp[0][j] = True # dp[0][1] ~ dp[0][n]
                    else:
                        break
                
                # recurrence relation
                for i in range(1, m+1): # 1~m
                    for j in range(1, n+1): # 1~n
                        # s1[i-2] : last element of s1[:i-1]
                        # s1[i-1] : last element of s1[:i]
                        # s3[i+j-1] : last element of s3[:i+j]
                        if s1[i-1] == s3[i+j-1] and dp[i-1][j]:
                            dp[i][j] = True
                        # s2[j-2] : last element of s2[:j-1]
                        if s2[j-1] == s3[i+j-1] and dp[i][j-1]:
                            dp[i][j] = True
                
                # s1[:m] = s1
                return dp[m][n]
        ```
        
    - base case 한번 더 다음은 final bottom-up
        - base case에서도 누적인 상태로 다 일치해야 True지 중간에 하나라도 불일치면 그때부터는 모두 False
        
        ```python
        class Solution:
            def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
                m, n, res_len = len(s1), len(s2), len(s3)
                if m + n != res_len:
                    return False 
                
                # array
                '''
                - state definition
                    dp[i][j] : s1[:i] & s2[:j] => s3[:i+j-1]? 
                - prefix valid index range
                    s1[:i] -> s1[0], s1[1], ..., s1[i-1] -> valid i : 1~m
                    s1[:0] -> "", s1[:m] -> s1
                - original problem
                    s1 & s2 => s3? 
                    s1[:m] & s[:n] => s3[:m+n]
                    s1[:m] = s1[0], ... s1[m-1] -> len(s1[:m]) = m
                    s2[:n] = s2[0], ... s2[n-1] -> len(s2[:n]) = n
                    s3[:m+n] = s3[0], ... s3[m+n-1] -> len(s3[:m+n]) = m+n-1 
                '''  
                dp = [[False] * (n+1) for _ in range(m+1)]
                
                # base case: two empty strings can make one empty string
                ## s1[:0] = "" & s2[:0] = "" -> "" 
                dp[0][0] = True 
                # edge of the matrix: dp[0][j], dp[i][0]
                for i in range(1, m+1):
                    if s1[i-1] == s3[i-1] and dp[i-1][0]: # last element of s1[:i]. 0 <= i-1 < m
                        dp[i][0] = True # dp[1][0] ~ dp[m][0]
                for j in range(1, n+1):
                    if s2[j-1] == s3[j-1] and dp[0][j-1]: # 0 <= j-1 < n
                        dp[0][j] = True # dp[0][1] ~ dp[0][n]
                
                # recurrence relation
                for i in range(1, m+1): # 1~m
                    for j in range(1, n+1): # 1~n
                        # s1[i-2] : last element of s1[:i-1]
                        # s1[i-1] : last element of s1[:i]
                        # s3[i+j-1] : last element of s3[:i+j]
                        if s1[i-1] == s3[i+j-1] and dp[i-1][j]:
                            dp[i][j] = True
                        # s2[j-2] : last element of s2[:j-1]
                        if s2[j-1] == s3[i+j-1] and dp[i][j-1]:
                            dp[i][j] = True
                
                # s1[:m] = s1
                return dp[m][n]
        ```
        
- Editorial
    - **Approach 3: Using 2D Dynamic Programming**
        - TD vs BU 접근법 차이 - prefix냐 suffix냐 차이인듯
            - top-down  접근법 요약 : s1[i:] + s2[j:] → s3[m+n-(i+j):]
                - a recursive function to check whether the remaining portions of s1 and s2 can be interleaved to form the remaining portion of s3
            - bottom-up 접근법 요약  : s1[:i] + s2[:j] → s3[:i+j-1]
                - Here, we include one character from s1 or s2 and
                - check whether the resultant string formed so far
                - by one particular interleaving of the the current prefix of s1 and s2
                - form a prefix of s3
        - state dp[i][j]
            - s1[:i+1]와 s2[:j+1]를 interleaving 해서 (각각 prefix임)
            - 길이가 (i+j+2)인 s3의 prefix(`s3[:(i+j+2)]`)를 만들어 낼 수 있는지
            
            +++ 근데 base case가 말이 되려면 내 코드처럼 하는 게 맞는 것 같음 
            
        - dp[i][j] entry 값 결정
            1. k = i + j + 1 일 때 s1[i]나 s2[j]가 s3[k]와 일치하지 않을 때 → False 
            2. 일치하는 경우 
                - s1[i]가 s3[k]와 일치하는 경우
                    - dp[i-1][j]도 True여야만 dp[i][j]가 True
                - s2[j]가 s3[k]와 일치하는 경우
                    - dp[i][j-1]도 True여야만 dp[i][j]가 True
- empty string 두 개는 더해도 empty string 하나
    
    ```python
    >>> x = ""
    >>> x
    ''
    >>> y = ""
    >>> y
    ''
    >>> x+y
    ''
    ```