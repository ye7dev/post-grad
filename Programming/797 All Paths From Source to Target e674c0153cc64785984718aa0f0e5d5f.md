# 797. All Paths From Source to Target

Status: done, in progress, with help
Theme: graph
Created time: December 14, 2023 5:04 PM
Last edited time: December 18, 2023 4:39 PM

- 과정
    
    DFS iterative로 풀고 싶은데 어디서 visited[node]=False 를 해야 하는지 모르겠음
    
    - trial code
        
        ```python
        class Solution:
            def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
                n = len(graph)
                src, dst = 0, n-1
                visited = [False] * n
                answer = []
        
                stack = [[src]]
                visited[src] = True
                while stack:
                    cur_path = stack.pop()
                    cur_node = cur_path[-1]
                    if cur_node == dst:
                        answer.append(cur_path)
                        visited[cur_node] = False
                        continue 
                    for neighbor in graph[cur_node]:
                        if not visited[neighbor]:
                            stack.append(cur_path+[neighbor])
                            visited[neighbor] = True                 
        
                return answer
        ```
        
- Editorial
    - Backtracking
        - 모든 주어진 node에 대해, 재귀적으로 이웃 node를 시도하되, target에 도달하거나 더 이상 시도할 node가 없으면 중단
            
            ↳ 시도? 다음 노드로 넘어가기 넣의 상태를 표시해두고, 나중에 이 선택으로 돌아와서 다른 루트로 탐색을 다시 시작 
            
        - `backtrack(cur_node, path)` 라는 재귀 함수를 구현하는 것이 핵심
            - path: 지금까지 순회된 리스트 목록
            - base case - 우리가 재귀를 멈추는 순간을 결정하지
                - 현재 node가 destination 일 때
            - body - 현재 node의 모든 이웃을 돈다
                - path에 neighbor node를 붙임으로써 mark the choice
                - 재귀적으로 backtrack 함수 불러서 더 깊게 탐색
                - iteration 한 뒤에 path에서 위에서 추가했던 이웃 노드를 뺌으로써 reverse the choice → 그래야 다음 이웃 노드를 붙여서 또 탐색 시작할 수 있음
        - 시간복잡도
            - 그래프에 노드를 하나 추가할 때마다 path 개수는 두배가 된다
                - 왜냐면 원래 상태에서 존재하는 path에다가 새로운 node를 붙이기만 해서 같은 개수의 새로운 path를 만들 수 있기 때문
            
            → node가 N개면, 최대 path 개수는 2^i(for i in range(N-2)) = 2^(N-1)-1 
            
            → path 하나 당 최대 N-2개의 node를 갖게 됨 → 하나의 path를 빌드하는데 O(N) 걸림 
            
            ⇒ $O(2^N \cdot N)$ 
            
            - 공간 복잡도는 O(N)-recursion 사용하고, 최대 N번의 재귀 stack 사용될 수 있음
    - Top-down DP
        - target function `all_path_to_target(cur_node)`
            - input: cur_node → output: all the paths
            - current node의 이웃 node들을 iterate 하면서 계산
                - 현재 node 에서 target node로 까지의 path들은 현재 node의 이웃 노드 각각으로부터 시작하는 모든 path들로 구성되어 있다 (?)
        - 알고리즘
            - `all_path_to_target(cur_node)`
                - base case: 현재 node가 target node
                - body : 각 이웃 node에 대해 재귀 호출
            - 이 함수를 통해 return 받은 결과를 가지고, downstream paths(?) 앞에 현재 node를 붙인다
        - 결과의 재사용
            - target function으로부터 돌아온 결과를 캐싱
                - 왜냐면 path 간에 겹치는 부분이 있을 경우, 하나의 node를 여러번 마주하게 될 것이기 때문에
            - 그래서 일단 주어진 node에서 target node까지의 결과를 알게 되면, 저장해두기 (memoization)
        - 코드
            - 개빠름
            
            ```python
            class Solution:
                def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
                    src, dst = 0, len(graph)-1
                    dp = {}
                    
                    def all_path_to_target(cur_node):
            						# base case
                        if cur_node == dst:
                            return [[cur_node]]
            						# already calculated results
                        if cur_node in dp:
                            return dp[cur_node]
            						# new caculation
                        results = []
                        for neighbor in graph[cur_node]:
                            for path in all_path_to_target(neighbor):
                                results.append([cur_node] + path) # 점화식
                        dp[cur_node] = results
                        return results
            
                    return all_path_to_target(src)
            ```
            
    - DFS
        - 코드
            
            ```python
            class Solution:
                def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
                    def dfs(node):
                        path.append(node)
                        if node == len(graph) - 1:
                            paths.append(path.copy())
                            return
            
                        next_nodes = graph[node]
                        for next_node in next_nodes:
                            dfs(next_node)
                            path.pop()
            
                    paths = []
                    path = []
                    if not graph or len(graph) == 0:
                        return paths
                    dfs(0)
                    return paths
            ```
            
        - path.copy()를 써야 하는 이유
            1. **Appending the Same Object**: If you append **`path`** directly to **`paths`** without using **`path.copy()`**, you are actually appending a reference to the same **`path`** list object, not a snapshot of its current state.
            2. **Consequences of Shared References**: Since all appended paths in **`paths`** are references to the same list object, any modification to **`path`** (like popping an element at the end of a DFS traversal) affects all the entries in **`paths`**. This is why, without **`path.copy()`**, you end up with empty lists or incorrect paths in **`paths`**, as the single **`path`** list eventually becomes empty at the end of the DFS process.
            3. **Using `path.copy()`**: By using **`path.copy()`**, you create a new list object that is a snapshot of the **`path`** at that moment. This snapshot is then appended to **`paths`**. This way, subsequent modifications to the **`path`** list do not affect the snapshots already stored in **`paths`**.
- AC 코드
    
    ```python
    class Solution:
        def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
            src, dst = 0, len(graph)-1
            answer = []
    
            def backtrack(cur_node, path=[0]):
                if cur_node == dst:
                    answer.append(path[:])
                    return 
                for neighbor in graph[cur_node]:
                    path.append(neighbor)
                    backtrack(neighbor, path)
                    path.pop()
            
            backtrack(0)
    
            return answer
    ```
    
- BFS revisited
    - 여기서는 최대 n=15라서 path 자체를 큐에 넣어도 될 듯?
    - 얘도 color array 써서 visited 처리해야 하나? → 다른 문제([[**1059. All Paths from Source Lead to Destination**](https://leetcode.com/problems/all-paths-from-source-lead-to-destination/description/)](1059%20All%20Paths%20from%20Source%20Lead%20to%20Destination%205d6c4dcc578d41ddaba50bbb075a9a31.md) issue 였음)
    - 우선 path 큐에 넣기 & 일반 visited로 해본다
        - n = len(graph) 해도 될 것 같은게 예시 문제 보면 빈 List 자체도 graph에 들어 있음
    - TLE 나온 trial 코드
        - path exist 때랑 방문 처리 순서가 다른 게 아닐까 하고 비디오 설명 대로 넣어봤는데 TLE~
        
        ```python
        class Solution:
            def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
                n = len(graph)
                queue = collections.deque([[0]])
                visited = set()
        
                answer = []
                
                while queue:
                    cur_path = queue.popleft()
                    cur_node = cur_path[-1]
                    if cur_node == n-1: 
                        answer.append(cur_path[:])
                        return 
                    
                    for neighbor in graph[cur_node]:
                        if neighbor not in visited:
                            cur_path.append(neighbor)
                            queue.append(cur_path)
                            cur_path.pop()
        
                    visited.add(cur_node)
                
                return answer
        ```
        
    - Explore 해설
        - 아예 visited가 없다 ;;
            - 물론 직관적으로 생각해도 여러 경로를 통해 같은 노드에 도달할 테니 그런 것 같긴 함.
            - DFS 때도 안 썼나?
        - AC 코드
            
            ```python
            class Solution:
                def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
                    n = len(graph)
                    queue = collections.deque([[0]])
            
                    answer = []
                    
                    while queue:
                        cur_path = queue.popleft()
                        cur_node = cur_path[-1]
                        
                        for neighbor in graph[cur_node]:
                            if neighbor == n-1:
                                answer.append(cur_path + [neighbor])
                            else:
                                queue.append(cur_path + [neighbor])
            
                    return answer
            ```