# 1547. Minimum Cost to Cut a Stick

Created time: May 28, 2024 2:26 PM
Last edited time: May 29, 2024 6:00 PM

- 문제 이해
    
    주어진 나무 막대를 n개로 잘라라. label은 0~n. 
    
    자르는 지점이 주어져 있음. 자르는 순서는 마음 대로 
    
    한 번 자르는 비용은 잘리는 막대의 길이 
    
    - 예: `n = 7, cuts = [1,3,4,5]`
        - 3에서 한번 자르면 7
        - 1에서 한번 자르면 3
        - 5에서 한번 자르면 4
        - 4에서 한번 자르면 2
        
        ⇒ 총 커팅 비용은 16
        
    
    전체 커팅 비용 최소 값을 구하라 
    
- scratch
    
    for cut in cuts:
    
    cost(before_cut) + cost(after_cut)
    
    현재 subarray에서 컷해야 하는 지점이 하나 밖에 없으면 그대로 그 subarray 길이 return 
    
    여기도 정렬이 필요한가?
    
    뭔가 divide and conquer 생각난다 
    
- Trial
    - Top-down
        - index check를 다시 해볼 것
        
        ```python
        class Solution:
            def minCost(self, n: int, cuts: List[int]) -> int:
                # early return 
                if len(cuts) == 1:
                    return n 
                memo = {}
                cuts.sort()
                def recur(i, j):
                    # check memo
                    state = (i, j)
                    if state in memo:
                        return memo[state]
                    # check base case
                    if j == i+1:
                        return 1 
                    if i == j:
                        return 0
                    m = i+1
                    while m < j:
                        if m in cuts:
                            break 
                        m += 1
                    if m == j:
                        memo[state] = j-i
                        return memo[state]
                    # recursive case
                    min_cost = float('inf')
                    for c_idx in range(len(cuts)):
                        if cuts[c_idx] <= i:
                            continue
                        cur_cost = j-i + recur(cuts[c_idx], j)
                        min_cost = min(min_cost, cur_cost)
                    # save memo
                    memo[state] = min_cost
                    return memo[state]
                return recur(0, n)
                
        ```
        
    - Top-down 2
        - 양쪽으로 break 하는 건 잘한 것 같은데
        
        ```sql
        class Solution:
            def minCost(self, n: int, cuts: List[int]) -> int:
                # early return 
                if len(cuts) == 1:
                    return n 
                memo = {}
                cuts.sort()
                def recur(i, j, c_count): 
                    # check state
                    state = (i, j, c_count)
                    if state in memo:
                        return memo[state]
                    # base case 
                    if c_count == 0:
                        return j - i
                    # recursive case 
                    min_cost = float('inf')
                    cur_count = 0
                    for cidx, cut in enumerate(cuts):
                        if i < cut < j:
                            cur_count += 1
                            left = recur(i, cut, cur_count-1)
                            right = recur(cut, j, c_count-cur_count)
                            min_cost = min(min_cost, left + right)
                        elif cut >= j:
                            break 
                            
                    # save memo
                    memo[state] = min_cost
                    return memo[state]
                return recur(0, n, len(cuts))
                
        ```
        
    - Top-down 3
        - 솔루션 본 뒤인데 뭐가 틀린 것이냐 이번엔!
        
        ```sql
        class Solution:
            def minCost(self, n: int, cuts: List[int]) -> int:
                # early return 
                if len(cuts) == 1:
                    return n 
                memo = {}
                cuts.sort()
                cuts = [0] + cuts + [n]
                m = len(cuts)
                def recur(i, j): 
                    # check state
                    state = (i, j)
                    if state in memo:
                        return memo[state]
                    # base case 
                    if j - i == 1: # no cut in between 
                        return cuts[j] - cuts[i]
                    # recursive case
                    min_cost = float('inf')
                    cur_cost = cuts[j] - cuts[i]
                    for next_idx in range(i+1, j): # i, i+1이 처음 j-1, j가 마지막 base case
                        left_cost = recur(i, next_idx)
                        right_cost = recur(next_idx, j)
                        min_cost = min(min_cost, left_cost + right_cost) 
                    # save memo
                    memo[state] = min_cost + cur_cost
                    return memo[state]
                return recur(0, m-1)
                
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def minCost(self, n: int, cuts: List[int]) -> int:
                # early return 
                if len(cuts) == 1:
                    return n 
                cuts.sort()
                new_cuts = [0] + cuts + [n] # last_idx: m-1
                m = len(new_cuts)
                dp = [[float('inf')] * m for _ in range(m)]
        
                # base case
                for i in range(m-1): # m-2+1 = m-1
                    dp[i][i+1] = 0 # no need of cutting
                
                # recursive case
                for start in range(m-2): # m-3+2 = m-1 
                    for diff in range(2, m-start): # cur_cost
                        # end: start + diff <= m-1
                        # start + diff < m
                        # diff < m-start
                        end = start + diff 
                        for mid in range(start+1, end):
                            dp[start][end] = min(dp[start][end], diff + dp[start][mid] + dp[mid][end])
                
                return dp[0][m-1]
        
        ```
        
- Solution
    - state definition
        - cost(left, right)
            - cuts[left]가 왼쪽 end, cuts[right]가 오른쪽 end인 어느 막대를 자르는데 드는 최소 비용
                - 0이랑 n을 cuts에 추가해주는 게 핵심
                    - 처음 막대의 양 끝인 0과 n은 cuts array에 없으니까
                    - 그리고 1 < = cuts[i] ≤ n-1
                - 기존 cuts 길이가 m이라고 하면, 마지막 인덱스는 m
                    - 여기에 맨 앞에 0, 맨 뒤에 n이 붙으면서 길이는 m+2, 마지막 인덱스는 m+1이 되었음
    - return state
        - cost(0, m+1)
    - base case
        - cost(left, left+1) = 0
            - left+1이 가질 수 있는 가장 큰 값은 m+1이기 때문에
            - left는 m과 같거나 작아야 함
    - 재귀식
        - 어디를 자르던 현재 막대를 둘로 자르면 현재 막대의 길이 만큼의 비용은 지불해야 한다
            - cur_cost = cuts[right]-cuts[left]
            - return state로 보면 cuts[m+1]-cuts[0] = n-0 = n
        - 자른 지점을 m이라고 하면
            - 잘랐을 때 왼쪽 막대는 cuts[left], cuts[m]을 두 경계로 삼음
            - left_cost = recur(left, m)
            - right_cost = recur(m, right)
- AC 코드
    - Top-down
        - base case 유의!!!!
            
            ```python
            class Solution:
                def minCost(self, n: int, cuts: List[int]) -> int:
                    # early return 
                    if len(cuts) == 1:
                        return n 
                    memo = {}
                    cuts.sort()
                    cuts = [0] + cuts + [n]
                    m = len(cuts)
                    def recur(i, j): 
                        # check state
                        state = (i, j)
                        if state in memo:
                            return memo[state]
                        # base case 
                        if j - i == 1: # no cut in between 
                            return 0 # 자를 필요 없으니 비용도 0
                        # recursive case
                        min_cost = float('inf')
                        cur_cost = cuts[j] - cuts[i]
                        for next_idx in range(i+1, j): # i, i+1이 처음 j-1, j가 마지막 base case
                            left_cost = recur(i, next_idx)
                            right_cost = recur(next_idx, j)
                            min_cost = min(min_cost, left_cost + right_cost) 
                        # save memo
                        memo[state] = min_cost + cur_cost
                        return memo[state]
                    return recur(0, m-1)
                    
            ```
            
    - Bottom-up
        - for loop 순서 가지고 옥신각신
        - 근데 개빠르다…!
        
        ```python
        class Solution:
            def minCost(self, n: int, cuts: List[int]) -> int:
                # early return 
                if len(cuts) == 1:
                    return n 
                cuts.sort()
                new_cuts = [0] + cuts + [n] # last_idx: m-1
                m = len(new_cuts)
                dp = [[float('inf')] * m for _ in range(m)]
        
                # base case
                for i in range(m-1): # m-2+1 = m-1
                    dp[i][i+1] = 0 # no need of cutting
                
                # recursive case
                for diff in range(2, m): # m-1
                    for start in range(m-diff):
                        # end: start + diff <= m-1
                        # start + diff < m
                        # start < m - diff
                        end = start + diff 
                        cur_cost = new_cuts[end] - new_cuts[start]
                        for mid in range(start+1, end):
                            dp[start][end] = min(dp[start][end], cur_cost + dp[start][mid] + dp[mid][end])
                
                return dp[0][m-1]
        ```
        
        - 왜 식은 맞는데 start를 outer loop으로 올리면 안되는가
            - 재귀식에서 보면 dp[start][mid] + dp[mid][end] 얘네가 먼저 구해져 있어야 한다
            - 두 for loop으로 생성되는 pair 개수 및 구성 자체는 같다 그러나
            - start가 먼저 증가하는 경우
                - start 고정에다가 간격을 먼저 늘려간다 = start 고정에다가 end가 증가해나간다
                    
                    0 2 → m: 1 → (0, 1), (1, 2) 모두 base case
                    0 3 → m: 1, 2 → (0, 1), (1, 3) 에서 (1,3)은 아직 안 구해진 상태 
                    0 4 → m: 1, 2, 3
                    1 3 → base case 
                    1 4 → m: 1
                    2 4 → x 
                    
            - diff가 먼저 증가하는 경우
                - diff가 고정되어 있는 상황에서 start를 늘려간다
                    
                    = start와 end가 slide window 크기 유지하면서 같이 이동해나간다 
                    
                    0 2 → m: 1 → (0, 1), (1, 2) 모두 base case
                    1 3 → m:2 → (1, 2), (2,3) 모두 base case
                    2 4 → m:3 → (2, 3), (3, 4) 모두 base case
                    0 3 → m: 1, 2
                    
                    - (0, 1) base case, (1, 3) 이미 구해진 상태!
                    
                    1 4
                    0 4