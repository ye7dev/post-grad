# 1473. Paint House III

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP
Created time: January 14, 2024 6:12 PM
Last edited time: January 15, 2024 3:53 PM

- [ ]  Top-down, bottom-up으로 한번씩 다시 풀어보기
- Process
    
    cost[i][j]에서 j가 j+1로 해석되어야 하는 것으로 보아, j의 항목 즉 칠할 수 있는 색깔에 하나가 더 더해져야 할 듯
    
    그건 바로 이미 칠해진 경우인 것 같군! 안 칠하고 넘어가야 하는 경우는 비용이 무조건 0이지 which is cost[i][0]
    
    비용 순으로 쓸 수 있는 색깔을 정렬해야 하려나
    
    이미 칠해진 집의 색깔도 나옴 
    
    연속해서 몇 집을 칠해도
    
    각 집당 그룹을 바꾸는 경우(가능하면) 안바꾸는 경우 두 가지 선택사핟 제시
    
    그룹 수도 킵트랙
    
    그룹 수를 언제 바꿔줘야 하는지 모르겠음
    
    dp 초기화 시에 0과 max cost 중 어느 걸로? 
    
    neighborhood index를 잘 모르겠음. 1부터 시작해야 하는지
    
    아님 0부터 시작해야 하는지? 0은 base case에 들어가나?
    
    base case는 다 모든 이웃에 대해 다했는뎁 ;; 
    
- AC 코드 (🌟🏋️‍♀️)
    - Top-down (직관적)
        - base case를 생각해내는게 어려웠음
        - 집은 m-1 index까지 valid 하지만, recur 함수는 m index에서 base case
            - 더 좁은 범위의 subproblem 값이 앞에 더해지는 것이기 때문에 마지막 base case에서 조건에 부합하면 0을 도달하고 - 끝을 내기 위해
            - 아니면 끝까지 왔는데 조건에 부합하지 않는 다는 의미로 MAX COST return → 이러면 더 상위 값이랑 더해지고 나서 다른 후보들이랑 min을 했을 때 자동으로 제외되는 대상에 포함됨
        
        ```python
        class Solution:
            def minCost(self, houses: List[int], cost: List[List[int]], m: int, n: int, target: int) -> int:
                memo = {}
                MAX_COST = (10 ** 4) * 100 + 1
        
                # function
                def recur(cur_house, num_neigh, prev_color):
                    args = (cur_house, num_neigh, prev_color)
                    # base case
                    if cur_house == m:
                        if num_neigh == target:
                            return 0
                        else: 
                            return MAX_COST
                    if num_neigh > target:
                        return MAX_COST
        
                    # check memoized
                    if args in memo:
                        return memo[args]
                    
                    # already painted
                    if houses[cur_house] != 0:
                        if houses[cur_house] == prev_color:
                            return recur(cur_house+1, num_neigh, prev_color)
                        else:
                            return recur(cur_house+1, num_neigh+1, houses[cur_house])
                    # iteration of recurrence relation
                    min_cost = MAX_COST
                    for c in range(1, n+1):
                        if c != prev_color:
                            temp_cost = cost[cur_house][c-1] + recur(cur_house+1, num_neigh+1, c)
                        else:
                            temp_cost = cost[cur_house][c-1] + recur(cur_house+1, num_neigh, prev_color)
                        min_cost = min(min_cost, temp_cost)
                    
                    # save the results in the memo
                    memo[args] = min_cost
                    return memo[args]
        
                output = recur(0, 0, 0)
                if output == MAX_COST:
                    return -1
                return output
        ```
        
    - Bottom-up (좀 더 어렵고 좀 더 느림)
        - 제일 헷갈렸던 점 - 이미 색칠한 집인데, current color가 색칠된 색과 다른 경우
            - 처음에는 이전 집까지의 누적 비용을 들고 가야 하는 게 아닌가 생각했는데 → 이 경우는 current color가 이미 색칠된 색과 같은 경우에 covered
            - current color가 색칠된 색과 다르면 invalid case
                - 집을 다시 칠할 수 있는 것이 아니기 때문에 i, neighborhood가 고정된 상태에서는 절대 그 색을 그 집에 칠할 수 없다
                - 따라서 MAX_COST로 설정하고 다른 색과 비교할 때 자동으로 min 값이 안되게 해야 하는데 이미 초기값이 그렇게 설정되어 있기 때문에 더 할 게 없다
                - 다만 밑에서 다양한 prev_color일 때의 상황을 가정하고 하는 연산들을 거치지 않고 비효율적인 계산을 아낄 수 있도록 continue문을 color가 바뀔 때마다 넣는 것
        
        ```python
        class Solution:
            def minCost(self, houses: List[int], cost: List[List[int]], m: int, n: int, target: int) -> int:
                MAX_COST = (10 ** 4) * 100 + 1
        
                # array: house * neighborhood * color
                ## neighborhood max value: min(target, m)
                neigh_max = min(target, m)
                dp = [[[MAX_COST] * n for _ in range(neigh_max)] for _ in range(m)]
        
                # base case: first house
                for color in range(n):
                    if houses[0] - 1 == color:
                        dp[0][0][color] = 0 
                    elif houses[0] == 0:
                        dp[0][0][color] = cost[0][color]
                
                # iteration of recurrence relation 
                for i in range(1, m):
                    for j in range(min(i+1, neigh_max)):
                        for color in range(n): 
                            # already painted with different color -> invalid
                            if houses[i] != 0 and houses[i] - 1 != color:
                                continue
                            # painted with the current color 
                            for prev_color in range(n):
                                # new neighbor or not 
                                if color != prev_color:
                                    past_cost = dp[i-1][j-1][prev_color] if j > 0 else MAX_COST
                                else:
                                    past_cost = dp[i-1][j][color]
                                # newly painted or not 
                                if houses[i] != 0:
                                    cur_cost = 0
                                else:
                                    cur_cost = cost[i][color]
                                dp[i][j][color] = min(cur_cost + past_cost, dp[i][j][color])
                
                # get min of the target neighbor
                res = min(dp[m-1][target-1])
                if res == MAX_COST:
                    return -1 
                else:
                    return res
        ```
        
- Trial
    - post-top_down editorial
        - temp_cost에서 현재 집 색칠하는 비용을 더해주는 부분이 빠져서 수정해줌
        - recur에 대한 parameter 초기화 오류 - num_neigh
            - 첫번째 집에 대한 처리가 끝나고 다음 집으로 넘어갈 때 1로 들어가야 함
            - 초기값은 0이 되는 게 맞음
        - MAX_COST 설정 오류
            - house 하나 당 최대 10**4의 색칠 비용을 가질 수 있는데, 집이 100개 정도 되니까 100 * (10 ** 4) + 1이 전체 비용의 upper bound가 된다
        
        ```python
        class Solution:
            def minCost(self, houses: List[int], cost: List[List[int]], m: int, n: int, target: int) -> int:
                memo = {}
                MAX_COST = 10**4 + 1
        
                # function
                def recur(cur_house, num_neigh, prev_color):
                    args = (cur_house, num_neigh, prev_color)
                    # base case
                    if cur_house == m:
                        if num_neigh == target:
                            return 0
                        else: 
                            return MAX_COST
                    if num_neigh > target:
                        return MAX_COST
        
                    # check memoized
                    if args in memo:
                        return memo[args]
                    
                    # already painted
                    if houses[cur_house] != 0:
                        if houses[cur_house] == prev_color:
                            return recur(cur_house+1, num_neigh, prev_color)
                        else:
                            return recur(cur_house+1, num_neigh+1, houses[cur_house])
                    # iteration of recurrence relation
                    min_cost = MAX_COST
                    for c in range(1, n+1):
                        if c != prev_color:
                            temp_cost = cost[cur_house][c-1] + recur(cur_house+1, num_neigh+1, c)
                        else:
                            temp_cost = cost[cur_house][c-1] + recur(cur_house+1, num_neigh, prev_color)
                        min_cost = min(min_cost, temp_cost)
                    
                    # save the results in the memo
                    memo[args] = min_cost
                    return memo[args]
        
                output = recur(0, 0, 0)
                if output == MAX_COST:
                    return -1
                return output
        ```
        
    - post-bottom_up editorial
        - dp init 시에 neighborhood dim : target + 1
        - cell value는 max cost로 초기화 하는 것 맞았음
        - base case 설정 오류
            - 첫번째 집이 이미 색칠된 경우를 고려하지 않음
            - base case는 neighborhood가 1인 경우에 한정됨
        - why `if houses[house] != 0 and color != houses[house]:
        continue` → cell value stays as in the initialization?
            
            
        
        ```python
        class Solution:
            def minCost(self, houses: List[int], cost: List[List[int]], m: int, n: int, target: int) -> int:
                MAX_COST = (10 ** 4) * 100 + 1
        
                # array: house * neighborhood * color
                ## neighborhood max value: min(target, m)
                neigh_max = min(target, m)
                dp = [[[MAX_COST] * n for _ in range(neigh_max)] for _ in range(m)]
        
                # base case: first house
                for j in range(neigh_max):
                    for k in range(n):
                        dp[0][j][k] = cost[0][k]
                
                # iteration of recurrence relation 
                for i in range(1, m):
                    for j in range(neigh_max):
                        for color in range(n): 
                            for prev_color in range(n):
                                if color != prev_color:
                                    past_cost = dp[i-1][j-1][prev_color]
                                else:
                                    past_cost = dp[i-1][j][color]
                                if houses[i] != 0:
                                    cur_cost = 0
                                else:
                                    cur_cost = cost[i][color]
                                dp[i][j][color] = cur_cost + past_cost 
                
                # get min of the target neighbor
                res = min(dp[-1][-1])
                if res == MAX_COST:
                    return -1 
                else:
                    return res
        ```
        
- Editorial
    - Overview
        - A continuous group of houses with the same color is considered a single neighborhood.
        - 집들을 돌면서 안 칠해진 집에는 무슨 색을 칠해줄 것인지 결정해야
            - 최적의 선택은 이전 집을 무슨 색으로 칠했는지에 따라 달라짐
            - 이전 집과의 색깔이 일치하면 neighborhood 수가 유지되지만, 그렇지 않으면 1 증가
            
            → each decision we make is affected by the previous decisions we have made.
            
        - 모든 unpainted house를 최소로 칠할 수 있는 비용을 구해야
        
        ⇒ previous state에 대한 dependency가 & optimum = DP 
        
    - **Approach 1: Top-Down Dynamic Programming**
        - Intuition
            - 첫번째 집
                - 이미 색칠되었으면 더 할 거 없고 다음 집으로 넘어감
                - 그렇지 않으면 1~n 사이 색에 대한 각각의 비용을 치러야 색칠 가능
                - neighborhood 개수도 세야 함 `neighborhoodCount`
                - 이전 집과의 색깔 비교
                    - matching color가 아니면 neighbor 개수 1 증가
            - 재귀적으로 다음 집 이동, update values
                - 모든 집을 다 순회한 다음 neighbor이 target에 도달하면, 지금까지의 min cost를 비교
            - parameter
                - index of the house
                - count of neighborhoods
                - keep track of the previous hose color
        - Algorithm
            1. init parameters
                - current index : 0, current number of neighborhoods 0, previous house color 0
                    - 첫번째 집은 늘 새로운 neighborhood의 시작이기 때문에, previous house color는 0에서 시작
            2. 이미 색칠된 집의 경우
                - 이전 집과 색이 다르면 neighborhood 개수는 하나 증가
                - 재귀적으로 다음 집으로 이동
            3. 아직 색칠되지 않은 집의 경우
                - 1부터 n까지 돌면서 현재 집을 특정 색깔로 칠해보기
                - 그리고 recursively move on to the next house with updated values
                - min cost 변수에 1부터 n까지 색 중 가장 낮은 cost 저장
            4. min cost를 memo에 저장. 이 때 key는 함수에서 들고 다니는 세 가지 parameters
            5. base cases
                - 모든 집을 다 돈 상황에서
                    - neighborhood 개수가 target과 같다면 cost 0 return
                    - 그렇지 않으면 max cost return
                - 집을 다 돌기 전이라도 neighborhood 개수가 target보다 커지면 max cost return
                    
                    
        
    - **Approach 2: Bottom-Up Dynamic Programming**
        - Intuition
            - base case → initial query
            - initial query break
                - initial query: house개의 집을 neigh개의 neighborhood로 색칠하는 데 드는 최소 비용을 구하고자 한다
                - 하나의 집에 대해서는 n개의 색칠 옵션이 있음
                - 각 색깔 하나하나에 대해서는 두 가지 지나리오가 존재
                    - house i가 이미 색칠되어 있는 경우 - 그리고 색칠된 색깔이 이번 iteration color랑 일치하지 않는 경우
                        
                        → 이미 색칠된 집에 대해서는 할일이 없으므로 아무것도 안해도 됨 
                        
                    - 아직 집이 색칠되지 않은 경우 or 이미 색칠되어 있는데 이번 iteration color와 일치하는 경우
                        - 집이 아직 색칠되지 않은 경우
                            - corresponding cost로 이번 iteration color를 house에 색칠
                        - 이미 색칠된 경우는 corresponding cost 0
                - we must iterate over all of the color options (`prevColor`) for the previous house to do so.(?)
                    - 현재 color ≠ prev_color
                        
                        → subproblem은 `house-1, neighborhoods-1, prevColor`
                        
                    - 현재 color = prev_color
                        
                        → subproblem은 `house-1, neighborhoods, color`
                        
                - base case
                    - 첫번째 집 - neighborhood는 1개, 모든 색깔에 대해 상응하는 비용을 가지고 집을 칠할 수 있음
                - 모든 조합의 집, 색, neighborhood에 대해 다 구한 다음에 거기서 neighborhood = target일 때의 최소 값을 구하면 됨
                    - `dp[m-1][target]`
        - Algorithm
            1. base case에 대한 parameter 초기화
                - house = 0, neighbor = 1
                - 1부터 n까지의 color 돌면서 상응하는 가격을 부여
                    - min cost만 남기는 거겠지?
                - 만약 이미 색칠되어 있으면 cost를 0으로 설정
            2. 1부터 m-1까지의 집을 돌고, neighborhood는 1부터 min(house+1, target) 
                - 0-index house에서 house+1은 maximum number of neighborhoods possible(?)
                - 1~n까지 색깔에 대해
                    - 이미 색칠이 되어 있고, 이번 color와 색이 같지 않은 경우 continue
                    - current parameter에 대한 비용 `cur_cost`를 MAX_COST로 초기화
                    - previous house에 대한 color option `prev_color`를 1부터 n까지 돌면서
                        - 참고로 색깔에 대한 비용을 가져올 때는 색깔값에서 1 빼서 index로 사용한다
                        - `color != prev_color`
                            - cur_cost = dp[house-1][neighborhoods-1][prev_color-1]
                        - `color = prev_color`
                            - cur_cost = dp[house-1][neighborhood][color-1]
                        - `cost_to_paint` 현재 집을 칠하는 데 드는 비용
                        
                        ⇒ cur_cost랑 cost_to_paint를 더해서 dp[house][neighborhood][color-1]에 넣어준다 
                        
            3. neighborhood 값이 target인 상황에서 최소 값을 구한다