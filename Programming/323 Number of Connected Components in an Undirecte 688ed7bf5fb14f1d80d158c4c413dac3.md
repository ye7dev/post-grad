# 323. Number of Connected Components in an Undirected Graph

Status: done, in progress
Theme: graph
Created time: December 13, 2023 11:33 AM
Last edited time: December 13, 2023 11:42 AM

- 코드
    
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
            if root_x != root_y:
                if self.rank[root_x] > self.rank[root_y]:
                    self.root[root_y] = root_x
                elif self.rank[root_y] < self.rank[root_y]:
                    self.root[root_x] = root_y
                else: # same rank
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1 
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    class Solution:
        def countComponents(self, n: int, edges: List[List[int]]) -> int:
            UF = UnionFind(n)
            for a, b in edges:
                UF.union(a, b)
            root_set = []
            for i in range(n):
                cur_root = UF.find(UF.root[i])
                if cur_root not in root_set:
                    root_set.append(cur_root)
            return len(root_set)
    ```