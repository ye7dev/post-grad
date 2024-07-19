# 1631. Path With Minimum Effort

Status: done, in progress, with help, 🏋️‍♀️, 💎
Theme: graph
Created time: December 27, 2023 4:43 PM
Last edited time: January 2, 2024 5:34 PM

- [ ]  DFS, UF 복잡도 분석
- [ ]  
- 문제 이해
    - 어떤 경로의 effort: 그 경로에서 연속으로 위치한 두 cell의 높이 절대값 차 중 가장 큰 값
    - single source (0, 0) → (r-1, c-1)
    - 음수 weight도 존재. 그렇다면 다익스트라는 못 쓴다, BFS도 못쓴다
    - 남은 건 벨만 포드. k번의 제약은 없기 때문에 optimized version 사용 가능. SPFA도 사용 가능할지도?
    - 헷갈린다 effort 자체는 path 내에서 최대 차인데, 여러 path 중에 최대 차가 가장 작을 때의 값을 구하라는 건데…우선 나머지는 그대로 하고 거리 구하는 것만 max로 해서 짜본다
- Trial
    - 예제 3개 맞힘
    - 새로운 path: 0 → x, y → new_x, new_y
        - 기존 path에서의 min_effort 값(min_effort[new_x][new_y]이 아직 없거나 새로운 path 값보다 크면, 더 작은 값으로 update)
        - 새로운 path의 대표값: 0~x,y까지 오면서 두 개의 연속된 cell 사이의 절대값 높이 차 최대값 vs. x,y와 다음 cell인 new_x, new_y 사이의 절대값 높이 차, 둘 중에 더 큰 값이 된다
    
    ```python
    class Solution:
        def minimumEffortPath(self, heights: List[List[int]]) -> int:
            directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
            nrow, ncol = len(heights), len(heights[0])
            self.max_so_far = float('inf') # why put self?
    
            def dfs(x, y, max_diff):
                if x == nrow-1 and y == ncol-1: # reach dst 
                    # 도달지점이 dst인 경로 중 min_effort
                    self.max_so_far = min(self.max_so_far, max_diff)
                    return max_diff # 왜 max_diff를 return? max_so_far 값을 update 해두고서는?
                cur_height = heights[x][y]
                heights[x][y] = 0 # marking as visited 
    
                min_effort = float('inf')
                for d in directions:
                    new_x, new_y = x + d[0], y + d[1]
                    if 0 <= new_x < nrow and 0 <= new_y < ncol:
                        if heights[new_x][new_y] == 0: # already visited
                            continue
                        cur_diff = abs(heights[new_x][new_y] - cur_height)
                        max_cur_diff = max(max_diff, cur_diff)
                        if max_cur_diff < self.max_so_far: 
                            res = dfs(new_x, new_y, max_cur_diff)
                            min_effort = min(min_effort, res)
                
                # backtrack
                heights[x][y] = cur_height
    
                return min_effort 
            
            return dfs(0, 0, 0)
    ```
    
- Editorial
    - **Brute Force using Backtracking**
        - Intuition
            - src → dst 모든 가능한 경로를 순회. 가장 effort가 작은 path를 track
            - 모든 가능한 경로를 순회? backtracking!
                - DFS 사용해서 점진적으로 candidate building
                - 중간에 이 candidate이 조건을 만족하지 못하면 backtrack
            1. Choose
                - 임의의 candidate 선택
                    - 주어진 cell에 대해서, 4방으로 붙어 있는 cell이 임의의 candidate
            2. Constraint
                - 선택된 candidate이 만족해야 하는 제약사항 정의
                - 우리 문제에서의 validity
                    - matrix 범위 안에 있으면서 아직 방문되지 않은 cell
            3. Goal
                - required solution을 찾았는지 여부를 결정하는 목표를 정의
                - 우리 문제에서의 goal
                    - 목적지 cell에 도달하는 것
                    - 목적지 cell에 도착하자마자 maximum abosolute difference 를 track 해야 하고, backtrack
            - 일단 src → dst 경로를 찾고 나면, 그 path에 있는 all adjacent cells의 maximum absolute difference를 track ⇒ `maxSoFar` 변수에 저장 ⇒ 다른 path를 탐색할 때 maxSoFar보다 크거나 같은 maximum absolute difference를 가진 path는 피할 수 있음
                
                = src → dst 경로를 찾았다면, 우리는 그보다 적은 노력을 가진 path만 탐험 하겠다 
                
        - 알고리즘
            1. src 에서 DFS 순회 시작 
            2. 주어진 cell(x,y)에 대해 사방으로 인접한 cell을 탐험. 그 중에 가장 작은 effort가 드는 celldmf tjsxor 
            3. `maxDiff` : 현재 path에서 maximum absolute difference 기록 
            4. 매 adjacent cell로 옮길 때마다 maxDiff update 
                - curDiff = |adj_height - x,y height| 가 maxDiff보다 더 크면 maxDiff를 curDiff로 update
            5. dst cell에 도달하고 나면, DFS 순회로부터 backtrack 
            6. current path에서의 maximum absolute difference return 
            - 각 cell마다 이웃한 cell을 찾고, 그 cell에서 재귀적으로 dst에 도달하기 위해 필요한 노력을 계산, 그 중에 최소 effort를 찾는다
            - current cell의 height를 0으로 둠으로써 방문 처리
                - 현재 path로부터 backtrack 하고 나면 height를 다시 원래 값으로 돌려놓아야 한다
        - Code (TLE)
            
            ```python
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
                    nrow, ncol = len(heights), len(heights[0])
            				# 가장 큰 역할: candidate validity check 
                    self.max_so_far = float('inf') # why put self?
            
                    def dfs(x, y, max_diff):
            						===========================================
            						# base case. res에 넣어줄 값을 결정 
                        if x == nrow-1 and y == ncol-1: # reach dst 
                            # 도달지점이 dst인 경로 중 min_effort
                            self.max_so_far = min(self.max_so_far, max_diff)
                            return max_diff # 왜 max_diff를 return? max_so_far 값을 update 해두고서는?
            						============================================
                        cur_height = heights[x][y]
                        heights[x][y] = 0 # marking as visited 
            
                        min_effort = float('inf') # save best result among candidates
                        for d in directions:
                            new_x, new_y = x + d[0], y + d[1]
            								# candidate validity check 1 
                            if 0 <= new_x < nrow and 0 <= new_y < ncol:
            										# candidate validity check 2 
                                if heights[new_x][new_y] == 0: # already visited
                                    continue
            										
            										# update state of cur path 
                                cur_diff = abs(heights[new_x][new_y] - current_height)
                                max_cur_diff = max(max_diff, cur_diff)
            
            										# candidate validity check 3 
                                if max_cur_diff < self.max_so_far: 
            												# recursive 
                                    res = dfs(new_x, new_y, max_cur_diff)
                                    min_effort = min(min_effort, res)
                        
                        # backtrack
                        heights[x][y] = cur_height
            
            						return min_effort 
                    
                    return dfs(0, 0, 0)
            ```
            
            - res에 대하여
                - new_x, new_y에서 바로 base case hit 했으면 max_diff가 return 될 것이고
                - 아니면 이웃들을 거쳐서 base case hit 하고 쭉 올라온 min_effort가 return 될 것
        - 복잡도 분석
            - 시간복잡도: O(3^(m*n))
                - matrix cell 개수: m * n (num_row * num_col)
                - backtracking
                    - 최대 4개의 이웃. 근데 일단 한 칸 어느 방향으로 간 다음에 다시 돌아오는 건 아니니까 사실상 3개라고 함?
                - 하나의 cell당 3개의 옵션 고려해서 저렇게 된다고 함
                - 근데 TLE
            - 공간복잡도: O(m * n)
                - recursion stack 저장
                - 재귀적으로 이웃한 cell로 이동하는데, 최대 m * n 개의 call이 recursive call stack에 들어갈 수 있다
    - **다익스트라 변형**
        - Intuition
            - src → dst 최단 경로 찾는 문제로 접근
                - 문제에서의 최단 경로: min absolute diff를 갖는 path
                - 각 cell마다 높이가 주어져있기 때문에 단순 BFS 순회로는 충분하지 않음
            - 이웃한 셀 A와 B 사이의 절대값 차이 = 노드 A와 B 사이를 연결하는 edge의 weight로 볼 수 있음
            
            ⇒ 최단 경로의 정의만 조정해서 weighted graph에서의 최단 경로를 구할 때 사용하는 다익스트라 알고리즘 도입
            
        - 알고리즘
            - `differenceMatrix` 사용
                - 각 cell: 가능한 모든 path에서 그 cell로 도달하는 데 필요한 최소 노력값을 저장
                - 초기값은 양의 무한대 - 왜냐면 아직 어떠한 cell에도 도달하지 못한 상태이므로
            - 각 cell을 방문하기 시작하면서, 이웃한 cell들에도 도달 가능
                - current cell과 이웃한 cell 사이의 절대값 차이를 differenceMatrix에 저장
                - 동시에 모든 이웃한 cell을 우선순위 큐에 저장
                    - differenceMatrix의 셀 값을 기준으로 이웃한 cell들을 정렬한 채로 보관
                    
                    → 자기 이웃과 가장 작은 높이 절대값 차이를 가진 adjacent cell이 큐의 상단에 위치할 것 
                    
            - 큐에 source cell을 추가하면서 시작 (0, 0). destination cell을 방문하거나 큐가 비면 탐색 중단
            - 높이 차가 적은 cell부터 탐색 시작
                - 큐 탑에 있는 셀을 추출해서 방문 처리
                - 이웃한 4개의 셀에 대해 maxDifference 계산
                    - 현재 cell에서 이웃에 도달하기까지 maximum absolute difference
                - 이상적으로 PQ를 업데이트 할 때, 오래된 값은 지우고 새 maxDifference 값을 넣어야 함.
                    - 그러나 updated maximum value는 늘 오래된 값보다 작고, 큐에서 추출될 것이고, 오래된 값보다 먼저 방문될 것을 알고 있기 때문에(?) 오래된 값을 큐에서 지우는 일을 하지 않음으로써 시간을 아낄 수 있다
            - differenceMatrix[-1][-1]이 dest cell 방문하기 위한 최소 노력
        - 슬라이드쇼
            - 초기화
                
                ![Untitled](Untitled%2093.png)
                
            - (0, 0, 0) 큐에서 추출하고 난 뒤
                1. visited에서 방문 처리 
                2. 이웃 돌면서 difference update
                3. 큐에 이웃들 추가 
                
                ![Untitled](Untitled%2094.png)
                
            - 그 다음 큐 탑인 (0, 1, 1) 추출
                
                ![Untitled](Untitled%2095.png)
                
            - 큐에서 꼭 연속된 셀 순서로 추출되는 것은 아님
                
                ![Untitled](Untitled%2096.png)
                
                ![Untitled](Untitled%2097.png)
                
            
        - trial
            - 9/75
            
            ```python
            import heapq
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    num_row, num_col = len(heights), len(heights[0])
                    diff_mat = [[float('inf')] * num_col for _ in range(num_row)]
                    diff_mat[0][0] = 0 
                    visited =  [[False] * num_col for _ in range(num_row)]
                    queue = [(0, 0, 0)]
            
                    while queue:
                        cur_x, cur_y, max_diff = heapq.heappop(queue)
                        if cur_x == num_row-1 and cur_y == num_col-1:
                            return max_diff
                        visited[cur_x][cur_y] = True 
            
                        for d in directions:
                            new_x, new_y = cur_x + d[0], cur_y + d[1]
                            if 0 <= new_x < num_row and 0 <= new_y < num_col:
                                if visited[new_x][new_y]: continue
                                new_diff = abs(heights[cur_x][cur_y]-heights[new_x][new_y])
                                if new_diff < diff_mat[new_x][new_y]:
                                    diff_mat[new_x][new_y] = new_diff
                                    queue.append((new_x, new_y, new_diff))
            ```
            
        - AC 코드
            
            ```python
            import heapq
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    num_row, num_col = len(heights), len(heights[0])
                    diff_mat = [[float('inf')] * num_col for _ in range(num_row)]
                    diff_mat[0][0] = 0 
                    visited =  [[False] * num_col for _ in range(num_row)]
                    queue = [(0, 0, 0)]
            
                    while queue:
                        max_diff, cur_x, cur_y = heapq.heappop(queue)
                        visited[cur_x][cur_y] = True 
            
                        for d in directions:
                            new_x, new_y = cur_x + d[0], cur_y + d[1]
                            if 0 <= new_x < num_row and 0 <= new_y < num_col:
                                if visited[new_x][new_y]: continue
                                cur_diff = abs(heights[cur_x][cur_y]-heights[new_x][new_y])
                                new_diff = max(cur_diff, diff_mat[cur_x][cur_y])
                                if new_diff < diff_mat[new_x][new_y]:
                                    diff_mat[new_x][new_y] = new_diff
                                    heapq.heappush(queue, (new_diff, new_x, new_y))
                    
                    return diff_mat[-1][-1]
            ```
            
        - 복잡도 분석
            - 시간: O(*m*⋅*n ** log(*m*⋅*n*))
                - heapq에 최대 들어갈 수 있는 원소 수는 m, n
                
                → 한 번의 push, pop operation time complexity는 O(log(m*n))
                
                ↳ 새로운 cell이 heapq에 들어올 때마다 weight 기준으로 다시 sorting 해야 하므로 이렇게 걸리는 것 
                
                - 원소수 * operation 한번에 드는 시간 =  O(*m*⋅*n ** log(*m*⋅*n*))
    - **Binary Search Using BFS**
        - Intuition
            - height cell에 올 수 있는 값의 범위가 주어짐 → height difference 범위도 구할 수 있음 → middle value를 반복적으로 계산
                - 1 ≤ heights[i] ≤ 10^6 → 0 ≤ difference < 10^6-1
            - mid를 중심으로 탐색 공간 분할
                - src → dst path 중에 effort가 mid보다 작은 경우가 존재하면, required minimum effort value가 0과 mid (exclusive) 사이에 존재
                
                ↔ effort가 mid보다 작은 경우가 존재하지 않으면, required minimum effort value는 mid와 10^6(exclusive) 사이에 존재 
                
            - src → dst path의 effort와 mid value를 비교하는 방법
                - simple graph traversal - BFS
        - 알고리즘
            - lower bound, upper bound, mid 초기화
            - BFS 사용해서 src → dst path 구한 다음에 그 중에 effort가 mid보다 작거나 같은 경우가 있는지 체크 (별도 함수 정의)
            - 만약 작거나 같은 경우가 있으면 result value를 current result와 mid 중 더 작은 쪽으로 update(?) → left와 mid-1 사이를 탐색 (=right는 mid-1로 update)
            - 만약 그런 경우가 없으면 mid+1과 right가 다음 탐색 공간(=left를 mid+1로 update)
        - Trial
            - visited 표시하는 것과 cur_diff < route_effort[x][y] 상충되지 않나? visited 표시하는 건 해당 좌표는 큐에 한번밖에 못 들어온다는 건데 route_effort가 갱신될 일이 있나? ⇒ 맞다. cur_diff를 route_effort[x][y]와 비교하는 절차는 필요하지 않다
                - 뭐랑 헷갈렸냐면, 다익스트라에서 visited set을 사용하지 않는 경우의 typical 수도 코드를 보았는데, 여기서는 어떤 노드가 여러번 priority queue에 추가되는 것을 방지할 수단이 없으니, 조건문을 하나 추가해서 큐에 들어오더라도 처리가 되는 것을 막는 방법을 사용하고 있었음
                - 근데 원래 풀었던 문제에서는 visited set을 사용해서 일단 처리된 노드는 다시 못 들어오게끔 했기 때문에 차이가 있었고, 저 둘은 실제로 상충되는 것이 맞음. 결국 역할은 같기 때문에.
        - AC 코드 (좀 느림)
            
            ```python
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    nrows, ncols = len(heights), len(heights[0])
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    
                    def can_reach(mid):
                        visited = [[False] * ncols for _ in range(nrows)]
                        queue = collections.deque([(0,0)])
                
                        while queue: 
                            x, y = queue.popleft()
                            if x == nrows-1 and y == ncols-1:
                                return True
            
                            visited[x][y] = True # avoid adding a node multiple times 
                            
                            for d in directions:
                                new_x, new_y = x + d[0], y + d[1]
            										# candidate validity check 
                                if 0 <= new_x < nrows and 0 <= new_y < ncols:
                                    if visited[new_x][new_y]:
                                        continue 
            												# check condition 
                                    cur_diff = abs(heights[x][y] - heights[new_x][new_y])
                                    if cur_diff <= mid:
            														# no need to attend this edge twice 
                                        visited[new_x][new_y] = True 
                                        queue.append((new_x, new_y))   
            
                    left, right = 0, 10**6
                    while left < right:
                        mid = (left + right) // 2
                        if can_reach(mid):
                            right = mid  
                        else:
                            left = mid + 1
                    return left
            ```
            
        - 복잡도 분석
            - 시간복잡도: O(m * n)
                - Binary search: O(log 10**6)
                - BFS: O(V+E)
                    - m * n matrix 기준으로 보면 노드도, edge도 m * n개
                    
                    ⇒ O(m*n + m*n) = O(2 * m* n) = O(m * n)
                    
                
                ⇒ O(log 10**6 * (m*n)) = O(m * n)
                
                - binary search에서 계산되는 모든 mid 값마다 BFS 수행하기 때문에 곱셈
            - 공간복잡도: O(m * n)
                - 큐가 포함할 수 있는 원소 개수의 upper bound m * n
                - visited array size = matrix size → m * ㅜ
    - **Binary Search Using DFS**
        - 매 mid가 given maximum effort. 그보다 같거나 적은 effort로 갈 수 있는 path가 있는지 봐야 함
        - trial
            - stack으로 바꿔도 답이 바로 나와서 recursive로 짜봤는데 안 풀린다
                
                ```python
                class Solution:
                    def minimumEffortPath(self, heights: List[List[int]]) -> int:
                        nrows, ncols = len(heights), len(heights[0])
                        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                
                        def can_reach(mid):
                            visited = [[False] * ncols for _ in range(nrows)]
                            def dfs(dist, x, y):
                                if x == nrows-1 and y == ncols-1:
                                    return dist
                                
                                visited[x][y] = True
                
                                neighbor_dist = float('inf')
                                for d in directions:
                                    new_x, new_y = x + d[0], y + d[1]
                                    if 0 <= new_x < nrows and 0 <= new_y < ncols:
                                        if visited[new_x][new_y]:
                                            continue 
                                        cur_diff = abs(heights[x][y] - heights[new_x][new_y])
                                        new_diff = max(cur_diff, dist)
                                        res = dfs(new_diff, new_x, new_y)
                                        if res < neighbor_dist:
                                            neighbor_dist = res 
                                return neighbor_dist
                                
                            if dfs(0, 0, 0) <= mid:
                                return True
                            else:
                                return False
                                
                
                        left, right = 0, 10**6
                        while left < right:
                            mid = (left + right) // 2
                            if can_reach(mid):
                                right = mid  
                            else:
                                left = mid + 1
                        return left
                ```
                
            - dfs에서 visited를 해야 하나
                - 안해도 되지 않나 왔다갔다 하다가 더 적은 route 대표 값을 만날 수 도 있지 않나?
                - 안하면 무한 재귀 불러지는 거 아님요?
                    - 우선 안하고 해보자 → 무한 재귀 불러온다
                - 하는 게 맞다
        - AC 코드 (mine)
            
            ```python
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    nrows, ncols = len(heights), len(heights[0])
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            
                    def can_reach(mid):
                        visited = [[False] * ncols for _ in range(nrows)]
                        
                        def dfs(route_max, x, y):
                            visited[x][y] = True 
            
                            if x == nrows-1 and y == ncols-1:
                                return True 
                            
                            for d in directions:
                                new_x, new_y = x + d[0], y + d[1]
                                if 0 <= new_x < nrows and 0 <= new_y < ncols:
                                    if visited[new_x][new_y]: continue
                                    cand = abs(heights[x][y] - heights[new_x][new_y])
                                    new_route_max = max(cand, route_max)
                                    if new_route_max <= mid:
                                        if dfs(new_route_max, new_x, new_y):
                                            return True 
                            return False
            
                        return dfs(0, 0, 0)
            
                    left, right = 0, 10**6
                    while left < right:
                        mid = (left + right) // 2
                        if can_reach(mid):
                            right = mid
                        else:
                            left = mid+1
                    return left
            ```
            
        - AC 코드 (visited marking 주의. 조금 더 빠름)
            
            ```python
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    nrows, ncols = len(heights), len(heights[0])
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            
                    def can_reach(x, y, mid):
                        if x == nrows-1 and y == ncols-1:
                            return True
                       
                        visited[x][y] = True 
            
                        for d in directions:
                            new_x, new_y = x + d[0], y + d[1]
                            if 0 <= new_x < nrows and 0 <= new_y < ncols:
                                if visited[new_x][new_y]: continue
                                cand = abs(heights[x][y] - heights[new_x][new_y])
                                if cand <= mid:
                                    if can_reach(new_x, new_y, mid):
                                        return True 
            
                    left, right = 0, 10**6
                    while left < right:
                        mid = (left + right) // 2
                        visited = [[False] * ncols for _ in range(nrows)]
                        if can_reach(0, 0, mid):
                            right = mid
                        else:
                            left = mid+1
                    return left
            ```
            
    - **Union-Find 심화**
        - Intuition
            - matrix와 graph
                
                
                | matrix | graph |
                | --- | --- |
                | cell | node(component) |
                | path cur → adj | edge connecting 2 cells |
            - 초기에 각각의 cell은 모두 하나의 component → src to dst가 하나의 component에 속하도록 개별 cell(component)를 병합해나감
            - 각 connected component는 대표자가 있음 -parent
                - src와 dst의 parent가 같아질 때까지 병합 수행
        - 알고리즘
            - 초기에는 각 cell의 부모가 모두 자기 자신
            - 2차원 matrix를 1차원으로 변형 → (x, y)의 index는 (x * num_col + y)로 치환
                
                ![Untitled](Untitled%2098.png)
                
            - Building an `edgeList`
                - matrix에서 맞닿아 있는 모든 cell 간의 absolute difference를 저장
                - non-decreasing order of difference로 edge list 정렬
                - len(edgeList) ≠ num_row * num_col
                
                ![Untitled](Untitled%2099.png)
                
            - sorted edge list를 돌면서 UF 알고리즘을 통해 각 edge를 연결 → 하나의 component로 병합
                - 매 병합이 끝날 때마다, src과 dst의 대표자가 같아졌는지(둘이 연결되었는지) 확인
                    - 만약 그렇다면, current edge가 우리의 결과
                    - difference 오름 차순으로 edge에 접근하고 있기 때문에, 현재 edge로 인해 src와 dst가 하나의 component에 속하게 되었다면, 현재 difference가 maximum absolute difference in our path with minimum efforts 라는 것을 알 수 있음
        - Trial
            - 예제 2/3 맞힘 → UnionFind union method를 잘못 알고 있었음 ;;
                
                ```python
                class UnionFind:
                    def __init__(self, size):
                        self.rank = [1] * size
                        self.root = [i for i in range(size)]
                    def find(self, x):
                        if self.root[x] != x:
                            self.root[x] = self.find(self.root[x])
                        return self.root[x]
                    def union(self, x, y):
                        root_x, root_y = self.root[x], self.root[y] # or self.root(x)?
                        if root_x != root_y:
                            if self.rank[x] > self.rank[y]:
                                self.root[y] = root_x
                            elif self.rank[x] < self.rank[y]:
                                self.root[x] = root_y
                            else: # same height
                                self.root[y] = root_x
                                self.rank[x] += 1 
                    def is_connected(self, x, y):
                        return self.find(x) == self.find(y)
                
                class Solution:
                    def minimumEffortPath(self, heights: List[List[int]]) -> int:
                        num_row, num_col = len(heights), len(heights[0])
                        num_cell = num_row * num_col
                        UF = UnionFind(num_cell)
                        flatten_mat = [0] * num_cell
                        for i in range(num_row):
                            for j in range(num_col):
                                idx = i * num_col + j
                                flatten_mat[idx] = heights[i][j]
                        
                        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                        edge_list = []
                        for i in range(num_row):
                            for j in range(num_col):
                                cur_idx = i * num_col + j
                                for d in directions:
                                    new_i, new_j = i + d[0], j + d[1]
                                    if 0 <= new_i < num_row and 0 <= new_j < num_col:
                                        new_idx = new_i * num_col + new_j
                                        diff = abs(heights[i][j]-heights[new_i][new_j])
                                        edge_list.append((cur_idx, new_idx, diff))
                        edge_list.sort(key=lambda x: x[2])
                
                        for e in edge_list:
                            dep, arr, diff = e
                            UF.union(dep, arr)
                            if UF.is_connected(0, num_cell-1):
                                return diff
                ```
                
        - AC 코드
            
            ```python
            class UnionFind:
                def __init__(self, size):
                    self.rank = [1] * size
                    self.root = [i for i in range(size)]
                def find(self, x):
                    if self.root[x] != x:
                        self.root[x] = self.find(self.root[x])
                    return self.root[x]
                def union(self, x, y):
                    root_x, root_y = self.find(x), self.find(y)
            				### 이제부터는 root_x, root_y의 시대~!! ###
                    if root_x != root_y:
                        if self.rank[root_x] > self.rank[root_y]:
                            self.root[root_y] = root_x
                        elif self.rank[root_x] < self.rank[root_y]:
                            self.root[root_x] = root_y
                        else: # same height
                            self.root[root_y] = root_x
                            self.rank[root_x] += 1 
                def is_connected(self, x, y):
                    return self.find(x) == self.find(y)
            
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    num_row, num_col = len(heights), len(heights[0])
                    if num_row == 1 and num_col == 1:
                        return 0
                    num_cell = num_row * num_col
                    UF = UnionFind(num_cell)
                    flatten_mat = [0] * num_cell
                    for i in range(num_row):
                        for j in range(num_col):
                            idx = i * num_col + j
                            flatten_mat[idx] = heights[i][j]
                    
                    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                    edge_list = []
                    for i in range(num_row):
                        for j in range(num_col):
                            cur_idx = i * num_col + j
                            for d in directions:
                                new_i, new_j = i + d[0], j + d[1]
                                if 0 <= new_i < num_row and 0 <= new_j < num_col:
                                    new_idx = new_i * num_col + new_j
                                    diff = abs(heights[i][j]-heights[new_i][new_j])
                                    edge_list.append((cur_idx, new_idx, diff))
                    edge_list.sort(key=lambda x: x[2])
            
                    for e in edge_list:
                        dep, arr, diff = e
                        UF.union(dep, arr)
                        if UF.is_connected(0, num_cell-1):
                            return diff
            ```
            
        - 보너스
            - edge list를 만드는 더 간단한 방법
                - 나는 정직하게 current cell 기준으로 사방 이웃을 봤지만
                - current cell 기준으로 upper, left cell만 봐도 complete edge list를 만들 수 있다고 함
                    - 다만, upper이 있으려면 row가 0이면 안되고
                    - left가 있으려면 col이 0이면 안됨
                    - 그래서 조건 체크하는 부분이 있음
            
            ```python
            edge_list = []
            for current_row in range(row):
                for current_col in range(col):
                    if current_row > 0:
                        difference = abs(
                            heights[current_row][current_col] -
                            heights[current_row - 1][current_col])
                        edge_list.append(
                            (difference, current_row * col + current_col,
                             (current_row - 1) * col + current_col))
                    if current_col > 0:
                        difference = abs(
                            heights[current_row][current_col] -
                            heights[current_row][current_col - 1])
                        edge_list.append(
                            (difference, current_row * col + current_col, current_row
                             * col + current_col - 1))
            ```
            
- Review
    - backtracking + DFS
        
        ```python
        class Solution:
            def minimumEffortPath(self, heights: List[List[int]]) -> int:
                directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                nrow, ncol = len(heights), len(heights[0])
                self.dst_min = float('inf')
        
                def dfs(x, y, route_max):
                    if x == nrow-1 and y == ncol-1:
                        self.dst_min = min(self.dst_min, route_max)
                        return route_max 
                    
                    # update current state
                    cur_height = heights[x][y]
                    heights[x][y] = 0
                    
                    # candidate validity check
                    neighbor_min = float('inf')
                    for d in directions:
                        new_x, new_y = x + d[0], y + d[1]
                        if 0 <= new_x < nrow and 0 <= new_y < ncol:
                            if heights[new_x][new_y] == 0:
                                continue 
                            cand_max = abs(cur_height - heights[new_x][new_y])
                            new_route_max = max(cand_max, route_max)
                            if new_route_max < self.dst_min:
                                res = dfs(new_x, new_y, new_route_max)
                                neighbor_min = min(res, neighbor_min)
                    
                    # backtrack
                    heights[x][y] = cur_height
                    return neighbor_min
                
                return dfs(0, 0, 0)
        ```
        
    - variation of Dijkstra
        
        ```python
        import heapq
        class Solution:
            def minimumEffortPath(self, heights: List[List[int]]) -> int:
                directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                nrow, ncol = len(heights), len(heights[0])
                visited = [[False] * ncol for _ in range(nrow)]
                route_min = [[float('inf')] * ncol for _ in range(nrow)]
                route_min[0][0] = 0
        
                queue = [(0, 0, 0)]
                while queue:
                    cur_effort, cur_x, cur_y = heapq.heappop(queue)
                    visited[cur_x][cur_y] = True 
        
                    for d in directions:
                        new_x, new_y = cur_x + d[0], cur_y + d[1]
                        if 0 <= new_x < nrow and 0 <= new_y < ncol:
                            if visited[new_x][new_y]:
                                continue 
                            cur_diff = abs(heights[cur_x][cur_y]-heights[new_x][new_y])
                            new_route_effort = max(cur_diff, cur_effort)
                            if new_route_effort < route_min[new_x][new_y]:
                                route_min[new_x][new_y] = new_route_effort
                                heapq.heappush(queue, (new_route_effort, new_x, new_y))
                return route_min[-1][-1]
        ```
        
    - BS + BFS
        - mid보다 cur_diff가 작을 때만 이웃을 enqueue 해서 더 전진할 수 있도록 했는데, 안 풀린다. 왜?
            
            → 왜냐면 부등호를 잘못 넣었기 때문이지 ;; 
            
        - AC 코드
            
            ```python
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    nrows, ncols = len(heights), len(heights[0])
                    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                    def can_reach(mid):
                        visited = [[False] * ncols for _ in range(nrows)]            
                        queue = collections.deque()
            
                        queue.append((0, 0))
                        visited[0][0] = True # marking on enqueueing
            
                        while queue:
                            x, y = queue.popleft()
                            if x == nrows-1 and y == ncols-1:
                                return True
                            for d in directions:
                                new_x, new_y = x + d[0], y + d[1]
                                if 0 <= new_x < nrows and 0 <= new_y < ncols:
                                    if visited[new_x][new_y]: continue 
                                    cur_diff = abs(heights[x][y]-heights[new_x][new_y])
                                    if cur_diff <= mid:
                                        queue.append((new_x, new_y))
                                        visited[new_x][new_y] = True # marking on enqueueing
                    
                    left, right = 0, 10**6
                    while left < right:
                        mid = (left + right) // 2
                        if can_reach(mid):
                            right = mid
                        else:
                            left = mid + 1 
                    return left
            ```
            
    - BS + DFS
        - AC 코드 🪇
            
            ```python
            class Solution:
                def minimumEffortPath(self, heights: List[List[int]]) -> int:
                    nrows, ncols = len(heights), len(heights[0])
                    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                    def can_reach(mid):
                        visited = [[False] * ncols for _ in range(nrows)]            
                        
                        def dfs(x, y):
                            if x == nrows-1 and y == ncols-1:
                                return True
                            visited[x][y] = True # marking on pop 
            
                            for d in directions:
                                new_x, new_y = x + d[0], y + d[1]
                                if 0 <= new_x < nrows and 0 <= new_y < ncols:
                                    if visited[new_x][new_y]: continue 
                                    cur_diff = abs(heights[x][y]-heights[new_x][new_y])
                                    if cur_diff <= mid:
                                        if dfs(new_x, new_y):
                                            return True   
            
                        return dfs(0, 0)                 
            
                    
                    left, right = 0, 10**6
                    while left < right:
                        mid = (left + right) // 2
                        if can_reach(mid):
                            right = mid
                        else:
                            left = mid + 1 
                    return left
            ```