# 1168. Optimize Water Distribution in a Village

Status: done, in progress, with help, 🤺
Theme: graph
Created time: December 14, 2023 1:05 PM
Last edited time: January 2, 2024 11:34 PM

- 과정
    - 최소 비용 우물을 먼저 파야 한다는 보장도 없음. 더 비싼 우물을 팠을 때 주변 파이프 설치료가 낮으면 그게 더 이익일 수도 있음
    - 일반적으로 union을 한다고 하면…
        - pipe를 비용 별로 정렬 하고, union을 앞에서부터 해나가려면 우물이 둘 중 하나는 있어야 하니까 확인하고. - 둘 중 wells 비용이 적은 쪽으로?
        - 하나씩 해나간다고 하면…self.find(root_x) 해서 하나로 귀결되는지 봐야함? 하나로 귀결되면 하나의 same component인데 여기서는 꼭 그럴 필요는 없을 듯. 오히려 연결 비용이 비싸면 자기 혼자만의 우물을 갖는게 더 나을 수도…근데 그걸 어떻게 구하지?
    - 어느 집 우물을 파야 연결성이 제일 좋은지도 모르겠당
    - kruskal에서는 edge weight만 비교하는데…
    - 두 집 다 우물이 없는 경우, 어느 집에 우물을 줘야 최소 비용이 될까?
- Editorial
    - Intuition
        - MST 문제 복습
            - connected, edge-weighted, undirected graph 가정
            - weight sum을 최소로 가져가면서 모든 노드를 연결하는 subset of edges
            - cost는 edge만 연결되어 있음
        - 우리 문제의 경우 vertex에도 cost가 달려 있음
            - kick: **현재 그래프에 가상의 노드를 하나 추가**
                
                ![Untitled](Untitled%2053.png)
                
                - 물론 이 가상의 노드와 다른 모든 노드를 연결하는 edge들도 추가해야 함
                - 각 노드에 할당된 비용을 새롭게 생긴 가상의 노드-각 노드 사이의 edge의 비용에 부여
    - AC 코드-크루스칼(짱 빠름)
        
        ```python
        class UnionFind:
            def __init__(self, size):
                self.root = [i for i in range(size)]
                self.rank = [1] * size
            def find(self, x):
                if self.root[x] != x:
                    self.root[x] = self.find(self.root[x])
                return self.root[x]
            def union(self, x, y):
                root_x, root_y = self.find(x), self.find(y)
                if root_x != root_y:
                    if self.rank[root_x] > self.rank[root_y]:
                        self.root[root_y] = root_x
                    elif self.rank[root_x] < self.rank[root_x]:
                        self.root[root_x] = root_y
                    else: # same level
                        self.root[root_y] = root_x
                        self.rank[root_x] += 1 
        
            def is_connected(self, x, y):
                return self.find(x) == self.find(y)
        
        class Solution:
            def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
                # house: 1, ..., n
                # ith house cost: wells[i-1]
                # virtual: 0
                for i in range(1, n+1):
                    pipes.append((0, i, wells[i-1]))
                pipes.sort(key=lambda x:x[2]) # sort by cost
                UF = UnionFind(n+1)
                total_cost = 0 
                for p in pipes:
                    h1, h2, cost = p
                    if not UF.is_connected(h1, h2):
                        total_cost += cost
                        UF.union(h1, h2)
                return total_cost
        ```
        
    - AC 코드-프림(짱 느림)
        
        ```python
        import heapq
        
        class Solution:
            def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
                # house: 1, ..., n
                # ith house cost: wells[i-1]
                # virtual: 0
                for i in range(1, n+1):
                    pipes.append((0, i, wells[i-1]))
                mst = [False] * (n+1)
                graph = {i:[] for i in range(n+1)}
                for a, b, cost in pipes:
                    graph[a].append((cost, b))
                    graph[b].append((cost, a))
                total_cost = 0
                mst[0] = True
                heapq.heapify(graph[0])
                priority_queue = graph[0]
                while priority_queue:
                    cur_cost, cur_node = heapq.heappop(priority_queue)
                    if not mst[cur_node]:
                        mst[cur_node] = True
                        total_cost += cur_cost
                    for next_cost, next_node in graph[cur_node]:
                        if not mst[next_node]:
                            heapq.heappush(priority_queue, (next_cost, next_node))
                return total_cost
        ```
        
    - 이론 상으로는 둘의 time complexity가 동일한데 의문이다