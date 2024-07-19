# 994. Rotting Oranges

Status: in progress
Theme: graph
Created time: December 20, 2023 3:31 PM
Last edited time: December 20, 2023 4:39 PM

- 문제 이해
    
    모든 cell이 2가 될 때까지 걸리는 시간
    
    빈칸은 그냥 넘겨도 되고, rotten orange 기준으로 4방 이웃이 썩게 된다는 것인듯 
    
    1인 cell을 굳이 큐에 넣을 필요가 있나? 없는 것 같은데? 2로 바꿔준 다음에 큐에 넣어야 할 듯? 
    
    아님 2가 있는 cell을 처음부터 한 곳에 쫙 넣는 방법도 있음 
    
    방문 처리를 나중에 하는 게 좋을 듯 
    
    근데 동시 다발 적으로 오렌지가 썩는 거면 순차적으로 시간이 늘어나서는 안되겠어 
    
- AC 코드
    
    ```python
    class Solution:
        def orangesRotting(self, grid: List[List[int]]) -> int:
            m, n = len(grid), len(grid[0])
            visited = set()
            dq = collections.deque()
            def get_neighbors(r, c):
                neighbors = []
                directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                for d in directions:
                    new_r, new_c = r + d[0], c + d[1]
                    if (new_r, new_c) in visited:
                        continue
                    if 0 <= new_r < m and 0 <= new_c < n:
                        if grid[new_r][new_c] == 1:
                            neighbors.append((new_r, new_c))
                return neighbors
            
            for i in range(m):
                for j in range(n):
                    if grid[i][j] == 0:
                        visited.add((i, j))
                    elif grid[i][j] == 2:
                        dq.append((i, j))
            
            cur_time = 0
    				# base case
            if len(visited) == m * n:
                return cur_time 
                
            while dq:
                num_nodes = len(dq)
                if len(visited) + num_nodes == m * n:
                    return cur_time 
                for _ in range(num_nodes):
                    r, c = dq.popleft()
                    fresh_oranges = get_neighbors(r, c)
                    for new_r, new_c in fresh_oranges:
                        grid[new_r][new_c] = 2
                        dq.append((new_r, new_c))
                    visited.add((r, c))
                cur_time += 1
    
            return -1 
    
                    
                
    
                
            
            if len(visited) == m * n:
                return cur_time
            else:
                -1
    ```