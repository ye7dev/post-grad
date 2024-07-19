# 1335. Minimum Difficulty of a Job Schedule

Status: in progress
Theme: DP
Created time: January 7, 2024 12:00 PM
Last edited time: January 7, 2024 11:04 PM

- 설명은 [[Dynamic Programming](https://leetcode.com/explore/learn/card/dynamic-programming/)](Dynamic%20Programming%207dcf39589230406d98662b9562c792f0.md) 의 common patterns 참고
- AC 코드
    - top-down 기본
        
        ```python
        class Solution:
            def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
                n = len(jobDifficulty)
                if n < d:
                    return -1 
        
                memo = {}
                def recur(i, day):
                    # base case
                    if day == d:
                        return max(jobDifficulty[i:])
                    # check memoization
                    if (i, day) in memo:
                        return memo[(i, day)]
                    # recurrent relation 
                    boundary = n - (d - day)
                    # 6 works, d = 3, day = 1 -> two days left
                    # need to left at least 2 works
                    # 0, 1, 2, 3, 4, 5 -> we can handle 0~3 works
                    temp = float('inf')
                    for idx in range(i, boundary):
                        today = max(jobDifficulty[i:idx+1])
                        future = recur(idx+1, day+1)
                        if today + future < temp:
                            temp = today + future
                    memo[(i, day)] = temp
                    return memo[(i, day)]
                
                return recur(0, 1)
        ```
        
    - top-down 조금 더 빠른 버전
        - base case에 대한 계산을 미리 해놓기
        - 시간을 확 줄인 부분
            - 기존 today: 매 for 문에 대해 `jobDifficulty[i:idx+1]`를 불러오고 여기서 max 값 취함
            - 변경 today: 초기 today를 시작 업무의 난이도로 설정해두고, for 문 돌면서 추가되는 업무 하나만의 난이도를 불러와서 더 큰쪽으로 지속 업데이트 `max(today, jobDifficulty[idx])`
        
        ```python
        class Solution:
            def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
                n = len(jobDifficulty)
                if n < d:
                    return -1 
                # Pre-calculate base cases for efficiency
                hardest_remain = [0] * n
                for i in range(n):
                    hardest_remain[i] = max(jobDifficulty[i:])
        
                memo = {}
                def recur(i, day):
                    # base case
                    if day == d:
                        return hardest_remain[i]
                    # check memoization
                    if (i, day) in memo:
                        return memo[(i, day)]
                    # recurrent relation 
                    boundary = n - (d - day)
                    # 6 works, d = 3, day = 1 -> two days left
                    # need to left at least 2 works
                    # 0, 1, 2, 3, 4, 5 -> we can handle 0~3 works
                    temp = float('inf')
                    today = jobDifficulty[i]
                    for idx in range(i, boundary):
                        today = max(today, jobDifficulty[idx])
                        future = recur(idx+1, day+1)
                        if today + future < temp:
                            temp = today + future
                    memo[(i, day)] = temp
                    return memo[(i, day)]
                
                return recur(0, 1)
        ```
        
    - bottom-up 기본
        
        ```python
        class Solution:
            def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
                n = len(jobDifficulty)
                if n < d:
                    return -1 
                
                # d starts from 1 -> 0th row usage?
                dp = [[0] * n for _ in range(d+1)]
                # base case
                for i in range(n):
                    dp[d][i] = max(jobDifficulty[i:])
                # recurrent relation
                for day in range(d-1, 0, -1):
                    for i in range(n-1, -1, -1):
                        boundary = n - (d - day)
                        temp = float('inf')
                        today = jobDifficulty[i]
                        for idx in range(i, boundary):
                            today = max(today, jobDifficulty[idx])
                            future = dp[day+1][idx+1]
                            if today + future < temp:
                                temp = today + future
                        dp[day][i] = temp
                return dp[1][0]
        ```
        
    - bottom-up editorial
        - dp table 초기값 설정
            - minimum value를 return 해야 하기 때문에 dp matrix 초기화는 float(’inf’)
        - base case
            - dp[d][n-1]과 나머지 dp[d][i] (i: n-2 ~ 0) 을 따로 둠
                - 왜냐면 max(jobDifficulty[i:]) 연산 cost가 많이 들어서 그런 것 같음
            - dp[d][n-1]: 마지막날에 마지막 일에서 시작하는 경우 → 그 일 하나면 하면 되기 때문에 jobDifficulty[-1]
            - 나머지 경우
                - i index가 작아질 수록 왼쪽으로 start index를 한 칸 미는 것과 동일
                - dp table 상으로는 바로 다음 i 에 해당하는 값이 max(jobDifficulty[i+1:]) 일 것 → 그 값과 이번 jobDifficulty[i] 값만 비교하면 max(jobDifficulty[i:]) 연산을 하는 것과 마찬가지
                - dp[d][i] = max(jobDifficulty[i], dp[d][i+1])
        - i (work starting index)도 조금 다름
            - 나는 n-1부터 0까지 다했는데
            - 여기에서는 (day - 1) ~ (n-1)-(d-day)
                - day 앞에 날까지 하루에 한 개씩만 수행했다면
                    - 지금까지 수행한 일의 개수가 (day - 1)
                    - work는 0-index이기 때문에 0, …, (day-2)까지 수행한 상태 → 오늘 day에 시작하게 될 일의 index는 day - 1
                - day까지의 날들에 최대한 몰아서 하고 -하루에 몇 개씩 했는지는 모르겠지만- day 이후의 날들은 하루에 한개씩만 하는 상황 가정
                    - 남은 날 수 : d - day(day inclusive)
                    - 남은 일의 개수
                        - 오늘 어디까지 수행해야 남은 날들에는 일을 한 개씩 할 수 있을까? n - (d - day)가 남겨야 하는 일의 개수
                        - 그럼 오늘 해야 하는 마지막일은 n - (d - day) -1
                            - range에서 stop은 exclusive인 점 고려할 때 n - (d - day) 그대로 넣으면 된다
        
        ```python
        class Solution:
            def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
                n = len(jobDifficulty)
                # If we cannot schedule at least one job per day, 
                # it is impossible to create a schedule
                if n < d:
                    return -1
                
                dp = [[float("inf")] * (d + 1) for _ in range(n)]
                
                # Set base cases
                dp[-1][d] = jobDifficulty[-1]
        
                # On the last day, we must schedule all remaining jobs, so dp[i][d]
                # is the maximum difficulty job remaining
                for i in range(n - 2, -1, -1):
                    dp[i][d] = max(dp[i + 1][d], jobDifficulty[i])
        
                for day in range(d - 1, 0, -1):
                    for i in range(day - 1, n - (d - day)):
                        hardest = 0
                        # Iterate through the options and choose the best
                        for j in range(i, n - (d - day)):
                            hardest = max(hardest, jobDifficulty[j])
                            # Recurrence relation
                            dp[i][day] = min(dp[i][day], hardest + dp[j + 1][day + 1])
        
                return dp[0][1]
        ```
        
- 복잡도 분석
    - 공간
        - bottom-up의 경우 가능한 모든 state 개수와 동일
            - n * d = dp table 크기
        - top-down의 경우 : memo dict의 원소수에 따라 결정됨
            - 특정 argument 조합을 방문하고 결과를 계산해야만 원소가 하나 늘어난다
            - 하루에 최소 하나의 task 수행해야 한다는 restriction 때문에, 실제로 n * d state 전부에 대해 계산을 하게 되는 것은 아니다
            - iteration in the recurrence relation을 보면
                - 우선 모든 날에 대해 돌긴 해야 하니까 d (day)
                - i는 0~n 사이의 모든 수를 다 도는 것은 아니고, 범위가 정해져있음
                    - 최소: day 앞에 날들에 일을 하나씩만 해서 day 번째 날에 일을 시작할 수 있는 가장 빠른 위치
                        - 오늘 날짜 day
                        - 예) 3번째 날. 앞에 1, 2 두 개의 날이 지난 상태 → 6개의 일이 있다면 0, 1개는 했고, 2개부터 시작 = day  - 1
                    - 최대: day 이후의 날들에 일을 한 개씩만 하도록 일을 최소한으로 남겨두는 경우-가능한 가장 오른쪽까지 다 해버리는 경우-
                        - 남은 날 수: d - day = 남겨야 하는 일의 개수
                        - 예) 0, …, 5가 있을 때, 남은 날이 2일이라고 하면, 4, 5를 남겨야 하고, 오늘 할 수 있는 마지막 일의 index는 3 = 6 - (4-2) -1
                        - range stop exclusive 생각하면 n - (d - day)가 마지막에 들어가면 됨
                    - 최대로 가능한 index - 최소로 가능한 index = n  - (d - day) - day = n - d
                        - 0, 1, 2, 3, 4, 5 → n = 6, d = 4 → n - d = 2
                
                ⇒ 모든 날 d * 가능한 일의 start index 개수 n-d = d * (n-d) state를 방문하면 되는 것 
                
                ⇒ top-down의 space complexity도 d * (n-d) 
                
                ↳ d는 양수이기 때문에 n-d < n ⇒ bottom-up의 경우 n * d를 피할 수 없지만, top-down의 경우 n 대신 n-d가 들어와서 space complexity가 훨씬 작다는 것이 장점 
                
        
    - 시간
        - 실제로 방문해야 하는 state 개수 d * (n-d)
        - 각 state에 대해 가능한 recurrent relation explore (j의 iteration)
            - j의 average iteration 횟수
                - range(start, stop) 안의 element 개수 : stop - start
                    - 예) range(1, 4) : 1, 2, 3
                        - 4-1 = 3 → 3개
                - (n - (d - day) - i) 개
                    
                    = n - d + day - i 
                    
                    → day, i 는 loop 돌면서 값이 달라지기 때문에 평균 값으로 대체해야 함 
                    
            - day의 평균 값
                - (d - 1 + 1) / 2 = d/ 2
                    - 예) range(1, 4) : 1, 2, 3
                        - 평균값은 2 = (1 + 3(inclusive end)) / 2 = 4/ 2
            - i의 평균값
                - (n - (d - day) - 1 + day - 1) / 2
                    
                    = (n - d + day - 1 + day - 1) / 2 
                    
                    = (n - d + 2 day) / 2 
                    
                    = (n  - d + 2 * d/2) / 2 = n / 2
                    
            
            ⇒ j의 식에 대입해보면 n - d + d/ 2 - n / 2 = (n - d)/ 2 → 1/2은 상수니까 O 표기법에서 생략되고, 그 결과 j은 O(n-d)의 복잡도를 갖는 것으로 구해짐 
            
        
        → state 개수 * state 별 j의 평균 개수 = d * (n-d)^2