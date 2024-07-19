# 1091. Shortest Path in Binary Matrix

Status: done, in progress, with help
Theme: BFS
Created time: December 18, 2023 5:27 PM
Last edited time: December 20, 2023 3:23 PM

- 문제 이해
    - 이것도 같은 level의 node들을 모두 둘러 봐야겠군 우선
    - queue를 도입해야겠지?
    - 그리고 top_left → bottom_right 이니까 다음으로 진출할 cell은 무조건 bottom 이나 right려나? BFS인거 보면 bottom을 먼저 봐야 할 듯. 근데 왼쪽에만 1이 있으면 가긴 가야 하겠지만 서도…
    - 8방을 고려했을 때 top-left → bottom-right 진행 방향에 부합하는 건 바로 오른쪽, 왼쪽, 대각선 아래쪽 3개인듯?
    - 이 세 개 중에 0이 없는 경우는 어떻게 커버하지? 우선 세 개만 고려하는 걸 짜볼까
    - BFS에서는 무조건 두 노드 간의 거리가 최단 경로다
    - same y coordinate → same level
        - 앞에서 같은 y 값에 이미 0이 나왔으면 이번거는 그냥 Pop
    - 그리고 BFS는 양의 가중치를 얘기했으니까 왠지 오른쪽 아래쪽 대각선 세 개로 커버될 것 같음
    - 여기서는 뒤집은 니은자 모양의 cell들이 같은 layer에 있다고 생각하면 되겠다
- Trial
    - 좀 잘 짰다고 생각했는데 53/90…
        
        ```python
        class Solution:
            def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
                if grid[0][0] == 1:
                    return -1 
        
                n = len(grid)
                queue = collections.deque([[(0, 0), 0]])
                num_blocks = 0
                level_clear = [False] * n
        
                while queue:
                    coord, level = queue.popleft()
                    cur_x, cur_y = coord
                    if cur_x == n-1 and cur_y == n-1:
                        if grid[cur_x][cur_y] != 0:
                            return -1
                        else:
                            return num_blocks + 1
                    if level_clear[level]:
                        continue
                    if grid[cur_x][cur_y] == 0:
                        num_blocks += 1 
                        level_clear[level] = True
                        if cur_x < n-1 and cur_y < n-1:
                            queue.append([(cur_x+1, cur_y+1), max(cur_x+1, cur_y+1)])
                        if cur_x < n-1:
                            queue.append([(cur_x+1, cur_y), max(cur_x+1, cur_y)])
                        if cur_y < n-1:
                            queue.append([(cur_x, cur_y+1), max(cur_x, cur_y+1)])
                        
                return -1
        ```
        
    - 8방으로 추가했는데도 틀린 53번째 문제 또 틀림
        
        ```python
        class Solution:
            def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
                if grid[0][0] == 1:
                    return -1 
        
                n = len(grid)
                queue = collections.deque([[(0, 0), 0]])
                num_blocks = 0
                level_clear = [False] * n
                directions = [[1, 1], [0, 1], [1, 0], [-1, 1], [1, -1], [0, -1], [-1, 0], [-1, -1]]
        
                while queue:
                    coord, level = queue.popleft()
                    cur_x, cur_y = coord
                    if 0 <= cur_x < n and 0 <= cur_y < n:
                        if cur_x == n-1 and cur_y == n-1:
                            if grid[cur_x][cur_y] != 0:
                                return -1
                            else:
                                return num_blocks + 1
                        if level_clear[level]:
                            continue
                        if grid[cur_x][cur_y] == 0:
                            num_blocks += 1 
                            level_clear[level] = True
                            for d in directions:
                                new_x, new_y = cur_x + d[0], cur_y + d[1]
                                new_level = max(new_x, new_y)
                                queue.append([(new_x, new_y), new_level])
                        
                return -1
        ```
        
    - Editorial 수도 코드 보고 짰는데 두번째 예제 틀림
        
        ```python
        class Solution:
            def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
                n = len(grid)
                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), \
                             (0, 1), (1, -1), (1, 0), (1, 1)]
                queue = collections.deque([(0, 0)])
                grid[0][0] = 1 
        
                while queue:
                    r, c = queue.popleft()
                    dist = grid[r][c]
                    for d in directions:
                        new_r, new_c = r + d[0], c + d[0]
                        if new_r == n-1 and new_c == n-1:
                            return dist + 1 
                        if 0 <= new_r < n and 0 <= new_c < n and grid[new_r][new_c] == 0:
                            grid[new_r][new_c] = dist + 1 
                            queue.append((new_r, new_c))
                return -1
        ```
        
- Editorial
    - Overview
        - BFS로 최단 경로 문제 해결
        - A* 알고리즘 이용
    - BFS, Overwriting input
        - intution
            - grid는 graph. cell value 0인 칸은 node. 그 사이를 연결하는 선들은 edge → lattice graph라고 부름
                
                ![Untitled](Untitled%20140.png)
                
        - 알고리즘
            - 큐와 BFS 간단 요약
                
                시작 node를 큐에 넣고, 큐에 노드가 있는 한 가장 밑에 있는 것을 꺼내고(enqueue) 꺼낸 노드의 이웃들을 다시 큐에 추가함(dequeue)
                
            - 이 문제에서 큐의 사용
                - current cell 자체는 numbered(?) 되었지만, 그 cell의 이웃들은 아직 numbered 되지 않은 상태의 cell들을 추적하기 위해 사용 (?) - 아마도 color array의 gray 상태 같은 애들?
            - 이 풀이에서는 visited set 필요 없음
                - 일반적으로는 inifinite loop 피하기 위해 visited set이 필요하지만, 여기서는 input을 overwrite 하기 때문에, 방문되지 않은 cell들만 cell value 0을 갖고 있을 것이다 - 아 방문한 cell의 값은 0에서 다른 걸로 덮어쓰기 한다는 뜻인 가보군
            - 초기화 수도 코드
                
                ```python
                queue = a new queue
                enqueue cell (0, 0)
                set grid[0][0] to 1 # 1은 distance라고 함(?)
                ```
                
            - BFS loop
                - queue에 cell이 있는 한 → dequeue → dequeue된 cell의 distance를 look up(?) → 그 이웃들을 탐색
                - 이웃이 누구냐
                    - current cell에 adjacent 하고(8방 중에 하나지만?), 아직 cell value가 0인 경우(=방문 가능하지만 아직 방문 안되었음)
                    - 각 이웃에 대해 distance + 1을 부여한 뒤 enqueue
                - 수도 코드
                    
                    ```python
                    while queue:
                    	cell = deque a cell
                    	look up distance at grid[r][c]
                    	for each open neighbor:
                    		if this neighbor is the bottom right cell:
                    			return distance + 1 
                    		set grid[neighbor_r][neighbor_c] = distance + 1
                    		enqueue neighbor 
                    return -1 
                    ```
                    
                    - 부가 설명
                        1. `return -1` 
                            - success case에서 return에 아직 도달하지 못했는데 탐색할 노드가 더 이상 없다는 것이므로 fail → -1
                        2. `distance at grid[r][c]`
                            - 이렇게 할 수 있는 이유는 숫자가 쓰여진 후에만 cell이 큐에 들어가기 때문-무슨 말인지 모르겠음?
                        3. 현재 값이 0인 cell들에게만 숫자를 써야한다 
                            - 이미 2를 갖고 있는 cell의 값을 4로 변경한다면, 더 이상 top left로부터 해당 cell까지의 최단 거리를 의미하는 숫자가 아니게 된다
                        4. `return distance + 1`
                            - 아직 bottom-right cell이 current cell이 되지 않았지만, outer loop에서 체크한 뒤에 +1 해서 return  해도 된다
                - 한 cell의 모든 이웃을 어떻게 가져와야 하는가?
                    - 전통적인 그래프 표현에서는 주어진 node의 모든 edge를 살피는 일에 해당
                    - grid에서는 row, column의 offset-기준이 되는 cell로부터 얼마나 떨어져있는지를 나타내는 것, (1, -1) 같이 더해지는 좌표-으로 식별
                        
                        나도 이렇게 했지 - `directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]`
                        
                    - 이 list를 돌면서 더하면 이웃이 찾아지지만, 모서리나 가장자리에 있는 cell로부터는 8개의 이웃을 다 얻을 순 없음
                        
                        → 더해진 neighbor row, col이 valid 범위에 있는지 먼저 체크 
                        
                        → 만약 그렇다고 하면 그 cell의 현재 값이 0인지 체크 
                        
                        → 그럼 그 이웃 cell을 a list of all the neighbors to be returned(queue)에 추가 
                        
                - 위의 내용을 모두 반영한 수도 코드-grid 문제에서 자주 사용될 함수라 기억해두는 것이 좋다
                    
                    ```python
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    
                    define function get_neighbors(row, col):
                    	neighbors = a container to put the neighbors of (row, col) in
                    	    for each (row_direction, col_direction) pair in directions:
                    	        neighbor_row = row + row_direction
                    	        neighbor_col = col + col_direction
                    	        if (neighbor_row, neighbor_col) is NOT over the edge of the grid AND is 0:
                    	            add (neighbor_row, neighbor_col) to neighbors
                    	    return neighbors
                    ```
                    
        - 복잡도 분석
            - N : grid에 있는 모든 cell의 개수
            - 시간복잡도 : O(N).
                - 각 cell은 최대 한번만 enqueue 되도록 보장됨. 일단 큐에 어떤 노드를 집어넣었다면, 바로 직전에 그 노드의 값은 0에서 다른 값으로 바뀌었기 때문에 다시 큐에 들어올 일이 없음. 큐에는 값이 0인 상태의 노드만 들어올 수 있기 때문
                - 이웃 cell을 찾는 건 상수. 왜냐면 8을 상수 처리하기 때문
            - 공간복잡도: O(N)
                - additional space는 큐 뿐이고, 큐에는 최대 N개의 cell만 들어갈 수 있기 때문
    - BFS, Without Overwriting the Input
        - Intutition
            - in-place 알고리즘의 위험 부담
                - 멀티쓰레드 환경에서 알고리즘이 돌아가서 grid에 대해 exclusive access가 보장되지 않는 경우 - 다른 쓰레드도 grid를 읽는 경우, input 값이 바뀌는 상황을 고려하지 않고 돌아갈 것임
                    - 이 부분을 인터뷰어와 잘 체크해야 한다고 함
                - 싱글쓰레드에 배타적 접근이 보장되는 상황이더라도, grid가 재사용되거나 lock이 풀린 뒤에 다른 쓰레드가 grid에 접근해야 하는 경우 → 다시 double for loop을 돌면서 grid를 원복하는 코드가 추가로 필요
            - 대안: 전통적 BFS + visited set + distance 기록하는 또 다른 방법
        - 알고리즘
            - 이웃 가져오는 건 그대로 사용
            - BFS loop → visited set 사용
            - Distances on queue
                - visited set의 간단한 변형 + 큐에 row, col, distance를 같이 집어넣는 것(triplet)
                - 수도 코드
                    
                    ```python
                    visited = a new set
                    queue = a new queue
                    enqueue (0, 0, 1)
                    add (0, 0) to visited # visited에 좌표 추가
                    
                    while the queue is not empty:
                    
                        row, col, distance = dequeue and unpack a cell
                        if (row, col) is the bottom right cell:
                            return distance
                    
                        for each open neighbour:
                            if neighbour is in visited: # 큐에 넣기 전에 방문 여부 확인
                                continue
                            otherwise, add neighbour to visited # 방문 처리
                            enqueue (neighbour_row, neighbour_col, distance + 1)
                    
                    return -1
                    ```
                    
            - *Starting a new collection for each distance*
                - BFS - starting point로부터의 거리 순으로 cell을 조사해나감
                    - starting point로부터 거리가 x인 cell들은 거리가 x+1인 cell들보다 먼저 방문 됨
                    - 거리가 x인 cell들은 거리가 x+1인 cell들만 큐에 넣을 수 있음 → 따라서 한 번에 큐에 있을 수 있는 unique distances는 최대 두 개
                - 탐색할 cell들의 모음을 두 개로 가져감
                    - 현재 dist와 같은 dist를 가지면서 아직 탐색되지 않은 cell들
                    - 다음 dist를 가지면서 아직 탐색되지 않은 cell들
                - 큐를 사용할 필요 없음 - 같은 거리를 갖는 cell들의 순서는 중요하지 않음. 추가/제거에 O(1) 걸리는 아무 자료 구조든 상관 없음
                - 수도 코드
                    
                    ```python
                    visited = a new set
                    add (0, 0) to visited
                    current_layer = a new list
                    next_layer = a new list
                    add (0, 0) to current layer
                    
                    while current_layer is not empty:
                    
                        row, col = remove and unpack a cell from current_layer
                    
                        if (row, col) is the bottom right cell (target):
                            return distance
                    
                        for each open neighbor:
                            if the neighbor is in visited:
                                continue
                            add neighbor to visited
                            add neighbor to next_layer
                        
                        if current_layer is now empty:
                            current_distance += 1
                            current_layer = next_layer
                            next_layer = a new list 
                    
                    return -1
                    ```
                    
            - *Keeping track of how many cells at each distance are on the queue*
                - 시작할 때는 거리가 1인 cell이 하나 밖에 없음
                - 이 cell을 큐에서 꺼내서 처리하고 나면, 큐에 남아 있는 cell들의 거리는 모두 2임을 알 수 있음
                    - 큐에 몇 개가 남았는지 보고, 해당 거리를 갖는 cell들을 큐에서 꺼내서 처리한다 (?)
                - 거리가 2인 cell을 모두 처리하고 나면 큐에 남은 cell들은 모두 거리 3을 갖고 … 이런 식으로 전체 grid에 대해 진행
                - 수도 코드
                    
                    ```python
                    visited = a new set
                    queue = a new queue
                    enqueue cell (0, 0)
                    add (0, 0) to visited
                    current_distance = 1
                    
                    while queue is not empty:
                    
                        nodes_on_queue = current queue length
                    
                            repeat nodes_on_queue_times:
                    
                            row, col = dequeue and unpack a cell
                            if (row, col) is the bottom right cell (target):
                                return distance
                    
                            for each open neighbour:
                                if neighbour is in visited:
                                    continue
                                add neighbour to visited
                                enqueue (neighbour_row, neighbour_col, distance + 1)
                        
                        current_distance += 1
                    
                    return -1
                    ```
                    
- 여러 버전의 AC 코드
    - BFS-overwrite input
        
        ```python
        class Solution:
            def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        				# base case 1 
                if grid[0][0] != 0 or grid[-1][-1] != 0:
                    return -1 
                n = len(grid)
                
                directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), \
                             (0, 1), (1, -1), (1, 0), (1, 1)]
                queue = collections.deque([(0, 0)])
                grid[0][0] = 1 
        
                while queue:
                    r, c = queue.popleft()
                    dist = grid[r][c]
        						# base case 2
                    if r == n-1 and c == n-1:
                        return dist
                    for d in directions:
                        new_r, new_c = r + d[0], c + d[1]
                        if new_r == n-1 and new_c == n-1:
                            return dist + 1
                        if 0 <= new_r < n and 0 <= new_c < n and grid[new_r][new_c] == 0:
                            grid[new_r][new_c] = dist + 1 
                            queue.append((new_r, new_c))
                return -1
        ```
        
    - Distances on queue
        
        ```python
        class Solution:
            def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        				# base case
                if grid[0][0] != 0 or grid[-1][-1] != 0:
                    return -1
        
                n = len(grid)
                def get_neighbors(r, c):
                    neighbors = []
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    for d in directions:
                        new_r, new_c = r+d[0], c+d[1]
                        if (new_r, new_c) in visited:
                            continue
                        if 0 <= new_r < n and 0 <= new_c < n:
                            if grid[new_r][new_c] == 0:
                                neighbors.append((new_r, new_c))
                    return neighbors 
                
                visited = set([(0, 0)])
                queue = collections.deque([(0, 0, 1)])
                
                while queue:
                    r, c, dist = queue.popleft() 
                    if r == n-1 and c == n-1:
                        return dist 
                    neighbors = get_neighbors(r, c)
                    for neighbor in neighbors:
                        queue.append((*neighbor, dist+1))
                        visited.add(neighbor)
                return -1
        ```
        
    - Two collections
        
        ```python
        from collections import deque
        class Solution:
            def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
                def get_neighbors(r, c):
                    neighbors = []
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    for d in directions:
                        new_r, new_c = r + d[0], c + d[1]
                        if (new_r, new_c) in visited:
                            continue 
                        if 0 <= new_r < n and 0 <= new_c < n:
                            if grid[new_r][new_c] == 0:
                                neighbors.append((new_r, new_c))
                    return neighbors 
        
                if grid[0][0] != 0 or grid[-1][-1] != 0:
                    return -1 
                n = len(grid)
                visited = set([(0, 0)])
                current_layer = []
                next_layer = []
                current_layer.append((0, 0))
                cur_dist = 1
        
                while current_layer:
                    row, col = current_layer.pop() # list pop 해도 같은 결과?
                    if row == n-1 and col == n-1:
                        return cur_dist
        
                    neighbors = get_neighbors(row, col)
                    for nei in neighbors:
                        visited.add(nei)
                        next_layer.append(nei)
        						# 이 아래 세 줄 덕분에 덱 없이도 BFS 이용 가능
                    if not current_layer:
                        current_layer = next_layer
                        next_layer = []
                        cur_dist += 1 
                return -1
        ```
        
    - Same distance at once
        
        ```python
        from collections import deque
        class Solution:
            def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
                def get_neighbors(r, c):
                    neighbors = []
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    for d in directions:
                        new_r, new_c = r + d[0], c + d[1]
                        if (new_r, new_c) in visited:
                            continue 
                        if 0 <= new_r < n and 0 <= new_c < n:
                            if grid[new_r][new_c] == 0:
                                neighbors.append((new_r, new_c))
                    return neighbors 
        
                if grid[0][0] != 0 or grid[-1][-1] != 0:
                    return -1 
                n = len(grid)
                visited = set([(0, 0)])
                queue = deque([(0, 0)])
                cur_dist = 1
        
                while queue:
                    num_nodes = len(queue)
                    for _ in range(num_nodes):
                        r, c = queue.popleft()
                        if r == n-1 and c == n-1:
                            return cur_dist
                        neighbors = get_neighbors(r, c)
                        for nei in neighbors:
                            queue.append(nei)
                            visited.add(nei)
                    cur_dist += 1 
                return -1
        ```