# 1402. Reducing Dishes

Created time: May 24, 2024 4:17 PM
Last edited time: May 24, 2024 9:02 PM

- 결국 bottom-up에서 왜 그렇게 어려웠냐 하면…
    
    time은 1부터 시작하고, 점화식에서 건너 뛸 수 없다 
    
    index는 0부터 시작하고, 점화식에서 건너 뛸 수 있다
    
    근데 점화식에서 보면 막상 index를 건너 뛰는 건 time의 index를 그대로 두는 것과 다름 없고 
    
    - 다음 요리를 같은 시간에 시작하기 때문에 
    
- 문제 이해
    
    satisfaction[i]: i번째 요리에 대한 만족도
    
    - 음수 일수 있다
    
    모든 요리는 1단위 시간에 완성 가능
    
    요리 i에 대한 like-time coefficient: 요리 i와 그 전까지의 요리를 하는 데 들었던 시간 = time[i] * satisfaction[i]
    
    일정 개수의 요리를 준비하고 난 뒤, 쉐프가 달성할 수 있는 max sum of like-time coefficient는? 
    
    `satisfaction = [-1,-8,0,5,-9]`
    
    -1*1 =-1
    
    -8*2 = -16 → remove
    
    0*2 = 0
    
    5*3=15
    
    -9*4=-36
    
    접시 순서도 고려해야 함;;; 
    
- Trial
    - Top-down (1) : 예제 1개만 맞음
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                n = len(satisfaction)
                # early exit
                if min(satisfaction) >= 0:
                    return sum([satisfaction[i]*(i+1) for i in range(n)])
                if max(satisfaction) < 0:
                    return 0
        
                memo = {}
                def recur(time, dish_idx):
                    # check memo
                    state = (time, dish_idx)
                    if state in memo:
                        return memo[state]
                    # base case
                    if dish_idx == n-1:
                        return time * satisfaction[dish_idx]
                    # recursive case
                    ## take this dish
                    take = time * satisfaction[dish_idx] + recur(time+1, dish_idx+1)
                    ## skip this dish
                    skip = recur(time, dish_idx+1)
                    memo[state] = max(take, skip)
                    return memo[state]
                
                ans = recur(1, 0)
                print(memo)
                return ans
        
                
        ```
        
    - Top-down(2): sorting 했더니 예제 다 맞고 51/60에서 시간 초과
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
                # early exit
                if min(satisfaction) >= 0:
                    return sum([satisfaction[i]*(i+1) for i in range(n)])
                if max(satisfaction) < 0:
                    return 0
        
                memo = {}
                def recur(time, dish_idx):
                    # check memo
                    state = (time, dish_idx)
                    if state in memo:
                        return memo[state]
                    # base case
                    if dish_idx == n-1:
                        return time * satisfaction[dish_idx]
                    # recursive case
                    ## take this dish
                    take = None
                    for j in range(dish_idx+1, n):
                        if take is None:
                            take = recur(time+1, j)
                        else:
                            take = max(take, recur(time+1, j))
                    take += time * satisfaction[dish_idx] 
                    ## skip this dish
                    skip = recur(time, dish_idx+1)
                    memo[state] = max(take, skip)
                    return memo[state]
        
                return recur(1, 0)
        
                
        ```
        
    - Bottom-up(1): 50/60에서 시간초과. 예제에서는 답이 더 빨리 나왔는데
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
                # early exit
                if min(satisfaction) >= 0:
                    return sum([satisfaction[i]*(i+1) for i in range(n)])
                if max(satisfaction) < 0:
                    return 0
        
                dp = [[-float('inf')] * (n+1) for _ in range(n+1)]
                # state dp[i][j-1]: time이 i, dish_idx가 j일 때 누적 만족도
                # return: max(dp[i][-1] for i in range(n+1)) 
                ans = -float('inf')
                # base case 
                dp[0][0] = 0
                for j in range(1, n+1):
                    dp[0][j] = 0
                    dp[1][j] = satisfaction[j-1] # 0~n-1
                    ans = max(ans, dp[0][j], dp[1][j])
                # recursive case
                for time in range(2, n+1):
                    for dish_idx in range(1, n+1):
                        # skip
                        dp[time][dish_idx] = dp[time][dish_idx-1]
                        cur_dish = time * satisfaction[dish_idx-1]
                        # take 
                        for prev_idx in range(dish_idx):
                            dp[time][dish_idx] = max(dp[time][dish_idx], dp[time-1][prev_idx] + cur_dish)
                        ans = max(ans, dp[time][dish_idx])
                return ans 
        
        ```
        
- AC 코드
    - Top-down
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
        
                memo = {}
                def recur(time, dish_idx):
                    # check memo
                    state = (time, dish_idx)
                    if state in memo:
                        return memo[state]
                    # base case
                    if dish_idx == n:
                        return 0
                    # recursive case
                    ## take this dish
                    take = time * satisfaction[dish_idx] + recur(time+1, dish_idx+1)
                    ## skip this dish
                    skip = recur(time, dish_idx+1)
                    memo[state] = max(take, skip)
                    return memo[state]
        
                return recur(1, 0)
        
                
        ```
        
    - Bottom-up (solution)
        - time은 건너뛸 수 없음. dish만 건너뛸 수 있음
        - time을 바깥 for loop으로 두면 답이 틀려진다 - 현재 dp table에서 행이 index고, time이 column이기 때문에
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
                
                # dp 배열 초기화
                dp = [[0] * (n + 2) for _ in range(n + 1)]
                
                # 역순으로 dp 배열 채우기
                for index in range(n - 1, -1, -1):
                    for time in range(1, n + 1):
                        # 현재 요리를 선택하는 경우
                        take = satisfaction[index] * time + dp[index + 1][time + 1]
                        # 현재 요리를 선택하지 않는 경우
                        skip = dp[index + 1][time]
                        # 최대값 저장
                        dp[index][time] = max(take, skip)
                
                return dp[0][1]
        
        ```
        
        - state definition
            - `dp[i][j]`는 i번째 요리부터 시작하여 j번째 시간 단위에 요리를 시작했을 때의 최대 만족도를 의미
                
                → return 값
                
        - base case
            - `dp[n][time] = 0`는 모든 요리를 다 고려한 후에는 추가적인 만족도가 없다는 것을 나타냅니다.
        - 해결 안됐던 것
            - 왜 정렬 상태는 index가 클 수록 값이 큰데,
            - time은 왜 작은 값 부터 시작하는가? 요리도 시간도 큰 값끼리 곱해야 만족도가 높은 거 아닌가?
            - 흐름을 보면 cumulative sum임
                
                // at i = n-1 i.e 4 -> Cumulative_sum = 0, and cur = 5 (5*1) = 5
                // at i = 3 -> Cumulative-sum = 5, and cur = 5 + 5 + 0 (0*1 + 5*2) = 10
                // at i = 2 -> Cumulative-sum = 5 (5 + 0), and cur = cur + Cumlative_sum + satis[i] = (10 + 5 + -1) = -1*1 + 0*2 + 5*3 = 14
                // at i = 1 -> Cumulative-sum = 4 (5 + 0 + -1), and cur = cur + Cumlative_sum + satis[i] = (14 + 4 + -8) = -8*1 + -1*2 + 0*3 + 5*5= 14
                // And similarly for i = 0 and and max of all currents is printed
                
    - My bottom-up
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
        
                dp = [[-float('inf')] * (n+1) for _ in range(n+1)]
                # state dp[i][j-1]: time이 i, dish_idx가 j일 때 누적 만족도
                # return: max(dp[i][-1] for i in range(n+1)) 
                # base case 
                dp[0][0] = 0
                for j in range(1, n+1):
                    dp[0][j] = 0
                    dp[1][j] = satisfaction[j-1] # 0~n-1
                # recursive case
                for time in range(2, n+1):
                    for dish_idx in range(1, n+1):
                        # skip
                        dp[time][dish_idx] = dp[time][dish_idx-1]
                        cur_dish = time * satisfaction[dish_idx-1]
                        dp[time][dish_idx] = max(dp[time][dish_idx], dp[time-1][dish_idx-1] + cur_dish)
                ans = max([dp[i][-1] for i in range(n+1)])
                return ans 
        ```
        
    - 솔루션에서 진행 방향만 나란하게 이동하도록 맞춘 답
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
                
                # dp 배열 초기화
                dp = [[0] * (n + 2) for _ in range(n + 1)]
                
                # 역순으로 dp 배열 채우기
                for index in range(n - 1, -1, -1):  # 요리의 역순
                    for time in range(n, 0, -1):  # 시간의 역순
                        # 현재 요리를 선택하는 경우
                        take = satisfaction[index] * time + dp[index + 1][time + 1]
                        # 현재 요리를 선택하지 않는 경우
                        skip = dp[index + 1][time]
                        # 최대값 저장
                        dp[index][time] = max(take, skip)
                
                return dp[0][1]
        ```
        
    - time을 n 넘지 않도록 하는 방법-dp row 개수도 n+1
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
        
                satisfaction.sort()
                n = len(satisfaction)
                
                # dp 배열 초기화
                dp = [[0] * (n + 1) for _ in range(n + 1)]
                
                # 역순으로 dp 배열 채우기
                for index in range(n - 1, -1, -1):  # 요리의 역순
                    for time in range(n, 0, -1):  # 시간의 역순
                        # 현재 요리를 선택하는 경우
                        if time + 1 <= n:  # 배열 범위 내에 있는지 확인
                            take = satisfaction[index] * time + dp[index + 1][time + 1]
                        else:
                            take = satisfaction[index] * time  # 현재 요리만의 만족도 계산
                        
                        # 현재 요리를 선택하지 않는 경우
                        skip = dp[index + 1][time]
                        
                        # 최대값 저장
                        dp[index][time] = max(take, skip)
                
                return dp[0][1]
        
        ```
        
    - 더 최적화하면 time은 index를 넘을 수 없다
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
                
                # dp 배열 초기화
                dp = [[0] * (n + 1) for _ in range(n + 1)]
                
                # 역순으로 dp 배열 채우기
                for index in range(n - 1, -1, -1):  # 요리의 역순
                    for time in range(index, -1, -1):  # time은 index보다 클 수 없음
                        # 현재 요리를 선택하는 경우
                        take = satisfaction[index] * (time + 1) + dp[index + 1][time + 1]
                        
                        # 현재 요리를 선택하지 않는 경우
                        skip = dp[index + 1][time]
                        
                        # 최대값 저장
                        dp[index][time] = max(take, skip)
                
                return dp[0][0]
        ```
        
    - time은 1과 n 사이 범위에 있게 하려면
        
        ```python
        class Solution:
            def maxSatisfaction(self, satisfaction: List[int]) -> int:
                satisfaction.sort()
                n = len(satisfaction)
                
                # dp 배열 초기화
                dp = [[0] * (n + 2) for _ in range(n + 1)]
                
                # 역순으로 dp 배열 채우기
                for index in range(n - 1, -1, -1):  # 요리의 역순
                    for time in range(index+1, 0, -1):  # time은 index보다 클 수 없음
                        # 현재 요리를 선택하는 경우
                        take = satisfaction[index] * time + dp[index + 1][time + 1]
                        
                        # 현재 요리를 선택하지 않는 경우
                        skip = dp[index + 1][time]
                        
                        # 최대값 저장
                        dp[index][time] = max(take, skip)
                
                return dp[0][1]
        ```