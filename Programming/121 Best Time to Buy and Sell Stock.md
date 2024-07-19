# 121. Best Time to Buy and Sell Stock

Status: done, in progress
Theme: DP
Created time: November 28, 2023 12:56 PM
Last edited time: November 28, 2023 1:06 PM

- 몸풀기 easy
- 맞긴 맞는데 왜케 느리지 - 그냥 for loop만으로도 풀 수 있기 때문
- 코드
    
    ```python
    class Solution:
        def maxProfit(self, prices: List[int]) -> int:
            n = len(prices)
            profit = [0] * (n+1)
            cost = prices[0]
            for i in range(1, n):
                profit[i] = max(profit[i-1], prices[i]-cost)
                cost = min(cost, prices[i])
            return max(profit)
    ```