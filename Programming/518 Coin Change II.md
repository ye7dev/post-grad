# 518. Coin Change II

Status: done, in progress, with help
Theme: DP
Created time: January 10, 2024 11:20 AM
Last edited time: January 10, 2024 4:17 PM

- Trial and Error
    - 예제 2/3 통과 코드 (top-down)
        
        ```python
        class Solution:
            def change(self, amount: int, coins: List[int]) -> int:
                memo = {}
        
                # function
                def recur(left_amount):
                    # base case
                    if left_amount < 0:
                        return 0
                    if left_amount == 0:
                        return 1 # one way: no coins
                    # check memoized
                    if left_amount in memo:
                        return memo[left_amount]
                    # iteration of the recurrence relation
                    num_ways = 0
                    for c in coins:
                        temp = recur(left_amount-c)
                        num_ways += temp
                    memo[left_amount] = num_ways
                    return memo[left_amount]
                
                return  recur(amount)
        ```
        
    - 순서에 상관없이 같은 조합은 하나로 count 해야 하는데, 순서마다 다르다고 인식해서 하나의 조합을 여러 개로 count 해서 틀린 답이 나옴 (combination not permutation)
        - 예) amount = 3, coins = [1, 2]
            
            for c in coins: 
            
            temp = recur(3-1=2) = 2 → recur(2-1)=1 + recur(2-2)=1 
            
            temp = recur(3-2=1) = 1 
            
            → 합은 3. 그러나 valid count combination은 [1, 2] 한 개뿐 
            
    
    ⇒ 매 recursive call마다 current coin과 그 뒤에 올 coin만 비교해야 
    
    - 예제 + 25/28 까지 통과코드(bottom-up)
        
        ```python
        class Solution:
            def change(self, amount: int, coins: List[int]) -> int:
                # array
                dp = [[0] * (len(coins)+1) for _ in range(amount+1)]
        
                # base case
                # i == len(coins) -> 0. auto covered
                # amount == 0 -> one way. empty subset 
                for i in range(len(coins)):
                    dp[0][i] = 1 
        
                # iteration
                for left_amount in range(1, amount+1):
                    for i in range(len(coins)-1, -1, -1):
                        if left_amount - coins[i] >= 0:
                            inclusion = dp[left_amount-coins[i]][i]
                            exclusion = dp[left_amount][i+1]
                            dp[left_amount][i] = inclusion + exclusion
        
                return dp[amount][0]
        ```
        
    - dp array 만들 때 i도 고려해야 하나? 아님 amount만?
    - dp는 iteration이라 하나의 금액에 대해 모든 동전을 고려할 수 밖에 없는데?
- AC code
    - Top-down
        - state definition : `recur(i, left_amount)`
            - coins[i:]를 가지고 left_amount를 만들 수 있는 방법의 개수 (중복 없이, subset의 개수)
        - i th 동전을 포함하는 경우, 포함하고 바로 다음 동전으로 넘어가지 않는 것에 주의.
            - 조금 다르지만 비슷한 경우-[[**188. Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/description/) (🪂)**](188%20Best%20Time%20to%20Buy%20and%20Sell%20Stock%20IV%20(%F0%9F%AA%82)%2066d8df6e12fc45498219aa1d37d25af0.md) 에서 buy_stock에서 trx 개수가 변화하지 않은 것처럼.
            - 여기서도 하나의 동전을 여러번 사용할 수 있기 때문에 (예를 들어 5는 1 동전 5개로 만들 수 있음), 사용할 수 있는 동전의 범위는 그대로 유지하면서 만들어야 하는 금액만 바꾼 채 다음 subproblem으로 이동
        
        ```python
        class Solution:
            def change(self, amount: int, coins: List[int]) -> int:
                memo = {}
        
                # function
                def recur(i, left_amount): 
                    # base case
                    if left_amount < 0 or i == len(coins):
                        return 0
                    if left_amount == 0:
                        return 1 # one way: no coins
                    # check memoized
                    if (i, left_amount) in memo:
                        return memo[(i, left_amount)]
                    # iteration of the recurrence relation
                    include = recur(i, left_amount-coins[i])
                    exclude = recur(i+1, left_amount)
                    
                    memo[(i, left_amount)] = include + exclude
                    return memo[(i, left_amount)]
                
                return  recur(0, amount)
        ```
        
    - Bottom-up
        - exclusion에서는 left_amount 변화가 없기 때문에 현재 coin을 뺀 나머지 금액이 음수던 양수던 상관이 없다
        - inclusion에서만 상관이 있다. 양수인 경우에만 넘겨서 0이 아닌 숫자를 받아와야 하기 때문이다
        - 근데 그럼 왜 amount = 100, coins = [99, 1]에서 걸렸냐
            - left_amount = 1, i = 0인 경우를 보면
                - left_amount - coins[i] = 1 - 99 = -98 <0 이라서 inclusion은 건너뛴다
                - 그러나 exclusion = dp[1][1] = 1이다
                    - 이걸 건너뛰면 dp[1][0]은 그냥 0이 된다
                    - 그러나 우리 식에 따르면 inclusion + exclusion이기 때문에 1을 포함하고 갔어야 했다
                    - 그래서 답이 틀리게 나왔던 것
        
        ```python
        class Solution:
            def change(self, amount: int, coins: List[int]) -> int:
                # array
                dp = [[0] * (len(coins)+1) for _ in range(amount+1)]
        
                # base case
                # i == len(coins) -> 0. auto covered -> amount == 0 overrules
                # amount == 0 -> one way. empty subset 
                for i in range(len(coins)+1):
                    dp[0][i] = 1 
        
                # iteration
                for left_amount in range(1, amount+1):
                    for i in range(len(coins)-1, -1, -1):
                        inclusion = 0 
                        if left_amount - coins[i] >= 0:
                            inclusion = dp[left_amount-coins[i]][i]
        
                        exclusion = dp[left_amount][i+1]
                        dp[left_amount][i] = inclusion + exclusion
        
                return dp[amount][0]
        ```