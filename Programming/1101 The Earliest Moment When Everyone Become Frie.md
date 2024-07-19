# 1101. The Earliest Moment When Everyone Become Friends

Status: in progress
Theme: graph
Created time: December 13, 2023 11:43 AM
Last edited time: December 13, 2023 12:15 PM

- 과정
    - all connected method 추가했는데 9/67에서 막힘
        
        ```python
        class UnionFind:
            def __init__(self, size):
                self.root = [i for i in range(size)]
                self.rank = [1] * size
                self.n = size
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
                    else: # same level 
                        self.root[root_y] = root_x
                        self.rank[root_x] += 1 
            def connected(self, x, y):
                return self.find(x) == self.find(y)
            def all_connected(self):
                for i in range(self.n):
                    for j in range(i+1, self.n):
                        if not self.connected(i, j):
                            return False
                return True
        
        class Solution:
            def earliestAcq(self, logs: List[List[int]], n: int) -> int:
                UF = UnionFind(n)
                i = 0
                while i < n:
                    t, a, b = logs[i]
                    UF.union(a, b)
                    if UF.all_connected():
                        return t 
                    else:
                        i += 1 
                return -1
        ```
        
    - log를 시간 순으로 sort 했더니 21/67에서 막힘
- 코드
    - input n이랑 Logs 길이랑 다른 숫자였음
    
    ```python
    class UnionFind:
        def __init__(self, size):
            self.root = [i for i in range(size)]
            self.rank = [1] * size
            self.n = size
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
                else: # same level 
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1 
        def connected(self, x, y):
            return self.find(x) == self.find(y)
        def all_connected(self):
            root_set = []
            for i in range(self.n):
                cur_root = self.find(i)
                if cur_root not in root_set:
                    root_set.append(cur_root)
            print(root_set)
            if len(root_set) == 1: 
                return True
            else:
                return False
    
    class Solution:
        def earliestAcq(self, logs: List[List[int]], n: int) -> int:
            logs.sort()
            UF = UnionFind(n)
            i = 0
            while i < len(logs):
                t, a, b = logs[i]
                UF.union(a, b)
                if UF.all_connected():
                    return t 
                else:
                    i += 1 
            return -1
    ```
    
     
    
- Editorial 보고 수정한 훨씬 빨라진 코드
    
    ```python
    class UnionFind:
        def __init__(self, size):
            self.root = [i for i in range(size)]
            self.rank = [1] * size
            self.n = size
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
                else: # same level 
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1 
                return True
            else:
                return False # merge already  
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    class Solution:
        def earliestAcq(self, logs: List[List[int]], n: int) -> int:
            logs.sort()
            UF = UnionFind(n)
            group_cnt = n 
            for t, a, b in logs:
                if UF.union(a, b):
                    group_cnt -= 1 
                if group_cnt == 1:
                    return t
            return -1
    ```