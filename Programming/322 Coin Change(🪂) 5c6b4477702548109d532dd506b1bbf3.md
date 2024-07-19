# 322. Coin Change(🪂)

Status: done, in progress
Theme: DP
Created time: January 7, 2024 11:25 PM
Last edited time: January 8, 2024 2:53 PM

[[Dynamic Programming](https://leetcode.com/explore/learn/card/dynamic-programming/)](Dynamic%20Programming%207dcf39589230406d98662b9562c792f0.md) 의 Iteration of the recurrence relation 예제 중 하나 

- Trial
    - 예제 통과, 31/189
        - num_coins가 같더라도 금액이 다를 수 있고, 또 심지어 cur_amount, num_coins가 같아도 조합이 달라질 수 있을 것 같은데…여기엔 그게 반영이 안되어 있는 듯
        
        ```python
        class Solution:
            def coinChange(self, coins: List[int], amount: int) -> int:
                memo = {}
                def recur(cur_amount, num_coins):
                    # base case
                    if cur_amount == 0:
                        return num_coins
                    if cur_amount < 0:
                        return -1 
                    # memoization
                    if (cur_amount, num_coins) in memo:
                        return memo[(cur_amount, num_coins)]
                    # recurrence relation
                    min_coin = float('inf')
                    for c in coins:
                        if cur_amount >= c:
                            temp = recur(cur_amount - c, num_coins + 1)
                            min_coin = min(min_coin, temp)
        
                    if min_coin == float('inf'):
                        min_coin = -1
                        
                    memo[(cur_amount, num_coins)] = min_coin
                    return memo[(cur_amount, num_coins)] 
                return recur(amount, 0)
        ```
        
    - TLE
        
        ```python
        class Solution:
            def coinChange(self, coins: List[int], amount: int) -> int:
                memo = {}
                def recur(cur_amount, num_coins):
                    if cur_amount == 0:
                        return num_coins 
                    if cur_amount < 0:
                        return -1 
                    min_coins = float('inf')
                    for c in coins:
                        if cur_amount >= c:
                            temp = recur(cur_amount - c, num_coins + 1)
                            if temp != -1:
                                min_coins = min(min_coins, temp)
                    if min_coins == float('inf'):
                        min_coins = -1
                    return min_coins
                return recur(amount, 0)
        ```
        
    - 내 접근법에 대한 반박
        - 우리 문제의 초점: 특정 금액을 만들 수 있는 동전의 최소 개수
            
            vs. `num_coins` : 같은 금액에 대해 조합에 따라 전체 동전 개수가 달라질 수 있음 → 특정 금액에 따라 동전 개수가 달라져야 하는데, 조합에 따라 달라지므로 state를 표현하기에 올바른 변수가 아니라고 함 
            
            - intrinsic property는 하나의 state를 unique하게 정의할 수 있어야 함. 우리의 state는 금액인데, 같은 금액에 여러 num_coins로 정의할 수 있으면 intrinsic property가 될 수 없음.
            - num_coins는 정확히 말하면 path taken to get there(cur_amount)의 property
        - cur_amount 금액 자체가 아니라, 그 금액에 도달하는 각 path에 대한 memoization을 하면 비효율
            - 금액 자체에 대해 memoization을 하면, 여러 path 중에 최소 개수를 가진 것만 저장 → 이후에 다른 parameter가 들어왔다가 쪼개져서 아까 구해둔 금액에 대한 결과를 필요로 하면, 그냥 이걸 건네주면 됨
            - 그러나 path 별로 memoization을 하면 전체 금액이 같더라도 서로 다른 path를 하나로 aggregate 하지 않기 때문에, 아까 구해둔 금액에 대한 결과로 무얼 건네주려나? 최소를 건네준다고 해도 extra 단계가 하나 더 추가되는 것이고, 바로 딱 가져다가 건네주기만 하면 되는 the overlapping nature of subproblems in dynamic programming을 최대로 활용하지 못하는 셈
            - not on the cumulative effect of the decisions made to reach that state
        - 조합이 state variable로 들어오는 순간, subproblem 간에 겹치는 부분이 줄어들게 됨
            - This means that for the same amount **`x`**, you could have multiple subproblems, each corresponding to a different count of **`num_coins`**.
            - As a result, these subproblems are no longer overlapping in the traditional sense, because the same amount **`x`** with a different **`num_coins`** is treated as a distinct problem.
    - 맞는 방향의 사고
        - independent of the path taken to reach that amount.
            - A subproblem in dynamic programming is defined by a set of parameters that uniquely identify the state required to solve it.
        - Each subproblem is meant to be solved once, and its solution is reused wherever needed. This is efficient because many of these subproblems overlap;
        - 문제에서 미지수를 잘 체크해야 함
            - x는 우리가 만들어야 하는 금액 자체임 → subproblem의 본질을 결정하는 미지수
            - x에 이르는 동전 조합 자체는 중요하지 않음 → num_coins를 state variable로 두는 것은 조합 고려할 때의 선택
                - solving many more specific problems of "minimum coins for amount **`x`** with **`y`** coins already used
            - In the coin change problem, a natural subproblem is "What is the minimum number of coins needed to make up a particular amount, **`x`**?"
            - This subproblem is solely defined by the amount **`x`**. The path taken to arrive at **`x`** (i.e., which coins were used to sum up to **`x`**) does not change the nature of this subproblem.
        - The most efficient approach is to let each recursive call return the minimum number of coins needed for a given **`cur_amount`** and use memoization to store these results based solely on **`cur_amount`**
        
- AC 코드
    - Top-down
        
        ```python
        class Solution:
            def coinChange(self, coins: List[int], amount: int) -> int:
                memo = {}
                # function
                def recur(left_amount):
                    # output minimum number of tokens to make the left_amount
        
                    # base case 
                    ## for zero, no need to add any coin
                    if left_amount == 0:
                        return 0 
                    ## no way to reach that exact amount for the given coins
                    if left_amount < 0:
                        return -1
        
                    # check memoization
                    if left_amount in memo:
                        return memo[left_amount]
        
                    # iteration of the recurrence relation
                    min_coins = float('inf')  # best among current options
                    for c in coins:
                        res = recur(left_amount - c)
                        if res != -1:
                            min_coins = min(min_coins, res + 1)
        
                    # no options available
                    if min_coins == float('inf'):
                        memo[left_amount] = -1 
                    else:
                        memo[left_amount] = min_coins
                    
                    return memo[left_amount]
                
                return recur(amount)
        ```
        
    - Bottom-up
        - recur에서 left_amount는 amount에서 시작해서 base case 0까지 hit 해야 함.
            
            → state: 0~amount
            
        - 음수가 나올 때 -1로 return 하는 건 어떻게 처리?
            
            → 음수가 나오면 continue 해서 다음 coin을 또 넣어보는데, 모든 coin에 대해서 음수가 나오면 초기 cell값 float(’inf’)에서 변한 것이 없을 것 → 그럼 -1로 cell 값을 갖게 됨 → 이후에 이 값을 hit 하는 경우는 모두 invalid 해져서 continue
            
        
        ```python
        class Solution:
            def coinChange(self, coins: List[int], amount: int) -> int:
                # array 
                dp = [float('inf')] * (amount + 1)
                # base case
                dp[0] = 0
        
                # iteration
                for cum_amount in range(1, amount+1):
                    for c in coins:
                        if cum_amount - c < 0:
                            continue
                        if dp[cum_amount - c] == -1:
                            continue
                        dp[cum_amount] = min(dp[cum_amount], dp[cum_amount - c] + 1)
        
                    # no option
                    if dp[cum_amount] == float('inf'):
                        dp[cum_amount] = -1 
        
                return dp[amount]
        ```
        
        +++ 모범답안에서는 continue 하는 부분이 없음
        
        ```python
        dp[x] = min(dp[x], dp[x - coin] + 1)
        ```
        
        - x - coin이 음수가 나오면 아직 계산되지 않은 dp array의 오른쪽에서 값을 가져올 것 → float(’inf’) 값 → float(’inf’), float(’inf’) + 1 에 대해 min을 해도 그대로 float(’inf’) → 결국 -1의 값을 갖게 될 것