# 265. Paint House II

Status: done, in progress
Theme: DP
Created time: January 14, 2024 11:28 AM
Last edited time: January 14, 2024 6:12 PM

- [x]  O(nk) solution check
- AC 코드 (🪇)
    
    ```python
    class Solution:
        def minCostII(self, costs: List[List[int]]) -> int:
            n, k = len(costs), len(costs[0])
            # array
            dp = costs.copy()
            # base case: the first house has no restrctions on color choice
            ## automatically covered
    
            '''
            # save the first and second minimums 
            minimums = []
            for i in range(n):
                sorted_row = sorted(costs[i]) # klogk ...
                minimums.append([sorted_row[:2]])
            '''
    
            # recurrence relation
            for i in range(1, n):
                for c in range(k):
                    dp[i][c] += min(dp[i-1][:c]+dp[i-1][c+1:])
    
            return min(dp[-1])
    ```
    
- O(nk) solution
    - 직전에 칠한 집 기준 min_color, second_color update
        - min_color가 아직 없거나, min_color보다 더 적은 비용으로 칠할 수 있는 color가 나타나면
            - second_min_color를 기존 min_color로 update
                - min_color가 아직 없는 상태였으면 second_min_color가 None이 됨
            - min_color는 현재 color로 update
        - second_color가 아직 none이거나 second color보다 더 적은 비용으로 칠할 수 있는 color가 나타나면
            - second_color를 현재 color로 update
            - min_color에 대한 filtering이 먼저이기 때문에 min_color보다 작은 값이 second_color가 될 걱정은 안해도 됨
    - 현재 집에 최소 비용으로 색칠하기
        - 현재 집에 min_color 칠하는 경우
            - 이전 집과 min_color 연속으로 칠할 수 없기 때문에, 두번째로 비용이 적은 second_color를 직전 집에 칠한 비용에 현재 칠하는 비용을 누적
        - 현재 집에 min_color 말고 다른 색깔을 칠하는 경우
            - 가장 비용이 적은 min_color를 이전 집에 칠한 경우의 비용에 현재 칠하는 비용을 누적
    - 정답은 마지막 집에 칠할 수 있는 모든 색깔을 칠하고 나서의 누적 비용 중 최소
    
    ```python
    class Solution:
        def minCostII(self, costs: List[List[int]]) -> int:
    
            n = len(costs)
            if n == 0: return 0
            k = len(costs[0])
    
            for house in range(1, n):
                # Find the colors with the minimum and second to minimum
                # in the previous row.
                min_color = second_min_color = None
                for color in range(k):
                    cost = costs[house - 1][color]
                    if min_color is None or cost < costs[house - 1][min_color]:
                        second_min_color = min_color
                        min_color = color
                    elif second_min_color is None or cost < costs[house - 1][second_min_color]:
                        second_min_color = color
                # And now update the costs for the current row.
                for color in range(k):
                    if color == min_color:
                        costs[house][color] += costs[house - 1][second_min_color]
                    else:
                        costs[house][color] += costs[house - 1][min_color]
    
            #The answer will now be the minimum of the last row.
            return min(costs[-1])
    ```