# 1584. Min Cost to Connect All Points

Status: done, in progress
Theme: graph
Created time: December 20, 2023 6:52 PM
Last edited time: December 22, 2023 11:05 AM

- 문제 이해
    - 크루스칼 알고리즘 첫 문제인데 템플릿이 안나왔으니까 마음 편하게 풀자
    - edge부터 sort 하고 봐야 하는데 edge weight는? → 이게 맨하탄 distance
    - union-find도 undirected인 거 맞지?
- AC 코드-크루스칼 🪇
    
    ```python
    class UnionFind:
        def __init__(self, size):
            self.root = [i for i in range(size)]
            self.rank = [1] * size
        def find(self, x):
            if x != self.root[x]:
                self.root[x] = self.find(self.root[x])
            return self.root[x]
        def union(self, x, y):
            root_x, root_y = self.find(x), self.find(y)
            if self.rank[root_x] > self.rank[root_y]:
                self.root[root_y] = root_x 
            elif self.rank[root_y] > self.rank[root_x]:
                self.root[root_x] = root_y
            else: # same level
                self.root[root_y] = root_x
                self.rank[root_x] += 1 
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    class Solution:
        def minCostConnectPoints(self, points: List[List[int]]) -> int:
            min_cost = 0
            n = len(points)
            edges = []
            UF = UnionFind(n)
            for i in range(n):
                for j in range(i+1, n):
                    manhattan_d = abs(points[i][0]-points[j][0]) + abs(points[i][1]-points[j][1]) 
                    edges.append([i, j, manhattan_d])
            sorted_edges = sorted(edges, key=lambda x:x[2])
            for e in sorted_edges:
                p1, p2, cost = e
    						# checking num edges
                if not UF.connected(p1, p2):
                    UF.union(p1, p2)
                    min_cost += cost
            return min_cost
    ```
    
- AC 코드-프림 🪇
    
    ```python
    import heapq 
    class Solution:
        def minCostConnectPoints(self, points: List[List[int]]) -> int:
            heap = [] 
            visited = set()
            cost = 0
            
            heapq.heappush(heap, (0, (points[0][0], points[0][1])))
            while heap:
                cur_cost, cur_node = heapq.heappop(heap)
                if cur_node in visited:
                    continue
                visited.add(cur_node)
                cost += cur_cost
                if len(visited) == len(points):
                    return cost
                for p in points:
                    if tuple(p) not in visited:
                        new_cost = abs(cur_node[0]-p[0]) + abs(cur_node[1]-p[1])
                        heapq.heappush(heap, (new_cost, tuple(p)))
    ```