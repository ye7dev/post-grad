# 983. Minimum Cost For Tickets

Status: in progress
Theme: DP
Created time: November 21, 2023 11:09 PM
Last edited time: November 22, 2023 1:44 PM

- [x]  한번 더 풀어보기
- 과정
    
    ```python
    class Solution:
        def mincostTickets(self, days: List[int], costs: List[int]) -> int:
            n = len(days)
            max_day = max(days)
            dp = [float('inf')] * (max_day+1)
            dp[0] = 0
            for i in range(1, max_day+1):
                if i >= 1:
                    dp[i] = min(dp[i], dp[i-1]+costs[0])
                if i >= 7:
                    dp[i] = min(dp[i], dp[i-7]+costs[1])
                if i >= 30:
                    dp[i] = min(dp[i], dp[i-30]+costs[2])
            print(dp)
            return dp[-1]
    ```
    
- 코드
    
    index i가 하나 더 들어가서 여행을 해야 하는 날과 안 해야 하는 날을 구분지어줘야 
    
    ```python
    class Solution:
        def mincostTickets(self, days: List[int], costs: List[int]) -> int:
            last_day = days[-1]
            dp = [0] * (last_day + 1) # dp[2] = dp[0] + two_step 가능 시나리오 
            travel = 0 # indices of days 
    
            for i in range(1, last_day+1):
                if i < days[travel]: # no need to buy ticket on this day 
                    dp[i] = dp[i-1] # former state extends
                else: # i == days[travel] or i > days[travel]
                    dp[i] = min(dp[i-1]+costs[0], 
                                dp[max(0, i-7)]+costs[1], 
                                dp[max(0, i-30)]+costs[2])
                    travel += 1 
            
            return dp[-1]
    ```
    
    - else 분기 관련
        
        ```python
        for i in range(1, last_day+1):
            if i < days[travel]: # no need to buy ticket on this day 
                dp[i] = dp[i-1] # former state extends
            elif i == days[travel]: # i == days[travel] or i > days[travel]
                dp[i] = min(dp[i-1]+costs[0], 
                            dp[max(0, i-7)]+costs[1], 
                            dp[max(0, i-30)]+costs[2])
                travel += 1
        ```
        
        - 이렇게 돌려도 정답(오히려 속도가 더 빠름)인 걸로 봐서 i > days[travel]은 걱정 안 해도 된다. 어차피 i == days[travel] 도달하자마자 travel이 증가하기 때문에 i가 days[travel]보다 더 커지는 경우는 없다