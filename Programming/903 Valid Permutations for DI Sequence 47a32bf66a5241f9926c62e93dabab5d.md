# 903. Valid Permutations for DI Sequence

Created time: June 3, 2024 2:02 PM
Last edited time: June 11, 2024 1:26 PM

- 문제 이해
    
    input: string s 
    
    - 각 char는 D나 I
    - s의 길이는 n. 0~n까지 n+1개의 정수에 대해 permutation을 했을 때, s[i] 글자에 따라 규칙이 지켜지는지 확인
        - s가 가질 수 있는 마지막 index는 n-1이지만, 규칙에서는 i+1 자리의 글자와 비교하므로…
    - 예: s = did
        - s[0] = d → perm[0] > perm[1]
        - s[1] = i → perm[1] < perm[2]
        - s[2] = d → perm[2] > perm[3]
        - 4 * 3 * 2 *
- scratch
    
    index 하나 당 자기보다 큰 숫자, 작은 숫자를 세어두는 게 좋을까?
    
- Trial
    - top-down
        
        ```python
        class Solution:
            def numPermsDISequence(self, s: str) -> int:
                n = len(s)
                mod = 10 ** 9 + 7
                memo = {}
                def recur(i, num):
                    # check memo
                    state = (i, num)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i == n:
                        return 1
                    # recursive case
                    num_way = 0
                    if s[i] == 'I':
                        for next_num in range(num+1, n+1):
                            num_way += recur(i+1, next_num)
                    else:
                        for next_num in range(num):
                            num_way += recur(i+1, next_num)
                    # save memo
                    memo[state] = num_way % mod 
                    return memo[state]
                
                ans = 0
                for i in range(n):
                    ans += recur(0, i)
                ans %= mod 
                print(memo)
                return ans
        
                             
                    
        ```
        
    - top-down: MLE (68/83)
        
        ```python
        class Solution:
            def numPermsDISequence(self, s: str) -> int:
                n = len(s)
                mod = 10 ** 9 + 7
                memo = {}
                def recur(indices):
                    # check memo
                    state = tuple(indices)
                    if state in memo:
                        return memo[state]
                    # base case
                    if len(indices) == n+1:
                        return 1
                    # recursive case
                    num_way = 0
                    last_perm = indices[-1]
                    cur_idx = len(indices)-1
                    if s[cur_idx] == 'I':
                        for next_num in range(last_perm+1, n+1):
                            if next_num in indices:
                                continue
                            num_way += recur(indices + [next_num])
                    else:
                        for next_num in range(last_perm):
                            if next_num in indices:
                                continue
                            num_way += recur(indices + [next_num])
                    # save memo
                    memo[state] = num_way % mod 
                    return memo[state]
                
                ans = 0
                for i in range(n+1):
                    ans += recur([i])
                ans %= mod 
                return ans
        
                             
                    
        ```
        
    - bottom-up
        
        ```python
        class Solution:
            def numPermsDISequence(self, s: str) -> int:
                n = len(s)
                mod = 10 ** 9 + 7
                dp = [[0] * (n+1) for _ in range(n+1)]
                # base case - num_unused: n+1. each and every index 
                for j in range(n+1):
                    dp[0][j] = 1 
                # state transition - looking backward 
                for i in range(1, n+1):
                    # num_unused: n+1 - (i+1) = n-i
                    # 지금 붙이려는 숫자까지 합치면 n-i+1 개. j의 index는 0~n-i까지 가능      
                    if s[i-1] == 'I':
                        for j in range(n-i+1): 
                            num_ways = 0
                            for k in range(j): # n-i+1 개 중 0~j-1번째까지가 기여 가능 
                                num_ways += dp[i-1][k]
                            dp[i][j] = (num_ways) % mod
                    else:
                        # n-i+1개 중 j+1부터 n-i까지 기여 가능 
                        for j in range(n-i+1):
                            num_ways = 0
                            for k in range(j+1, n-i+1):
                                num_ways += dp[i-1][k]
                            dp[i][j] = (num_ways) % mod
                print(dp)
                return dp[n][0]
                            
        
        ```
        
    - bottom-up fail
        
        ```python
        class Solution:
                def numPermsDISequence(self, s: str) -> int:
                    MOD = 10**9 + 7
                    n = len(s)
                    dp = [[0] * (n+1) for _ in range(n+1)]
        
                    # base case
                    for j in range(n+1): # 0~n
                        dp[0][j] = 1 # j itself 
        
                    # state transition
                    for i in range(1, n+1): # 1~n
                        # num available: n+1-(i+1) = n-i
                        for j in range(n-i):
                            if s[i] == 'D':
                                for k in range(j+1, n-i):
                                    dp[i][j] = (dp[i][j] + dp[i-1][k]) % MOD
                            else:
                                for k in range(j+1):
                                    dp[i][j] = (dp[i][j] + dp[i-1][k]) % MOD
        
                    return dp[n][0]
        
        ```
        
- 이해하기 위한 노력들
    - solution1 (🤷‍♀️)
        - dp state
            - dp[i][j]: 첫 i+1개의 숫자에 대해 가능한 perm 개수
                - 사용되지 않은 숫자들 중에 i+1번째 수는 j+1번째로 작은 숫자
            - 예) dp[3][0]
                - 3021, 2031, 1032, 3120, 2130
                - i+1번째 = 4번째 숫자는 각각 1, 1, 2, 0, 0
                - j+1번째 = 1번째
                - 302까지 와서 안 쓰인 숫자는 1. 당연히 가장 작은 숫자도 1
            - 예) dp[2][1]
                - 31까지 와서 아직 안 쓰인 숫자는 0,2
                    - 이 중 2번째로 작은 숫자는 2
                    - 따라서 3,1,2은 dp[2][1]의 경우에 들어감
        - base case
            - dp[0][j]: 아직 숫자가 아무것도 없기 때문에 j에 뭐가 와도 1
                - 예) dp[0][3]
                    - 사용되지 않은 숫자들 중에 i+1 = 1, 첫번째 수는 3+1=4번째로 작은 숫자
                    - 가장 작은 건 첫번째로 작은 숫자니까, 4번째로 작은 수는 가장 큰 수를 의미 = 3만 있는 경우를 의미
        - recurrence relation
            - dp[i][j]
                - 이번에 붙이는 숫자까지 해서 i+1개의 길이가 됨
                - 처음 함수 진입했을 때는 i개까지 있다는 뜻
                - 증가, 감소의 기준은 s[i]
                - 이번에 붙이는 숫자가 사용 안된 n+1-i개 중에 j
            
    - solution2 (🤷‍♀️)
        - state definition: dp[i][j]
            - i: perm에서 지금 다루는 index
            - j: 현재 숫자 + 아직 사용 안한 숫자들을 정렬 했을 때 현재 숫자의 index
            - 예-dp[0][3]
                - 아직 사용 안한 숫자가 총 n+1 = 0, 1, 2, 3을 정렬 했을 때 index=3인 숫자는 3
        - return state
            - dp[n][0]
                - 0~n 중 마지막 자리를 다루고 있고
                - 숫자를 이미 다 써서 남은 숫자가 0개라 가능한 index는 0밖에 없음
        - base case
            - dp[0][j]
                - 0~n 중 첫번째 자리를 다루고 있고
                - 숫자를 아직 하나도 안 썼기 때문에 남은 숫자가 n개고, 여기서 j번째 숫자는 정해져 있음
        - state transition
            - 감소하는 경우
                - looking forward
                    - i+1개의 숫자를 사용했고, 남은 숫자는 n+1-i-1 = n-i
                        - 예) dp[0][3]
                            - 1개의 숫자를 사용했고, 남은 숫자는 3개.
                    - n-i랑 현재 숫자랑 합친 뒤 정렬하면 현재 숫자가 j번째 위치
                        - 남은 숫자랑 현재 숫자랑 합친 뒤 정렬하면 현재 숫자 3이 3번째 위치
                    - 현재 숫자보다 더 작은 수를 원하면 0~j-1개가 가능
                        - 0, 1, 2 가능
                    - 현재 숫자보다 더 큰 수를 원하면 j+1~n-i개가 가능
                        - 3+1 = 4
                        - 4-1 = 3
                        - 범위 invalid
                    
                    → dp[0][3]은 dp[1][0], dp[1][1], dp[1][2]에 기여할 수 있음  
                    
                    → 일반화 하면 dp[i][j]는 dp[i+1][0]~dp[i+1][j-1]에 기여할 수 있음 
                    
                - looking backward
                    - dp[1][0]은
                        - dp[0][1], dp[0][2], dp[0][3]으로부터 기여를 받을 수 있음
            - 증가하는 경우
                - looking forward
                    - dp[0][2]
                        - 현재 숫자랑 남은 거 합치니까 현재 숫자 인덱스가 2
                        - 이는 dp[1][3], dp[1][4]에 기여할 수 있다
                - looking backward
                    - dp[2][3]
                        - 현재 숫자랑 남은 거 합치니까 현재 숫자 인덱스가3
                        - dp[1][0], dp[1][1], dp[1][2]로부터 기여 받을 수 있음
            - sol2에서 이해가 안 갔던 부분
                - 예-dp[0][3]
                    - 아직 사용 안한 숫자가 총 n+1 = 0, 1, 2, 3을 정렬 했을 때 index=3인 숫자는 3
                - n-i랑 현재 숫자랑 합친 뒤 정렬하면 현재 숫자가 j번째 위치
                    - 남은 숫자랑 현재 숫자랑 합친 뒤 정렬하면 현재 숫자 3이 3번째 위치
                - 현재 숫자보다 더 작은 수를 원하면 0~j-1개가 가능
                    - 0, 1, 2 가능
                    - 현재 숫자랑 같은 순위를 원할 때도 가능
                - 현재 숫자보다 더 큰 수를 원하면 j+1~n-i개가 가능
                    - 3+1 = 4
                    - 4-1 = 3
                    - 범위 invalid
    - solution3
        - state definition: 0~i까지 perm 할 때 마지막 수가 j 이면서 valid perm인 경우의 수
        
        1032 마지막 수 2를 기준으로 increasing은 exclusive 
        
        1032로 다음 step에 기여할 수 있는 방안…~ 
        
        <decreasing> 
        
        1032 → 2보다 크거나 같은 수에 모두 1을 더하고, 마지막에 2를 붙이기 
        
        10432 
        
        1032→ 1보다 크거나 같은 수에 모두 1을 더하고, 마지막에 1을 붙이기
        
        20431
        
        ---
        
        <increasing>
        
        1032→ 3보다 크거나 같은 수에 모두 1을 더하고, 마지막에 3을 붙이기 
        
        10423 
        
        1032 → 4보다 크거나 같은 수에 모두 1을 더하고, 마지막에 4를 붙이기
        
        10324 
        
        ---
        
    - 문제 정의에 따르면 다음 index는 strictly increasing/decreasing. sol2는 이 부분을 제대로 설명하지 못하는 듯
        - 그래프를 보면 increasing 하는 same j에 기여하긴 함
            
            ![Untitled](Untitled%2054.png)
            
            - state definition: dp[i][j]
                - i: perm에서 지금 다루는 index
                - j: 현재 숫자 + 아직 사용 안한 숫자들을 정렬 했을 때 현재 숫자의 index
            - 예를 들어 dp[1][0] → dp[2][0]
                - 세번째로 올 숫자를 붙이려고 하는데, 이 숫자가 아직 사용 안한 숫자들이랑 합쳤을 때 가장 작은 숫자여야 함
                - dp[1][0]에서 쓰고 사용 안한 숫자들 중 가장 작은 걸 붙이면 됨
                    - 예) 10 → 아직 사용 안한 2,3 중 가장 작은 2를 붙인다
                    - 예) 20 → 아직 사용 안한 1, 3 중 가장 작은 1을 붙인다
            - increasing case의 경우
                - dp[1][0] → dp[2][1]
                    - 세번째로 올 숫자를 붙이려고 하는데, 이 숫자와 아직 사용 안한 숫자들이랑 합쳤을 때 두번째로 작은 값이어야 함
                        
                        = 두번째까지 붙인 상태에서 남은 숫자들 중 두번째로 작은 값이어야 함 
                        
                    - 예) 10 → 아직 안 붙인 숫자들은 2, 3 → 이 중 두번째로 작은 값은 3
            - 결국 dp[i][j]는 i-1 인덱스까지 만든 상태에서
                - 남은 숫자들을 정렬했을 때 j index에 위치한 값을 가져옴
                - 이게 앞 state랑 무슨 관련이냐
                - 앞에서 숫자를 몇개까지 썼는지에 따라 남은 숫자 개수가 달라지고, 그 개수가 j보다 작으면 원하는 시나리오가 없음
                - 숫자는 총 0~n, n+1개
                - N-i+1개
                
    - 다시 정리
        - 쓸 수 있는 숫자는 n+1-i개
            - 원래 쓸 수 있는 숫자는 n+1이고, 우리는 index 상으로 i-1까지 채운 상태에서 i번째 자리의 숫자를 채우려고 함
            - 근데 index +1이 실제로 사용한 숫자 개수이기 때문에
            - n+1 - ((i-1) +1) 하면 결국 n+1-i가 되는 것
            - 이걸 다시 index로 나타내면 n+1-i-1 = n-i
        - j는 인덱스이고 j를 기준으로 `0~(j-1)`, `j`,  `(j+1)~(n-i)` 세 부분이 존재
            - 만약 다음 index가 decreasing이어야 하면
                - 이전이 3이었다면 0, 1, 2가 가능
                    - dp[i-1][3]이면 i-1까지 채웠을 때 마지막 숫자가 남은 숫자들 중 3번째로 큰 숫자니까
                - 반대로 보면 dp[i][2]의 입장에서는 dp[i-1][3]부터 d[i-1][n-i]까지 모든 숫자가 기여할 수 있음
            - 만약 다음 index가 increasing이어야 하면
                - 이전이 0이었다면 dp[i-1][0]은 dp[i][1]~dp[i][n-i]에 모두 기여 가능
                - 반대로 보면 dp[i][2]의 입장에서는 dp[i-1][0]~dp[i-1][1]까지의 모든 숫자가 기여 가능
                - 여기서 중요한 점은 dp[i-1][2]도 기여 가능하다는 것
                    - 더 쉬운 예로 보면 dp[i-1][0]과 dp[i][0]의 관계를 보면
                        - dp[i-1][0]까지 채우고 남은 숫자 중에 제일 처음에 오는 게 dp[i][0]
                        - dp[i-1][0]을 채우던 시절에는 두번째로 오는 숫자 였겠지
                    - i-2까지 채우고 난 상황에서 남은 숫자를 정렬했을 때 인덱스가 0, 1, 2, …, n-i+1 이렇게 있다고 하면
                        - index 2의 숫자를 dp[i-1][2] 채우는 데 사용하고 나면
                        - 0, 1, 3, …, n-i+1 이렇게 있음. 총 개수는 n-i+1개 임
                        - 숫자를 이미 하나 썼기 때문에 재정렬 하면 0, 1, 2, …, n-i 이렇게 됨
                        - 그래서 현재 2 자리에 있는 숫자도 직전에는 3 자리에 있었고, 아까 채운 dp[i-1][2]보다 큰 숫자이기 때문에 dp[i][2]에 들어올 수 있음
        - 그래서 다시 state를 정의하면
            - dp[i][j]: i-1까지 채우고 난 상태에서, 남은 숫자를 재정렬했을 때 이번 substring이 D이면 j보다 작은 k들로부터 dp[i-1][k] 기여를 받고, I이면 j와 같거나 그보다 큰 k들 dp[i-1][k]로부터 기여를 받는다
            - 숫자를 쓰고, 남은 숫자를 재정렬했을 때 index 상태를 생각하는 게 핵심
            - 초기에는 D나 I가 없음
                - i가 0부터 시작하고 `s[i] == 'D'`, then `perm[i] > perm[i + 1]`
                - perm[0] > perm[1] 이렇게 시작
            - base case의 경우
                - dp[0][j]: 아무것도 안 채운 상태에서 남아 있는 0~n까지 총 n+1개의 숫자를 정렬했을 때, j번째 오는 숫자가 들어감
                - [ ]  base case랑 state transition이랑 의미가 잘 안 이어짐
            
    - [solution2 다시 시도](https://leetcode.com/problems/valid-permutations-for-di-sequence/solutions/715588/How-to-define-the-DP-states-(with-clear-picture-explanation)/)
        - dp [i][j] 정의
            - lee215
                - dp[i][j]: i+1개 숫자를 사용해서 얻을 수 있는 valid permutation 개수
                    - i+1: 현재까지 채운 permutation array의 숫자 총 개수. 사용한 총 숫자 개수. 마지막으로 추가한 숫자의 index + 1
                    - j+1: 사용하지 않은 n+1-(i+1) = n-i개 숫자 중에 j+1번째로 작은 숫자가 array에서 i+1번째 숫자. 오름차순 정렬에서 j+1번째 위치. index로 따지면 j번째 오는 숫자
                - dp[0][3]: 첫번째 숫자가 사용되지 않은 숫자(0~4) 중 네번째로 작은 숫자인 경우. 1, 2, 3, 4 중 네번째로 작은 숫자는 4
                    
                    ![Untitled](Untitled%2055.png)
                    
            - i: 숫자 인덱스(?)
            - j: 현재 숫자 + 아직 사용하지 않은 숫자들을 정렬했을 때 현재 숫자의 index
                - 이 세 state는 정렬 후 인덱스로 표현하면 모두 같다
                    
                    ```python
                    0, 1, 2   ->   0, 1, 2
                    1, 2, 3   ->   0, 1, 2
                    1, 2, 4   ->   0, 1, 2
                    ```
                    
- ❤️‍🔥 solution1 다시 보기
    - state definition
        - dp [i][j] 정의
            - lee215
                - dp[i][j]: i+1개 숫자를 사용해서 얻을 수 있는 valid permutation 개수
                    - chatgpt는 ‘i개의 문자를 처리한 후, j번째 위치에 올 수 있는 가능한 순열의 수’로 정의
                    - i+1: 현재까지 채운 permutation array의 숫자 총 개수. 사용한 총 숫자 개수. 마지막으로 추가한 숫자의 index + 1
                    - j+1: 사용하지 않은 n+1-(i+1) = n-i개 숫자 중에 j+1번째로 작은 숫자가 array에서 i+1번째 숫자. 오름차순 정렬에서 j+1번째 위치. index로 따지면 j번째 오는 숫자
                - dp[0][3]: 첫번째 숫자가 사용되지 않은 숫자(0~4) 중 네번째로 작은 숫자인 경우. 1, 2, 3, 4 중 네번째로 작은 숫자는 4
                    
                    ![Untitled](Untitled%2055.png)
                    
    - state transition
        - dp[i] → dp[i+1] 만들기
            - s[i] = I
                - dp[i+1][j]에 j와 같거나 그보다 작은 모든 k에 대해 dp[i][k]가 기여
                - k가 없이 코드를 쓰면
                    
                    ```python
                    for i in range(n):
                        cur = []
                        for j in range(n - i):
                            cur.append(j)
                            print(f'i: {i+1}, j:{j}, contributors:{i, cur}')
                    ```
                    
                - 결과
                    
                    ```python
                    i: 1, j:0, contributors:(0, [0])
                    i: 1, j:1, contributors:(0, [0, 1])
                    i: 1, j:2, contributors:(0, [0, 1, 2])
                    i: 1, j:3, contributors:(0, [0, 1, 2, 3])
                    i: 2, j:0, contributors:(1, [0])
                    i: 2, j:1, contributors:(1, [0, 1])
                    i: 2, j:2, contributors:(1, [0, 1, 2])
                    i: 3, j:0, contributors:(2, [0])
                    i: 3, j:1, contributors:(2, [0, 1])
                    i: 4, j:0, contributors:(3, [0])
                    ```
                    
            - s[i] = D
                - dp[i+1][j]에 j보다 큰 모든 k에 대해 dp[i][k]가 기여
                - k 없이 코드를 쓰면
                    
                    ```python
                    for i in range(n):
                        cur = []
                        for j in range(n - i - 1, -1, -1):
                            cur.append(j+1)
                            print(f'i: {i+1}, j:{j}, contributors:{i, cur}')
                    ```
                    
                - 결과
                    
                    ```python
                    i: 1, j:3, contributors:(0, [4])
                    i: 1, j:2, contributors:(0, [4, 3])
                    i: 1, j:1, contributors:(0, [4, 3, 2])
                    i: 1, j:0, contributors:(0, [4, 3, 2, 1])
                    i: 2, j:2, contributors:(1, [3])
                    i: 2, j:1, contributors:(1, [3, 2])
                    i: 2, j:0, contributors:(1, [3, 2, 1])
                    i: 3, j:1, contributors:(2, [2])
                    i: 3, j:0, contributors:(2, [2, 1])
                    i: 4, j:0, contributors:(3, [1])
                    ```
                    
                - 직관적으로 잘 이해가 안가서 그림으로 보면
                    
                    0     1      2      3      4
                    
                             ⬅︎     `j`     `j+1` [4]
                    
                    ⬅︎     `j`    `j+1`           [4, 3]
                    
                    ⬅︎   `j`   `j+1`                    [4, 3, 2]
                    
                
                     `j`  `j+1`                            [4, 3, 2, 1]
                
                - 한번의 iteration으로 현재 j 기준 j보다 큰 원소를 모두 담을 수 있게 됨
- AC 코드
    
    ```python
    class Solution:
            def numPermsDISequence(self, s: str) -> int:
                MOD = 10**9 + 7
                n = len(s)
                dp = [[0] * (n+1) for _ in range(n+1)]
    
                # base case
                for j in range(n+1): # 0~n
                    dp[0][j] = 1 # j itself 
    
                # state transition
                for i in range(n): # dp[i] -> dp[i+1]
                    if s[i] == 'I':
                        cur = 0 
                        for j in range(n-i):
                            cur = (cur + dp[i][j]) % MOD
                            dp[i+1][j] = cur
                    else:
                        cur = 0
                        for j in range(n-i-1, -1, -1):
                            cur = (cur + dp[i][j+1]) % MOD
                            dp[i+1][j] = cur
                return dp[n][0]
    ```
    
- 요약
    - state definition
        - i개의 숫자를 이미 채운 상태를 바탕으로, 뒤에 어떤 숫자를 붙여서 길이 i+1의 valid permutation을 만들 수 있는 경우의 수를 구하는 것
        - dp[i+1]들 중 dp[i+1][j]는 마지막에 붙인 i+1번째 숫자가 붙이기 전 남은 숫자들 중에 j번째에 위치할 때의 valid permutation 개수를 의미
        - i는 이번에 붙인 숫자의 특성(인덱스)를 가리키고, j는 붙이기 전 정렬된 상태에서의 순서를 가리키므로 헷갈림
    - return state
        - dp[n][0]
            - 0~n까지 전체 숫자 개수는 n+1개. index는 0으로 시작하므로 모든 숫자를 다 썼을 때 수열에서 마지막 자리의 index는 n
            - nth index에 오는 숫자는 그냥 남는 거 붙이는 거였음
                - n-1th까지 채우고 남은 1개 중에 가장 앞에 있는 숫자이므로 0번째 위치
    - base case
        - dp[0][j]
            - 아직 채운 숫자가 없어서 이번에 처음으로 붙일 숫자가 n+1개의 전체 숫자 중 j번째에 위치하는 경우의 수
            - 정렬된 그대로 j번째 숫자를 하나 뽑아오는게 유일한 경우
            - j는 0~n, 경우의 수는 모두 1
    - state transition
        - i는 0~n-1
            - 왜냐면 s의 길이가 n이니까
            - dp[0][j]는 이미 채웠지만, 점화식에서 우리가 새로 채우는 대상은 dp[i+1][j]라서 사실상 dp[1][j]~dp[n][j]를 채우는 것임
        - dp[i]까지 왔으면 i+1개의 숫자를 사용한 상태.
            - 전체 숫자는 0~n n+1개인데 i+1개 사용했으므로 남은 숫자는 n-i개
        - s[i] = I → perm[i] < perm[i+1]
            - 마지막에 붙일 숫자가 직전 숫자보다 커야 함
            - 이번에 붙일 숫자가 크려면, 직전 숫자는 자기보다 큰 수를 가진 수여야 함
                - 남은 숫자 n-i개 중에 이번 숫자가 제일 마지막에 있는 거면 정렬된 인덱스 기준 n-i-1
                    - 0부터 시작해서 n-i-2까지 모두 가능
                - 남은 숫자 n-i개 중에 이번 숫자가 두번째에 있는 거면 정렬된 인덱스 기준 1
                    - 0만 가능
            - 근데 여기서 주의해야 할 점은 이번에 붙일 숫자랑 같은 자리에 있어도 됨
                - 그니까 dp[i-1]까지 채우고 난 상태에서 0, 1, 2, … , n-i+1의 index를 가진 정렬된 숫자들이 있을 때 여기서 j번째 숫자를 빼서 i에 채웠다고 하면
                - 남은 상태는 0, 1, 2, …, j-1, j+1, …, n-i+1
                    - 이걸 다시 재정렬 하면 0, 1, 2, …, j-1, j, …, n-i
                    - i까지 채운 상태에서 j번째에 위치한 숫자는 여전히 i에 들어간 숫자보다 큰 숫자임
                    - 우리가 여기서 j번째 숫자를 가져다가 i+1위치에 채워도 s[i]=I 규칙을 준수하게 됨
                    - 따라서 dp[i][j]까지 dp[i+1][j]에 기여한다
                - 다시 쓰면
                    - 과거 0, 1, 2, …, j-1, j, j+1, …, n-i+1
                    - 현재 0, 1, 2, …, j-1, ,  j, …, n-i
                    - 현재 j 기준으로 j보다 작은 수는 과거 0부터 j까지
            - 코드 상으로는 제일 앞에서부터 push 하고 순방향으로 진행하면 됨
                - 어차피 j 자체도 포함되니까
        - s[i] = D → perm[i] > perm[i+1]
            - 직전에 채운 숫자보다 작은 숫자가 있어야 함
            - 지금 채우려는 숫자 j보다 strictly 다 커야 함
                - 과거 0, 1, 2, …, j-1, j, j+1, …, n-i+1
                - 현재 0, 1, 2, …, j-1, j, …, n-i
                - 현재 j기준으로 j보다 작은 큰 수는 j+1, …, n-i+1
            - 코드 상으로 보면 자기보다 하나 큰 수 j+1을 push 하면서 역방향으로 움직이면, 모든 j에서 자기보다 큰 원소들을 구할 수 있음