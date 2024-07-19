# 983. Minimum Cost For Tickets(🪂)

Status: done, in progress, incomplete, with help
Theme: DP
Created time: January 16, 2024 1:06 PM
Last edited time: January 16, 2024 4:54 PM

- Progress
    - 일반적인 문제라고 생각하면 그냥 마지막 날까지 쭉 array 만든 다음에 누적으로 할 텐데, 여기는 비 연속.
    - day 8에 도달하기 위한 방법
        - day 7까지 도달하는 비용 + 1 -day pass
        - day 1까지 도달하는 비용 + 7 - day pass
        - day 8에 1 day pass를 구매
    - days 값은 1에서 365
- Trial
    - Bottom-up 예제 1
        - 티켓 구매해두고 i index를 늘리지 않았음
        
        ```python
        class Solution:
            def mincostTickets(self, days: List[int], costs: List[int]) -> int:
                last_day = days[-1]
                i = 0
                # array
                dp = [0] * (last_day + 1) 
                # base case - auto covered. dp[0] = 0
        
                # iteration
                for day in range(1, last_day+1):
                    next_travel_day = days[i]
                    if day < next_travel_day:
                        dp[day] = dp[day-1]
                        continue
                    
                    # iteration of recurrence relation
                    thirty_pass, seven_pass, one_pass = float('inf'), float('inf'), float('inf')
                    if day - 30 >= 0:
                        thirty_pass = costs[2] + dp[day-30]
                    if day - 7 >= 0:
                        seven_pass = costs[1] + dp[day-7]
                    one_pass = costs[0] + dp[day-1]
                    min_cost = min(thirty_pass, seven_pass, one_pass)
                    dp[day] = min_cost
                
                return dp[last_day]
        ```
        
    - Bottom-up 64/70
        - day-유효기간이 음수다 = day - 유효기간 < 0.  day < 유효기간
        - 전에 구매한 티켓으로 첫날부터 오늘까지를 커버하고도 남는다는 뜻
        - 따라서 이 경우 비용은 무한대가 될 것이 아니라 0이 되어야 함. 티켓 구매값만 더해져야 함
        
        ```python
        class Solution:
            def mincostTickets(self, days: List[int], costs: List[int]) -> int:
                last_day = days[-1]
                i = 0
                # array
                dp = [0] * (last_day + 1) 
                # base case - auto covered. dp[0] = 0
        
                # iteration
                for day in range(1, last_day+1):
                    next_travel_day = days[i]
                    if day < next_travel_day:
                        dp[day] = dp[day-1]
                        continue
                    
                    # iteration of recurrence relation
                    thirty_pass, seven_pass, one_pass = float('inf'), float('inf'), float('inf')
                    if day - 30 >= 0:
                        thirty_pass = costs[2] + dp[day-30]
                    if day - 7 >= 0:
                        seven_pass = costs[1] + dp[day-7]
                    one_pass = costs[0] + dp[day-1]
                    min_cost = min(thirty_pass, seven_pass, one_pass)
                    dp[day] = min_cost
                    i += 1
                
                return dp[last_day]
        ```
        
- AC 코드
    - Top-down
        
        ```python
        class Solution:
            def mincostTickets(self, days: List[int], costs: List[int]) -> int:
                memo = {}
        
                # function
                def recur(day):
                    # base case: all days covered
                    if day > days[-1]: 
                        return 0
                    # check memoized
                    if day in memo:
                        return memo[day]
                    # recurrence relation
                    if day not in days:
                        memo[day] = recur(day+1)
                    else:
                        # iteration of the recurrence relation
                        one_pass = costs[0] + recur(day+1)
                        seven_pass = costs[1] + recur(day+7)
                        thirty_pass = costs[2] + recur(day+30)
                        memo[day] = min(one_pass, seven_pass, thirty_pass)
                    return memo[day]
                
                return recur(1)
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def mincostTickets(self, days: List[int], costs: List[int]) -> int:
                last_day = days[-1]
                i = 0
                # array
                dp = [0] * (last_day + 1) 
                # base case - auto covered. dp[0] = 0
        
                # iteration
                for day in range(1, last_day+1):
                    next_travel_day = days[i]
                    if day < next_travel_day:
                        dp[day] = dp[day-1]
                    else:            
                    # iteration of recurrence relation
                        thirty_pass = costs[2] + dp[max(0, day-30)]                
                        seven_pass = costs[1] + dp[max(0, day-7)]
                        one_pass = costs[0] + dp[day-1]
                        min_cost = min(thirty_pass, seven_pass, one_pass)
                        dp[day] = min_cost
                        i += 1
                
                return dp[last_day]
        ```
        
- Editorial
    - Overview
        - 문제의 특징
            1. days를 iterate 하면서 둘 중 하나를 결정해야 함 
                1. 새로운 ticket을 오늘 구매해야 하는지 
                2. 오늘에도 유효한 티켓을 이미 가지고 있는 상태인지 
                
                → 오늘은 선택은 이전에 얼마 간 유효한 티켓을 언제 샀는지로부터 영향을 받음. 또 오늘 무슨 티켓을 구매하느냐에 따라 미래의 결정에 영향을 줌 
                
            2. 최소 비용을 구해야 함 
            
            ⇒ DP를 사용해야 
            
        
    - **Approach 1: Top-Down Dynamic Programming**
        - Intuition
            - 각 날에 대해
                - 여행하지 않아도 되는 날에는 티켓을 살 필요가 없다
                    - 다음 날로 그냥 넘어간다
                - 그러나 오늘이 여행해야 하는 날이고 이전으로부터 산 티켓이 없으면 구매 가능한 티켓의 종류가 세 가지 - 세 가지 중 하나를 선택
            - 필요한 parameters
                - current day that we are iterating over
                - `recur(cur_day)` returns: cur_day에 출발했을 때의 문제의 답을 줌(?)
            - recursive function
                - cur_day starts at 1
                - base condition
                    - 모든 날에 대해 다 돌았을 때. cur_day > last_day
                - cur_day에 여행해야 하는지 안해야 하는지 결정해야
                    - cur_day가 days에 없으면 티켓을 안사도 되고 다음 날로 넘겨도 됨
                - cur_day에 여행을 해야 하면 세 가지 option 존재
                    1. 원데이 패스 사고, 다음 날로 넘어감 
                    2. 7-day 패스 사고, 7일 뒤로 넘어감
                    3. 30-day 패스 사고, 30일 뒤로 넘어감 
    - **Approach 2: Bottom-up Dynamic Programming**
        - Intuition
            - `dp[day]` : day까지 여행하는 데 드는 최소의 비용
            - each value of day에 도달하기까지 세 가지 option 존재
                - day-1 에 one-day pass 구매
                - day-7 에 7-day pass 구매
                - day-30에 30-day pass 구매
            - 근데 그럼 여행을 하지 않아도 되는 무시해야 하는 날들은 어떻게 처리하느냐
                - 변수 i를 지정 - days array에서 여행해야 하는 다음 날을 가리킴
                - 만약 days[i]보다 작은 날을 여행하고 있을 경우, 여행 안 해도 되는 날에 있다는 뜻 → 그럼 전날이랑 cost가 달라질 필요가 없음
        - Algorithm
            1. 여행해야 하는 마지막 날 + 1 만큼의 size로 dp array 생성. 초기값은 0
            2. next travel day index i는 0으로 초기화 
                - the index in the array days
                - we must buy the ticket at that day
            3. 1부터 days의 마지막 날을 돌면서, 각 day에 대해 
                - current day < days[i] 이면 전날 값을 그대로 사용
                - 그렇지 않으면 세 가지 티켓 사는 경우의 수 중 가장 적은 비용을 dp[day]에 저장
                    - 티켓을 구매했으므로 i 변수의 값을 다음 index로 옮김
            
            3. dp[last_day] return 
            
- 기타 헷갈렸던 점
    - bottom-up base case
        - dp[0] = 0. 여행을 시작하기 전 아무 티켓도 구매하지 않았기 때문에 그냥 지불한 비용이 없으므로 0
    - 여행은 1일부터 시작하는데, 그날을 여행하기 위해서는 당일 티켓을 구매해야 함
        - 8일에 대한 여행 비용은
            - 1일까지 여행한 비용 + 7일 동안 유효한 티켓 구매 비용
                - 2, 3, 4, 5, 6, 7, 8 → 8이 유효기간 7일에 포함되어 있다
    - dp[day]
        - day까지 여행할 수 있는 최소 비용
    - next_travel_day에 도달하기 전까지만 추가 비용 없이 여행 지속. 도달하면 바로 티켓 사야 함