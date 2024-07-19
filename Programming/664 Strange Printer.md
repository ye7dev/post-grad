# 664. Strange Printer

Created time: June 12, 2024 10:49 PM
Last edited time: June 15, 2024 11:03 AM

<aside>
<img src="https://www.notion.so/icons/checkmark_gray.svg" alt="https://www.notion.so/icons/checkmark_gray.svg" width="40px" /> [best code](664%20Strange%20Printer%203725ce0be11a48ff98c2a0976a84614c.md)

</aside>

- 문제 이해
    - string s가 주어질 때, 그것을 프린트하기 위한 최소 turn수를 구하라
        - 같은 문자는 하나의 sequence로 프린트
        - 이미 어떤 문자들이 프린트 되어 있는 상태에서, 새로운 글자는 그 중 어느 자리에서든지 시작해서 끝날 수 있고, 기존에 있던 문자를 덮어버린다
            - 예-’aba’
                - aaa 프린트 해둔 상태에서
                - b 한 글자를 index 1 자리에서 시작하고 끝나게 프린트
                - 기존 index 1에 있던 a는 b로 덮인다
- scratch
    - base case
        - 구간 안의 letter가 한 종류면 1번
        - 구간 길이가 1이면 1번
    - recursive case
        - 따로 따로 프린트
            - min(dp[0, k)) + min(dp[k, len(s)))
                - for k in range(1, len(s)): # len(s)-1까지
        - 덮어서 프린트
            - 덮어서 프린트한다는 것은 어떤 구간 앞뒤로 같은 글자가 오는 것을 의미 - 이조건을 체크해봐야 할 듯
            - 전체 구간을 첫번째 글자로 모두 프린트 : 1
            - 이런 느낌
                - 앞-첫번째 글자
                - 처음으로 다른 글자가 나오면 거기서부터 다음으로 첫번째 글자 나오기 전까지
                - 뒤-첫번째 글자
                - 앞뒤를 따로 따로 프린트 하는 것보다 하나로 프린트 하고 중간 구간에 대해 구하는 게 더 나은 경우가 있을 수있지
                    - aaaa/bc/aaaa 이런 거
                    
- Trial
    - recursive (15/200)
        
        ```python
        class Solution:
            def strangePrinter(self, s: str) -> int:
                def recur(i, j):
                    # base case
                    if j-i == 1:
                        return 1 
                    if j-i == 0:
                        return 0
                    substr = s[i:j]
                    if len(set(substr)) == 1:
                        return 1 
        
                    # recursive case - seperate
                    min_turn = float('inf')
                    for k in range(1, len(substr)):
                        temp = recur(i, i+k) + recur(i+k, j)
                        min_turn = min(min_turn, temp)
                    
                    # recursive case - cover up 
                    k = 1
                    char = substr[0]
                    while substr[k] == substr[0] == substr[j-i-k]:
                        k += 1 
                    cover_up = 1 + recur(i+k, j-k)
        
                    return min(min_turn, cover_up)
                    
                return recur(0, len(s))
        
        ```
        
    - top-down
        
        ```python
        class Solution:
            def strangePrinter(self, s: str) -> int:
                n = len(s)
                def recur(l, r):
                    # base case
                    if l == r:
                        return 0
                    j = l
                    while j < r and s[j] == s[r]:
                        j += 1
                    # base case
                    if j == r-1:
                        return 0
                    # no worries for s[l..j]
                    min_cost = float('inf')
                    for i in range(j, r):
                        middle = recur(j, i)
                        right = recur(i+1, r)
                        min_cost = min(min_cost, middle + right)
                    return min_cost + 1 
                
                return recur(0, n-1)
        ```
        
    - bottom-up
        
        ```python
        class Solution:
            def strangePrinter(self, s: str) -> int:
                n = len(s)
                dp = [[n] * n for _ in range(n)]
        
                # base case
                for i in range(n):
                    # print that one char
                    dp[i][i] = 1
        
                # recursive case - from shorter range to longer one
                for r in range(n-1, -1, -1):
                    for d in range(1, n-2):
                        l = r - d 
                        j = -1 
                        cur_cost = n 
                        for i in range(l, r):
                            if s[i] != s[r] and j == -1:
                                j = i
                            if j != -1:
                                temp = dp[j][i] + dp[i+1][r]
                                cur_cost = min(cur_cost, temp + 1)
                        dp[l][r] = cur_cost 
        
                return dp[0][n-1]
        ```
        
- Editorial
    - state
        - substring s_l..r: s[l:r+1]
        - (c, l, r): substring s_l..r 위에 문자 c를 프린트 하는 작업
            - 여기서 c=s[r]
    - cover up 예시
        - s = `aba`
            - (a, 0, 2)
                - s[0:3] = aba 위에 a를 프린트
                - c = a = s[2]
            - (b, 1, 1)
                - s[1:2] = s[1] 위에 b를 프린트
                - c = b = s[1]
        - s = `leetcode`
            - (e, 0, 7)
                - s[0:8]에 e를 프린트 한다 : eeeeeeee
            - (l, 0, 0)
                - s[0]에 l을 프린트한다: leeeeeee
            - (t, 3, 3)
                - s[3]에 t를 프린트한다: leeteeee
            - (c, 4, 4)
                - s[4]에 c를 프린트한다: leetceee
            - (o, 5, 5)
                - s[5]에 o를 프린트한다: leetcoee
            - (d, 6, 6)
                - s[6]에 d를 프린트한다: leetcode
    - lemma: c=s_r인 (c, l, r) operation 마다 최소 하나의 optimal sequence가 존재한다
        - bad operation을 포함하는 optimal answer를 생각
            
            ![Untitled](Untitled%2051.png)
            
            - [x]  bad operation: c ≠ s_r인 (c, l, r)
            - optimal answer: print turn 숫자가 최소인 sequence
            - (o, 5, 7)에서 c = o ≠ s_r = s[7] = e
            - [x]  Immediately after this operation, the character at the *r*th position is c, but in the end, it must be s_r, meaning that printing c at the rth position was useless.
                - 그림에서 (o, 5, 7)을 하고 나면 leetcooo 이고, 7번째 문자는 o(c)
                - 우리가 만들려는 string에서 s[7] = e
                - 7번째 문자는 결국 e가 되어야 하기 때문에 o로 만든 건 쓸모 없는 거였음
        - [ ]  Thus one can safely replace the operation (c, l, r) with (c, l, r-1).
            - (c, l, r-1)도 c = s_(r-1)을 만족하지 않는 bad operation일 수 있다
            - (o, 5, 7)을 (o, 5, 6)으로 대체하면 leetcooe
                - 그러나 s[6]은 d라서 o로 바꾼 건 여전히 쓸모 없고 bad operation임
            - 한 칸 더 뒤로 가서 (o, 5, 5)로 (o, 5, 7)을 대체하면 leetcoee라서 optimal
            - [ ]  그러나 아직도 replace 한다는 것의 의미를 정확하게 모르겠음
        - sequence에 bad operation이 없을 때까지 (c, l, r)을 (c, l, r-1)로 대체 가능 (iterative process)
            - 끝나고 나면 모든 (c, l, r) operation은 c=s_r을 만족하게 될 것
            - 작업을 다른 것으로 대체하는 건 작업 횟수를 더 늘리진 않는다 → 새로운 sequence도 여전히 optimal 하기 때문에 lemma를 증명 완료
        - lemma의 조건을 만족하는 sequence들 중에서 정답을 찾을 것
        
        - 
    - Top-down w/ memoization
        - 모든 가능한 substirng을 고려 → 최소 operation 숫자를 찾기
        - `solve(l, r)`
            - `t`: s_r 문자로만 구성된 길이 (r-l+1)의 string
            - t → s_l…r로 변환하는 데 필요한 최소 작업의 숫자
            - 예) s = leetcode
                - solve(1, 5): s_l…r = s[1:6] = eetco
                    - eeeee 에서 3글자 바꾸면 되니까 정답은 3.
        - base case
            - 같은 글자로만 구성된 substring
            - s_r로 구성된 길이 (r-l+1)에서 바꿀 것이 없으므로 0
        - state transition
            - `s_l..r` : 최소 서로 다른 두 개의 문자로 구성된 문자열
            - `j` : 아래 두 조건을 만족하는 가장 작은 index(leftmost index)
                1. j ≥ l
                2. s_j ≠ s_r 
                    - s_j: 주어진 범위(s[l:r+1])에서 마지막 글자와 같지 않은 첫번째 글자
                - 그림 예시
                    
                    ![Untitled](Untitled%2052.png)
                    
                    - l=1, r = 7 일 때 s[7]=e.
                        - 주어진 범위에 있는 글자 중 처음으로 e와 다른 글자는 t
                        - index로 따지면 3 → j =3
            - 우리가 하고 싶은 것
                - 같은 문자 s_r로 r-l+1개 반복해 놓은 문자열 ➜ 같은 길이의 input string인 s_l..r
                - s_j ≠ s_r 이므로 현재 string에서 j 번째 자리에 있는 문자를 다른 문자로 프린트해서 덮어야 함
                    - cur_string[l..j-1]은 s_r과 같기 때문에 걱정 안해도 됨
                        - j의 정의에 따라 target[l..j-1]도 s_r과 같다는 점을 확인했기 때문에
                    - 걱정해야 하는 부분은 cur_string[j..r]
            - [j, r] 범위로 들어와서
                - position j에 프린트하는 첫번째 작업
                    - 시작점은 j인데 끝점은 어디? 우선 i라고 하자
                    - 그럼 정의에 따라 (s_i, j, i)
                - i가 고정되었으면
                    - substring s_j..i 자리에 s_i를 print
                    - 그리고 나면 두 개의 하위 문제로 reduce
                        1. j..i는 s_i가 i-j+1 번 반복된 segment 
                            - solve 함수의 정의에 따라 이 segment가 원래 s_j..i로 가려면 `solve(j, i)` 번의 연산이 필요
                        2. 뒷부분 i+1..r는 s_r이 r-(i+1)+1 = r-i-1+1 = r-i번 반복되어 있는 상태 
                            - 원래 l..r 상태는 s_r이 r-l+1번 반복된 상태였는데, i+1부터는 어떤 걸로도 cover up 하지 않았으므로
                            - 여기서 원래 input string s_i+1..r로 가려면 solve의 정의에 따라 `solve(i+1, r)` 번의 연산이 필요
                - 정리하면 고정된 i가 있을 때 1 + `solve(j, i)` + `solve(i+1, r)` 로 l..r을 s_l..r로 만들 수 있다
                    - j는 정의에 따라 찾고
                    - i는 j ≤ i < r  범위에서 돌아가면서 값을 고정시키면서 가장 비용이 작게 나오는 것으로 고정
    - Bottom-up 헷갈리는 인덱스
        - **좁은 범위부터 채워야 하므로 d가 제일 outer for loop**
        
        ```python
        for d in range(1, n+1):
            for l in range(n-d+1):
                r = l + d - 1 
        ```
        
        - d: difference. length. 문자 1개~n개까지 가능
        - l: d=1 일 때 n-1+1 = n → range(n), d=n일 때 n-n+1 = 1 → range(1).
            - d가 길어질 수록 l의 운신의 폭이 좁아짐
        - r은 l, d에 의해 결정
            - l, r이 inclusive 경계라 둘 사이의 길이는 r-l+1
            - r-l+1 = d 니까 r에 대해 정리하면 l + d - 1
        - c.f. 더 직관적인 코드…그러나
            
            ```python
            for l in range(n):
            		for r in range(l, n):
            				d = r - l + 1
            ```
            
            - 우리는 d가 좁은 범위부터 채우고 싶은데, l, r 루프로 돌면 d는 자꾸 커지는 방향으로 간다
        - l이 직관적으로 잘 이해가 안가는데 이렇게 계산해보면 됨
            - r-l+1 = d
            - r = l + d - 1 < n
            - l < n - d + 1
    - Editorial Bottom-up 잘 이해가 안간다
        
        ```python
        class Solution:
            def strangePrinter(self, s: str) -> int:
                n = len(s)
                dp = [[n] * n for _ in range(n)]
        
                # recursive case - from shorter range to longer one
                for d in range(1, n + 1):
                    for l in range(n - d + 1):
                        r = l + d - 1
                        j = -1
                        for i in range(l, r):
                            if s[i] != s[r] and j == -1:
                                j = i
                            if j != -1:
                                # l~j-1 automatically covered
                                temp = dp[j][i] + dp[i+1][r]
                                dp[l][r] = min(dp[l][r], temp + 1)
        
                        # base case
                        if j == -1: # no different letter exists
                            dp[l][r] = 0
        
                return dp[0][n-1] + 1 
        ```
        
- [Bottom-up 또 다른 솔루션](https://leetcode.com/problems/strange-printer/solutions/106795/python-straightforward-dp-with-explanation/?envType=problem-list-v2&envId=50vtr1g3)
    - 영어의 문제일까 아님 글쓴이의 글솜씨의 문제일까…진짜 횡설수설도 이런 횡설수설이 없다
        - state definition
            - `dp(i, j)`
                - s[i:j+1]을 만들기 위해 프린트 해야 하는 최소 횟수
                - [x]  Note that whichever turn creates the final print of S[i], might as well be the first turn, and also there might as well only be one print, since any later prints on interval [i, k] could just be on [i+1, k].
                    - 대충 맨 앞 문자 하나만 한 번의 turn으로 인쇄하고, 뒷부분을 한 구간으로 본다는 의미 같음
            - first print가 i..k 구간라고 하면
                - s[i] == s[k]인 곳만 고려하면 된다
                    - 같은 결과를 얻기 위해 첫번째 turn에 last printed index(k?)까지 인쇄하면 되기 때문에
                        - [x]  because we could instead take our first turn by printing up to the last printed index where S[k] == S[i] to get the same result.
                            - 대충 s[i] == s[k]일 때 i..k 구간 길이 만큼 s[i]를 출력하면 i랑 k 둘다 커버된다는 뜻인 것 같다.
            - s[i] == s[k]인 구간 [i,k]에 대한 프린트를 하려면, [i, k-1] 구간을 프린트하는 만큼의 turn 수가 필요할 것이다.
                - 한 번에 [i, k] 구간을 인쇄하는 것이 따로따로 인쇄하는 것보다 항상 더 좋기 때문(?)
            - 뒷부분 k+1..j도 같은 방식으로 완성
            - 전체적으로는
                - dp(i, k-1) + dp(k+1, j)
                - k == i 일 때는
                    - 1 + dp(i+1, j)도 후보가 될 수 있다
                    - 한번의 print로 s[i] 문자 하나를 처리하고, 뒷부분은 따로 이어서
    - 코드는 깔끔하다
        
        ```python
        def strangePrinter(self, S):
            memo = {}
            def dp(i, j):
        		    # invalid range
                if i > j: return 0
                if (i, j) not in memo:
        		        # 첫글자만 따로 프린트 
                    ans = dp(i+1, j) + 1
                    for k in range(i+1, j+1):
                        if S[k] == S[i]:
                            ans = min(ans, dp(i, k-1) + dp(k+1, j))
                    memo[i, j] = ans
                return memo[i, j]
        
            return dp(0, len(S) - 1)
        ```
        
        - 후보 1: dp(i+1, j) + 1
            - s[i] 한 글자만 인쇄하고 뒷부분을 넘겨 버리기
        - 후보 2: S[k] == S[i] 일 때 dp(i, k-1) + dp(k+1, j)
            - i, i+1, … k-1, k, k+1, … j
            - i..k 길이만큼 s[i]를 프린트하면 우선 i랑 k는 커버되는 셈
                - 근데 왜 1 + dp(i+1, k-1) 이 아니고 dp(i, k-1)인가?
                    - 재귀식 바뀐 버전
                        
                        ```python
                        class Solution:
                            def strangePrinter(self, S):
                                memo = {}
                                def dp(i, j):
                                    # invalid range
                                    if i > j: return 0
                                    if j < len(S)-1 and S[i] == S[j+1]:
                                        return dp(i+1, j)
                                    if (i, j) not in memo:
                                        ans = dp(i+1, j) + 1
                                        for k in range(i+1, j+1):
                                            if S[k] == S[i]:
                                                ans = min(ans, 1 + dp(i+1, k-1) + dp(k+1, j))
                                        memo[i, j] = ans
                                    return memo[i, j]
                        
                                return dp(0, len(S) - 1)
                        ```
                        
- 그 외
    - 나란히 중복된 문자들은 하나로 치환하고 풀어도된다고 함
        - aaabbb면 ab로 두고 풀어도 답이 동일하다
- AC 코드
    - top-down + memo
        
        ```python
        class Solution:
            def strangePrinter(self, s: str) -> int:
                n = len(s)
                memo = {}
                def recur(l, r):
                    # check memo
                    state = (l, r)
                    if state in memo:
                        return memo[state]
                    
                    min_cost = n
                    j = -1
                    
                    for i in range(l, r):
                        # first different letter
                        if s[i] != s[r] and j == -1: # j는 한번 바뀌면 더 이상 바뀌지 않음
                            j = i
                        # 한번 j 값이 정해진 뒤로는 i만 바뀌면서 늘 아래 조건문 hit
                        if j != -1:
                            temp = recur(j, i) + recur(i+1, r)
                            min_cost = min(min_cost, temp)
                    
                    # base case
                    if j == -1: # no different letter from s[r]
                        min_cost = 0 
                    else:
                        min_cost += 1 
        
                    # save memo
                    memo[state] = min_cost 
                    return memo[state]
                
                return recur(0, n-1) + 1
        
        ```
        
    - mine_recursive + memo
        
        ```python
        class Solution:
            def strangePrinter(self, s: str) -> int:
                n = len(s)
                memo = {}
                def recur(l, r):
                    # check memo
                    state = (l, r)
                    if state in memo:
                        return memo[state]
                    # base case
                    if l == r:
                        return 0
                    j = l
                    while j < r and s[j] == s[r]:
                        j += 1
                    # base case
                    if j == r:
                        return 0
                    # no worries for s[l..j]
                    min_cost = float('inf')
                    for i in range(j, r):
                        middle = recur(j, i)
                        right = recur(i+1, r)
                        min_cost = min(min_cost, middle + right)
                    
                    # save memo
                    memo[state] = min_cost + 1 
                    return memo[state]
                
                return recur(0, n-1) +1
        ```
        
- 재귀식 관련 헷갈리는 부분
    
    ```python
    for k in range(i+1, j+1):
        if S[k] == S[i]:
            ans = min(ans, dp(i, k-1) + dp(k+1, j))
    ```
    
    - 질문
        - i에 있는 글자랑 k에 있는 글자가 같으면 한번의 프린트 해당 구간이 커버되고 (+1)
        - dp(i+1, k-1) 로 구간이 좁혀져야 할 것 같은데
        - 1 + dp(i+1, k-1) + dp(k+1, j)로 하면 답이 제대로 안나온다
    - 예상 할 수 있는 이유
        - aaaaa의 경우. i=0, k=4
            - ans = min(ans, 1 + dp(2, 3) + dp(5, 4))
                - dp(5, 4)는 invalid range라서 0.
                - dp(2, 3)은 다시 1 + dp(2, 2) + ~~dp(4, 3)~~
                - dp(2, 2)는 for loop 진입 없이 1
            - 그럼 1 + 1 + 1 = 3이 나온다
            - 근데 정답은 한번만 프린트하면 된다.
    - 답
        - 좁혀진 구간이 직전 단계의 edge 문자와 동일할 경우 거기서 다시 구간을 좁히면서 +1을 할 필요 없는데, 1 + dp(i+1, k-1) + dp(k+1, j)로 재귀식을 짜면 중복으로 1을 더하게 되어서 틀린 답이 나옴
        - 재귀식을 위처럼 바꿨을 때 추가되는 base case
            
            ```python
            if j < len(S)-1 and S[i] == S[j+1]:
                return dp(i+1, j)
            ```
            
            - 제대로 하려면 바깥 뚜껑 (직전 단계의 i,j)랑 이번 edge의 문자가 같으면 1을 더할 필요 없음
            - i, j가 직전 단계의 i+1, k-1이라고 생각해보자
                - j+1 = 전 단계의 k
                - s[i] = s[j+1] 이면 전 단계의 s[i+1] = s[k]라는 것
                    - 전 단계에서 이번 단계로 넘어 오려면 s[i] = s[k] 여야 하는데 s[i+1]도 같다는 것은 이번 단계의 첫 글자는 따로 프린트할 필요 없다는 뜻
                    - 다음 글자를 시작 글자로 하고 넘기면 된다
            - 그렇게 계속 앞글자를 패싱해나가다가
                - i, i+1, …, k-1, k
                - i가 k-1이면 dp(k-1+1,k) = dp(k, k)
                - dp(k+1, k) = 0 값이 쭉 윗단계로 return
    - 원래 재귀식을 다시 보면
        - dp(i, k-1)
            - s[i]랑 s[k]니까 k는 i를 프린트하면서 해결된다고 제쳐 놓고
            - dp[i, k-2], … dp[i, i+1], dp[i, i], dp[i+1, i]+1 = 1로 return