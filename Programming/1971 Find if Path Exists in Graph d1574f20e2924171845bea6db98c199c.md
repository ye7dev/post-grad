# 1971. Find if Path Exists in Graph

Status: done, in progress, 🏋️‍♀️
Theme: graph
Created time: December 14, 2023 2:59 PM
Last edited time: December 18, 2023 4:24 PM

- 과정
    - Memory exceed error
    
    ```python
    class Solution:
        def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
            stack = []
            visited = [False] * n
            stack.append([source])
            while stack:
                top = stack.pop()
                if not visited[top[-1]]:
                    visited[top[-1]] = True
                    if top[-1] == destination: 
                        return True
                for s, e in edges:
                    if s == top[-1]:
                        stack.append(top+[e])
                    elif e == top[-1]:
                        stack.append(top+[s])
                visited[top[-1]] = False
            return False
    ```
    
- Editorial
    - graph traversal problem : 하나의 노드에서 순회를 시작해서 다른 노드에 도달가능한지 확인 → BFS, DFS
    - Disjoint Set Union으로도 풀 수 있다네? - root가 같으면 같은 path위에 있다는 거니까 True return 하면 되나봄?
        - [ ]  해보기
    - DFS Recursive
        - 알고리즘
            - `seen` : 방문 여부 표시. seen[source] = True
            - `graph` : 모든 edge를 저장하는 hash map
            - source node에서 탐색 시작. 현재 node (`cur_node`)가 destination과 같으면 return True
                - 그렇지 않으면 아직 방문하지 않은 이웃 node를 모두 찾는다
                - 그런 이웃 노드가 있으면 visited 표시를 하고, 이 node로 옮겨 간 다음 다시 과정을 반복
                - 이 이웃 노드가 destination에 도달할 수 있으면 return True. 아니면 다음 이웃 시도
            - 모든 이웃에 대해 탐색을 하고도 destination에 닿지 못하면 return False
        - 코드 (AC 코드 보다 더 빠름)
            
            ```python
            class Solution:
                def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
                    graph = collections.defaultdict(list)
                    for s, e in edges: # O(m)
                        graph[s].append(e)
                        graph[e].append(s)
            
                    visited = [False] * n
                   
                    def dfs(cur_node):
            						# base case 
                        if cur_node == destination:
                            return True
                        if not visited[cur_node]: # each node visited once -> O(n)
                            visited[cur_node] = True            
                            for neighbor in graph[cur_node]:
                                if dfs(neighbor):
                                    return True
                        return False
                    
                    return dfs(source)
            ```
            
        - 시간복잡도 O(n+m) ← num nodes + num edges. 공간복잡도도 동일
    - DFS Iterative
        - top node on the stack은 항상 next branch로 이어진다
            - end of the current branch에 당도하면, stack으로 가서 top을 받아온 다음, 거기서부터 시작하는 다른 branch 탑승
        - visited 처리: unvisited node를 stack에 넣자마자 바로 visited 처리 → 다음번에 다시 방문하는 일이 없게끔 함
        - 알고리즘
            1. 빈 stack을 초기화하고 방문해야 할 node들을 저장한다
            2. visited 와 graph도 생성
            3. source node를 stack에 추가하고, 방문 처리 한다
            4. stack에 node가 있는 한, top node를 stack에서 꺼내온다
            5. 만약 top node가 destination이면 return True
                - 그렇지 않으면 top node의 아직 방문되지 않은 이웃 노드들을 stack에 추가하고, 방문 처리한 뒤. 4.를 반복한다
            6. 다 iterate 하고도 destination 안나오면 false return 
        - 코드
            - Recursive보다 훨씬 빠르다
            
            ```python
            class Solution:
                def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
                    graph = collections.defaultdict(list)
                    for s, e in edges:
                        graph[s].append(e)
                        graph[e].append(s)
                    stack = []
                    visited = [False] * n
            
                    stack.append(source)
                    visited[source] = True 
            
                    while stack:
                        cur_node = stack.pop()
                        if cur_node == destination:
                            return True 
                        for neighbor in graph[cur_node]:
                            if not visited[neighbor]:
                                stack.append(neighbor)
                                visited[neighbor] = True 
                    
                    return False
            ```
            
- AC 코드
    - Editorial 보고 짰더니 통과
    
    ```python
    class Solution:
        def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
            graph = {}
            for s, e in edges:
                if s not in graph:
                    graph[s] = [e]
                else:
                    graph[s].append(e)
                if e not in graph:
                    graph[e] = [s]
                else:
                    graph[e].append(s)
            visited = [False] * n
            visited[source] = True
    
            def dfs(cur_node):
                if cur_node == destination:
                    return True
                else:
                    for neighbor in graph[cur_node]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            if dfs(neighbor):
                                return True
                return False
            
            if dfs(source):
                return True
            return False
    ```
    
- BFS revisited
    - Trial
        - memory exceed error 남
            
            ```python
            class Solution:
                def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
                    graph = collections.defaultdict(list)
                    for s, e in edges: # bidirectional
                        graph[s].append(e)
                        graph[e].append(s)
                    visited = set()
                    queue = collections.deque([[source]])
                    while queue:
                        cur_path = queue.popleft()
                        cur_node = cur_path[-1]
                        if cur_node == destination:
                            return True 
                        for neighbor in graph[cur_node]:
                            if neighbor not in visited:
                                queue.append(cur_path + [neighbor])
                        visited.add(cur_node)
                    return False
            ```
            
        - path를 다 넣는게 아니라 노드만 넣으면? → Time exceed error남
            
            ```python
            class Solution:
                def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
                    graph = collections.defaultdict(list)
                    for s, e in edges: # bidirectional
                        graph[s].append(e)
                        graph[e].append(s)
                    visited = set()
                    queue = collections.deque([source])
                    while queue:
                        cur_node = queue.popleft()
                        if cur_node == destination:
                            return True 
                        for neighbor in graph[cur_node]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                        visited.add(cur_node)
                    return False
            ```
            
        - 설명이랑 다르게 모범답안에서는 방문 여부를 큐에 넣기 전에 확인하고, 큐에 넣자마자 방문 처리 해버리네 ;; 뭐가 맞는 건지
        - AC 코드
            
            ```python
            class Solution:
                def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
                    graph = collections.defaultdict(list)
                    for s, e in edges: # bidirectional
                        graph[s].append(e)
                        graph[e].append(s)
                    
                    queue = collections.deque([source])
                    visited = set([source])
                    while queue:
                        cur_node = queue.popleft()
                        if cur_node == destination:
                            return True 
                        for neighbor in graph[cur_node]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                                visited.add(neighbor)
                        
                    return False
            ```