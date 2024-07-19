# 2742. Painting the Walls

Status: in progress, with help, 🏋️‍♀️
Theme: DP
Created time: November 29, 2023 12:41 PM
Last edited time: November 30, 2023 6:08 PM

- [ ]  처음부터 다시 짜기
- 문제 이해
    
    paid painter는 i번째 벽을 칠하는 time, cost 고정
    
    free painter는 어느 벽이던 시간 1, cost 0로 칠할 수 있음 
    
    둘 다 각각 한 명씩이고 free painter는 paid painter가 일하고 있을 때만 데려다가 쓸 수 있음
    
    n개의 벽을 칠하는 데 드는 가장 적은 비용을 계산 하라 
    
- 과정
    
    free painter를 쓰는 게 여러모로 개이득이네
    
    그니까 paid painter는 시간이 가장 오래 걸리는 걸로 해두고 그 사이에 free painter를 데려다가 최대한 맣은 벽을 칠하게 하는 게 유리함 
    
    ```python
    class Solution:
        def paintWalls(self, cost: List[int], time: List[int]) -> int:
            n = len(cost)
            spec_dict = {}
            for i in range(n):
                spec_dict[i] = cost[i]
            sorted_spec = sorted(spec_dict.items(), key=lambda item: item[1])
            left, right = 0, n-1
            cost = 0
            while left < right:
                cost += sorted_spec[left][1]
                cur_time = time[sorted_spec[left][0]]
                while cur_time > 0:
                    right -= 1 
                    cur_time -= 1
                left += 1 
            return cost
    ```
    
    - 이 코드가 안 먹히는 경우-비용이 좀 더 비싸도 시간이 2개이면, 그 사이에 free painter는 다른 2개를 해치워버릴 수 있음. 그러니까 남은 2개의 합이 더 긴 시간에 대한 비용보다 더 크면, 당장 더 싸고 짧은 거 대신 더 길고 비싼 걸 사는게 맞음
- Editorial
    - Top-down
        - paid painter를 돈이 덜 들고 시간은 가장 오래 걸리는 벽으로 보내는 게 이득 -그 사이에 free painter를 최대한 많이 써서 많은 벽을 칠하도록
        - paid painter가 i번째 벽을 cost[i]와 time[i]로 칠하고 있는 동안…
            - free painter는 time[i]개의 벽을 0원에 칠해주고 있음
            
            → cost[i]로 1+time[i]개의 벽을 칠하는 셈 
            
        - `dp(i, remain)` : walls[i..n-1] 중에서 remain 개의 벽을 칠하는 데 드는 최소 비용
            - remain ≤0 → 이미 다 칠한 상태라서 비용은 0
            - i == n → 유료 화가를 배치할 수 있는 벽이 더 이상 없는 상태 → ∞ return
        - transition: 이번 벽을 위해 유료 화가를 고용하거나 하지 않거나
            - 고용: cost[i]가 더해지고 칠할 수 있는 벽은 1+times[i]
                
                → `cost[i] + dp(i+1, remain-times[i]-1)`
                
            - 고용 안 하면 index만 옮김
                - remain이 그대로라서 칠해야 하는 벽의 개수는 유지됨
                
                → `dp(i+1, remain)`
                
            - 둘 중에 더 작은 값이 `dp(i, remain)`
        
- Editorial 보고 짠 코드
    - top-down
        
        ```python
        class Solution:
            def paintWalls(self, cost: List[int], time: List[int]) -> int:
                n = len(cost)
                @cache
                def dp(i, remain):
                    if remain <= 0:
                        return 0
                    if i == n:
                        return float('inf')
                    hire = cost[i] + dp(i+1, remain-1-time[i])
                    dont = dp(i+1, remain)
                    return min(hire, dont)
                
                return dp(0, n)
        ```
        
    - bottom-up
        
        ```python
        class Solution:
            def paintWalls(self, cost: List[int], time: List[int]) -> int:
                n = len(cost)
                dp = [[0] * (n+1) for _ in range(n+1)]
                for i in range(1, n+1): # no more walls
                    dp[n][i] = float('inf')
        
                for i in range(n-1, -1, -1):
                    for j in range(1, n+1):
                        hire = cost[i] + dp[i+1][max(0, j-1-time[i])]
                        dont = dp[i+1][j]
                        dp[i][j] = min(hire, dont)
                
                return dp[0][n]
        ```
        
    - 사설 풀이 bottom-up
        - 좀 더 직관적임
        
        ```python
        class Solution:
            def paintWalls(self, cost: List[int], time: List[int]) -> int:
                n = len(cost)
                dp = [float('inf')] * (n+1)
                dp[0] = 0 # no cost for painting no walls
        
                for painter in range(n):
                    for j in range(n, 0, -1):
                        dp[j] = min(dp[j], dp[max(0, j-1-time[painter])] + cost[painter])
            
                return dp[n]
        ```