# 309. Best Time to Buy and Sell Stock with Cooldown(🪂)

Status: done, in progress
Theme: DP
Created time: January 9, 2024 2:26 PM
Last edited time: January 9, 2024 3:09 PM

- Process
    - state variables
        - day, holding
            - no restrictions on the transaction numbers
    - cooldown 여부도 state variable에 들어갈까?
        - holding의 경우 cooldown과 상관없는데
        - not holding의 경우
            - 어제 sell 했으면 do nothing이 mandatory이고, no other option
            - 엊그제 sell 했거나 애초에 없는 상태면 do nothing하거나 사거나 둘 중 하나
        - 근데 memo 자체에는 그 값을 안 넣어도 되지 않을까? 넣어야 할까?
            - 안전하게 넣어보자
    - base case에 대한 부분이 array 초기값으로 대체가 되는 경우 아래와 같은 표현을 쓰면 된다 - The base cases are automatically handled
    - holding = True인데, yesterday_sell일수가 있나?
        - 아니.어제 팔았으면 바로 다시 살 수가 없기 때문에
- AC 코드
    - top-down
        
        ```python
        class Solution:
            def maxProfit(self, prices: List[int]) -> int:
                memo = {}
                def recur(day, holding, yesterday_sell):
                    cur_args = (day, holding, yesterday_sell)
                    # base case
                    if day == len(prices):
                        return 0 
                    # check memoized 
                    if cur_args in memo:
                        return memo[cur_args]
                    
                    # iteration of the recurrence relation
                    if holding: 
                        do_nothing = recur(day+1, holding, 0)
                        sell_stock = prices[day] + recur(day+1, 0, 1)
                        memo[cur_args] = max(do_nothing, sell_stock)
                    else: # not holding
                        ## yesterday_sell will be always False
                        ## we have no stock in hand so no selling in today
                        do_nothing = recur(day+1, 0, 0)
                        if yesterday_sell: # need cooldown 
                            memo[cur_args] = do_nothing
                        else: # no need to rest
                            buy_stock = -prices[day] + recur(day+1, 1, 0)
                            memo[cur_args] = max(do_nothing, buy_stock)
                    return memo[cur_args]
                    
                return recur(0, 0, 0)
        ```
        
    - bottom-up
        - day 계산 순서를 어디서부터 가져가야 하는지 헷갈렸음
        
        ```python
        class Solution:
            def maxProfit(self, prices: List[int]) -> int:
                # array
                ## n(len(prices)) * 2(holding) * 2(yesterday_sell)
                n = len(prices)
                dp = [[[0] * 2 for _ in range(2)] for _ in range(n+1)]
                
                # base case
                ## day = n -> 0. automatically handled
                
                # iteration of the recurrence relation
                for day in range(n-1, -1, -1): # 0 -> n-1
                    for holding in range(2):
                        if holding:
                            do_nothing = dp[day+1][1][0]
                            sell_stock = prices[day] + dp[day+1][0][1]
                            dp[day][1][0] = max(do_nothing, sell_stock)
                        else: # not holding
                            for yesterday_sell in range(2):
                                do_nothing = dp[day+1][0][0]
                                if yesterday_sell:
                                    dp[day][0][1] = do_nothing
                                else:
                                    buy_stock = -prices[day] + dp[day+1][1][0]
                                    dp[day][0][0] = max(do_nothing, buy_stock)
                
                return dp[0][0][0]
        ```