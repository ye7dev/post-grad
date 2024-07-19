# 122. Best Time to Buy and Sell Stock II

Status: done, in progress
Theme: DP
Created time: February 3, 2024 11:53 AM
Last edited time: February 3, 2024 12:07 PM

- Progress
    - 문제 이해
        - 한 번에 하나의 주식만 들고 있을 수 있다
        - 그리고 같은 날에 사고 팔기가 가능
        - max_profit 구하라
- AC 코드
    - Bottom-up (🪇)
        - 마지막 return 값은 at the end of the last day, 주식이 손에 없는 상태여야 함
        
        ```python
        class Solution:
            def maxProfit(self, prices: List[int]) -> int:
                n = len(prices)
                dp = [[0,0] for _ in range(n)]
                # dp[i]: max profit at the end of the day 
                # dp[i][0]: not holding any stock
                # dp[i][1]: holding a stock 
        
                # base case - day 1 
                dp[0][1] = - prices[0]
        
                # recurrence relation
                for day in range(1, n):
                    # not holding 
                    dp[day][0] = max(dp[day-1][0], dp[day-1][1] + prices[day])
                    # holding
                    dp[day][1] = max(dp[day-1][0] - prices[day], dp[day-1][1])
                
                return dp[-1][0]
        ```