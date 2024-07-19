# 1463. Cherry Pickup II

Status: done, in progress
Theme: DP
Created time: March 12, 2024 11:58 AM
Last edited time: March 12, 2024 1:37 PM

- AC 코드
    - Top-down
        
        ```python
        class Solution:
            def cherryPickup(self, grid: List[List[int]]) -> int:
                nrow, ncol = len(grid), len(grid[0])
                directions = [-1, 0, 1]
                memo = {}
                def to_next_cell(r, c1, c2):
                    # check memo
                    state = (r, c1, c2)
                    if state in memo:
                        return memo[state]
                    # base case
                    if c1 < 0 or c1 >= ncol:
                        return 0
                    if c2 < 0 or c2 >= ncol:
                        return 0
        
                    cur_crop = grid[r][c1] + grid[r][c2]
                    if c1 == c2:
                        cur_crop /= 2 
                    if r == nrow-1:
                        return cur_crop
        
                    max_crop = 0
                    # recursive case 
                    for d1 in directions:
                        for d2 in directions:
                            next_crop = to_next_cell(r+1, c1+d1, c2+d2)
                            if max_crop < next_crop:
                                max_crop = next_crop
                    
                    memo[state] = cur_crop + max_crop
                    return memo[state]
        
               
                return to_next_cell(0, 0, ncol-1)
        
                    
        
                
        ```
        
    - Bottom-up (🐌)
        
        ```python
        class Solution:
            def cherryPickup(self, grid: List[List[int]]) -> int:
                nrow, ncol = len(grid), len(grid[0])
                directions = [-1, 0, 1]
                dp = [[[0] * ncol for _ in range(ncol)] for _ in range(nrow)]
        
                # base case: bottom row
                for i in range(ncol):
                    for j in range(ncol):
                        if i == j:
                            dp[nrow-1][i][j] = grid[nrow-1][i]
                        else:
                            dp[nrow-1][i][j] = grid[nrow-1][i] + grid[nrow-1][j]
                # transition 
                for r in range(nrow-2, -1, -1):
                    for i in range(ncol):
                        for j in range(ncol):
                                for d1 in directions:
                                    if i + d1 < 0 or i + d1 >= ncol:
                                        continue 
                                    for d2 in directions:
                                        if j + d2 < 0 or j+ d2 >= ncol:
                                            continue 
                                        dp[r][i][j] = max(dp[r][i][j], dp[r+1][i+d1][j+d2])
                                dp[r][i][j] += grid[r][i]
                                if i != j:
                                    dp[r][i][j] += grid[r][j]
                return dp[0][0][-1]
        
        ```
        
- 과정
    - sequentially 두 robot을 운영한다고 하면, 앞선 로봇이 체리를 따간 자리를 0으로 만들어야 하는데 → 동시에 움직인다
    - 그냥 dp 방식으로 하면 어떻게 추적해야 할지 모르겠음 → 추적 안해도 되고 두 로봇이 같은 자리에 있으면 한 cell만 더해준다
    - visited 처리는 어떻게?
- Trial
    - memoization + dfs → 예제 1
        
        ```python
        class Solution:
            def cherryPickup(self, grid: List[List[int]]) -> int:
                nrow, ncol = len(grid), len(grid[0])
                directions = [(1, -1), (1, 0), (1, 1)]
                memo = {}
                def to_next_cell(r, c):
                    # check memo
                    if (r, c) in memo:
                        return memo[(r, c)]
                    # base case
                    if r == nrow or c == ncol:
                        return 0
                    cur_crop = grid[r][c]
                    max_crop = 0
                    max_next = (0, 0)
                    # recursive case 
                    for d in directions:
                        next_cell = (r+d[0], c+d[1])
                        next_crop = to_next_cell(next_cell[0], next_cell[1])
                        if max_crop < next_crop:
                            max_crop = next_crop
                            max_next = next_cell
                    
                    memo[(r, c)] = cur_crop + max_crop
                    # mark as visited 
                    grid[r][c] = 0
                    return memo[(r, c)]
        
                robot1 = to_next_cell(0, 0)
                robot2 = to_next_cell(0, ncol-1)
                return robot1 + robot2
        ```
        
        - robot1, 2 자리를 바꾸면 답이 달라지나?
            - 달라진다. 훨씬 크게 나온다
- Editorial
    - **Approach #1: Dynamic Programming (Top Down)**
        - robot1, 2 순서 상관 없다고 함
        - 그치만 DP에 적절한 순서가 필요
            - robot1을 먼저 bottom row로 보내고 robot2를 보내는 방법
                - robot1의 이동이 robot2에 영향
                - 여기에 DP를 적용하려면 robot1의 전체 track을 하나의 state로 일일히 다 기록해야 함 → subproblem 개수가 너무 많음
        - robot 두 개를 동시에 이동시키기
            - dp state: (row1, col1, row2, col2)
                - (row1, col1) : robot1의 위치, (row2, col2): robot2의 위치
                - 동시에 움직이면 늘 같은 row에 위치하게 됨
                    - 모두 최상단 row에서 시작하고 row 이동 방향은 아래로 밖에 없으므로
                    
                    → state 구성하는 변수를 하나 줄일 수 있음 
                    
                
                ⇒ (row, col1, col2)
                
                - robot1이 저 위치, robot2가 저 위치에서 시작할 때 딸 수 있는 최대 체리 개수
        - recur function 정의
            - base case
                - robot1, robot2가 최하단 row에서 시작하는 경우 → 더 이동 불가 → 현재 있는 cell에서 체리 따는 수밖에
                    - 만약 두 로봇이 같은 cell에 있는 경우 체리 개수를 두번 카운트 하지 않도록 주의
            - recursive case
                - 미래에(더 전진해서) 따게 될 체리 개수 중 최대를 더해야 함
                - 각 robot이 하나의 cell에서 갈 수 있는 방향은 총 3개이고, 두 로봇이 동시에 움직이기 때문에 3 * 3 = 9의 가능한 state가 있는 셈
                    - 이 중에 max cherries를 얻을 수 있는 옵션을 고르면 됨
                - row는 언제나 + 1
    - **Approach #2: Dynamic Programming (Bottom Up)**
        - 3차원 array
            - state: dp[row][col1][col2]
            - 로봇이 각자들 자리에서 체리 따기 시작할 때 얻을 수 있는 최대 체리 개수
            - 로봇 두 개는 동시에 움직임 → 항상 같은 row에 존재
        - base case
            - bottom row에 있을 때 - current cell에 있는 체리 개수만 세면 됨
            - iteration은 bottom row → top row
            - 공간 절약 하려면 두 Row만 가지고 움직여도 됨
        - transition
            - 미래에 따게 될 체리 개수 중 가장 큰 값