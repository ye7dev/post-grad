# 1478. Allocate Mailboxes

Created time: May 28, 2024 11:02 AM
Last edited time: May 28, 2024 2:24 PM

- 문제 이해
    
    집들의 위치가 주어질 때, k개의 우편함을 배분해라 
    
    - k는 집의 개수보다 작거나 같다
    
    각 집에서 가장 가까운 우편함의 거리 합이 최소가 되도록 해야 
    
    집은 늘 정렬되어서 주어지는가? 아니, 정렬해야 한다 
    
- scratch
    
    i, …, k-1, k, k+1, …, j
    
    state는 remain opportunity, 
    
    거리는 절댓값으로 계산하고, 어떤 집 위에 놓아도 됨 
    
    근데 집의 거리가 최대 10**4까지 되는데 재귀로 시간 초과 안나려나 모르겠다 
    
    집도 드문드문 있어서 하우스가 되어야 하는데… 
    
    집 별로 거리를 저장해야 할까? 중복이 없다는 걸로 봐서 key로 쓰라고 하는 것도 같은데… 
    
- Trial
    - unhashable type: ‘dict’
        
        ```python
        import copy
        class Solution:
            def minDistance(self, houses: List[int], k: int) -> int:
                memo = {}
                n = len(houses)
                # house index: shortest dist to the nearest mailbox 
                dist = {i: houses[-1]+1 for i in range(n)}
                def recur(left, right, remain, dist):
                    state = (left, right, remain)
                    # check memo? 
                    if state in memo:
                        return memo[state]
                    # base case
                    if remain == 0:
                        return sum(dist.values())
                    # recursive case
                    temp = houses[-1] + 1 
                    for loc in range(houses[left], houses[right]+1):
                        new_dist = dist.deepcopy()
                        for key in range(left, right+1):
                            if new_dist[key] > abs(houses[key]-loc):
                                new_dist[key] = abs(houses[key]-loc)
                            else:
                                break 
                        temp = min(temp, recur(key, right, remain-1, new_dist))
                    memo[state] = temp
                    return memo[state]
                    
                return recur(0, n-1, k, dist)
                
        ```
        
    - bottom-up
        
        ```python
        class Solution:
            def minDistance(self, houses: List[int], k: int) -> int:
                n = len(houses)
                # early return
                if n == k:
                    return 0 
                max_dist = houses[-1] + 1 
                dp = [[[max_dist] * (n+1) for _ in range(n+1)] for _ in range(k+1)]
        
                def get_median(subarr):
                    arr_len = len(subarr)
                    if len(subarr) % 2 == 0:
                        res = (subarr[arr_len//2-1] + subarr[arr_len//2]) // 2 
                    else:
                        res = subarr[arr_len//2]
                    return res 
        
                # base case 
                ## k == 1 -> median of subarray
                for i in range(n):
                    for j in range(i+1, n+1): # exclusive
                        median_value = get_median(houses[i:j])
                        for h in range(i, j):
                            dp[1][i][j] += abs(houses[h]-median_value)
                
                # recursive case
                for num_box in range(2, k+1):
                    for i in range(n):
                        for j in range(i+1, n+1): # exclusive
                            for mid in range(i, j):
                                dp[num_box][i][j] = min(dp[num_box][i][j], dp[1][i][mid] + dp[num_box-1][mid][j])
                
                return dp[k][0][n]
        
        ```
        
- Solution
    - one
        - k개의 연속적인 subarray houses[i:j]에 우편함을 하나씩 배분
            - `[0..i], [i+1..j], ..., [l..n-1]`
            - 어디서 쪼개느냐에 따라 각 그룹별 cost가 달라질 것
        - cost[i][j]
            - house[i:j]의 total travel distance
            - houses[i:j] 범위 중에 우편함을 median에 놓으면 best
            
    - two
        - base case
            - k= 1 → 현재 집 둘 중에 median에 놓는다
            - k=len(houses) → 0
        - recursive case
            - 예) k = 3 → k=2에서 어느 한 쪽을 다시 쪼갬
                - houses = [1, 300, 301, 302], K= 2
                    - [1], [300, 301, 302]
                        - K=3이면 후자를 한 번 더 나누어서
                            
                            [300] [301, 302]
                            
                            [300, 301] [302]
                            
            - dp as careful brute force
                - 가능한 모든 지점에서 partitioning
                - 대신 같은 계산 여러번 하지 않도록 일단 계산한 결과는 저장
            - 요약하면 하나의 그룹을 짓기 위해 그룹 경계 지점을 고르고, 남은 원소들에 대해서는 k-1 개의 그룹을 짓도록 함
        - median 계산법
            - 주어진 subarray의 길이가 홀수냐 짝수냐에 따라 다름
            - 홀수면 n//2 때리면 되고
            - 짝수면 1234에서 2,3의 중간값이 되는데
                - 2,3의 인덱스는 1, 2 = (n//2-1, n//2)
        - median이 어떤 subarray에서 최선의 선택이냐?
            - 예) 1 2 1000
                - 1과 1000의 중간값인 500으로 두면
                    - 499 + 498 + 500 = 1500-3=1497
                - index상 median인 2로 두면
                    - 1 + 0  + 998 = 999
                    - 여기가 훨씬 거리가 짧다
- AC 통과
    - 느리지만 bottom-up
        - recursive case에서 4중 for문이라 엄청 느린듯
        
        ```python
        class Solution:
            def minDistance(self, houses: List[int], k: int) -> int:
                n = len(houses)
                # early return
                if n == k:
                    return 0 
                houses.sort()
                max_dist = houses[-1] + 1 
                dp = [[[max_dist] * (n+1) for _ in range(n+1)] for _ in range(k+1)]
        
                def get_median(subarr):
                    arr_len = len(subarr)
                    if len(subarr) % 2 == 0:
                        res = (subarr[arr_len//2-1] + subarr[arr_len//2]) // 2 
                    else:
                        res = subarr[arr_len//2]
                    return res 
        
                # base case 
                ## k == 1 -> median of subarray
                for i in range(n):
                    for j in range(i+1, n+1): # exclusive
                        dp[1][i][j] = 0  # 초기값 설정
                        median_value = get_median(houses[i:j])
                        for h in range(i, j):
                            dp[1][i][j] += abs(houses[h]-median_value)
                
                # recursive case
                for num_box in range(2, k+1):
                    for i in range(n):
                        for j in range(i+1, n+1): # exclusive
                            for mid in range(i, j):
                                dp[num_box][i][j] = min(dp[num_box][i][j], dp[1][i][mid] + dp[num_box-1][mid][j])
                
                return dp[k][0][n]
        
        ```
        
    - top-down 훨씬 빠름
        
        ```python
        class Solution:
            def minDistance(self, houses: List[int], k: int) -> int:
                n = len(houses)
                # early return
                if n == k:
                    return 0 
                houses.sort()
                memo = {} 
                def get_median(subarr):
                    arr_len = len(subarr)
                    if len(subarr) % 2 == 0:
                        res = (subarr[arr_len//2-1] + subarr[arr_len//2]) // 2 
                    else:
                        res = subarr[arr_len//2]
                    return res 
        
                def recur(remain, i, j):
                    # check memo
                    state = (remain, i, j)
                    if state in memo:
                        return memo[state]
                    # base case 
                    if remain == 1:
                        res = 0
                        med_val = get_median(houses[i:j])
                        for h in range(i, j):
                            res += abs(houses[h]-med_val)
                        memo[state] = res
                        return memo[state]
                    # recursive case
                    res = float('inf')
                    for mid in range(i+1, j):
                        temp = recur(1, i, mid) + recur(remain-1, mid, j)
                        res = min(res, temp)
                    memo[state] = res
                    return memo[state]
                
                return recur(k, 0, n)
        ```