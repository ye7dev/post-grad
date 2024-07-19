# 1059. All Paths from Source Lead to Destination

Status: done, in progress, with help
Theme: graph
Created time: December 15, 2023 11:06 PM
Last edited time: December 18, 2023 4:28 PM

- 문제 이해
    - If a path exists from the `source` node to a node with no outgoing edges, then that node is equal to `destination`.
        - 이 말이 이해가 잘 안간다.
        - 아래 그림에서 1도 destination이 된다는 설명 같았는데 막상 return value는 False
            
            ![Untitled](Untitled%2062.png)
            
    - destination과 cycle 관계를 이루면 그건 True? False?
    
    ⇒ outgoing edge가 없는데 destination이 아니면 무조건 return False 하라는 뜻 
    
- Trial
    - 1st trial code
        
        ```python
        class Solution:
            def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
                graph = collections.defaultdict(list)
                for s,e in edges:
                    graph[s].append(e)
        
                visited = [False] * n
                
                def lead_to_dest(node):
                    if node == destination:
                        return True 
                    if visited[node]: # cycle 
                        return False
                    visited[node] = True
        						if not edges[node]: # no neighbor
        								return False
                    for neighbor in edges[node]:
                        if not lead_to_dest(neighbor):
                            return False
                    return True
                        
                return lead_to_dest(source)
        ```
        
        - 예제 2개 맞고 하나 틀림
        - `RecursionError: maximum recursion depth exceeded in comparison`
            - 재귀 문제를 풀면 자주 만나는 친구…
            - `visited` marking을 생략해서 그렇게 되었다고 한다…
    - Editorial 다 읽고 짠 코드 (AC)
        
        ```python
        class Solution:
            def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
                graph = collections.defaultdict(list)
                for s,e in edges:
                    graph[s].append(e)
                
                color = ["w"] * n
                
                def lead_to_dest(node):
                    if not graph[node]:
                        if node == destination:
                            return True 
                        return False 
                    if color[node] == 'g': # cycle
                        return False 
                    if color[node] == 'w':
                        color[node] = 'g'
                        for neighbor in graph[node]:
                            if not lead_to_dest(neighbor):
                                return False
                        color[node] = 'b'
                        return True 
        						# 이 위까지는 51/56이었는데 아래 두 줄 추가하면서 AC
                    if color[node] == 'b':
                        return True 
                    
                return lead_to_dest(source)
        ```
        
        - 51/ 56
- Editorial
    - Overview
        - directed graph
        - adjacency list 자료 구조에서 더 이상 이웃이 없는 노드는 destination이거나 아닐 수 있는데, 아닌 경우는 무조건 return False
        - src → dst 경로 개수는 유한하다 == True가 나오는 경우의 그래프는 트리다
            - 그래프에는 cycle이 없다
        
        ⇒ graph traversal 알고리즘을 타면서 체크해야 할 사항이 두 가지 
        
        1) cycle이 있으면 return False
        
        2) traversal 중에 만나는 leaf node가 destination이 아니면 return False
        
    - DFS
        - Intuition
            - cycle 체크하는 데 node-coloring variant를 사용하는 경우
                - 한 노드 당 세 가지 state가 존재
                - white: node가 아직 처리되지 않은 경우
                - gray: node가 처리되었다
                    - 해당 node의 DFS가 시작되기는 했지만, 끝나지 않은 경우
                    - DFS tree에서 이 노드의 후손들이 아직 처리되지 않았거나 function call stack에 있는 경우
                    - 그림-cycle detection
                        
                        ![Untitled](Untitled%2063.png)
                        
                        - 2의 노드가 recursion stack에 있기 때문에 회색이 칠해졌는데, 프로세싱이 완료되기 전 2의 desendents로부터 2로 들어오는 edge를 마주함 → cycle
                - black: 해당 node와 그 후손들까지 모두 처리가 완료되었다
                    - 그림-visited array의 한계
                        
                        ![Untitled](Untitled%2064.png)
                        
                        - 1 → 2 → 4 경로 지난 다음 다시 1로 돌아온다
                        - 다음 경로는 1 → 3 → 4 인데 4는 이미 방문된 node이다. 그럼에도 1→2→4와 1→3→4는 서로 cycle을 형성하지 않는다. visited array만 두고 봤으면 4로 인해 cycle로 잡혔을 텐데.
                        - 2의 유일한 후손은 4고 4를 방문하면서 2의 처리는 완료된셈 → 검은색
                        - 4는 후손이 더 이상 없으므로 자기 자신을 방문처리 하면서 처리가 완료된 것 → 검은색
                        
                        ⇒ 따라서 검은색 노드는 다시 방문하더라도 cycle을 형성하는 게 아님! (↔ 회색 노드는 다시 방문하면 cycle)
                        
            - 알고리즘
                1. 재귀 함수 `leadsToDest` : 처리가 필요한 현재 node를 input으로 받는다 & array color 생성  
                2. input으로 들어온 node에 이웃이 있는지 없는지 체크 → 이웃이 없는 노드가 dest이면 return True, 아니면 return False 
                3. 현재 node의 상태는 세 가지가 가능
                    1. 검은색 → 이미 처리된 노드라 더 할 일 없음
                    2. 흰색 → 회색 처리하고 이 노드를 root로 삼는 subgraph를 처리 
                    3. 이미 회색이면 return False ← cycle detected 
                4. input node의 모든 이웃을 돌면서 재귀 함수 호출. 중간에 return False가 나오면 최종 return도 바로 False
                5. 현재 node를 검은색으로 표시하고, return True
                    - 4.에서 모든 이웃을 돌고도 False가 나오지 않았기 때문에