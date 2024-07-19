# 714. Best Time to Buy and Sell Stock with Transaction Fee

Status: done, in progress
Theme: DP
Created time: January 12, 2024 8:32 PM
Last edited time: January 13, 2024 10:49 AM

- Trial
    - 예제 통과는 못함
        
        ```python
        class Solution:
            def maxProfit(self, prices: List[int], fee: int) -> int:
                n = len(prices)
                # array
                # dp[i][0]: ith day max profit at the end of the day not holding any stock
                # dp[i][1]: ith day max profit at the end of the day holding a stock 
                dp = [[0,0] for _ in range(n)]
        
                # base case
                # dp[0][0]: first day finishing with no buying or selling -> 0 
                # dp[0][1]: first day finishing with buying a stock -> cost + fee
                dp[0][1] = -prices[0] - fee 
        
                # recurrence relation
                for i in range(1, n):
                    # buying 
                    buying = dp[i-1][0] - prices[i] - fee
                    # selling 
                    selling = dp[i-1][1] + prices[i] - fee
                    # finishing day with holding a stock
                    dp[i][1] = max(dp[i-1][1], buying)
                    # finishing day with not holding any stock
                    dp[i][0] = max(dp[i-1][0], selling)
                
                return dp[n-1][0]
        ```
        
- AC 코드
    - fee는 selling, buying에 둘 다 붙는게 아니라 둘 중 한번만 붙이면 되는 것이었음
        - 구매 판매 묶어서 하나의 transaction이 만들어지는데, 매 transaction마다 수수료가 붙는 개념
    - base case는 직관대로 한 것이 맞았음
    
    ```python
    class Solution:
        def maxProfit(self, prices: List[int], fee: int) -> int:
            n = len(prices)
            # array
            # dp[i][0]: ith day max profit at the end of the day not holding any stock
            # dp[i][1]: ith day max profit at the end of the day holding a stock 
            dp = [[0,0] for _ in range(n)]
    
            # base case
            # dp[0][0]: first day finishing with no buying or selling -> 0 
            # dp[0][1]: first day finishing with buying a stock -> cost + fee
            dp[0][1] = -prices[0] - fee 
    
            # recurrence relation
            for i in range(1, n):
                # buying 
                buying = dp[i-1][0] - prices[i] - fee
                # selling 
                selling = dp[i-1][1] + prices[i] 
                # finishing day with holding a stock
                dp[i][1] = max(dp[i-1][1], buying)
                # finishing day with not holding any stock
                dp[i][0] = max(dp[i-1][0], selling)
            
            return dp[n-1][0]
    ```