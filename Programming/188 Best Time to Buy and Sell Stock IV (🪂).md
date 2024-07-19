# 188. Best Time to Buy and Sell Stock IV (🪂)

Status: done, in progress
Theme: DP
Created time: January 8, 2024 9:50 PM
Last edited time: January 9, 2024 2:27 PM

- Trial
    - bottom-up
        - do nothing이 top-down에서와 다르게 두 개로 분기?
        - 181/210에서 불통
        
        ```python
        class Solution:
            def maxProfit(self, k: int, prices: List[int]) -> int:
                # array (3d) 
                ## (n+1) * (k+1) * (2)
                ## last_dim[0]: not holding, last_dim[1]: holding
                dp = [[[0, 0]] * (k+1) for _ in range(len(prices)+1)]
        
                # base case 
                ## day == n, chance = 0 -> 0. no explicit code
                for day in range(len(prices)-1, -1, -1):
                    for chance in range(1, k+1):
                        do_nothing = dp[day+1][chance]
                        # not holding
                        buy_stock = -prices[day] + dp[day+1][chance-1][1]
                        dp[day][chance][0] = max(do_nothing[0], buy_stock)
                        # holding
                        sell_stock = prices[day] + dp[day+1][chance-1][0]
                        dp[day][chance][1] = max(do_nothing[1], sell_stock)
        
                return dp[0][k][0]
        ```
        
- AC 코드
    - top-down
        - key가 무려 세 개~~~
        
        ```python
        class Solution:
            def maxProfit(self, k: int, prices: List[int]) -> int:
                memo = {}
        
                def recur(day, chance, holding):
                    # base case
                    if day == len(prices) or chance == 0:
                        return 0 
                    # check memoized 
                    if (day, chance, holding) in memo:
                        return memo[(day, chance, holding)]
                    # iteration of the recurrence relations
                    do_nothing = recur(day+1, chance, holding)
                    if holding == 1:
                        sell_stock = prices[day] + recur(day+1, chance-1, 0) 
                        max_profit = max(do_nothing, sell_stock)
                    else:
                        buy_stock = -prices[day] + recur(day+1, chance, 1)
                        max_profit = max(do_nothing, buy_stock)
                    
                    memo[(day, chance, holding)] = max_profit
                    return memo[(day, chance, holding)]
                
                return recur(0, k, 0)
        ```
        
    - bottom-up
        
        ```python
        class Solution:
            def maxProfit(self, k: int, prices: List[int]) -> int:
                # array (3d) 
                ## (n+1) * (k+1) * (2)
                ## last_dim[0]: not holding, last_dim[1]: holding
                dp = [[[0, 0] for _ in range(k+1)] for _ in range(len(prices)+1)]
        		
                # base case 
                ## day == n, chance = 0 -> 0. no explicit code
                for day in range(len(prices)-1, -1, -1):
                    for chance in range(1, k+1):
                        do_nothing = dp[day+1][chance]
                        # not holding
                        buy_stock = -prices[day] + dp[day+1][chance][1]
                        dp[day][chance][0] = max(do_nothing[0], buy_stock)
                        # holding
                        sell_stock = prices[day] + dp[day+1][chance-1][0]
                        dp[day][chance][1] = max(do_nothing[1], sell_stock)
        
                return dp[0][k][0]
        ```
        
        - 3차원 dp array 생성 시 주의
            - dp 이렇게 생성해도 AC
                - `[[[0]*2 for _ in range(k+1)] for _ in range(len(prices)+1)]`
            - [0,0]*2는 그냥 [0]*4와 같음
            - [[[0, 0]] * (k+1) for _ in range(len(prices)+1)]
                - 이렇게 할 경우 modifying any one of them will modify all others in that row.
                - 예
                    
                    ```python
                    >>> x = [[0,0]] * 3
                    >>> x
                    [[0, 0], [0, 0], [0, 0]]
                    >>> x[0][1] = 3
                    >>> x # 첫번째 row만 바꾸려 했는데 나머지도 다 바뀜
                    [[0, 3], [0, 3], [0, 3]]
                    ```