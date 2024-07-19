# 1563. Stone Game V

Created time: June 18, 2024 11:52 AM
Last edited time: June 19, 2024 8:42 PM

- 문제 이해
    - 매 round마다 (번갈아서 차례가 결정되는 것이 아님)
        - Alice는 array(row)를 두 개의 non-empty arrays로 쪼갬
        - Bob은 각 subarray의 합을 구한 뒤 둘 중 더 큰 쪽의 점수를 날린다.
        - 남은 subarray의 합이 Alice의 얻는 점수
        - 만약 두 subarray 합이 동일할 경우, Bob 이 아니라 Alice가 어느 쪽을 날릴지 결정한다
        - 그 다음 round는 남아 있는 subarray를 가지고 진행된다
    - 게임은 돌이 단 하나 남았을 때 끝나고, Alice의 점수는 0에서 시작
    - Alice가 얻을 수 있는 최대 점수를 구하라
- Trial
    - top-down + memo : 10/132
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                memo = {}
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
                def recur(i, j):
                    # check memo
                    state = (i, j)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i >= j:
                        return 0
                    if i + 1 == j:
                        return min(stoneValue[i], stoneValue[j])
                    # recursive case
                    max_gain = -1 
                    for k in range(i, j+1): # i~k-1, k~j
                        subarr1 = prefix_sum[k] - prefix_sum[i]
                        subarr2 = prefix_sum[j+1] - prefix_sum[k]
                        if subarr1 > subarr2:
                            next_run = recur(k, j)
                            cur_gain = subarr2 
                        elif subarr1 < subarr2:
                            next_run = recur(i, k-1)
                            cur_gain = subarr1
                        else:
                            cur_gain = subarr1
                            right = recur(k, j) 
                            left = recur(i, k-1)
                            if left == right:
                                next_run = max(recur(k, j), ecur(i, k-1))
                        max_gain = max(max_gain, cur_gain + next_run)
                    # save memo
                    memo[state] = max_gain
                    return memo[state]
                
                return recur(0, n-1)
                            
        
                
        ```
        
    - top-down + memo: 130/132 (TLE)
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                memo = {}
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
                def recur(i, j):
                    # check memo
                    state = (i, j)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i >= j:
                        return 0
                    # recursive case
                    max_gain = -1 
                    for k in range(i, j+1): # i~k-1, k~j
                        subarr1 = prefix_sum[k] - prefix_sum[i]
                        subarr2 = prefix_sum[j+1] - prefix_sum[k]
                        if subarr1 > subarr2:
                            next_run = recur(k, j)
                            cur_gain = subarr2 
                        elif subarr1 < subarr2:
                            next_run = recur(i, k-1)
                            cur_gain = subarr1
                        else:
                            cur_gain = subarr1
                            right = recur(k, j) 
                            left = recur(i, k-1)
                            next_run = max(recur(k, j), recur(i, k-1))
                        max_gain = max(max_gain, cur_gain + next_run)
                    # save memo
                    memo[state] = max_gain
                    return memo[state]
                
                return recur(0, n-1)
                            
        ```
        
    - bottom-up: 18/132
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
        
                dp = [[0] * n for _ in range(n)]
        
                # base case: i >= j -> 0 (auto covered)
        
                # iterative relation
                for start in range(n-1):
                    for length in range(2, n+1-start):
                        # end - start + 1 = length 
                        # end = length + start - 1 < n
                        # length < n - start + 1 
                        end = start + length - 1
                        for mid in range(start, end+1):
                            # i to k-1
                            left_gain = prefix_sum[mid] - prefix_sum[start]
                            # k to j
                            right_gain = prefix_sum[end+1] - prefix_sum[mid]
                            if left_gain > right_gain:
                                dp[start][end] = max(dp[start][end], right_gain + dp[mid][end]) 
                            elif left_gain < right_gain:
                                dp[start][end] = max(dp[start][end], left_gain + dp[start][mid-1])
                            else:
                                dp[start][end] = max(dp[start][end], left_gain + max(dp[mid][end], dp[start][mid-1]))
                return dp[0][n-1]
        ```
        
    - bottom-up: 126/132 (TLE)
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
        
                dp = [[0] * n for _ in range(n)]
        
                # base case: i >= j -> 0 (auto covered)
        
                # iterative relation
                # for start in range(n-1):
                #     for length in range(2, n+1-start):
                for length in range(1, n):
                    for start in range(n-length):
                        # end - start + 1 = length 
                        # end = length + start - 1 < n
                        # length < n - start + 1 
                        end = start + length
                        for mid in range(start, end):
                            # i to k-1
                            left_gain = prefix_sum[mid+1] - prefix_sum[start]
                            # k to j
                            right_gain = prefix_sum[end+1] - prefix_sum[mid+1]
                            if left_gain > right_gain:
                                dp[start][end] = max(dp[start][end], right_gain + dp[mid+1][end]) 
                            elif left_gain < right_gain:
                                dp[start][end] = max(dp[start][end], left_gain + dp[start][mid])
                            else:
                                dp[start][end] = max(dp[start][end], left_gain + max(dp[mid+1][end], dp[start][mid]))
        
                return dp[0][n-1]
        ```
        
    - bottom-up index fixed: 126/132(TLE)
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
        
                dp = [[0] * n for _ in range(n)]
        
                # base case: i >= j -> 0 (auto covered)
        
                # iterative relation
                for length in range(2, n+1):
                    for start in range(n-length+1):
                        end = start + length - 1
                        # end - start + 1 = length 
                        # end = length + start - 1 < n
                        # length < n - start + 1 
                        for mid in range(start, end):
                            # i to k
                            left_gain = prefix_sum[mid+1] - prefix_sum[start]
                            # k+1 to j
                            right_gain = prefix_sum[end+1] - prefix_sum[mid+1]
                            if left_gain > right_gain:
                                dp[start][end] = max(dp[start][end], right_gain + dp[mid+1][end]) 
                            elif left_gain < right_gain:
                                dp[start][end] = max(dp[start][end], left_gain + dp[start][mid])
                            else:
                                dp[start][end] = max(dp[start][end], left_gain + max(dp[mid+1][end], dp[start][mid]))
        
                return dp[0][n-1]
        ```
        
    - bottom-up + trick: 127/132(TLE)
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
        
                dp = [[0] * n for _ in range(n)]
        
                # base case: i >= j -> 0 (auto covered)
        
                # iterative relation
                # for start in range(n-1):
                #     for length in range(2, n+1-start):
                for length in range(2, n+1):
                    for start in range(n-length+1):
                        end = start + length - 1
                        # end - start + 1 = length 
                        # end = length + start - 1 < n
                        # length < n - start + 1 
                        
                        # special case
                        temp = start
                        while temp < end:
                            if stoneValue[temp] == stoneValue[end]:
                                temp += 1 
                            else:
                                break 
                        if temp == end:
                            cnt = 0
                            l = length
                            while l > 1:
                                l //= 2 
                                cnt += l
                            dp[start][end] = cnt * stoneValue[end]
                            continue 
        
                        for mid in range(start, end):
                            # i to k-1
                            left_gain = prefix_sum[mid+1] - prefix_sum[start]
                            # k to j
                            right_gain = prefix_sum[end+1] - prefix_sum[mid+1]
                            if left_gain > right_gain:
                                dp[start][end] = max(dp[start][end], right_gain + dp[mid+1][end]) 
                            elif left_gain < right_gain:
                                dp[start][end] = max(dp[start][end], left_gain + dp[start][mid])
                            else:
                                dp[start][end] = max(dp[start][end], left_gain + max(dp[mid+1][end], dp[start][mid]))
        
                return dp[0][n-1]
        ```
        
    - top-down + memo+ trick: 132/132(TLE)
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                memo = {}
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
                def recur(i, j):
                    # check memo
                    state = (i, j)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i >= j:
                        return 0
                    # speical case
                    temp = i
                    while temp < j:
                        if stoneValue[temp] == stoneValue[j]:
                            temp += 1 
                        else:
                            break 
                    if temp == j:
                        l = j - i + 1
                        cnt = 0
                        while l > 1:
                            l //= 2
                            cnt += l
                        memo[state] = cnt * stoneValue[j]
                        return memo[state]
                    # recursive case
                    max_gain = -1 
                    for k in range(i, j+1): # i~k-1, k~j
                        subarr1 = prefix_sum[k] - prefix_sum[i]
                        subarr2 = prefix_sum[j+1] - prefix_sum[k]
                        if subarr1 > subarr2:
                            next_run = recur(k, j)
                            cur_gain = subarr2 
                        elif subarr1 < subarr2:
                            next_run = recur(i, k-1)
                            cur_gain = subarr1
                        else:
                            cur_gain = subarr1
                            right = recur(k, j) 
                            left = recur(i, k-1)
                            next_run = max(recur(k, j), recur(i, k-1))
                        max_gain = max(max_gain, cur_gain + next_run)
                    # save memo
                    memo[state] = max_gain
                    return memo[state]
                
                return recur(0, n-1)
                            
        ```
        
    - bottom-up + trick: 127/132 (TLE)
        
        ```python
        class Solution: 
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
        
                dp = [[0] * n for _ in range(n)]
                
                for length in range(2, n+1):
                    for start in range(n-length+1):
                        end = start + length - 1
                        
                        # 특수 케이스
                        temp = start
                        while temp < end and stoneValue[temp] == stoneValue[end]:
                            temp += 1
                        if temp == end:
                            cnt = 0
                            l = length
                            while l > 1:
                                l //= 2
                                cnt += l
                            dp[start][end] = cnt * stoneValue[end]
                            continue
        
                        max_gain = -1 
                        for mid in range(start, end):
                            temp = -1 
                            left_gain = prefix_sum[mid+1] - prefix_sum[start]
                            right_gain = prefix_sum[end+1] - prefix_sum[mid+1]
                            if left_gain > right_gain:
                                temp = right_gain + dp[mid+1][end]
                            elif left_gain < right_gain:
                                temp = left_gain + dp[start][mid]
                            else:
                                temp = left_gain + max(dp[mid+1][end], dp[start][mid])
                            max_gain = max(max_gain, temp)
                        dp[start][end] = max_gain
        
                return dp[0][n-1]
        ```
        
- TLE를 방지하기 위한 trick
    - shortcut for a special case
        - 특정 구간에 있는 모든 원소의 값이 같은 경우
        - 이 구간에서는 O(log N)으로 시간복잡도가 감소
    - base case로 추가
        - 주어진 구간 내의 모든 원소 값이 같으면 원소 길이가 1이 될때까지 2로 나눈 뒤, 몫을 누적으로 더해준다
            - 이렇게 얻은 최종 점수는 이번 한번으로 얻는 점수가 아니라, 해당 구간을 base case hit 할 때까지 쪼개고 쪼갰을 때 얻는 점수
        - 예) [1, 1, 1, 1, 1]
            - alice가 [1], [1, 1, 1, 1]로 쪼개면 bob은 뒤쪽을 날려서 1점만 얻을 수 있음 → 끝
            - alice가 [1, 1], [1, 1, 1]로 쪼개면 bob은 뒤쪽을 날려서 2점을 얻을 수 있음 → [1, 1]을 [1], [1]로 쪼개면 또 다시 반쪽이 날라가서 1점을 얻을 수 있음 ⇒ 총 3점 획득 가능
            - 식으로 나타내면 length = 4-0+1 = 5
                - length // 2 = 2 → cnt = 2
                - length // 2 = 1 → cnt = 3
                - length = 1 이라서 while loop break
- AC 코드
    - top-down + memo+ trick + mid idx 조정
        
        ```python
        class Solution:
            def stoneGameV(self, stoneValue: List[int]) -> int:
                n = len(stoneValue)
                memo = {}
                # prefix sum
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
                def recur(i, j):
                    # check memo
                    state = (i, j)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i >= j:
                        return 0
                    # speical case
                    temp = i
                    while temp < j:
                        if stoneValue[temp] == stoneValue[j]:
                            temp += 1 
                        else:
                            break 
                    if temp == j:
                        l = j - i + 1
                        cnt = 0
                        while l > 1:
                            l //= 2
                            cnt += l
                        memo[state] = cnt * stoneValue[j]
                        return memo[state]
                    # recursive case
                    max_gain = -1 
                    for k in range(i, j): # i~k, k+1~j
                        subarr1 = prefix_sum[k+1] - prefix_sum[i]
                        subarr2 = prefix_sum[j+1] - prefix_sum[k+1]
                        if subarr1 > subarr2:
                            next_run = recur(k+1, j)
                            cur_gain = subarr2 
                        elif subarr1 < subarr2:
                            next_run = recur(i, k)
                            cur_gain = subarr1
                        else:
                            cur_gain = subarr1
                            right = recur(k+1, j) 
                            left = recur(i, k)
                            next_run = max(recur(k+1, j), recur(i, k))
                        max_gain = max(max_gain, cur_gain + next_run)
                    # save memo
                    memo[state] = max_gain
                    return memo[state]
                
                return recur(0, n-1)
                            
        ```
        
- 왜 이 문제에서는 top-down이 더 나은가?
    - pruning state
        - 합이 더 큰 쪽의 interval
    - state definition
        - f[i][j]는 구간 [i, j]에서 얻을 수 있는 최대 점수
            - lf[i][j]는 i에서 시작하여 [i, j] 범위 내의 모든 구간 [i, k] (i <= k <= j)에 대해 f[i][k] + sum[i][k]의 최대값입니다. (i 고정)
                - 왜 lf[i][i]는 0이 아니고 stoneValue[i]인가?
                    - i = m, j = m
                    - f[i][i] = 0
                    - sum[i][i] = stoneValue[i]
                    
                    → lf[i][j] = max(0+stoneValue[i]) = stoneValue[i] 
                    
            - f[i][j]는 j에서 끝나는 [i, j] 범위 내의 모든 구간 [k, j] (i <= k <= j)에 대해 f[k][j] + sum[k][j]의 최대값입니다. (j 고정)
        - sum[i][j]: i to j stoneValue sum (prefix sum)
- 이해가 잘 안가는 솔루션 코드 읽기
    
    ```python
    class Solution:
        def getsum(self, prefix_sum, l, r):
            if l > r:
                return 0
            if l == 0:
                return prefix_sum[r]
            return prefix_sum[r] - prefix_sum[l - 1]
        
        def stoneGameV(self, stoneValue):
            n = len(stoneValue)
            prefix_sum = [0] * n
            for i in range(n):
                if i > 0:
                    prefix_sum[i] += prefix_sum[i - 1]
                prefix_sum[i] += stoneValue[i]
            
            f = [[0] * n for _ in range(n)]
            lf = [[0] * n for _ in range(n)]
            rf = [[0] * n for _ in range(n)]
            
            for i in range(n):
                lf[i][i] = rf[i][i] = stoneValue[i]
            
            for i in range(n - 1, -1, -1):
                for j in range(i + 1, n):
                    segsum = self.getsum(prefix_sum, i, j)
                    l, r = i - 1, j
                    while l < r - 1:
                        mid = (l + r) // 2
                        left = self.getsum(prefix_sum, i, mid)
                        if left * 2 <= segsum:
                            l = mid
                        else:
                            r = mid
                    
                    if l >= i:
                        f[i][j] = max(f[i][j], lf[i][l])
                    
                    rst = l
                    if self.getsum(prefix_sum, i, l) * 2 < segsum:
                        rst += 2
                    else:
                        rst += 1
                    
                    if rst <= j:
                        f[i][j] = max(f[i][j], rf[rst][j])
                    
                    lf[i][j] = max(lf[i][max(i, j - 1)], f[i][j] + segsum)
                    rf[i][j] = max(rf[max(0, i + 1)][j], f[i][j] + segsum)
            
            return f[0][n - 1]
    ```
    
    - 예시 `stoneValue = [3, 2, 4, 1, 5, 6]`
        - n = 6, i = 4, j = 5
        - segsum = 5+6 = 11
        - l = 3, r = 5
            - mid = 4
            - left = 1+5 = 6
                - 6*2 = 12 > 11
                - r = 4
        - l = 3, r = 4
            - r-1 = 3 → while loop break
        - [3, 2, 4, 1] [5, 6]
            - 10 vs. 11
        - l = 3 < i → pass
        - rst = 3
            - i to l = 0 (i > l)
                - prefix_sum[3]-prefix_sum[4-1] = 0 < 11
                - rst += 2 = 5
        - rst = 5 ≤ 5
            - f[4][5] = max(f[4][5], rf[5][5])
        
- 조금 더 내 입맛에 맞게 바꾼 것.
    
    ```python
    class Solution:   
        def stoneGameV(self, stoneValue):
            n = len(stoneValue)
            prefix_sum = [0] * (n+1)
            for i in range(1, n+1):
                prefix_sum[i] = prefix_sum[i-1] + stoneValue[i-1]
            
            f = [[0] * n for _ in range(n)]
            lf = [[0] * n for _ in range(n)]
            rf = [[0] * n for _ in range(n)]
            
            for i in range(n):
                lf[i][i] = rf[i][i] = stoneValue[i]
            
            for i in range(n - 1, -1, -1):
            # for j in range(i + 1, n):
                for length in range(2, n-i+1):
                    j = length + i -1 
                    segsum = prefix_sum[j+1] - prefix_sum[i]
                    
                    l, r = i-1, j
                    while l < r - 1:
                        mid = (l + r) // 2
                        left = prefix_sum[mid+1] - prefix_sum[i]
                        if left * 2 <= segsum:
                            l = mid
                        else:
                            r = mid
                    
                    if l >= i:
    	                f[i][j] = max(f[i][j], lf[i][l])
                    
                    rst = l
                    if (prefix_sum[l+1] - prefix_sum[i]) * 2 < segsum:
                        rst += 2
                    else:
                        rst += 1
                    
                    if rst <= j:
                        f[i][j] = max(f[i][j], rf[rst][j])
                    
                    lf[i][j] = max(lf[i][j - 1], f[i][j] + segsum)
                    rf[i][j] = max(rf[i + 1][j], f[i][j] + segsum)
            
            return f[0][n - 1]
    ```
    
    - 어쨌든 while loop의 목적은 전체 합의 절반보다는 작지만 가장 값이 큰 subarray를 만들기 위한 왼쪽 subarray 경계값 l을 찾는 것
    - while loop에서의 목적은 i..l 구간의 합이 l+1..j 구간의 합보다 작도록 만족시키는 것
        - 근데 [2, 1, 1] 처럼 같게 되는 경우도 있다.
    - rst의 목적은 rst..j의 구간의 합이 i..rst-1보다 작게 하는 것
        - while loop 거치고 나온 l이 원하는 대로 목적을 달성했으면, rst가 l+1될 수 없다. 왜냐면 i..l 구간의 합이 l+1..j 구간의 합보다 작도록 만족시켰기 때문에
            - 따라서 rst는 두 칸을 가야 함
        - 근데 l이 원하는 대로 목적을 달성하지 않아서 i..l 구간의 합이 전체의 절반보다 크거나 같으면 l+l…j는 최소 같거나 작다는 것이므로 rst는 l+1로도 가능
- l = i-1로 설정 안하면 [6, 1] 같은 경우에서 답이 틀리게 나온다
    - i = 0, j = 1
        
        ```python
        while l < r - 1: # l = r-1이면 stop 
          mid = (l + r) // 2
          left = prefix_sum[mid+1] - prefix_sum[i]
          if left * 2 <= segsum:
              l = mid
          else: 
              r = mid
        ```
        
        - 이미 l = 0 < r-1 = 1-1=0을 만족하지 않음
        - 그대로 0, 1로 나옴
- rst ≤j 로 설정 안하면 ‘[9,8,2,4,6,3,5,1,7]’ 와 같은 경우에서 답이 틀리게 나온다
    - rst > j이면 rf에 대한 valid range가 아니라서
    
- n**2 * logn solution 요약
    - lf: 구간에서 얻을 수 있는 최대 점수 + 해당 구간의 subsum
        - start 고정
    - rf: 구간에서 얻을 수 있는 최대 점수 + 해당 구간의 subsum
        - end 고정
    - binary search로 k를 구한다
        - k: i..k 구간의 합이 전체 i..j 범위에서 더 작은 쪽에 속하는 것 중 가장 큰 k
        - alice가 구간에서 얻을 수 있는 가장 큰 left sum을 의미
    - right sum도 구하기 위해 k가 조건 만족하는지 체크하고, 그 바로 다음 칸이나 다다음칸을 체크
    - 이번 구간에 대한 최대 점수를 left sum, right sum 중 더 큰 쪽으로 가져간다
    - 다음 turn을 위해 lf, rf를 업데이트 한다
- [ ]  다음 날 코드 복기