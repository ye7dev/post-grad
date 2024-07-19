# 261. Graph Valid Tree

Status: done, in progress
Theme: graph
Created time: December 12, 2023 6:38 PM
Last edited time: December 13, 2023 11:33 AM

- 문제 이해
    
    valid tree가 아니다 = cycle이 있다 
    
    이미 Union 된 set 안에 있는 다른 원소와 연결된다 
    
    union 하고도 root가 안바뀐다 
    
- 과정
    
    union에서 root_x == root_y 면 return False 하라고 했는데 이걸로 하니 38/45
    
    invalid tree의 경우가 cycle 말고 not connected도 있다- 예를 들어 [0, 1], [2, 3] 얘네를 union 하면 최종 root값이 서로 다르게 나올 것 
    
- 코드
    
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
    
    elif self.rank[root_x] < self.rank[root_y]:
    
    self.root[root_x] = root_y
    
    else: # same rank
    
    self.root[root_y] = root_x
    
    self.rank[root_x] += 1
    
    else:
    
    return False
    
    def connected(self, x, y):
    
    return self.find(x) == self.find(y)
    
    class Solution:
    
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
    
    uf = UnionFind(n)
    
    for a, b in edges:
    
    if uf.union(a, b) is False:
    
    return False
    
    first_root = uf.root[0]
    
    for i in range(1, n):
    
    if uf.find(uf.root[i]) != first_root:
    
    return False
    
    return True
    
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
                elif self.rank[root_x] < self.rank[root_y]:
                    self.root[root_x] = root_y
                else: # same rank
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1 
            else:
                return False
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    class Solution:
        def validTree(self, n: int, edges: List[List[int]]) -> bool:
            uf = UnionFind(n)
    				# cycle
            for a, b in edges:
                if uf.union(a, b) is False:
                    return False
    				# not connected 
            first_root = uf.root[0]
            for i in range(1, n):
                if uf.find(uf.root[i]) != first_root:
                    return False
            return True
    ```