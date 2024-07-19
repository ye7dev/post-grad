# 1143. Longest Common Subsequence

Status: done, in progress, with help, 💎
Theme: DP
Created time: January 4, 2024 6:03 PM
Last edited time: January 9, 2024 4:29 PM

- 문제 이해
    - 어느 쪽으로 input이 작아지는가?
        - end를 고정해두고 start가 점점 작아질 수록 input이 커짐
            - 이 경우는 앞의 계산 결과를 가지고, start 부분만 처리하면 더 큰 범위의 input에 대한 결과를 가져갈 수 있음
        - start를 고정해두고 end가 점점 커질 수록 input이 커짐
            - 근데 이 경우는 먼저 한 계산 결과가 그 다음 계산 결과에 도움이 안됨
    - state
        - dp[i][j]: text1 end부터 i까지, text2 end부터 j까지 범위에서 가장 긴 common subsequence의 길이
    - return
        - dp[0][0]
    - base case
        - end부터 end까지면 범위가 없다고 봐야하나?
            - len(text1) = 5
            - text1[4:5] = e
            - text1[5:5] = ‘’
- Trial
    - 예제 통과! 16/47
        
        ```python
        class Solution:
            def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                n, m = len(text1), len(text2)
                # array
                dp = [[0] * (m+1) for _ in range(n+1)]
                # base case
                # dp[i][m] = dp[n][j] = 0 
        
                for i in range(n-1, -1, -1):
                    for j in range(m-1, -1, -1):
                        if text1[i] == text2[j]:
                            dp[i][j] = max(dp[i+1][j], dp[i][j+1]) + 1
                        else:
                            dp[i][j] = max(dp[i+1][j], dp[i][j+1])
                
                return dp[0][0]
        ```
        
- Explore hints
    - dp(i, j) : text1[:i+1], text2[:j+1] 까지 고려했을 때 둘 사이에서 나올 수 있는 가장 긴 common subsequence
    - recurrence relation
        - 두 char이 같으면 1 + dp(i-1, j-1)
        - 그렇지 않으면 두 text 중 하나의 index를 뒤로 민다
    - base case
        - i나 j 중에 0보다 작은 index가 생기면 out of bounds → return 0
- 알고 싶은 점
    - 현재의 어떤 결정이 미래에 영향을 미치는 건지?
        - current index에 해당하는 두 char이 일치하거나 안하거나 두 가지 경우가 있는데, 이게 어떻게 미래에 영향을 미치는 거지? 그냥 결과가 누적돼서 그런가?
            - 현재 일치하는 char을 longest substring으로 삼을 것이냐 안 삼을 것이냐. 왜냐면 일단 그걸로 삼는 순간, 두번째 string에서 그보다 앞에 있는 char는 모두 고려대상에서 제외되기 때문-순서는 그대로 유지한다는 제약 때문에
                
                ![Untitled](Untitled%201.png)
                
                ![Untitled](Untitled%202.png)
                
    - recurrence relation
        
        → hint 참고 
        
- AC 코드
    - Explore hints 보고 top-down으로 짜기
        
        ```python
        class Solution:
            def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                n, m = len(text1), len(text2)
                memo = {}
                # function
                def recur(i, j):
                    if i < 0 or j < 0:
                        return 0
                    if (i, j) in memo:
                        return memo[(i, j)]
                    
                    if text1[i] == text2[j]:
                        # top-down에서 equation 오른쪽에 있는 요소는 아직 계산 전인 요소. 더 타고 들어가야 얻을 수 있는 결과 
                        memo[(i, j)] = recur(i-1, j-1) + 1 
                    else:
                        memo[(i, j)] = max(recur(i-1, j), recur(i, j-1))
                    return memo[(i, j)]
        
                return recur(n-1, m-1)
        ```
        
    - bottom-up으로 전환(⚡️)
        
        ```python
        class Solution:
            def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                n, m = len(text1), len(text2)
                
                # array
                dp = [[0] * (m+1) for _ in range(n+1)]
                # base case
                # i = n, j = m -> no valid char -> no common -> len = 0
        
                # iteration
                for i in range(n-1, -1, -1):
                    for j in range(m-1, -1, -1):
                        if text1[i] == text2[j]:
                            # bottom up에서 equation 오른쪽은 이미 계산 완료된 부분 
                            dp[i][j] = 1 + dp[i+1][j+1]
                        else:
                            dp[i][j] = max(dp[i+1][j], dp[i][j+1])
                
                return dp[0][0]
        ```
        
- Editorial
    - Overview
        - 현실 문제와 깊은 연관-Git에서 merging branch 할 때 두 파일 간의 내용 비교, genetic code 비교 등
        - common sequence 제약-letters cannot be rearranged
            
            ![Untitled](Untitled%203.png)
            
            ↳ 이렇게 같은 문자끼리 연결하는 선을 그었을 때, 교차하는 지점이 생기면  common subsequence가 될 수 없음. letter이 rearranged 되어야만 common subsequence가 될 수 있는 상태인데, 이는 문제에서 주어진 제약에 반함 
            
        - greedy 알고리즘이 존재하면, 언제나 DP로도 풀 수 있고, 그 방법이 더 효율적이라는 것을 의미
    - **Applying Dynamic Programming to a Problem**
        - ㅋㅋ 시간이 지나면 언제 greedy 알고리즘을 포기해야 하는지 감이 오게 될 것이라고 함
        - memoization
            - caching to a function
            - recursive, top-down
            - 원래의 가장 큰 input을 다루는 문제에서 시작해서, 반복적으로 더 작은 문제로 재귀적으로 진입
        - tabulation
            - 더 작은 문제부터 풀기 시작해서 table에 결과를 저장
            - 더 작은 문제에서 더 큰 문제로 iterative 방식으로 진행
    - **Approach 1: Memoization**
        - Intuition (⭐️⭐️)
            - 원래 문제를 더 작은 문제로 재귀적으로 쪼개야
                - 더 작은 문제의 해를 가지고 원래 문제의 optimal solution을 얻고자 함
            - 동일한 글자끼리 선을 그어보자
                
                ![Untitled](Untitled%204.png)
                
                - the first possible line(?)에 대한 두 가지 입장
                    - optimal solution의 일부일 것이다
                        
                        ![Untitled](Untitled%205.png)
                        
                        - 그럼 나머지 line들은 a 다음에 나오는 substring들 사이에서 찾아야 할 것
                        - a 끼리 연결한 line 1에 뒤에 나오는 substring들에 대한 답을 더하면 optimal solution이 나올 것
                            - 1 + subproblem solution
                    - optimal solution의 일부가 아닐 것이다
                        
                        ![Untitled](Untitled%206.png)
                        
                        - 첫번째 line을 연결하려 했던 letter가 optimal solution에 포함되지 않을 것이라는 의미(?)
                            - 첫번째 letter a에 대한 최선의 선택은 a-a 였는데 그게 포함이 안된다고 하는 거니까
                        - optimal solution은 첫번째 string에서 첫번째 letter(a)를 제외한 나머지를 범위로 삼는 subproblem의 해가 될 것
                    - 근데 a-a line이 optimal solution의 일부인지 아닌지는 알 수 없기 때문에, 두 가지 경우에 대한 정답을 다 찾아야 하고, 둘 중에 더 값이 큰 것이 optimal solution (longest length)
                - 두 string 중 하나가 길이 0일 때는 subproblem으로 쪼갤 필요 없이 그냥 0 return 하면 됨 - recursion에 대한 base case
                - 총 몇 개의 subproblem을 풀게 될까?
                    - 한 번에 하나의 string 혹은 두 string 모두에서 character 하나를 take off 하기 때문에 len(first_string) * len(second_string) 개의 가능한 subproblem이 있을 것
                    - 부가적인 예
                        1. **Initial Comparison**: We start by comparing the first characters of both strings. Here, it's **`A`** in both String 1 and String 2. Since they match, we include **`A`** in our LCS.
                        2. **Taking Off the Matching Character**: After finding the match, we remove this character from both strings. Now our strings look like this:
                            - String 1: **`BCD`**
                            - String 2: **`EBD`**
                        3. **Recursively Solving the Reduced Problem**: We now solve the LCS problem for these reduced strings **`BCD`** and **`EBD`**.
                        4. **Continuing the Process**: We compare the first characters of these reduced strings (**`B`** from **`BCD`** and **`E`** from **`EBD`**). They don't match, so we don't remove them simultaneously. Instead, we explore further by considering different possibilities (like removing a character from only one string at a time).
                    - 또 다른 관점은 string의 길이가 K이면 K개의 unique suffixe(접두어)가 있는 것 → first string에서 M개의 suffix, second string에서 N개의 suffix 존재
                        - 전체 subproblem은 모든 조합의 suffix를 다 비교하고 거기서 +1 하느냐 마느냐, next step 뭘로 가져가느냐 정하는 거니까(base case 제외) → M * N 개의 subproblem 존재하는 셈
        - Algorithm
            - top-down pseudo
                - functools lru_cache decorator 사용 가능할 듯
            
            ```python
            # function
            def LCS(text1, text2):
            		# base case
            		if len(text1) == 0 or len(text2) == 0:
            				return 0 
            		
            		letter1 = text1[0]
            		# the line is not part of optimal solution
            		case1 = LCS(text1[1:], text2)
            
            		case2 = 0 # 만약 letter1이 text2에 없으면 그대로 0
            			if letter1 is in text2:
            			first_occurence = first position of letter 1 in text2 
            			# part of optimal
            			case2 = 1 + LCS(text1[1:], text2[first_occurence+1:])
            		
            		return max(case1, case2)
            ```
            
            ```python
            from functools import lru_cache
            
            class Solution:
                def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                    
                    @lru_cache(maxsize=None)
                    def memo_solve(p1, p2):
                        
                        # Base case: If either string is now empty, we can't match
                        # up anymore characters.
                        if p1 == len(text1) or p2 == len(text2):
                            return 0
                        
                        # Option 1: We don't include text1[p1] in the solution.
                        option_1 = memo_solve(p1 + 1, p2)
                        
                        # Option 2: We include text1[p1] in the solution, as long as
                        # a match for it in text2 at or after p2 exists.
                        first_occurence = text2.find(text1[p1], p2)
                        option_2 = 0
                        if first_occurence != -1:
                            option_2 = 1 + memo_solve(p1 + 1, first_occurence + 1)
                        
                        # Return the best option.
                        return max(option_1, option_2)
                            
                    return memo_solve(0, 0)
            ```
            
        - 복잡도 분석
            - 시간: O(M * N^2)
                - 재귀 함수의 input parameter 들은 integer 쌍
                    - text1 index, text2 index
                    - 각각 0~M-1, 0~N-1 사이의 값을 가짐 → M * N pair 존재
                    
                    → 해결해야 하는 subproblem의 개수 O(M*N)
                    
                - subproblem 하나 당 시간 복잡도
                    - 최악의 경우 O(N)- 왜냐면 text1의 current char의 first occurrence 위치를 찾기 위해 text2의 모든 char를 돌아야 하기 때문
                    
                    → 문제 하나당 최악의 경우 O(N)
                    
                
                ⇒ 이 문제를 해결하기 위한 전체 시간은 O(N) * O(M*N) = O(M*N^2)
                
            - 공간: O(M*N)
                - 각 subproblem에 대한 답을 모두 저장해야 하므로 subproblem 개수에 비례해서 저장 공간 필요
                - 각 문제당 필요한 저장 공간은 O(1)
                
                ⇒ O(M*N)
                
    - **Approach 2: Improved Memoization (⭐️⭐️⭐️)**
        - Intuition
            - 문제를 쪼개는 방식이 approach1과 조금 다름
                - approach1에서는 first string은 같든 아니든 무조건 한 칸 전진
                - 두번째 string의 경우
                    - first string의 cur_char가 matching point 아닌 경우에는 현재 위치 그대로 다음 함수에서도 유지되고
                    - matching point인 경우, 두번째 string에서 cur_char가 처음으로 나온 지점 바로 다음 위치가 다음 함수의 parameter로 들어감
                        
                        = cur_char 앞의 string은 실제로 확인했던 아니던 모두 skip 하고 그 다음으로 넘어가는 것과 마찬가지 
                        
            - 이 접근법에서는 일치하면 둘다 한칸 전진, 안 일치하면 둘 중 하나씩만 전진 시켜서 더 큰 쪽을 선택
            - `LCS`(p1, p2)를 구하는 상황
                - 각 string의 첫번째 char이 같지 않으면, 둘 중 하나는 final results에 사용되지 않을 것 (그 문자로부터 나온 line이 optimal solution에 포함되지 않을 것)
                    
                    → max(`LCS`(p1+1, p2), `LCS`(p1, p2+1))
                    
                - 만약 첫번째 letter가 두 string 모두에서 같으면 무조건 optimal에 포함시키는 게 맞음 - 왜냐면 first letter 앞에는 더 원소가 없기 때문에, 확인 안한 채로 미래 옵션에서 제외되는 경우가 없어서.  → 1 + `LCS`(p1+1, p2+1)
        - Algorithm
            - first occurrence 찾는 부분 제외
            - index를 넘겨서 첫번째 letter만 비교하게끔
            
            ```python
            from functools import lru_cache
            class Solution:
                def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                    
                    @lru_cache(maxsize=None)
                    def memo_solve(p1, p2):
                        
                        # Base case: If either string is now empty, we can't match
                        # up anymore characters.
                        if p1 == len(text1) or p2 == len(text2):
                            return 0
                        
                        # Recursive case 1.
                        if text1[p1] == text2[p2]:
                            return 1 + memo_solve(p1 + 1, p2 + 1)
                        
                        # Recursive case 2.
                        else:
                            return max(memo_solve(p1, p2 + 1), memo_solve(p1 + 1, p2))
                        
                    return memo_solve(0, 0)
            ```
            
        - 복잡도 분석
            - 시간: O(M*N)
                - 첫번째 letter만 비교하면 되기 때문에 O(M*N)
            - 공간: O(M*N)
    - **Approach 3: Dynamic Programming**
        - Intuition
            - subproblem들은 natural size ordering을 갖고 있다
                - 가장 큰 input을 다뤄야 하는 subproblem은 우리에게 처음 주어진 문제이고, 거기서부터 한 letter씩 줄여가면서 가장 작은 subproblem, 즉 base case로 내려온다
                - 각 subproblem들은 더 작은 subproblem들의 answer에 따라 정해진다
            - 각 subproblem들은 index 쌍으로 나타내진다
                - 총 M * N개의 subproblem 존재
            - bottom-up에서는 가장 작은 문제부터 시작해서 중간 과정의 모든 답을 저장해나간다
                - 더 큰 subproblem의 답을 구할 때는, 더 작은 subproblem의 답에 의존하게 되는데, 이때는 이미 더 작은 subproblem들의 답이 구해져서 table에 저장된 상태
            - 두 가지 경우 고려
                - 두 string의 첫번째 letter가 일치하는 경우
                    - 1 더해주고 두 인덱스 다 한 칸씩 앞으로
                        
                        ![Untitled](Untitled%207.png)
                        
                - 서로 다른 경우
                    - 둘 중에 하나만 index 당기고, 더 큰쪽의 답을 취한다
                        
                        ![Untitled](Untitled%208.png)
                        
            - 각 column을 역순으로 iterate - 마지막 column에서 시작해서 하나씩 앞으로
        - Algorithm
            
            ```python
            class Solution:
                def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                    
                    # Make a grid of 0's with len(text2) + 1 columns 
                    # and len(text1) + 1 rows.
                    dp_grid = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)]
                    
                    # Iterate up each column, starting from the last one.
                    for col in reversed(range(len(text2))):
                        for row in reversed(range(len(text1))):
                            # If the corresponding characters for this cell are the same...
                            if text2[col] == text1[row]:
                                dp_grid[row][col] = 1 + dp_grid[row + 1][col + 1]
                            # Otherwise they must be different...
                            else:
                                dp_grid[row][col] = max(dp_grid[row + 1][col], dp_grid[row][col + 1])
                    
                    # The original problem's answer is in dp_grid[0][0]. Return it.
                    return dp_grid[0][0]
            ```
            
        - 복잡도 분석
            - 시공간 모두 Approach 2와 동일. 공간 복잡도의 경우 더 obvious - 2D array (M * N)
    - **Approach 4: Dynamic Programming with Space Optimization**
        - Intuition
            - 결국 필요한 계산 결과는 current column과 previous column 두개. 나머지 모든 계산 결과를 다 손에 들고 있을 필요가 없음
                - 그림 보면 바로 오른쪽 칸, 바로 아래 칸 두 개 max를 가져가거나 아님 대각선 칸 하나 값에 1 더한 걸 가져가거나 둘 중 하나
        - Algorithm
            
            ```python
            class Solution:
                def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                    
                    # If text1 doesn't reference the shortest string, swap them.
                    if len(text2) < len(text1):
                        text1, text2 = text2, text1
                    
                    
                    # The previous column starts with all 0's and like before is 1
                    # more than the length of the first word.
                    previous = [0] * (len(text1) + 1)
                    
                    # Iterate up each column, starting from the last one.
                    for col in reversed(range(len(text2))):
                        # Create a new array to represent the current column.
                        current = [0] * (len(text1) + 1)
                        for row in reversed(range(len(text1))):
                            if text2[col] == text1[row]:
                                current[row] = 1 + previous[row + 1]
                            else:
                                current[row] = max(previous[row], current[row + 1])
                        # The current column becomes the previous one.
                        previous = current
                    
                    # The original problem's answer is in previous[0]. Return it.
                    return previous[0]
            ```
            
            - current를 previous와 같은 곳에 만드는 방법
            
            ```python
            class Solution:
                def longestCommonSubsequence(self, text1: str, text2: str) -> int:
                    
                    # If text1 doesn't reference the shortest string, swap them.
                    if len(text2) < len(text1):
                        text1, text2 = text2, text1
                    
                    
                    # The previous and current column starts with all 0's and like 
                    # before is 1 more than the length of the first word.
                    previous = [0] * (len(text1) + 1)
                    current = [0] * (len(text1) + 1)
                    
                    # Iterate up each column, starting from the last one.
                    for col in reversed(range(len(text2))):
                        for row in reversed(range(len(text1))):
                            if text2[col] == text1[row]:
                                current[row] = 1 + previous[row + 1]
                            else:
                                current[row] = max(previous[row], current[row + 1])
                        # The current column becomes the previous one, and vice versa.
                        previous, current = current, previous
                    
                    # The original problem's answer is in previous[0]. Return it.
                    return previous[0]
            ```
            
        - 복잡도 분석
            - 시간은 동일하고 공간만 O(min(M, N) *2) = O(min(M, N))으로 감소