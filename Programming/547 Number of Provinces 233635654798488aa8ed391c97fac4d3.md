# 547. Number of Provinces

Status: done, in progress
Theme: graph
Created time: December 12, 2023 5:48 PM
Last edited time: December 12, 2023 6:33 PM

- disjoint set 이용해야 하는 문제
- 문제 이해
    - `isConnected[i][j] == isConnected[j][i]`
        
        → 이러면 j는 i보다 클 때만 보면 될 것 같은데? 
        
    - union find 클래스 정의 하고, connected pair에 대해서 Union 모두 수행. 그리고 마지막에 root에서 unique root 개수가 몇 개인지 세면 Province 개수라고 생각했는데 왜 답이 안나오지
    - 왜냐면 우리가 최종 외운 버전의 union에서는 input x, y의 root 값을 바꾸는게 아니라, root_x, root_y의 root 값을 바꾸는 거였음 → find로 호출되지 않은 node의 경우 root array는 parent node를 담고 있을 수도 있음. root 가 아니라.
    - 그래서 마지막에 self.root array 돌면서 진짜 root가 몇 개나오는지 확인해야 함
- 코드
    
    ```python
    class UnionFind:
        def __init__(self, size):
            self.rank = [1] * size
            self.root = [i for i in range(size)]
        def find(self, x):
            if x == self.root[x]:
                return x 
            else:
                self.root[x] = self.find(self.root[x])
                return self.root[x]
    
        def union(self, x, y):
            root_x, root_y = self.find(x), self.find(y)
            if root_x != root_y:
                if self.rank[root_x] > self.rank[root_y]:
                    self.root[root_y] = root_x # 헷갈림. root[root_x]를 넣는 건 아니겠지 
                elif self.rank[root_x] < self.rank[root_y]:
                    self.root[root_x] = root_y
                else: # same level
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1 
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    class Solution:
        def findCircleNum(self, isConnected: List[List[int]]) -> int:
            n = len(isConnected)
            node_UF = UnionFind(n)
            for i in range(n):
                for j in range(i+1, n):
                    if isConnected[i][j]:
                        node_UF.union(i, j)
    
            root_set = set()
            for i in range(n):
                root_i = node_UF.find(i)
                root_set.add(root_i)
                      
            return len(root_set)
    ```
    
- Editorial
    
    ```python
    def findCircleNum(self, isConnected):
            n = len(isConnected)
            dsu = UnionFind(n)
            numberOfComponents = n
    
            for i in range(n):
                for j in range(i + 1, n):
                    if isConnected[i][j] and dsu.find(i) != dsu.find(j):
                        numberOfComponents -= 1
                        dsu.union_set(i, j)
    
            return numberOfComponents
    ```
    
- Editorial 반영 버전-조금 더 빠르다
    
    ```python
    class UnionFind:
        def __init__(self, size):
            self.rank = [1] * size
            self.root = [i for i in range(size)]
        def find(self, x):
            if x == self.root[x]:
                return x 
            else:
                self.root[x] = self.find(self.root[x])
                return self.root[x]
    
        def union(self, x, y):
            root_x, root_y = self.find(x), self.find(y)
            if root_x != root_y:
                if self.rank[root_x] > self.rank[root_y]:
                    self.root[root_y] = root_x # 헷갈림. root[root_x]를 넣는 건 아니겠지 
                elif self.rank[root_x] < self.rank[root_y]:
                    self.root[root_x] = root_y
                else: # same level
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1 
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    class Solution:
        def findCircleNum(self, isConnected: List[List[int]]) -> int:
            n = len(isConnected)
            node_UF = UnionFind(n)
            num_root = n
            for i in range(n):
                for j in range(i+1, n):
                    if isConnected[i][j] and node_UF.find(i) != node_UF.find(j):
                        node_UF.union(i, j)
                        num_root -= 1 
            return num_root
    ```