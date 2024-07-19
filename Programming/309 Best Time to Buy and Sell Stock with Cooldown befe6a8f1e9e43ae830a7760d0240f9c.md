# 309. Best Time to Buy and Sell Stock with Cooldown

Status: done, 👀1
Theme: DP
Created time: November 17, 2023 4:59 PM
Last edited time: November 17, 2023 5:41 PM

- 코드
    
    ```python
    class Solution:
        def maxProfit(self, prices: List[int]) -> int:
            n = len(prices)
            hold = [0] * n
            not_hold = [0] * n
            # base case: at the end of the first day, I have a stack 
            hold[0] = 0-prices[0]
    
            for i in range(1, n):
                if i == 1: # not_hold[0] : did nothing on the first day 
                    hold[i] = max(hold[0], not_hold[0]-prices[1])
                else: # not_hold[i-2] : sold at i-2th day and then cooldown yesterday 
                    hold[i] = max(hold[i-1], not_hold[i-2]-prices[i])
                not_hold[i] = max(not_hold[i-1], hold[i-1]+prices[i])
    
            return not_hold[n-1]
    ```
    
- 난 이게 더 쉽다
    - 둘 다 초기 세팅: [0] * n
        - `hold[i]` : day i가 끝날 때 주식을 들고 있는 상황에서 얻을 수 있는 최대 이익
        - `not_hold[i]` : day i가 끝날 때 주식을 판매 완료한 상황에서 얻을 수 있는 최대 이익
        - 첫날(0)에는 주식을 안 사거나 사거나 두가지만 가능
            - 주식을 사는 경우: hold[i] = -prices[0] (실현된 이익은 없고 지불한 비용만 존재)
            - 주식을 안 사는 경우: not_hold[i] = 0
    - transition
        - not_hold[i] : 주식 없는 이전 상태로 유지 vs. 주식 있던 이전 상태 + 오늘 가격에 팔아서 얻은 이익
        - hold[i]
            - i = 1 → 바로 전날의 결정에만 영향을 받는 hold의 특수한 경우
                - 주식 있는 어제 상태 유지 vs. 아무것도 안한 어제 + 오늘 가격에 사서 지불한 비용
            - i > 1
                - 주식 있는 어제 상태 유지 vs. 주식 없이 어제 cool down + 오늘 가격에 사서 지불한 비용