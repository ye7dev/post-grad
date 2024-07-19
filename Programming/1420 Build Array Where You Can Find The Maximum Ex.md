# 1420. Build Array Where You Can Find The Maximum Exactly K Comparisons

Status: done, in progress, with help
Theme: DP
Created time: November 29, 2023 12:40 PM
Last edited time: November 29, 2023 10:31 PM

- 빈출 hard
- 문제 이해
    - target: 탐색 알고리즘이 주어졌을 때 탐색 비용이 k가 되게 하는 array
        - array는 양수로만 구성되어야 하고, n개의 원소가 들어 있다
        - 각 원소는 1과 m 사이의 어떤 값. m도 주어진다.
            
            → maximum element는 m! 
            
    - target array를 서로 다른 몇 가지로 만들 수 있는지 return
    - 주어진 탐색 알고리즘
        - 원소를 맨 앞에서 하나씩 보면서 maximum value를 update 할 때마다, 즉 maximum value보다 큰 원소가 나올 때마다 탐색 비용이 1씩 증가
        
        → 탐색 비용이 k가 되려면 가장 큰 원소보다 작은 애들이 k개 있어야 하는듯? 
        
        예) k = 3일 때 [1, 1, 1, 3, 1, 1]를 가지고 주어진 탐색 알고리즘을 따라가면 
        
        max_val = -1, search_cost = 0
        
        | i | arr[i] | update | search_cost |
        | --- | --- | --- | --- |
        | 0 | 1 | yes (1 > -1) | 1 |
        | 1 | 1 | no (1 ==1) |  |
        | 2 | 1 | no (1 ==1) |  |
        | 3 | 3 | yes | 2 |
        | 4 | 1 | no |  |
        | 5 | 1 | no |  |
        
        ⇒ 최종 search cost = 2 
        
        - 무조건 maximum element보다 작기만 해서는 안되고
            - 제일 처음 -1에서 어떤 값으로 update 하면서 cost + 1
            - 중간값이 있다면 이 값에서 진짜 최대값으로 update 하면서 cost + 1
                - -1에서 바로 최대값으로 update 하면 cost =1로 종료. 아마 base case가 되지 않을까
            - 여기서 더 늘리려면 update 횟수를 늘려야 하고, maximum element보다 작은 숫자들 중 오름차순으로의 순서가 몇번 있어야 함을 의미
            - k =1이 아닌 이상 최소 2에서 시작
        - 그리고 나머지 원소는 무조건 m보다 작아야 함
        - 아 근데 생각해보니까 최대값이 꼭 m이 될 필요는 없네
        - 최소 조건만 만족하면 될 듯
        - 그리고 update 없이 앞에 원소 채우고, update 를 맨 마지막에 하면서 k를 충족하도록 하는 방법도 있다;;
    - 결국 상태에 변화를 줄 수 있는 것들은
        - max_val을 얼마로 할 것인가
        - max_val을 어디에 위치시킬 것인가
    - 필수로 만족해야 하는 건 k를 채워야 - max_val 나오기 전까지 오름차순 pair가 k-1번 나와야 함
    - 원소수는 늘 n개로 고정
    - m과 n과 k의 관계
        - m = 1이면 max_val보다 작은 숫자는 없고, max_val 초기값에서 1로 한번 update 하면서 1의 search cost 만족할 수 있음 → k=1에서만 가능
        - m = 2이면 max_val보다 작은 숫자는 1, 두번 update 가능. k=2
        - m = 3 이면 max_val보다 작은 숫자는 2. 최대 3번 update 가능
        
        → 최대 m번 update 가능. k는 m을 넘을 수 없다 
        
- 과정
    - array에 i번째 원소를 추가할 때
        - search cost < k: i-1번째 원소보다 무조건 큰 값만 가능. 그래야 max_val이 한번 더 update되면서 search cost도 증가
        - search cost = k: 더 이상 search cost가 증가하지 않도록 i-1번째 원소보다 작거나 같은 값만 가능
    - dp table은 n by k로 만든 다음 dp[i][j]는 원소 i까지 추가했을 때 search cost = j를 만족시킬 수 있는 array 생성 방법 수 → 우리가 알고 싶은 건 dp[n][k]
    - base case:
        - j = 0
            - 0임. 왜냐면 array의 최소 원소 값이 1이라 무조건 한번은 update가 될 것이므로
        - i = 0
            - 아무 원소가 없으면 update가 일어날 수 없으므로 k ≥1에 대해서 모두 0인데
            - k =0 경우는 사실상 1이 아닌가? 의미 상 1에 더 가까우니까 dp[0][0] = 1로 사용해 보자
    - transition
        - dp[i][j]
            - = dp[i-1][j] + search cost를 더 늘리지 않는 애들의 수
            - + dp[i-1][j-1] + search cost를 더 늘리는 애들의 수
- 내가 놓치고 가이드에서 도움 받은 것들
    - max_so_far을 두고 여태 array에 넣은 원소 중에 가장 큰 값을 변수로 들고 다님
    - 3차원 dp 되시겠다…ㄷㄷ
    - 여기까지는 짜봤다
        
        ```python
        class Solution:
            def numOfArrays(self, n: int, m: int, k: int) -> int:
                if k > m: return 0 
                if m == 1 and k == 1: return 1 
                mod = 10 ** 9 + 7 
                # row: 0-indexed. 0..n-1 / col: 1-index. 1..k
                dp = [[0] * k for _ in range(n)]
                dp[0][0] = (1, -1) # num_ways, max_so_far 
                for i in range(1, n):
                    dp[i][0] = (0, -1)
                for j in range(1, k):
                    dp[0][j] = (0, -1)
                for i in range(1, n):
                    for cost in range(1, k):
                        # no increase in cost
                        num_ways, max_so_far = dp[i-1][cost]
                        for num in range(1, m+1):
                            if num <= max_so_far:
                                num_ways += 1
                        # increase in cost 
                        other_num_ways, other_max_so_far = dp[i-1][cost-1]
                        for num in range(1, m+1):
                            if num > other_max_so_far:
                                other_num_ways += 1
                        # combine? max? 
                        if num_ways > other_num_ways:
                            dp[i][cost] = (num_ways % mod, max_so_far)
                        else:
                            dp[i][cost] = (other_num_ways % mod, other_max_so_far)
        
                return dp[-1][-1][0]
        ```
        
    - 막힌 부분
        - new_maximum & not new_maximum 중 max를 취야 하는지 더해야 하는지
            - 처음엔 더하는 게 맞다고 생각했는데 그럼 max_so_far을 뭘로 잡아야 하는지 의문
        - base case
- Editorial
    - Top-down DP
        - 문제에서 요구하는 걸 다시 써보면
            - 아래의 조건을 만족하면서 1..m 사이의 원소 n개로 이루어진 array는 모두 몇 개가 있을까?
            - 조건: 왼쪽에서 오른쪽으로 traverse 할 때 k개의 new maximums를 찾는다
        - array buildling 하는 과정에서 고려해야 할 부분들
            1. 지금까지 array에 넣은 element가 총 몇 개인지? 
                
                → index `i` : 우리가 넣을 다음 원소의 자리 
                
            2. 지금까지 만든 array에서 가장 큰 원소의 값
                
                → `max_so_far` 
                
            3. 몇 개의 new maximum을 더 만나야 조건이 충족되는지?
                
                → `remain` : k-num_met_maximums
                
        - 문제를 풀기 위해 구해야 하는 값: `dp(0, 0, k)`
            - 아직 아무 원소도 넣지 않은 상태에서 시작해서, k개의 new maximum을 만나는 상태에까지 이르는 서로 다른 방법의 개수
        - base case
            - `i == n`
                - 이미 array를 다 채웠기 때문에 `remain == 0` 일 때만 valid → return 1. else return 0
            - `remain < 0`
                - max update가 너무 많았기 때문에 바로 return 0
        - transition
            - 이번에 원소를 넣어야 할 자리 `i` 에 넣을 수 있는 두 가지 경우의 수
                1. new maximum
                    - max_so_far..m 중 하나의 숫자 → 총 m-max_so_far +1 개의 숫자
                    - 숫자를 추가하고 나면 i→i+1, max_so_far→ 현재 숫자, remain → remain-1로 update
                    
                    ⇒ `(m-max_so_far+1) * dp(i+1, new_max_so_far, remain-1)`
                    
                2. not new maximum
                    - 1..max_so_far 중 하나의 숫자 → 총 max_so_far-1+1 = max_so_far 개의 숫자
                    - 숫자를 추가하고 나더라도 max_so_far, remain에는 변화가 없다 & i만 i+1로 증가
                        
                        → dp(i+1, max_so_far, remain) 
                        
                    
                    ⇒ `max_so_far * dp(i+1, max_so_far, remain)`
                    
    - Bottom-up DP
        - 3차원 matrix
            - dp[i][max_so_far][remain]
        - base case
            - `i==n` & `remain==0` → valid. cell value : 1
                - remain ≠ 0인 경우는 어차피 matrix 초기값이 0이라서 별도의 설정 필요 없음
            
            → `dp[n][every max so far][0] = 1`
            
        - for loops
            - one nested for loop per state variable → 세 겹의 nested for loop
            - 우리의 return 대상으로부터(`dp[0][0][k]`) 가장 먼 곳에서부터 시작
                - i : n-1 → 0
                - max_so_far: m → 0
                - remain: 0 → k
            - 주의! remain=0에 도달하면 새로운 maximum을 만나는 경우를 전혀 고려해서는 안됨
- Editorial 보고 짠 코드 - top down
    
    ```python
    class Solution:
        def numOfArrays(self, n: int, m: int, k: int) -> int:
            if k > m or k == 0: return 0
            if m == 1 and k == 1: return 1 
            mod = 10 ** 9 + 7
    
            @cache
            def dp(cur_idx, max_so_far, remain):
                if remain < 0: return 0 
                if cur_idx == n:
                    if remain == 0: return 1 
                    else: return 0 # no place but mission incomplete
                
                # not meeting new maximums: 1..max_so_far 
                ans = max_so_far * dp(cur_idx+1, max_so_far, remain) 
    
                # meeting new maximums: max_so_far+1..m
                for num in range(max_so_far+1, m+1):
                    ans += dp(cur_idx+1, num, remain-1)
                
                return ans % mod
            
            return dp(0, 0, k)
    ```
    
- Editorial 보고 짠 코드 - bottom up
    - 엄청 느리긴 하지만 잘 이해하고 짰다
    
    ```python
    class Solution:
        def numOfArrays(self, n: int, m: int, k: int) -> int:
            mod = 10**9+7
            # init triple dp table
            dp = [[[0] * (k+1) for _ in range(m+1)] for _ in range(n+1)]
            # base case
            for max_val in range(1, m+1):
                dp[n][max_val][0] = 1 # array complete & remain zero 
            # transition
            for i in range(n-1, -1, -1):
                for max_val in range(m, -1, -1):
                    for remain in range(k+1):
                        # no new maximum: possible num 1..max_val
                        dp[i][max_val][remain] = max_val * dp[i+1][max_val][remain] % mod
                        # new maximum
                        for num in range(max_val+1, m+1):
                            if remain > 0:
                                dp[i][max_val][remain] += dp[i+1][num][remain-1] % mod
    
            # end
            return dp[0][0][k] % mod
    ```