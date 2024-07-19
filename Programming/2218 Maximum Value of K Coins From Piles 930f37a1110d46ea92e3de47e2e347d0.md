# 2218. Maximum Value of K Coins From Piles

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP
Created time: January 24, 2024 6:39 PM
Last edited time: January 26, 2024 5:56 PM

- Process
    - top에서 제거한다는 거 보니 stack이겠지?
        - 예시와 그림을 매치해보면 top은 list[0]이다. Popleft 해야 하니 deque 사용해야 할 듯
    - 취할 수 있는 option은 여러 파일 중 하나의 top
    - 혹은 이미 top이 없어진 pile에서 또 top을 가져오면 수직으로 순서대로 가져오게 되는 셈
    - 이런 예시도 있다
        
        ```python
        Input: piles = [[100],[100],[100],[100],[100],[100],[1,1,1,1,1,1,700]], k = 7
        Output: 706
        Explanation:
        The maximum total can be obtained if we choose all coins from the last pile.
        ```
        
    - 2차원 dp로 해결가능한가?
        - 앞에서 숫자를 뽑은 Pile과 이번에 숫자를 뽑은 pile이 같은 경우
            - 앞에서 총 몇 개가 뽑힌 줄 알고 이번 숫자를 뽑을 index를 결정?
            - 이 정보도 기록을 해야 하려나?
            - 3차원 만들자…
                - 왜냐면 직전 칼럼이 다를 경우, 직전 칼럼의 몇 번째 원소를 가져왔는지를 저장해뒀는데, 이게 이번 칼럼에서 몇 번째 원소 가져가는지랑은 관련 없음
    - i=2. 앞에 하나의 동전을 뽑은 상태
        - j = j 일 때 dp[i-1][j][?] = dp[1][j][?]
            - dp[1][j][1]만 값이 있고 나머지는 0
    - 직전 다른 column에서 뽑은 값의 max에 지금 내 걸 더해야 하나?
- Trial
    - 3차원 bottom-up 시도
        
        ```python
        from collections import deque
        class Solution:
            def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
                n = len(piles)
                dp = []
        
                for i in range(k+1):
                    temp = [] 
                    for j in range(n):
                        len_p = len(piles[j])
                        inner_arr = [0 for _ in range(len_p)]
                        temp.append(inner_arr)
                    dp.append(temp)
                
                # dp[i][j][k] 
                ## choosing i coins optimally
                ## last chose coin is from k th element from j column 
                ## k cannot be over the length of piles[j]
        
                # base case 
                ## choosing 1 coin from each column (first element)
                for j in range(n):
                    dp[1][j][0] = piles[j][0]
                
                # recurrence relation
                for i in range(2, k+1):
                    for j in range(n):
                        len_p = len(piles[j])
                        for k in range(len_p):
                            cur_val = piles[j][k]
                            if k == 0:
                                same_col = 0 
                            else:
                                same_col = dp[i-1][j][k-1]
                            for l in range(n):
                                if l == j:
                                    continue
                                diff_col = max(dp[i-1][l])
                            dp[i][j][k] = max(dp[i][j][k], max(diff_col, same_col) + cur_val)
                
                max_val = -1
                for j in range(n):
                    len_p = len(piles[j])
                    for k in range(len_p):
                        max_val = max(max_val, dp[k][j][k])
                
                return max_val
        ```
        
    - top-down TLE(77/123)
        - 마지막에 결과 저장을 안해서 생기는 문제였음
        
        ```python
        class Solution:
            def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
                memo = {}
                n = len(piles)
                
                # function
                def recur(i, coins):
                    # base case
                    if i == 0 or coins == 0:
                        return 0 
                    # check memoized
                    if (i, coins) in memo:
                        return memo[(i, coins)]
                    # recurrence relation 
                    cur_pile = piles[i-1]
                    pile_len = len(cur_pile)
                    cur_sum = 0
                    max_sum = 0
                    for current_coins in range(min(coins, pile_len)+1):
                        if current_coins > 0:
                            cur_sum += cur_pile[current_coins-1]
                        prev_sum = recur(i-1, coins-current_coins)
                        max_sum = max(max_sum, prev_sum + cur_sum)
                    return max_sum
                
                return recur(n, k)
        ```
        
- AC 코드
    - Bottom-up
        
        ```python
        class Solution:
            def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
                n = len(piles)
                dp = [[0] * (k+1) for _ in range(n+1)]
        
                # base case: dp[0][j] = 0 # no pile
        
                # recurrence relation
                # increment by 1 : num_pile. not num_coin
                for num_pile in range(1, n+1): # 1 -> n
                    cur_pile = piles[num_pile-1] # 0 -> n-1
                    len_pile = len(cur_pile)
                    for num_coin in range(1, k+1):
                        max_val = 0
                        cur_val = 0
                        for cur_coin in range(min(num_coin, len_pile)+1): # 0 -> valid
                            if cur_coin > 0:
                                cur_val += cur_pile[cur_coin-1]
                            prev_coin = num_coin - cur_coin
                            prev_val = dp[num_pile-1][prev_coin]
                            max_val = max(max_val, cur_val + prev_val)
                        dp[num_pile][num_coin] = max_val
                
                return dp[n][k]
        ```
        
    - Top-down
        
        ```python
        class Solution:
            def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
                memo = {}
                n = len(piles)
                
                # function
                def recur(i, coins):
                    # base case
                    if i == 0 or coins == 0:
                        return 0 
                    # check memoized
                    if (i, coins) in memo:
                        return memo[(i, coins)]
                    # recurrence relation 
                    cur_pile = piles[i-1]
                    pile_len = len(cur_pile)
                    cur_sum = 0
                    max_sum = 0
                    for current_coins in range(min(coins, pile_len)+1):
                        if current_coins > 0:
                            cur_sum += cur_pile[current_coins-1]
                        prev_sum = recur(i-1, coins-current_coins)
                        max_sum = max(max_sum, prev_sum + cur_sum)
                    # save at memo
                    memo[(i, coins)] = max_sum
                    return memo[(i, coins)]
                
                return recur(n, k)
        ```
        
- Editorial
    - **Bottom-up Dynamic Programming**
        - Intuition
            - state definition
                - `dp[i][coins]` : 왼쪽에서 i개 pile들 통틀어서 (pile index: 0~i-1, piles[:i]) 최대 coins 개수의 동전을 선택하는 경우 얻을 수 있는 최대 가치
                - 예) dp[4][7]: 왼쪽에서 네번째 pile까지에서 최대 7개의 동전을 취할 때 얻을 수 있는 최대 가치. 모든 동전은 양수이기 때문에, 7보다 적은 개수의 동전을 취하는 건 절대 최대 가치를 만들 수 없다
            - base case
                - `dp[0][coins]`=0
                    - piles[:0] = None
                    - pile이 하나도 없지만 coins는 여러 개 값이 될 수 있나봄?
                    - 근데 명시적으로 그렇게 안해도 초기값은 모두 0
            - recurrence case
                - dp[i][coins] 경우의 수
                    - 왼쪽에서 i개의 pile 들 통틀어서 coins 개의 동전을 선택하는 경우 얻을 수 있는 최대 가치 (0~i-1)
                    1. piles[:i-1]개에서 coins 개를 모두 가져오고, 현재 pile인 piles[i-1]에서는 하나도 안 가져오는 경우 
                    2. 하나만 current pile에서 가져오고 나머지(coins-1)는 piles[:i-1]에서 가져오는 경우 
                    3. 두개만 current pile에서 가져오고 나머지(coins-2)는 piles[:i-1]개에서 가져오는 경우 
                    4. …
                    5. current coins 개수만 current pile에서 가져오고 나머지(coins-current coins)는 piles[:i-1]개에서 가져오는 경우 
                - `currentSum` : current pile(i-1)에서 current coin개의 동전을 들고 올 때 얻을 수 있는 sum
                - 점화식: dp[i][coins] = dp[i-1][coins-current_coins] + currentSum
                - current Coins에 대한 두 가지 제약
                    - current pile이 갖고 있는 동전의 개수보다 더 클 수 없음
                    - 최대 coins개의 동전을 가져오도록 허락되기 때문에 coins를 넘을 수 없음
                    
                    → valid range : (0, min(len(piles[i-1]), coins))
                    
            - return value
                - 모든 동전이 양수의 값을 갖기 때문에 k보다 적은 개수의 동전을 취하는 건 절대 Optimal이 될 수 없음
                - dp[n][k]가 우리가 return 해야 할 값 - 전체 범위의 Pile을 고려하면서, 이중에서 k개의 동전을 선택하는 경우
                
        - 알고리즘
            - cell value = 0으로 dp table 초기화
            - i : 1→ n
                - coins: 0 → k
                    - currentSum = 0으로 초기화
                    - currentCoins: 0 → min(len(piles[i-1]), coins)
                        - currentCoins > 0 → currentSum += piles[i-1][currentCoins-1]
                            - 현재 pile(piles[i-1])에서 가져오는 동전 개수
                            - 2개면 마지막으로 더해지는 동전의 index는 1
                        - dp[i][coins] = dp[i-1][coins-currentCoins] + currentSum
            - return dp[n][nk]