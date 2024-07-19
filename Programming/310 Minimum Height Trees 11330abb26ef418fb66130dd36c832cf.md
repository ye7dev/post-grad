# 310. Minimum Height Trees

Status: done, in progress, with help
Theme: graph
Created time: January 2, 2024 2:18 PM
Last edited time: January 2, 2024 5:35 PM

- [ ]  복잡도 분석
- 문제 이해
    - 트리: 두 노드가 정확히 하나의 path로만 연결되는 undirected graph
    - simple cycle이 없는 graph는 모두 tree
    - 아무 노드나 root로 삼을 수 있음. 모든 가능한 rooted tree 중에 최소 높이를 갖는 tree들의 root label을 return 하라
    - 높이: longest downward path btw the root and a leaf
    - 이 문제가 칸 알고리즘의 예제로 나온 걸 고려하면, In-degree 숫자가 중요한 것 같은데…
    - 돌아가면서 큐에 start로 넣고, 그걸 탐색 완료 처리했을 때 선결 조건이 없어지는 애들이 몇 개인지 확인. len(queue) 별로 한 묶음씩 돌고, current len(queue)만큼 다 돌 때마다 height 하나 증가시켜야 할 듯
    - 근데 칸 알고리즘을 undirected에 대해 쓸 수 있나?
    - root node에는 선결조건이 없다. 어떤 노드를 root 삼는다고 할 때, 그 root는 다른 노드의 이웃으로 들어가있지 말자
    - 칸 알고리즘에서는 visited를 안썼던듯? 선결조건이 여러 개더라도 마지막 해결되는 순간==in_degree가 정확히 0인 순간에만 큐에 들어갈 수 있음. 이미 방문을 완료해서 in_degree가 0인 상태에서는 다른 조건에 의해 또 나오더라도, -=1 하는 순간 음수가 되어서 큐에 들어갈 수 없음
- Trial
    - 방법은 맞아서 예제 모두 맞히고, 65/71까지 가지만 TLE
        
        ```python
        class Solution:
            def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
                height = [0] * n
                graph = {i:[] for i in range(n)}
        
                for a,b in edges:
                    graph[a].append(b)
                    graph[b].append(a)
                
                for i in range(n):
                    root = i 
                    visited = [False] * n
                    visited[root] = True
                    queue = collections.deque([root])
                    while queue:
                        cur_level = len(queue)
                        for _ in range(cur_level):
                            cur_node = queue.popleft()
                            for neighbor in graph[cur_node]:
                                if not visited[neighbor]:
                                    queue.append(neighbor)
                                    visited[neighbor] = True
                        
                        height[root] += 1 
        
                answer = []
                min_height = min(height)
                for i in range(n):
                    if height[i] == min_height:
                        answer.append(i)
                    
                return answer
        ```
        
    - 꼼수-그런데 이제 예제 통과를 하지 못하는
        
        ```python
        class Solution:
            def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
                height = [0] * n
                graph = {i:set() for i in range(n)}
                
                for a,b in edges:
                    graph[a].add(b)
                    graph[b].add(a)
        
                graph = sorted(graph.items(), key=lambda x:len(x[1]))
        
                if n % 2 == 0:
                    return [graph[-2][0], graph[-1][0]]
                else:
                    return [graph[-1][0]]
        ```
        
    - 2개까지 남았는데, 두 개중에 하나는 어떻게 걸러냄?
        
        ```python
        class Solution:
            def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
                height = [0] * n
                graph = {i:set() for i in range(n)}
        
                # edge case : *, *-*
                if n <= 2: 
                    return [i for i in range(n)]
                
                # populate adjacency list
                for a,b in edges:
                    graph[a].add(b)
                    graph[b].add(a)
        
                start = [key for key in graph if len(graph[key]) == 1]
                queue = collections.deque(start)
                remains = n
                while remains > 2:
                    cur_node = queue.popleft()
                    for neighbor in graph[cur_node]: # connection is mutual
                        graph[neighbor].remove(cur_node)
                        if len(graph[neighbor]) == 1:
                            queue.append(neighbor)
        
                    graph[cur_node] = set()
                    remains -= 1 
        
                ans = []
                for key in graph:
                    if len(graph[key]) != 0:
                        ans.append(key)
                return ans
        ```
        
- Editorial - Topological Sorting
    - Intuition
        - 두 노드 간의 거리: 두 노드를 연결하는 edge의 개수
            - 보통은 노드를 연결하는 path가 여러 개 있지만, 문제에서는 어떤 노드로부터 트리를 형성할 수 있다고 했기 때문에, 두 노드 간의 path는 하나만 존재
            - 그래프 안에 cycle도 없음
        - 트리의 높이: root와 모든 leaf node 사이 거리 중 maximum distance
        - 위의 두 가지 정의를 바탕으로 문제를 다시 서술해보면
            - overall 다른 모든 노드들 특히 leaf 노드들과 가까운 노드들을 찾아라(?)
            - 그래프를 원의 영역이라고 보면, leaf node는 원의 경계가 되고, 우리는 사실 centroid들을 찾게 되는 것임
                - centroid: 모든 경계 노드(leaf nodes)들과 가까운 노드
        - tree-alike graph에 대해서는, centroid 개수가 2개를 넘을 수 없다
            - 노드가 chain을 형성한다고 하면, 위의 서술이 직관적으로 이해가 갈 것이다
                
                ![Untitled](Untitled%2022.png)
                
                - 만약 노드의 개수가 짝수면, 두 개의 centroid가 존재
                - 노드가 홀수개면, 하나의 centroid만 존재
            - contradiction으로 증명
                - 그래프에 3개의 centroid가 존재한다고 가정하고, centroid가 아닌 노드들을 모두 지운다고 해보자
                - 그러면 남은 3개의 centroid 들은 삼각형을 형성하게 될 것 - 왜냐면 centroid들은 서로에게 똑같이 중요하기 때문에(?), 그리고 서로 서로와 같은 거리를 갖고 있어야 할 것
                    
                    ![Untitled](Untitled%2023.png)
                    
                - 만약 삼각형 중 어느 하나의 edge라도 없어진다면, 3개의 centroid는 하나의 centroid들로 줄여질 것
                - 근데 삼각형은 cycle을 이루기 때문에 tree-alike graph라는 우리의 가정에 반하게 됨
                - 이처럼 2개보다 더 많은 centroid들을 가진 경우는 centroid 들 사이에서 cycle을 형성할 수 밖에 없게 되는데 이는 가정에 어긋난다
    - 알고리즘
        - 추가 설명
            - 문제를 다시 요약하면: tree-alike graph에서 2개 이하의 모든 centroid를 찾는 것
            - layer-by-layer로 가장자리 leaf node들을 쳐내다가 graph에 중심에 도달하기
                - first layer of the leaf nodes: connection을 하나만 갖고 있는 노드들
                - 첫번째 layer에 있는 노드들을 걷어내고 나면, 그 다음 layer에 있던 non-leaf node들이 이제 leaf node가 된다
                - 이렇게 계속 다듬기 작업을 하다가 두 개의 노드만 graph에 남게 되면, 우리가 찾던 centroid들을 만나게 되는 것
            - dependency에 따라 object를 정렬하는 topological sorting과 닮아있음(어디가?)
                - 예를 들어 과목 짜기 문제에서처럼, 가장 dependency가 적은 과목이 수강해야 하는 순서상 가장 처음으로 나타나게 될 것
                - 우리 경우에는 centroid로부터 가장 먼 노드부터 쳐낸다
        - 구현 설명
            1. adjacency list로 그래프 생성
            2. leaf node를 담을 큐 만들기 
            3. 현재 leaf node를 큐에 담는다 
            4. 그래프에서 노드 두 개만 남을 때까지 loop 진행 
            5. 각 iteration에서 큐에서 현재 leaf node를 제거 
                - 이 때 노드를 제거하면서 노드에 연결된 edge도 제거
                - 그래야 non-leaf node들도 leaf node가 될 수 있음. 그리고 얘네가 다음 iteration에서 다듬어질 대상
                - 그래프에 두 개 이하의 노드가 남을 때까지 iteration 진행
    - AC 코드
        
        ```python
        class Solution:
            def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
                height = [0] * n
                graph = {i:set() for i in range(n)}
        
                # edge case : *, *-*
                if n <= 2: 
                    return [i for i in range(n)]
                
                # populate adjacency list
                for a,b in edges:
                    graph[a].add(b)
                    graph[b].add(a)
        
                leaf_nodes = [key for key in graph if len(graph[key]) == 1]
                remains = n
                while remains > 2:
                    remains -= len(leaf_nodes) 
                    next_leaf_nodes = []
                    for node in leaf_nodes:
                        sole_neighbor = graph[node].pop() # goodbye to the one
                        graph[sole_neighbor].remove(node) # might be one of them
                        if len(graph[sole_neighbor]) == 1:
                            next_leaf_nodes.append(sole_neighbor)
                    leaf_nodes = next_leaf_nodes
                
                return leaf_nodes
        ```
        
- 내 설명
    - 이 문제에서의 위상: edge 개수가 몇 개냐-1개인 노드들에 대해 먼저 처리 작업을 한다는 점에서 위상에 따라 순서가 달라진다는 개념이 적용되는 듯
    - 꼭 알아야 풀 수 있는 점: tree-alike graph에서 나올 수 있는 centroid 개수는 최대 2개다-특히 전체 노드 개수가 홀수면 1개. 짝수면 2개나 1개
    - edge case: 노드가 하나 (**), 두 개(*-**)
        - 가진 거 전부가 다 centroid다
    - bfs, dfs 사용 안하는 걸로 보임
        - iteration 시작 노드는 bfs랑 비슷하게 시작하긴 함
    - edge 개수가 1개인 애들이 다음번 제거 대상
        - 제거할 때는 그래프가 undirected 임에 주의
        - 제거하는 시점에서
            - current node는 이웃이 하나밖에 안남았다는 것이 알려진 상태
            - 이웃 입장에서는 current node가 유일한 이웃일 수도 아닐수도
            - 따라서 두 node에 대해서 제거 방법 다르게 써야
        - 그리고 이웃도 다음 제거 대상에 낄 수 있는지 확인하고.