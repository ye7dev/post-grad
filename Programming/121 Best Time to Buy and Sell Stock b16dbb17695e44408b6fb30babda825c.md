# 121. Best Time to Buy and Sell Stock

Status: done, in progress
Theme: DP
Created time: January 12, 2024 10:03 AM
Last edited time: January 12, 2024 11:00 AM

- III, IV 는 state transition by inaction에 속하는 DP 문제였지만, I은 카데인 알고리즘을 사용하는 문제로 나옴
- 거꾸로 돈다고 하면
    - 얻을 수 있는 금액은 지나온 금액 중 최대 값
    - 빼는 금액은 지금 금액
    - 2, 4, 7
        - 7이 우선 더해진 상태
        - current - prices[i] = 3 vs. prices[i] = 4 → 4?
- 이거랑 maximal subarray랑 무슨 상관?
- AC 코드
    - 원래 kadane’s algo에서는 current랑 best가 추적하는 대상이 같았는데
        - current: max(누적 + 현재값, 누적 버리고 현재 값만)
        - best: max(누적 값만, updated current)
    - 여기서 current는 순전히 내 지갑에 있는 금액이고, best는 profit 중 best
        - 그래서 updated current가 그대로 best에 들어갈 수 없고, 얻는 이득이 더해져서 기존 best랑 비교 된다
        - 왜냐면 updated current는 주식을 팔고 났을 때의 이득인 상태일 수도 있지만, 지금 가격에서 주식을 사기만 한 상태일 수도 있기 때문에
    - 포인트는 생각했을 때 취할 수 있는 Option이 뭐뭐 있는지 잘 파악하는 것
        1. 지금 가격에 산다
        2. 지금 가격에 판다 → Profit 발생
        3. 아무것도 안한다 (이전 가격으로 구매한 상태를 유지, 더 좋은 가격이 나오면 팔겠다) 
    - current에서 비교하는 건 1. 3.
    - best에서 비교하는 건 이전에 만든 Profit과 2. 비교
    
    ```python
    class Solution:
        def maxProfit(self, prices: List[int]) -> int:
            n = len(prices)
            if n == 1:
                return 0 
    
            current = -prices[0] 
            best = -float('inf') 
    
            for i in range(1, n):
                # options : selling now, buying now, don't sell now
                current = max(-prices[i], current)
                best = max(best, current+prices[i])
                
            return best if best > 0 else 0
    ```
    
- Editorial
    - 명확하게 min_cost, max_profit 변수를 두고 Iteration
        
        ```python
        class Solution:
            def maxProfit(self, prices: List[int]) -> int:
                min_price = float('inf')
                max_profit = 0
                for i in range(len(prices)):
                    if prices[i] < min_price:
                        min_price = prices[i]
                    elif prices[i] - min_price > max_profit:
                        max_profit = prices[i] - min_price
                        
                return max_profit
        ```