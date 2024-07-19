# Graph

Status: algorithm, done
Theme: graph
Created time: December 11, 2023 5:19 PM
Last edited time: January 2, 2024 11:35 PM

# Introduction

- Types
    - Undirected: 두 정점 간 edge가 방향성 X.  늘 양방향 관계를 의미
    - Directed: edge 방향성 있음
    - Weighted: 각 edge마다 weight가 있음
- 용어
    - graph: 정점과 간선으로 구성된 non-linear 자료 구조
    - path: 하나의 정점에서 다른 정점으로 갈 때 통과하는 sequence of vertices
        
        ↳ 두 정점 간의 path는 여러 개가 될 수도 있다 
        
    - cycle: start, end가 같은 정점인 path
    - negative weight cycle: weighted graph에서, cycle을 이루는 모든 edge의 weight 합이 음수인 경우
    - connectivity: 두 정점 사이에 최소 하나의 path가 존재하는 경우
    - degree of a vertex
        - unweighted graph에 적용, vertex에 연결된 edge 수
    - in-degree: directed graph에서 어떤 vertex로 향하는 edge 수
    - out-degree: directed graph에서 어떤 vertex로부터 뻗어나가는 edge 수

# Disjoint Set

## Overview

- Overview
    - edge와 vertices가 주어졌을 때, 어떤 두 vertices들이 연결되어 있는지 어떻게 빠르게 확인할 수 있을까? (connectivity problem) → disjoint set (a.k.a union-find) 자료 구조 이용
    - disjoint set 자료 구조의 제 1 활용은 네트워크에서 요소들의 연결성을 확인하는 것
    - 용어
        - parent node: direct parent of a vertex
        - root node: a node without a parent node
- Introduction to Disjoint sets
    
    ![Untitled](Untitled%20150.png)
    
    - 어떤 set에 같이 속해 있으면, 연결되어 있는 것.
        - 연결시키는 행위 = 어떤 set에 특정 원소를 추가하는 행위 = 특정 원소의 대표값을 set의 대표값으로 변경하는 행위 = union
    - 각 요소가 어떤 set에 속해있는지는 알아보는 방법
        - 어떤 다른 자료구조(list 등)에서, 그 요소가 갖는 값이 어느 set의 대표값인지 확인
    
    ⇒ 두 node가 연결되어 있는지 확인하려면 두 node의 대표값이 같은 set의 대표값인지 확인
    
    - 그림에서 0과 5를 연결한다고 하면, 단순히 5를 0이 속한 set에 넣거나 vice versa가 아님. → 각자의 set을 merge! → 합병된 새로운 거대한 set의 대표값을 새로 정하고, 속한 요소들의 대표값을 그걸로 update 해준다
- Implementing Disjoint sets
    - 보조 array 생성
        - index: corresponding vertice가 무엇인지 가리킴
        - value: parent vertex
            - 초기화: 각 value는 index값과 같은 상황에서 시작
            - 왜냐면 초기 상태는 어떤 두 노드도 연결되어 있지 않고, 각자 고립된 상태로, 각자 하나의 set을 이루며, 각 set의 대표값(parent node)은 각자의 값 자체이기 때문
    - Connecting activity: Union
        - 연결하려는 두 노드 사이에서 어디를 대표값으로 삼을 것인지 결정 → 대표값으로 결정된 노드 말고 다른 노드의 대표값을 상대 노드의 값으로 갱신
        
        ![Untitled](Untitled%20151.png)
        
        - 1과 3을 연결하는 상황에서 parent node를 1로 삼는 경우
            - root[3] = 1 만 하면 됨
        - 1과 3을 연결하는 상황에서 parent node를 3으로 삼는 경우
            - 1의 corresponding root node를 찾아야 함. which is 0
            - 그리고 0의 parent node를 3으로 변경해야 함
    - root node array에서 찾는 법
        - root node의 특징: parent node of a root node is itself
        
        → array에서 parent node가 itself인 모든 node는 root node라고 할 수 있음 
        
        - 예: root[3] = 1 이라고 하면, itself가 아니라서 root node가 아님 → root[1] = 0으로 parent node가 itself 아님 → root[0] = 0 root node voila!
        - start at the node and follow the parent node until we find an element such that its index is equal to its element
    
    ![Untitled](Untitled%20152.png)
    
    - union 마친 root array 가지고 두 노드 간의 연결 여부 확인하는 법
        - 연결 여부 확인 → root array 이용하여 각 노드의 root node 체크 → 두 노드의 root node가 같으면 연결된 상태
    - 현재 연결성이 없는 (7, 8) 을 root array 이용하여 연결하는 법
        - 8의 root node인 4의 parent node를 7로 변경
        - 8의 root node를 다시 확인해보면
            - root[8] = 4 → root[4] = 7
                - 더 이상 parent node가 index와 같지 않아서 4는 8의 root node가 아니고 parent node다
            
            → root[7] = 5 → root[5] = 5 ⇒ root node! 
            
        - 8과 7의 root node가 같아졌으므로 두 노드는 하나의 set에 속하게 되었음을 의미하고, 연결성을 갖게 된다
    - `find` : input node의 root node를 찾아줌
    - `union` : perform connect operation
        - 둘의 root node를 같게 만들거나, 한쪽을 다른 한쪽의 parent node로 만든다
    - 구현 대표적인 두 가지 방법
        
        1) Quick Find
        
        - find function이 O(1), union function이 O(n)
        
        2) Quick Union
        
        - find function이 1)보다 느려지고, union function이 2)보다 빨라짐

## Quick Find

- Explanation
    - 기존: search step by step their parents → root array에 각자의 parent node 대신 root node를 저장 = find function으로 directly root node 가져올 수 있음
    - trade off: union 연산을 할 때마다 추가 단계를 거쳐야 함
    
    ![Untitled](Untitled%20153.png)
    
    - 0과 2를 연결하려고 할 때
        
        1) 2의 root node를 찾는다 → 2 
        
        2) 0을 parent node로 선정. root[2]에 0을 넣어준다
        
        3) 2의 root node가 바뀌면서, 5와 6의 root node도 0으로 변경해야 함 *extra step for the union operation 
        
    - 수도 코드
        
        ```python
        class UnionFind: # 자료 구조라서 class로 정의
        	root = []
        	
        	def UnionFind(size): # constructor 
        		root = [0] * size # size: # of vertices = N
        		for i in range(size): # O(N)
        				root[i] = i # itself root 
        	
        	def find(x):
        		return root[x] # O(1) 
        	
        	def union(x, y):
        		rootX = find(x)
        		rootY = find(y)
        		if rootX != rootY:
        				for i in range(len(root)): # O(N)
        						if root[i] == rootY:
        								root[i] = rootX
         
        	def connected(x, y): # O(1)
        		return find(x) == find(y)
        
        ```
        
- 레알 코드
    
    ```python
    # UnionFind class
    class UnionFind:
        def __init__(self, size):
            self.root = [i for i in range(size)]
    
        def find(self, x):
            return self.root[x]
    		
        def union(self, x, y):
            rootX = self.find(x)
            rootY = self.find(y)
            if rootX != rootY:
                for i in range(len(self.root)):
                    if self.root[i] == rootY:
                        self.root[i] = rootX
    
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    # Test Case
    uf = UnionFind(10)
    # 1-2-5-6-7 3-8-9 4
    uf.union(1, 2)
    uf.union(2, 5)
    uf.union(5, 6)
    uf.union(6, 7)
    uf.union(3, 8)
    uf.union(8, 9)
    print(uf.connected(1, 5))  # true
    print(uf.connected(5, 7))  # true
    print(uf.connected(4, 9))  # false
    # 1-2-5-6-7 3-8-9-4
    uf.union(9, 4)
    print(uf.connected(4, 9))  # true
    ```
    

## Quick Union

- Explanation
    - quick union에서 root array 값은 root가 아니라 parent!
    
    ![Untitled](Untitled%20154.png)
    
    - 0과 1 연결하는 경우
        
        1) 0과 1의 root node 찾기: 0, 1 
        
        2) 둘 중 하나를 parent node로 선정-0으로 결정
        
        3) 1을 0의 root node에 연결-which is 0 → 0을 1의 parent node로 assign → root[1] = 0
        
    
    ![Untitled](Untitled%20155.png)
    
    - 1과 2 연결하는 경우
        - 직관적인 방식은 1과 2를 연결하고, root[2] 에 1을 parent node로 assign
        - 더 빠른 방법!
            - 1의 root node 찾기-그건 바로 0
            - 2를 directly connect to the root node → root[2] = 0
    
    ![Untitled](Untitled%20156.png)
    
    - (4, 6)까지 연결하고 나면 root array 값이 처음과는 다르게 parent가 아니라 모두 root node를 가리키게 되는데 quick find랑 뭐가 다르냐 → 1과 5를 연결하는 경우
        
        1) 1과 5의 root node를 찾아야 → 0, 4
        
        2) 0을 parent node로 선택 → 4의 parent node를 0으로 바꿔야 
        
        3) root[4] = 0으로 변경하지만, 5와 6의 값은 4로 그대로 둔다. which is parent node not the final root node ↔ quick find 였다면 5, 6도 root node 인 0으로 값을 바꿨을 것  
        
        ![Untitled](Untitled%20157.png)
        
        → quick union 구현에서는 root node 찾기 위해 중간 과정의 부모 노드들을 거쳐가야 한다 
        
    - 수도 코드
        
        ```python
        class UnionFind:
        		root = []
        		
        		def UnionFind(size):
        				root = [0] * size
        				for i in range(size):
        						root[i] = i
        		def find(x): # <= O(N)
        				while x != root[x]: # not root -> continue searching
        						x = root[x]
        				return x # x == root[x]
        		def union(x, y): # for loop은 없지만 worst O(N)
        				rootX, rootY = find(x), find(y) # <= O(N)
        				if rootX != rootY:
        						root[rootY] = rootX 
        		def connected(x, y):
        				return find(x) == find(y)
        ```
        
- 왜 Quick Union이 더 효율적인가?
    - N개의 요소를 connect(union) 하는 경우
        - quickFind → union이 항상 O(N) 걸림 (for loop → N * O(1)) → N번 union 하면 O(N^2)
        - quickUnion → union이 worst case에 O(N) → ≤ O(N) → N번 union 하면 ≤O(N^2)
        
        ⇒ quickUnion이 더 효율적이다. (???)
        
        - 추가 설명
            - 노드를 연결하는 그래프 그림을 생각할 때, 각 level이 잘 차 있으면 높이가 높지 않을 것 → find 호출 시에 O(N)보다 작게 걸릴 것
            - 그러나 일렬로 쭉 연결되는 상황이면 linked list와 다름 없고, 이 때 tree 높이는 N(노드 개수)가 되어 find 호출 시에 O(N) 걸림
- 레알 코드
    
    ```python
    # UnionFind class
    class UnionFind:
        def __init__(self, size):
            self.root = [i for i in range(size)]
    
        def find(self, x): #O(N)
            while x != self.root[x]:
                x = self.root[x]
            return x
    		
        def union(self, x, y): # O(N) only in worst (find 구현 따라 달라짐)
            rootX = self.find(x)
            rootY = self.find(y)
            if rootX != rootY:
                self.root[rootY] = rootX
    
        def connected(self, x, y): # find 구현에 따라 달라지지만 원래는 O(N)
            return self.find(x) == self.find(y)
    
    # Test Case
    uf = UnionFind(10)
    # 1-2-5-6-7 3-8-9 4
    uf.union(1, 2)
    uf.union(2, 5)
    uf.union(5, 6)
    uf.union(6, 7)
    uf.union(3, 8)
    uf.union(8, 9)
    print(uf.connected(1, 5))  # true
    print(uf.connected(5, 7))  # true
    print(uf.connected(4, 9))  # false
    # 1-2-5-6-7 3-8-9-4
    uf.union(9, 4)
    print(uf.connected(4, 9))  # true
    ```
    

## Union by Rank - union 함수 최적화

- Explanation
    - 위의 두 방법 모두 비효율로 인한 우려 존재
        
        
        | quickFind | quickUnion |
        | --- | --- |
        | union → for loop → O(N) | 한 줄 그래프 → find  ≤ O(N) |
    - 개선 방법: union by rank
        - rank: 특정 기준에 따라 정렬 ↔ 기존 Union 함수에서는 무조건 x(먼저 들어온 parameter)의 root node를 다른 쪽(y)의 root node로 삼고 통합
        - rank에 따라 parent node를 선택할 경우, 각 node의 maximum height를 제한할 수 있다는 장점 → 모든 node가 일렬로 연결되는 불상사를 막을 수 있음
        - 더 정확히 말하면 rank는 각 node가 위치한 height
        - rank가 더 높은 root node를 선택해서 다른 쪽의 new root node로 삼음 → 더 키 큰 tree 쪽으로 더 키 작은 tree가 병합됨
        - quick Union 구현에만 적용될 수 있는 최적화 기법
            - quick Find의 경우 find는 tree 생김새와 상관없이 늘 O(1)
    - Video Explanation
        - node1과 6을 연결하는 경우
            
            ![Untitled](Untitled%20158.png)
            
            1. 1과 6의 root를 각각 찾는다: 0, 5
            2. 새 root를 0과 5중 어떤 걸로 할지 결정 → 기준: 각자가 대표하는 tree 높이
            3. 0을 새 root로 삼으면 tree 높이가 더 증가하지 않고 5로 할 때보다 balanced tree 얻을 수 있다 
        - 수도 코드
            
            ```python
            class UnionFind:
            	root = []
            	rank = []
            	
            	def UnionFind(size):
            		root = [0] * size
            		rank = [0] * size
            		for i in range(size):
            			root[i] = i
            			rank[i] = 1
            	
            	def find(x):
            		while (x != root[x]):
            			x = root[x]
            		return x 
            	
            	def union(x, y):
            		rootX, rootY = find(x), find(y)
            		if rank[rootX] > rank[rootY]:
            				root[rootY] = rootX
            		elif rank[rootX] < rank[rootY]:
            				root[rootX] = rootY  
            		else: # same rank
            				root[rootY] = rootX
            				rank[rootX] += 1 
            
            	def connected(x, y):
            		return find(x) == find(y)
            ```
            
- 레알 코드
    
    ```python
    # UnionFind class
    class UnionFind:
        def __init__(self, size): # O(N)
            self.root = [i for i in range(size)]
            self.rank = [1] * size
    
        def find(self, x): # O(logN)
            while x != self.root[x]:
                x = self.root[x]
            return x
    		
        def union(self, x, y): # O(logN)
            rootX = self.find(x)
            rootY = self.find(y)
            if rootX != rootY:
                if self.rank[rootX] > self.rank[rootY]:
                    self.root[rootY] = rootX
                elif self.rank[rootX] < self.rank[rootY]:
                    self.root[rootX] = rootY
                else:
                    self.root[rootY] = rootX
                    self.rank[rootX] += 1
    
        def connected(self, x, y): # O(log N)
            return self.find(x) == self.find(y)
    
    # Test Case
    uf = UnionFind(10)
    # 1-2-5-6-7 3-8-9 4
    uf.union(1, 2)
    uf.union(2, 5)
    uf.union(5, 6)
    uf.union(6, 7)
    uf.union(3, 8)
    uf.union(8, 9)
    print(uf.connected(1, 5))  # true
    print(uf.connected(5, 7))  # true
    print(uf.connected(4, 9))  # false
    # 1-2-5-6-7 3-8-9-4
    uf.union(9, 4)
    print(uf.connected(4, 9))  # true
    ```
    
    - 왜 find method의 TC가 O(log N)인가?
        - rank는 같은 rank의 tree들끼리 합칠 때만 증가한다
        - rank를 1 높이기 위해서는 같은 원래 높이 set(tree) 두 개가 합쳐져야 하므로 number of elements가 두배로 증가해야 한다
        - 매 rank 상승(+1) 마다 elements 개수를 두배로 늘린다 = tree의 높이가 elements 개수에 대해 logarithmically increase = h 높이의 tree를 얻기 위해서는 2^h개의 element가 필요하다
        
        ⇒ N개의 elements 로는 최대 log(N)의 높이의 tree를 만들 수 있다 
        
        - 최악의 경우에서 같은 높이의 요소들끼리 union 하는 작업을 반복하면, tree height는 최대 log(N)+1이다
            - +1 은 처음 rank 0을 1로 늘리는 initial step(초기화할 때인듯?)을 커버하기 위한 부분
        
        ⇒ 어쨌든 그래서 find의 TC는 O(H) == O(log N) 
        

## Path Compression - find 함수 최적화

- Explanation
    - 기존: find 함수에서 root node를 return 하기 위해 sequentially 모든 중간 parent node를 다 거슬러 올라가야 했음 → 만약 같은 요소의 root node를 반복해서 찾는 경우, 이 거슬러 올라가는 작업을 반복해야 해서 비효율적
        - 예시: 5의 root를 찾으려면 0까지 계속 가야한다-특히 array 기준으로 보면 더 비효율이 명확함
            
            ![Untitled](Untitled%20159.png)
            
    - 최적화: root node를 찾은 뒤에, 거기까지 가는 도중에 만난 모든 node의 parent node를 root node로 update → 같은 요소의 root node를 반복해서 찾더라도 효율적
        - 예시 - 5는 물론이고 5에서 0으로 가는 도중에 만난 1, 2, 3, 4도 root array(each value in the cell is parent vertex) 값을 0으로 바꿔버림 → 그래프 상으로 보면 0에 다른 모든 node가 directly 연결된 상태
            
            ![Untitled](Untitled%20160.png)
            
            ![Untitled](Untitled%20161.png)
            
    - path compression : recursion 이용한 find function 최적화 기법
        - union by rank와 마찬가지로 quick union 구현에만 적용 가능-quick find는 이미 O(1)으로 최적화된 상태
    - 수도 코드 - 나머지 부분은 quick union이랑 동일해서 생략
        
        ```python
        def find(x):
        		if x == root[x]: # we found our root! 
        				return x 
        		else:
        			 root[x] = find(root[x])
        			 return root[x]
        ```
        
- 코드
    
    ```python
    # UnionFind class
    class UnionFind: # O(N)
        def __init__(self, size):
            self.root = [i for i in range(size)]
     
        def find(self, x): # best: O(1), worst: O(N) -> avereage: O(log N)
            if x == self.root[x]:
                return x
            self.root[x] = self.find(self.root[x])
            return self.root[x]
    		
        def union(self, x, y): # O(log N) (average)
            rootX = self.find(x)
            rootY = self.find(y)
            if rootX != rootY:
                self.root[rootY] = rootX
    
        def connected(self, x, y): # O(log N) (average)
            return self.find(x) == self.find(y)
    
    # Test Case
    uf = UnionFind(10)
    # 1-2-5-6-7 3-8-9 4
    uf.union(1, 2)
    uf.union(2, 5)
    uf.union(5, 6)
    uf.union(6, 7)
    uf.union(3, 8)
    uf.union(8, 9)
    print(uf.connected(1, 5))  # true
    print(uf.connected(5, 7))  # true
    print(uf.connected(4, 9))  # false
    # 1-2-5-6-7 3-8-9-4
    uf.union(9, 4)
    print(uf.connected(4, 9))  # true
    ```
    

## **Optimized “disjoint set” 
with Path Compression and Union by Rank**

- 최최종 코드
    
    ```python
    # UnionFind class
    class UnionFind:
        def __init__(self, size):
            self.root = [i for i in range(size)]
            # Use a rank array to record the height of each vertex, i.e., the "rank" of each vertex.
            # The initial "rank" of each vertex is 1, because each of them is
            # a standalone vertex with no connection to other vertices.
            self.rank = [1] * size
    
        # The find function here is the same as that in the disjoint set with path compression.
        def find(self, x):
            if x == self.root[x]:
                return x
            self.root[x] = self.find(self.root[x])
            return self.root[x]
    
        # The union function with union by rank
        def union(self, x, y):
            rootX = self.find(x)
            rootY = self.find(y)
            if rootX != rootY:
                if self.rank[rootX] > self.rank[rootY]:
                    self.root[rootY] = rootX
                elif self.rank[rootX] < self.rank[rootY]:
                    self.root[rootX] = rootY
                else:
                    self.root[rootY] = rootX
                    self.rank[rootX] += 1
    
        def connected(self, x, y):
            return self.find(x) == self.find(y)
    
    # Test Case
    uf = UnionFind(10)
    # 1-2-5-6-7 3-8-9 4
    uf.union(1, 2)
    uf.union(2, 5)
    uf.union(5, 6)
    uf.union(6, 7)
    uf.union(3, 8)
    uf.union(8, 9)
    print(uf.connected(1, 5))  # true
    print(uf.connected(5, 7))  # true
    print(uf.connected(4, 9))  # false
    # 1-2-5-6-7 3-8-9-4
    uf.union(9, 4)
    print(uf.connected(4, 9))  # true
    ```
    
- 최최종 TC
    - N : # of vertices in the graph
    - α : Inverse Ackermann function. 사실상 상수
    
    | Operation | Union-find Constructor | Find | Union | Connected |
    | --- | --- | --- | --- | --- |
    | Time Complexity | O(N) | O(α(N)) ≈ O(1) | O(α(N)) | O(α(N)) |

## Summary

- disjoint set의 핵심 아이디어
    - 연결(직접 연결이든 간접 연결이든)된 노드들은 모두 같은 parent나 root node를 가지게끔 함
    - 두 노드의 연결 여부를 파악하기 위해서는 root node만 확인하면 됨
- disjoint set 자료 구조에서 가장 중요한 함수
    - `find` 주어진 노드의 root node를 찾아줌
    - `union` 이전에 서로 연결이 안되어 있던 두 노드의 root node를 통일해서 연결시켜줌
    - `connected` 두 노드의 연결 여부 파악

# DFS

- 핵심 문제: 그래프가 주어졌을 때, 어떻게 그래프에 속한 노드를 모두 찾고, 두 노드 사이에 존재하는 모든 경로를 찾을 수 있는가?

## **Traversing all Vertices – Depth-First Search Algorithm**

- D for depth: going as deep as possible
- 보조 자료 구조 필요: stack
    - 이전 state로 돌아가는 능력이 필요하기 때문
    - first-in-last-out = last-in-first-out
        - 이전 state로 돌아가고 싶으면, current stack 맨 위에 있는(?) current state를 제거하면 된다
- stack을 명시적으로 사용하지 않고 재귀 호출
    - 간접적으로 stack 사용하는 것과 동일
- 주어진 그래프 위의 노드들의 방문 여부를 추가적으로 마킹해야 함
- 예시
    - A를 방문 처리
    
    → A와 연결된 모든 path를 저장 (A와 연결된 node를 저장) - 그렇게 하지 않으면 어떤 node를 방문하고 A로 돌아왔을 때 어디로 가야할지 알 수 없기 때문 (stack: B, D, C)
    
    → stack top이 B라서 다음 방문 차례 → B의 방문 여부 확인 → 방문 안했으면 방문 처리 → B에서 방문 가능한 노드들을 모두 stack에 넣는다. A는 이미 방문했으므로 clear (stack: E,F,D,C)
    
    → stack top이 E라서 다음 방문 차례 → E의 방문 여부 확인 → 방문 안햇으면 방문 처리 → E에서 방문 가능한 노드들을 모두 stack에 넣는다. C, D, B, F 중 B는 방문 처리 되었으므로 clear (stack: FBDCFDC)
    
    → F 방문 안했으므로 방문 처리 → F에서 방문 가능한 node를 모두 stack에 넣는다 → B, E는 방문 처리되어 있으므로 stack에서 clear 
    
    → 이전 상태인 E로 돌아간다 → E에서 갈 수 있는 F, B, D, C 중 B는 이미 방문했으므로 D 방문 처리
    
    → D에서 방문할 수 있는 노드는 A, E → 둘 다 이미 방문 완료 
    
    → 이전 상태인 E로 돌아간다 → C 방문 가능→ 방문 처리
    
    → C에서 방문 할 수 있는 노드는 A, E → 둘 다 이미 방문 완료 
    
    → 이전 상태인 E로 돌아간다 → 방문 가능한 노드 없으므로 이전 상태인 B로 돌아간다 → 방문 가능한 노드가 남아 있지 않으므로 이전 상태인 A로 돌아간다 → 방문 가능한 노드가 없고, stack도 비었으므로 모든 노드를 순회했다 
    
    ⇒ ABEFDC
    
- 시간 복잡도
    - O(V+E) # num_nodes + num_edges
    - 공간 복잡도는 O(V)
- 복습
    - ability to return to the previous state → stack
        - 직전 상태로 돌아가고 싶으면 current state를 stack에서 빼버리기만 하면 됨
    - source를 stack에 넣는다 → top of the stack remove → source 방문 여부 체크 → 방문 안 했으면 마킹 → 그 노드의 모든 path를 체크해야. 연결된 모든 node를 stack에 추가 (이 때 연결된 노드의 방문 여부는 상관 없이 모두 stack에 넣고 본다
    - stack top: 다음 차례로 살펴볼 노드
    - stack top을 꺼내서 방문 처리 안되어 있으면 방문 처리
    - A-B 사이의 path가 유효한 것으로 밝혀지면, 그 다음으로 A의 다른 path를 보는 것이 아니라 유효한 path를 이어서 더 이상 갈 수가 없을때까지 살펴봐야 함
        
        ![Untitled](Untitled%20162.png)
        
    - B를 기준으로 보면 연결된 노드가 A, E, F → 우선 stack에 다 넣고 본다 → A부터 먼저 stack에서 꺼낸다 → A의 방문 여부 체크 → 이미 방문했으므로 B로 돌아온다  → B의 다른 이웃이자 stack top인 E를 살펴본다 → E는 방문 전이라 B-E는 방문 유효한 path (현재까지 path: A-B-E) → E 방문 처리 …
    

## **Traversing all paths between two vertices – Depth-First Search Algorithm**

- A(start) → B(end)로 가는 모든 경로를 찾고 싶을 때
    - stack에 뭘 저장하느냐 - all the paths we have taken
    - starting point A (given) → add A stack → remove A → mark as visited → A에서 갈 수 있는 모든 edge 체크
    - stack add (A, C), (A,D), (A, B)
    - top (A, B) remove → B marking visited → destination!
        - answer = (a, b)
    - (a, b)가 유일한 path가 아닐 수 있으니 back to previous state : A
    - A에서 B로 갈 수 있는 다른 path 파악하기 위해 B를 다시 unvisited로 만듦 (remove the visited mark from B)
        - 예를 들어 D→E→B 이런 식으로 B에 다시 도달할 수 있는 path가 있기 때문
    - stack을 보면 다시 갈 수 있는 path가 (A, D), (A,C) 두 가지 있음
    - top element (A, D) remove from the stack → going along the A-D → 다음으로 D 노드 방문 → 방문 처리
    - D에서 시작해서 갈 수 있는 edge check
        - A와 E 두 가지가 있음 → A는 이미 방문해서 invalid
    - stack에 (A, D, E) 추가 → 새로운 stack top이라서 remove → node E 방문, 방문 처리 → E에서 방문 가능한 edge 체크: B, C, D, F가 있음 → D는 이미 방문한 상태
    - stack에 (A, D, E, C), (A, D, E, B), (A, D, E, F) 추가
    - stack top이 (A, D, E, F) 라서 → F 방문, 방문 처리 → F에서 방문 가능한 edge 체크: E, B → E는 방문한 상태
    - stack에 (A, D, E, F, B) 추가 → top stack element out of the stack → B 노드 방문, 방문 처리
        - answer = (a, b), (a, d, e, f, b)
    - finish searching on this path → returning to the previous state
    - return F from B
        - unmark B → B is now unvisited
    - F에서 모든 node 방문했으므로 unmark F → F is not unvisited
    - node E로 돌아옴
        - stack에 방문할 path가 두 가지 있음. top부터 방문 → (A, D, E, B) remove
    - B 방문 처리
        - answer = (a, b), (a, d, e, f, b), (a, d, e, b)
    - finish searching on this path → returning to the previous state
        - unmark B → B is now unvisited
    - return to E → still one untravelled path → remove top from the stack → (A, D, E, C)
    - C 노드 방문, 방문 처리 → C에서 갈 수 있는 node는 모두 방문된 상태 → return C back to E
        - unmark C → C is now unvisited
    - E에서 방문가능한 노드 모두 방문 → go back to D
        - unmark E → E is now unvisited
    - D에서 방문가능한 노드 모두 방문 → go back to A
        - unmark D → D is now unvisited
    - A로 돌아오니까 stack에 untravelled path (A, C) 남아 있음
        - C 방문 처리
    - C에서 방문 가능한 node: A, E. A는 방문처리 되어있는 상태고 E는 unvisited 상태 → stack에 (A, C, E) 추가
    - stack top remove → E 방문, 방문 처리
    - E에서 방문 가능한 node: D, B, F → stack에 세 개 다 추가
        - stack: (A, C, E, F), (A, C, E, B), (A, C, E, D)
    - stack top remove → F 방문, 방문 처리
    - F에서 방문 가능한 node: B → stack에 경로 추가
        - stack: (A, C, E, F, B)
    - stack top remove → B 방문, 방문 처리 → destination
        - answer = (a, b), (a, d, e, f, b), (a, d, e, b), (a, c, e, f, b)
    - return F from B
        - unmark B → B is now unvisited
    - F에서 더 방문해야 할 경로 없으므로 return to E
        - unmark F → F is now unvisited
    - E에서 더 방문해야 할 경로 : stack에 두 개 남아 있음
    - remove the top from the stack : (A, C, E, B)
        - B is our destination!
        - answer = (a, b), (a, d, e, f, b), (a, d, e, b), (a, c, e, f, b), (a, c, e, b)
    - go back to the previous state E from B
        - unmark B → B is now unvisited
    - E에서 더 방문해야 할 경로 : stack에 한 개 남아 있음
    - remove the top from the stack : (A, C, E, D) → D 방문, 방문 처리 → D에서 더 방문해야 할 경로 없으므로 return to the previous state E from D
        - unmark D → D is now unvisited
    - stack에 더 이상 남은 경로가 없으므로 탐색 종료
    
    ⇒ answer = (a, b), (a, d, e, f, b), (a, d, e, b), (a, c, e, f, b), (a, c, e, b)
    
- 시간 복잡도
    - O((V-1)!)
        - 모든 path를 탐색할 대의 최악의 경우는 complete graph(모든 노드가 연결되어 있는 상태)
        - complete graph에서 source vertex 빼고 그 다음으로 갈 수 있는 node의 개수는 V-1 = # of unique paths of length one that start at the source vertex
        - V-1개 중에서 하나는 target일 테니 그대로 종료
        - V-2개는 그대로 연장해서 unique paths가 됨 → 각 unique path 기준, 도착지 중에서 하나는 target일테니 그대로 종료 → 각 unique path 당 다음 단계 목적지로 V-3개를 가짐 … → (V-1)!
    - 더 정확한 시간 복잡도 계산이라는 데 잘 모르겠음
        
        The precise total number of paths in the worst-case scenario is equivalent to the [Number of Arrangements](https://oeis.org/wiki/Number_of_arrangements) of the subset of vertices excluding the source and target node, which equals e⋅(V−2)!
        
        While finding all paths, at each iteration, we add all valid paths from the current vertex to the stack, as shown in the video. Each time we add a path to the stack requires *O*(*V*) time to create a copy of the current path, append a vertex to it, and push it onto the stack. Since the path grows by one vertex each time, a path of length V must have been copied and pushed onto the stack V times before reaching its current length. Therefore, it is intuitive to think that each path should require *O*(*V*2) time in total. However, there is a flaw in our logic. Consider the example above; at 2:50 we add `ADE` to the stack. Then at 3:20, we add `ADEC`, `ADEB`, and `ADEF` to the stack. `ADE` is a subpath of `ADEC`, `ADEB`, and `ADEF`, but `ADE` was only created once. So the time required for each path to create `ADE` can be thought of as O(V)*O*(*V*) divided by the number of paths that stem from `ADE`. With this in mind, the time spent to create a path is *V* plus V−1divided by the number of paths that stem from this subpath plus V−2times... For a complete graph with many nodes, this averages out to O(2⋅V)=O(V) time per path.
        
        Thus, the time complexity to find all paths in an undirected graph in the worst-case scenario is equal to the number of paths found O((V−2)!)times the average time to find a path O(V) which simplifies to O((V−1)!).
        
    - Space Complexity: *O*(*V^*3)
        - The space used is by the stack which will contain:
        
        ![Untitled](Untitled%20163.png)
        
        - Therefore, in total, this solution will require O(V⋅(V−1)/2+1)⋅V=O(V^3)space. Note that the space used to store the result does not count towards the space complexity.

# BFS

## Overview

- 그래프 상의 모든 edge들이 같은 크기의 양수 가중치를 갖는 상황에서, 두 노드 간의 최단 경로를 찾는데 효율적으로 사용
    - DFS에서도 가능하지만, 최단 경로를 찾으려면 두 노드 사이의 모든 경로를 다 탐색한 다음에 거기서 최소를 얻어야 함
    - BFS에서는 안 그래도 되는 이유- 출발 노드와 목적지 노드 사이의 path가 발견되자마자 그게 둘 사이의 최단 경로라는 것이 보장되기 때문

## Traversing all Vertices

- Video Introduction
    - layer by layer
        - layer: distance from one of the vertices(source node) distancing
            
            ![Untitled](Untitled%20164.png)
            
            - distance : shortest distance
                - F를 기준으로 보면 A→B→F도 있고, A→C→E→F도 있지만 전자만 고려한다. 그리고 전자의 distance 2가 F의 layer가 된다
    - queue - first in first out
        
        ![Untitled](Untitled%20165.png)
        
        - 마킹 처리: 노란색
        - 아직 방문되지 않은 노드를 만나면 1) 방문 처리 2) 그 노드의 이웃을(이웃 자체의 방문 여부 상관없이) 모두 큐에 추가
        - 그리고 나서 다시 큐로 가서 가장 먼저 추가된 노드(가장 오랫동안 큐에서 기다린 노드)를 꺼내서 같은 행위 반복
            - 이때 이 노드가 이미 방문된 노드면 꺼내기만 하고 아무것도 안한다
        - 다 처리하고 나면 이렇게 되고, 한 layer 위에 있는 모든 노드를 방문하고 난 다음에야 다음 layer로 넘어간다
            
            ![Untitled](Untitled%20166.png)
            
- 복잡도 분석
    - 시간복잡도: O(V+E) # num nodes + num edges
        - graph위의 모든 노드와 edges를 확인해야 함
        - DFS와 동일
    - 공간복잡도: O(V)
        - 어떤 노드를 큐에 넣기 전에 방문 여부를 먼저 확인 → 큐에는 최대 V개의 노드가 들어갈 수 있음
- +α 방문 마킹 순서 - 큐나 스택에 들어가기 전이냐 후냐
    - BFS
        - 큐에 넣기 전 방문 여부를 확인한다
        
        ```python
        if node not in visited:
        	visited.append(node)
        	queue.append(node)
        ```
        
    - DFS
        - 스택ㅂ에 들어갔다가 나온 다음에 방문 여부 확인 및 마킹
        
        ```python
        node = stack.pop()
        if node not in visited:
        	visited.append(node)
        	for neighbor in graph[node]:
        		stack.append(node)
        ```
        

## Shortest Path Between Two Vertices

- Video Introduction
    - queue에 path 자체를 추가
    - 어떤 노드에서 이어지는 모든 path를 추가했으면 그 노드를 방문 처리
        
        ![Untitled](Untitled%20167.png)
        
    - 이미 방문한 node로 이어지는 path는 큐에 추가하지 않는다
    - 큐에서는 맨 아래에 있는 path부터 꺼내서 확인- 이 때 focus는 path의 맨 마지막 node
        - path의 맨 마지막에 있는 노드가 current node → cur node에서 연결되어 있으면 방문 안한 node를 기준 path에 추가한 뒤 다시 큐에 추가
    - 큐의 맨 아래 있는 path의 마지막 노드가 F가 아닌 이상 그 위에 F가 들어가 있는 path가 몇 개나 되던 F는 아직 방문 처리가 안된 상태로 유지됨
        
        ![Untitled](Untitled%20168.png)
        
        - F는 아직 방문 처리가 안되어있지만 큐에 들어가 있는 path의 마지막 요소로 들어가있다
    - 드디어 F가 맨 마지막 노드인 path가 큐에서 나왔다-나오자마자 F가 목적지인것이 확인되면 큐에 몇 개의 path가 아직 남았던 그대로 종료
        
        ![Untitled](Untitled%20169.png)
        
        - 그리고 큐에서 처음 나온 path가 최단 경로
        - layer by layer로 방문 하는데, F는 마지막 layer에 있고, B를 방문하면서 F를 만나게 처음으로 F를 본 경로. 이 다음부터는 경로가 길어질 뿐 (확실히는 이해가 안감)
    - 근데 최단 경로가 목적이 아니고 두 노드 사이의 모든 경로를 봐야 한다면 큐에 원소가 더 남아 있지 않을때까지 반복해야 함
- 복잡도 분석
    - 시간복잡도 O(V+E)
        - worst case: src → dst path가 maximum distance일 경우 모든 node와 edge를 일일히 확인해야 함
    - 공간복잡도 O(V)
        - worst case: queue stores all the nodes

# Minimum Spanning Tree

## Overview

- spanning tree
    - undirected graph의 connected subgraph
    - 이 subgraph의 모든 노드들은 최소 개수의 엣지로 연결
    - 하나의 undirected graph에서 spanning tree는 여러개 나올 수 있다
    - 그림
        
        ![Untitled](Untitled%20170.png)
        
- minimum spanning tree
    - weighted undirected graph에서 최소 total edge weight를 갖는 spanning tree
    - 그림
        
        ![Untitled](Untitled%20171.png)
        

## Cut Property

- Two basic concepts
    1. 그래프 이론에서 ‘cut’
        - 그래프에 있는 노드들을 두 개의 disjoint subset으로 분할하는 행위
        - 그림
            
            ![Untitled](Untitled%20172.png)
            
    2. Crossing edge 
        - 한 집합에 있는 노드를 다른 집합에 있는 노드와 연결하는 edge
        - 위의 그림에서 A-C가 대표적인 예
- 크루스칼 알고리즘와 프림 알고리즘의 이론적 토대
- 위키 정의
    - 그래프에서 어떤 cut C에 대해, C의 cut-set 생성
    - 이 set에 있는 어떤 edge E의 weightr가 C의 cut-set의 다른 모든 edge들보다 작을 때
    - 이 edge E는 그래프의 모든 minimum spanning tree에 속하는 edge이다
- Proof of the cut property
    
    ![Untitled](Untitled%20173.png)
    
    - 여기서 cut-set은 crossing edge를 말하는 듯
        - B-C의 edge가 나머지 edge들의 가중치 보다작기 때문에 MST를 이루는 edge가 된다
    - 왜 하나의 edge?
        
        ![Untitled](Untitled%20174.png)
        
        - edge가 0개면 두 개의 disjoint subset을 연결할 수가 없어서 MST를 만들어내지 못하고
        
        ![Untitled](Untitled%20175.png)
        
        - edge가 만약에 두 개면 cycle을 형성하게 되어 트리라고 부를 수 없음
    - 왜 최소 weight를 가진 edge?
        - 위의 상황처럼 연결 edge가 여러 개인 경우 하나만 골라야 하는데, 선택 기준이 최소 가중치이기 때문

## Kruskal’s Algorithm

- weighted undirected graph에서 MST를 생성하기 위한 알고리즘
- Video Explanation
    1. weight 오름차순으로 모든 edge 정렬
    2. 순서대로 각 edge를 돌면서 MST에 cycle을 만드는지 보고, 안 만들면 MST에 edge 추가
        - 예시
            
            ![Untitled](Untitled%20176.png)
            
            - B-E edge는 cycle 형성해서 skip
        - 이번 차례의 edge가 연결하는 두 개의 노드 중 하나라도 아직 MST의 일부가 아니라면, 그 edge를 MST에 ㅊ가
    3. MST에 N(노드 개수)-1개의 edge가 들어갈 때까지 2. 반복  
        
        ![Untitled](Untitled%20177.png)
        
        - A-C가 더 있다고 하더라도 이미 4개의 edge가 MST에 들어 있기 때문에 더 볼 필요 없다
- Why does Kruskal’s Algorithm only choose N-1 edges?
    - spanning tree 정의 Revisited
        - graph에 있는 모든 노드를 연결하는 edge의 최소 개수 집합
    - 모든 노드를 연결하는 최소 edge 개수는 늘 모든 노드 개수 -1이기 때문
- **Why can we apply the “greedy strategy”?**
    - greedy: weight가 가장 작으면서 cycle을 형성하지 않는 edge를 추가한다
        - 각 계산 단계에서 best choice를 선택
    - 크루스칼의 메인 아이디어
        - cycle을 형성하지 하지 않는 edge들 중에서, 가장 weight가 작은 edge를 고른다
    - Proof by contradiction
        - Kruskal → T (spanning tree이긴 하지만, MST는 아니라고 가정) vs. K (true minimum spanning tree)
            - 이 두 개의 tree는 서로 공통적으로 갖고 있는 edge가 있고, 아닌 edge도 있음
                
                ![Untitled](Untitled%20178.png)
                
        - e: T와 k 사이의 first different edge (T에만 들어 있고, k에는 안 들어 있음)
        - T에서 B-D 사이의 edge를 e라고 해보자
            - e를 K에 넣는 다고 하면 사이클이 생길 것. K는 이미 MST였기 때문에
                
                ⇒ K에 edge를 하나라도 더 더했다가는 사이클이 생길 것
                
            - 사이클을 피하기 위해서는 K를 이루던 edge 하나를 빼고 B-D를 추가해야 함
                
                ![Untitled](Untitled%20179.png)
                
            - 이렇게 하면 새로운 MST H가 만들어진다
                
                ![Untitled](Untitled%20180.png)
                
            - K의 C-D edge와 H의 B-D edge 빼고는 두 그래프가 서로 동일
            
            → K가 MST라고 가정했기 때문에 CD의 weight가 BD보다 훨씬 작아야 함 
            
            → 근데 그럼 크루스칼 알고리즘에서 만든 spanning tree T에서 CD를 선택하지 않고 BD를 선택?
            
            → 유일한 이유는 CD를 연결하면 사이클이 생기기 때문. e(B-D)를 연결하기 전에는 T와 K가 동일한 트리를 이루고 있었음(e는 first different edge)
            
            ⇒ C-D가 T에서 사이클을 만들기 때문에 추가되지 못했다면, 그 전단계까지 동일했던 K에서도 사이클을 만들어야 함 
            
            ⇒ 근데 그럼 C-D를 포함하고 있는 K가 어떻게 MST가 될 수 있겠는지?
            
            → 또 다른 가능성-BD의 가중치가 CD보다 작아서, T에서 CD 대신 BD를 선택했다의 경우 
            
            ⇒ 이렇게 되면 K랑 다른 건 다같고 BD를 갖고 있는 것만 다른 H가 MST가 되어야 하는데 그럼 K가 true MST라는 가정에 어긋남 
            
- 복잡도 분석
    - 시간 복잡도: O(E * log E) ←E: edge 개수
        - edge weight에 따라 sorting. sorting 하는데 nlogn인데 여기서 n은 edge개수 e라서 ⇒ eloge
        - 각 edge 별로 연결하고 있는 두 노드가 이미 연결된 요소가 아닌지 체크-아니면 edge 포함, 맞으면 cycle 형성할 거니까 pass ⇒ O(a(V))
            - α: inverse ackermann function
        - 최악의 경우 마지막 edge까지 다 돌아야 MST가 완성됨 ⇒ O(Ea(V))
        
        ⇒ O(ElogE + Eα(V)) = O(ElogE)
        
    - 공간복잡도: O(V) ← V: number of nodes
        - 모든 node에 대해 union-find 자료 구조에서 root를 저장하는 것은 O(V)만큼의 공간이 필요

## Prim’s Algorithm

- 크루스칼 알고리즘처럼 weighted undirected graph에서 minimum spanning tree를 만들기 위한 알고리즘
- Video Explanation
    
    ![스크린샷 2023-12-20 오후 7.30.23.png](%25EC%258A%25A4%25ED%2581%25AC%25EB%25A6%25B0%25EC%2583%25B7_2023-12-20_%25EC%2598%25A4%25ED%259B%2584_7.30.23.png)
    
    1. visited, unvisted 두 개의 set 생성
    2. 랜덤으로? 노드 하나 찍어서 visited에 넣는다
    3. 그 노드로부터 갈 수 있는 edge 중 가장 weight가 작은 것을 선택-edge가 닿는 목적지는 아직 방문 전이어야 한다
    4. 3에서 선택한 edge를 타고 도착한 node도 visited에 넣는다 
    5. 거기서 다시 3. 반복
    6. 모든 node가 visited에 들어 있으면 알고리즘 종료 
    
- **Proof of the Prim's Algorithm**
    - the greedy strategy
        - 매 단계에서 방문된 모든 노드를 하나의 덩어리로 보고
        - 이 덩어리에서 나가는 edge 들 중 가장 가중치가 작은 것을 선택
        - 이렇게 선택된 edge는 MST(optimal solution)를 형성
    - the cut property
        - 그래프가 크게 두 개로 나눠진 상황에서, 그 두개를 잇는 crossing edge 들 중 가중치가 가장 작은 것을 선택
        - 프림 알고리즘에서의 그래프 분할
            
            ![Untitled](Untitled%20181.png)
            
            - 방문된 set, 방문되지 않은 set
            - 이 두 component를 잇는 edge 중 가장 가중치가 작은 것을 선택
- Kruskal 알고리즘과의 차이
    - 크루스칼: edge를 추가하면서 MST를 키워나감
    - 프림: node를 추가하면서 MST를 키워나감
- 복잡도 분석
    - 시간복잡도
        - binary heap: O(E * log V)
            - 모든 노드를 탐방하는데 O(V+E) 소요
                - heap에 아직 MST에 포함되지 않은 노드들을 저장
            - minimum element 추출과 key decreasing operation 에 O(log V) 소요
        - finonacci heap: O(E+ VlogV)
            - 최소 요소 추출에 O(logV) 소요
            - key decreasing operation 에 amortized O(1) 소요
    - 공간복잡도
        - O(V) - V개의 노드를 자료 구조에 저장해야

# Single Source Shortest Path Algorithm

## Overview

- 개요
    - BFS를 최단 경로 탐색에 이용-그러나 unweighted graph일 경우만 가능
    - 그러나 실생활에서는 weighted graph에서의 최단 경로를 찾을 일이 더 많다
        - 집에서 버스 정류장까지 제일 시간이 적게 걸리는 경로를 찾을 때
            - 거리가 아니라 각 교통수단 별 속도 제한이나 교통체증 상황 등을 반영한 가중치를 고려해야
    - single source 최단 경로 문제 - starting vertex가 주어질 때, weighted graph의 모든 노드로의 최단 경로를 찾아라
        
        → 다 찾고 나면 given target vertex 찾기는 아주 쉽지 
        
- Edge Relaxation
    
    A에서 다른 모든 노드로의 최단 경로 찾고자 함 
    
    - 초기화 : direct connection만 고려
        
        ![Untitled](Untitled%20182.png)
        
        - E처럼 연결이 안 되어 있는 노드는 초기 거리가 양의 무한대
    - indirect까지도 고려하면
        - 예를 들어 A → D direct weight는 3. A → C → D indirect weight는 1+1 = 2 → 오른쪽 사전?에 D 항목 값 update
    - 이름이 왜 저려나
        - relaxation: directed connection weight보다 더 작은 indirect connection 경로를 발견하면, direct weight를 indirect weight로 update
        - 그래프의 각 edge를 rope로 생각
            - A와 D와 사이의 더 가까운 거리를 발견하면 tighten the rope
            - 그럼 원래 대각선에 있던 direct edge는 relaxed (loosening)
                - 더 짧은 rope가 있으니 A랑 D는 각각 그걸 당겨서 팽팽하게 만들고, 더 긴 rope는 놓는다는 의미라고
            - 
    - 어쨌든 해야 하는 건 최단 경로 찾아서 update the new distance
- 여기서 배우게 될 알고리즘 두 개
    - 다익스트라
        - non-negative weight에서 single source 최단 경로 문제 해결 시 사용 가능
    - 벨만 포드
        - single source 최단 경로 문제 해결 시 negative weight 있는 directed graph까지 모두 커버 가능

## **Dijkstra's Algorithm**

- non-negative weighted directed graph
- Video Explanation
    - 오른쪽 그래프가 주어질 때, 왼쪽 table로 필요한 정보를 keep track 한다
        - 필요한 정보
            - source → target 할 때 target node가 어딘지
            - source로부터 해당 노드의 최단 거리
            - source → target 경로에서 target 직전에 도착하는 node가 어딘지
        
        ![Untitled](Untitled%20183.png)
        
    - table 초기화
        - 아직 가지 않은 node
            - 양의 무한대 거리로 초기화
            - 직전 순회 노드는 빈칸
        - starting node itself
            - 거리는 0, 직전 순회 노드는 없음. None
    - starting node로부터 모든 direct connection 확인 → starting node 방문 처리
        
        ![Untitled](Untitled%20184.png)
        
    - 아직 방문 처리 안된 노드들 중 source로부터 최단 경로 가진 node 선택(동점일 경우에는 random) 후 direct connection 확인 → 이웃 노드와 source 노드 사이의 최단 경로 발견되면 table 정보 update → 해당 node 방문 처리
        - C 선택. C-A, C-D 두 개 있는데, A는 이미 방문 처리되어서 C-A edge는 볼 필요 없음
        - D는 아직 방문 처리가 되지 않아서 C-D로 전진
            - C-D를 취할 경우, A-D 사이의 distance는 어떻게 되는가?
            - 현재 A-C 사이의 최단 거리는 1 + C-D 최단 거리는 1 = 2
            
            → A-D 사이의 더 짧은 거리를 가진 경로가 발견되었으므로, table에서 D row update
            
            - 최단 거리 column 값 : 3→2
            - 직전 순회 노드: A → C
        
        ![Untitled](Untitled%20185.png)
        
        - 이제 다음 행보는 방문 처리 되지 않은 B, D, E 중 A와의 거리가 가장 짧은 B를 방문하는 것
    - 모든 노드 방문 처리 끝나면
        
        ![Untitled](Untitled%20186.png)
        
        - E 노드로의 최단 경로, 거리 구하는 것은 개꿀이다
            - E에서 직전 노드 타고 타고 가서 A 도달할 때까지 경로는 누적하면 되고
            - 거리는 그냥 E row의 값 가져오기만 하면 된다
- The main idea
    - 시작점 `u` 를 중심으로 삼아서 밖으로 확장
        - 다른 노드에 닿으면 최단 경로를 update 하면서
    - 그리디 접근법 사용
        - 매 단계에서 다음 행선지로 src로부터의 거리가 가장 작은 = 누적 가중치가 가장 작은 노드를 선택하기 때문
- **Proof of the Algorithm** (잘 이해가 안감)
    - 그리디 접근법에 따르면 매 단계에서 현재 상태 기준 최적의 선택을 수행 → 이게 어떻게 전체 결과의 최적을 보장하지?
    - set A : 방문한 노드의 집합
        - v, p는 아직 방문되지 않은 노드 → 이 둘 중 거리(가중치)가 더 작은 노드가 다음 행선지
        - v가 다음 행선지라고 하자
            - s → u →v가 s와 v 사이의 최단 경로
            - 혹시 그보다 더 짧은 경로가 있을까? s → r → p → v는 어떨까?
        - s→u→v가 최단 경로가 아니라고 가정해보자
            - 그럼 s로부터 v까지의 또 다른 경로인 s→r→p→v가 더 짧다는 소리가 된다
            
            → 식으로 정리하면 d[v] + d[uv] > d[r] + d[rp] + d[pv]
            
    - 이 그림에서는 아래의 path가 위의 path보다 greater 한것으로 보인다(?)
        
        ![Untitled](Untitled%20187.png)
        
        - 다익스트라는 가중치가 양수인 경우에만 적용 가능하기 때문에 s와 v 사이의 최단 거리는 위의 path의 길이가 된다(?)
        - 현재 최단 거리인 s to v는 s to p보다 작을 것이다(?)
        - 그런 점이 있다면 다익스트라 알고리즘이 다음 행선지로 p 대신 왜 v를 선택?
        - p가 v 보다 s에 더 가깝다면, v가 왜 선택되었을까?
            - 유일한 이유는 s와 v 사이의 거리가 s와 p 사이의 거리보다 가깝다는 것(?)
            - 이러면 불렛의 부등식과 반대 되는 이야기
- **Limitation of the algorithm**
    - 모든 edge의 가중치는 0 또는 양의 정수이어야 한다
    - 왜 negative weight에서는 이 알고리즘을 못 쓸까?
    - 예시
        
        ![Untitled](Untitled%20188.png)
        
        - 시작점: A 노드
        
        → A와 연결된 노드 중 가장 가중치가 낮은 간선으로 연결된 노드는 C 
        
        - C-D에 negative weight가 아니라고 해보자: -4 → 4
        - 그럼 위에서 1의 가중치를 가진 edge가 A-C 의 최단 경로
            - A → B → D → C로도 A→C 도달할 수 있지만, 양수인 가중치 상황에서 경로가 길어지면 길어질 수록 가중치도 같이 늘어남
            - A-B와 A-C 중 우리는 항상 가중치가 더 낮은 path를 선택. 그럼 이미 A-B가 A-C보다 크다는 건데, 거기다가 더 경로를 길어지게 하면 당연히 A-C보다 가중치 합이 커짐
        - 근데 여기서 negative weight가 등장하면 얘기가 달라짐
            - 우리가 다익스트라 알고리즘을 써서 A-C를 선택했을 때, 이거보다 더 긴 경로가 사실은 가중치 합이 더 작아서 최단 경로가 될 수도 있음
                - 예) C-D가 원래대로 -4라고 하면 A → B → D → C 가중치 합은 -1로 A-C 사이의 가중치보다 작아짐
- 복잡도 분석
    - 시간복잡도
        - fibonacci heap으로 min-heap 구현하는 경우, 최소 요소 추출에 O(logV), key decreasing operation은 amortized O(1) 시간 소요 → O(E+ VlogV)
        - binary heap 사용 시, O(V + ElogV)
    - 공간복잡도
        - O(V) : 자료 구조에 V개의 노드 저장해야 함

## Bellman Ford Algorithm

- 다익스트라 한계: negative weighted graph에서는 적용 불가
- Basic Theorem
    - Theorem 1: N개의 노드가 있고, negative weight cycle이 없는 그래프에서 어떤 두 노드 간의 최단 경로도 최대 N-1개의 edge들만 갖는다
        - “negative weight cycle이 없는”은 아래의 두 경우를 포함
            1. cycle이 없다 - Directed Acyclic Graph
            2. cycle이 있지만 Positive weight
                - 이 때 positive란 cycle을 이루는 모든 edge 각각의 weight가 positive라는 것이 아니고, cycle을 이루는 모든 edge의 weight sum이 양수인 경우를 의미
                - 물론 cycle을 이루면 두 노드 사이에 N-1보다 더 많은 개수의 edge를 지나는 path를 가지지만, 벨먼 포드 알고리즘에서는 최단 경로에 주목
                - cycle을 돌면 돌 수록 positive sum이 누적되기 때문에 최단 경로가 아니게 됨 → cycle이 없는 경우와 동일한 경론 도달
    - Theorem 2: negative weight cycles가 있는 그래프에서는 최단 경로라는 것이 없다
        - 최단 경로: minimum sum of weight path
        - cycle을 돌면 돌 수록 weight sum이 작아지기 때문에,
- **Using Dynamic Programming to Find the Shortest Path**
    - DAG or graph with positive cycles, A→ B 최단 경로는 최대 N-1 edges로 구성
        
        ![Untitled](Untitled%20189.png)
        
        - negative weight (-150) 존재 → 다익스트라 알고리즘은 안됨
        - 3→1→2 는 positive cycle
    - 최대 1개의 edge를 사용해서 A→B 도달 가능한지 확인 → 2개 edges → … → N-1개 edges
        - at most라는 개념에 주의! 최대 2개라고 하면 1개까지 포함하는 개념 → 최대 N-1개라고 하면 1, 2, …, N-1까지 포함 ⇒ DP!
    - N-1 = 4-1 = 3
        - 아무 두 노드 사이의 최단 경로는 최대 3개의 edge로 구성
    - Table
        - row : 노드 0이 출발지 일때 목적지 노드를 가리킴
        - col : 경로에 사용하는 ‘at most’ edge 수
        - 초기화: 그래프에 대해 아무것도 모르기 때문에 모두 양의 무한대
        - base case
            - 0개의 edge가 허락될 때
                - 도착지 0에서는 이미 도착한 것이므로 거리 0
                - 나머지 노드로는 출발지가 노드 0일 때 도착 불가 → 무한대로 그냥 둔다
        - 1개의 edge가 허락 될 때
            - 0개 또는 1개. 도착지가 0일 때는 최단 거리가 여전히 0.
            - 도착지가 1인 경우 1로 도착하는 엣지가 두 개 있음. 0→ 1, 3→ 1
                - 3→1의 경우, 0→3의 min weight(table[0][3]) + 3→1 weight 더해야 함.
                    - 무한대 - 150 = 여전히 무한대
                    - 왜 table[0][3]에서 가져오냐면, 최대 1개의 edge를 사용 가능한 건데, 그 1개를 3→1에 사용하니, 0→3은 edge가 0개 사용되는 경우의 weight를 가져와야 함
                - 0→ 1
                    - 0→0 = 0
                    - 0→1 = 100
                    
                    ⇒ 0 + 100 = 100 < 양의 무한대 → table cell value update
                    
        - 최대 2개의 edge가 허락될 때
            - 0→0 변화 없음
            - 0→1의 경우
                - 0→1 edge 하나만 거치는 last calculation result = 100
                - 0→3→1 edge 두 개 거치는 경우
                    - 0→3 사이의 minimum weight: edge 1개 사용한 경우 200
                    - 3→1 사이의 min weight: -150
                    
                    ⇒ 200-150 = 50 < 100 → 0과 1 사이의 min weight update in table 
                    
        - 점화식
            
            ![Untitled](Untitled%20190.png)
            
            - k: maximum number of edges to get to know u = table에서 col value
                - k = n-1까지 돌고 나면 종료
            - u : end vertex
            - the value itself vs. previous value of using k-1 edges + edge weight between the current node and previous node
- 복잡도 분석
    - 시간: O(V * E). 최악의 경우 모든 노드가 연결되어 있는 경우, 모든 노드로의 모든 경로를 다 체크해야 함
    - 공간: O(V^2). DP table matrix는 V by V
- **Explanation of the Bellman-Ford Algorithm**
    - 벨만 포드 알고리즘은 DP 식 풀이에서 공간 복잡도를 줄인 거라고 보면 됨
    - DP 풀이에서, current row 값을 계산하는 데 늘 previous row의 정보가 필요 했음 → 모든 이전 row를 다 보관할 필요가 없고 그냥 바로 직전 row 정보만 필요 → 공간복잡도를 O(V)로 줄일 수 있음
    - 아래 두 줄의 정보만 사용
        
        ![Untitled](Untitled%20191.png)
        
        - P: k-1 edge 사용해서 갈 때의 최단 거리
        - C: k개의 edge 사용해서 갈 때의 최단 거리
        - K+1개 edge 사용하는 경우를 계산하기 위해서는 P에다가 C를 복사해서 넣어주고, C는 다시 초기화해서 사용
    - passing by value vs by reference
        
        ![Untitled](Untitled%20192.png)
        
        - by value: a는 여전히 10
        - by reference: a는 [2, 3, 4]로 바뀐 상태
            - b의 모든 값을 a로 복사하는 것이 아니라 a가 b의 reference를 가리키게 되는 것
        
        → P = copy(C)를 해야 하는 이유. 
        
- **Optimizing the Bellman-Ford Algorithm**
    - 좀 이해 안가는 설명들
        - 위에서 사용한 table은 그대로 사용
        - 노드 2 기준으로 보면 0→2 or 0→ 1→2
            - 0→2 : 500 vs 0→1→2 : 200
            - table row 1에서는 왜 200이 아닌가?
                - 당연히 최대 사용 가능한 edge 수가 1이고, 그래서 0→2 경로만 가능하기 때문에 500
        - 만약 at most one edge constraint 없애면 just follow the iteration(?)
            - 0→1을 앞에서 이미 구했고(100) 여기에 1→2 (100) 더하면 0→2 바로 200 얻을 수 있음
            - 이 뒤의 cycle에서 노드2로의 min weight로부터 영향을 받는 모든 path들은 500말고 200이 더해지게 되므로 이전보다 더 작은 weight를 갖게 됨
            - all the results for the shortest path will be shifted up(?)
                - 원래 2번째 iteration에서 얻게 될 결과를 첫번째에 얻게 되어서
        - n-1번까지 다 DP 할 필요가 없다(?)
            - for the latter round, all the number stay the same, as our shortest path is already fixed(?)
            - iteration 몇 번을 더하든 결과는 동일
    - 결론
        - maximum number of edges는 걱정할 필요가 없다
        - you can loop through all the edges
        - each edge is looped through only once
        - 우리는 N-1번의 looping through all the edges(?) operation을 하기로 되어 있다
        - 만약 조건을 만족하면, early exit이 가능하다
            - 조건: for the current loop, the shortest distances to all the vertices are the same as the previous shortest distances
        - 일단 같은 결과를 한번 얻으면, 이후의 iteration에서도 변화가 없다는 것
    - How it is achieved?
        
        ![Untitled](Untitled%20193.png)
        
        - 처음에는 모두 양의 무한대로 초기화
        - 0은 base case라 당연히 0
        - 0→1 그래프 보면 100이니까 100으로 update
        - 1→2 edge는 100 ⇒ 앞에서 구한 100 + 100 = 200으로 update
        - 2→3  0→2가 200 + 2→3 100 = 300
        - 0→3 200 + 3→ 1 = 200 -150 = 50 → update
        - 0→2 500 > 200 → stay
        
        ![Untitled](Untitled%20194.png)
        
        - 1st iteration 끝난 상태. 2nd iteration 시작
            - 1st iteration 과 같은 순서로 모든 edge 다시 돈다
        - 0 → 1 100 > 50 → stay
        - 1→ 2 100  + 0→1은 이제 50 = 150 < 200 → update
        - 2→3 100 + 0→2 150 = 250 > 200 → stay
        - 3→1 200 - 150 = 50 → stay
        - 0 → 2 500 > 150 → stay
        - 여기까지 2nd iteration 마침. 1st iteration과 결과가 다르고, iteration limit인 N-1 = 4-1=3에 도달하지 않았으므로 한번 더 iteration
        
        ![Untitled](Untitled%20195.png)
        
        - 2nd iteration 끝난 상태. 3rd iteration 시작
        - 0 → 1 100 > 50 → stay
        - 1→2 100 + 0→1 50 = 150 → stay
        - 2→3 100 + 0→2 150 = 250 > 200 → stay
        - 0→3 200 → stay
        - 3→1 -150 + 0→3 200 = 50 → stay
        - 0→2 500 > 150 → stay
        
        ⇒ 2nd & 3rd iteration same 
        
        - 물론 여기서는 전 iteration이랑 값이 같은 걸 확인해야 iteration 끝나야 해서 N-1인 3번 돌긴 했지만, 엄밀히 말하면 두번째 Iteration에서 이미 최단 거리를 모두 찾은 것
    - 요약: 최대 N-1번의 Iteration으로 (그보다 더 적은 수의 iteration으로-예를 들어 2번째 Iteration 후 결과가 첫번째 iteration 후 결과와 같으면 바로 return) DP처럼 항상 N-1번을 돌지 않고도 원하는 결과를 얻을 수 있다
- **Comparing the Two Bellman-Ford Algorithm Variations**
    - 위에서 진행한 최적화 방법의 한계-대부분 문제에서 요구하는 상황은: maximum number of edges가 k로 제한될 때 두 지점 사이의 최소 거리(minimum weight) → DP를 쓸수 밖에 없음(=naive version of bellman-ford without optimization)
    - 만약 k번의 제약이 없으면 optimized version 쓰면 됨
- 벨먼-포드 한계: negative weight cycle이 없는 상황에서만 적용 가능
    - 다익스트라는 negative weighted graph면 무조건 안되고, 벨먼 포드는 negatively weighted라도 cycle weight sum이 positive인 경우면 사용 가능
    - DAG의 경우 벨먼 포드는 모두 사용 가능하고, 다익스트라는 DAG라도 negative weight 있으면 안됨
- 벨먼 포드가 어떻게 negative weigh cycle을 detect?
    - negative weight cycle에서 최단 경로는 못 구하더라도, 그런 상황에서 cycle이 존재하는지 여부는 확인할 수 있음
    - 방법: N-1번까지 iteration 한 다음, N번째 relaxation도 수행
        - 벨먼-포드 알고리즘에 다르면 각 edge를 N-1번 relaxing 하고 나면, 모든 거리들은 최단 거리가 되어야 한다
        - 근데 N번째 relaxing 후에도 distances[u] + weight(u, v) < distances(v) for anay edge(u, v)가 존재하면, 더 짧은 path가 존재한다는 것 ⇒ 그럼 negative weight cycle이 존재한다는 의미
- 복잡도 분석
    - 시간: 각 iteration 마다 모든 노드를 돈다면 각 appropriate(?) edge에 대해 relaxation 수행 해야 → O(V * E)
    - 공간: O(V). previous(current보다 하나 더 적은 edge 수 제약 있는 상황에서의 최단 거리), current 상황에 대해서 각각 source 노드로부터의 최단 거리를 저장해야 하므로 O(2V) = O(V) 저장공간 필요

## **Improved Bellman-Ford Algorithm with Queue — SPFA Algorithm**

- **Limitations of the Bellman-Ford Algorithm**
    
    ![Untitled](Untitled%20196.png)
    
    - 왼쪽 순서로 1번 모든 edge에 대해 relaxing operation 했을 때 대비, 오른쪽 순서로 했을 때 최단거리가 더 짧게 나온다
    - 왼쪽 순서로 돌 경우 무조건 최소 1번은 더 iteration 해야 한다는 것을 알 수 있음 = 두번째 순서가 더 효율적
    - 기존 벨먼 포드: choosing among any untraversed edges
    
    → SPFA 알고리즘은 이처럼 순회 순서를 통해 효율성을 극대화하는 전략
    
- SPFA 알고리즘
    - 큐를 사용해서, 다음 순서로 순회할 edge의 시작 노드를 저장해둠
    - 해당 노드의 최단 거리가 relaxed되고 그 노드가 큐에 있지 않을 때만 노드를 큐에 넣는다
    - 큐가 빌 때까지 해당 프로세스를 반복하고, 큐가 비고 나면 주어진 노드로부터 모든 노드로의 최단 거리가 계산된 상태
- **Video explanation of the SPFA algorithm**
    - 초기화
        - 최단 거리: 0만 0, 나머지는 양의 무한대
        1. 큐에 0 추가하고, added 인 상태 처리 
        2. 큐에서 0 추출하고, 0은 더이상 큐에 있지 않기 때문에 unmark it as ‘added’
        3. 0의 이웃 노드를 돌면서 최단 거리에 변화가 있는지 확인 
            1. 0→ 1 100 < inf ⇒ update 
                - 1의 최단 거리를 갱신했기 때문에 1을 큐에 넣고 added 처리
            2. 0→2 500 < inf ⇒ update
                - 2의 최단 거리를 갱신했기 때문에 2를 큐에 넣고 added 처리
            3. 0→3 200 < inf ⇒ update
                - 3의 최단 거리를 갱신했기 때문에 3을 큐에 넣고 added 처리
        4. 1의 최단 거리를 갱신했기 때문에, 0→1을 지나가는 모든 경로의 거리도 변경되어야 함 = 큐에 1을 넣어서 1의 이웃들을 확인할 수 있게끔 한 것
            1. 1을 큐에서 빼고, remove the marking 
            2. 1→2 100 + 0→1 100 = 200 < 500 ⇒ update and add 2 to the queue ⇒ 근데 보니까 이미 2는 큐에 들어 있는 상태로 마킹 처리 되어 있음 
        5. 2를 큐에서 빼고 marking removed
            1. 2→3 100 + 0→2 200 = 300 > 200 ⇒ stay
        6. 3을 큐에서 빼고 marking remove
            1. 3→1 -150 + 0→ 3 200 = 50 < 100 ⇒ update ⇒ 1의 최단 거리가 갱신되었으므로 큐에 추가하고 marking as added
        7. 1을 큐에서 빼고 marking remove 
            1. 1→2 100 + 0→1 50 = 150 < 200 ⇒ update ⇒ 2의 최단 거리가 갱신되었으므로 큐에 추가하고 marking as added
        8. 2를 큐에서 빼고 marking remove
            1. 2→3 100 + 0→2 = 150 + 100 = 250 > 200 ⇒ stay 
        9. 큐가 비었으므로 최단 거리가 모두 구해졌다 
        
        ![Untitled](Untitled%20197.png)
        
- 복잡도 분석
    - 시간: 모든 노드를 돌고, 각 iteration에서 approriate edge에 대해 relaxation operation 수행 → O(V * E)
    - 공간: 큐에 모든 노드를 넣을 수 있어야 하므로 O(V)

# Topological Sorting

## Overview of Kahn’s Algorithm

- 선수 과목 (prerequisite)
- topological sorting
    - linear sorting based one the required ordering between vertices in directed acyclic graph
    - cycle이 있으면 뭐부터 시작해야 할지 알길이 없다 물리고 물린 사이…
        - in-degree가 0인 노드가 애초에 없을 것
- Video Explanation
    - 선행조건이 없는 요소부터 큐에 넣는다 → 앞의 요소를 선행 조건으로 갖는 요소를 큐에 넣는다
    - in-degree: number of arrows pointing towards the node
        - C를 기준으로 보면 1개
        - 노드 별로 계산
            
            ![Untitled](Untitled%20198.png)
            
            - in-degree 수가 0인 node를 큐에 먼저 넣는다
        - A를 큐에서 추출하고 방문 처리 하고 나면, A를 선행 조건으로 갖는 노드들의 in-degree 수를 하나씩 빼준다
            
            ![Untitled](Untitled%20199.png)
            
            - updated in-degree가 0인 노드를 다시 큐에 넣어준다
        - 위의 작업을 반복하다보면 모든 노드의 in-degree 값이 0이 된다
            
            ![Untitled](Untitled%20200.png)
            
    - out-degree: number of arrows pointing out from the node
        - C를 기준으로 보면 2개
        - 
    - 복잡도 효율 높이기
        - adjacency list 만들기 → adjList[course] : course를 선행 수강해야 수강 가능한 다른 과목들
        - 이럼 하나의 course를 완료했을 때마다 모든 edge를 돌아야 할 필요 없이 사전에 담긴 애들만 Iterate 하면 됨 → 시간 복잡도가 O(V * E)에서 O(V+E)로 감소
        - 공간복잡도는 O(V)(기존에는 각 노드별로 in-degree tracking) → O(E) (사전에 들어가는 모든 원소는 edge 수와 같다)
- Limitation of the Algorithm
    - DAG에서만 작동
    - in-degree가 0인 노드가 최소 하나는 있어야 순회 시작 가능
        - 그렇지 않으면 모든 노드가 최소 하나의 선행 요건을 갖고 있다는 건데, 그럼 도대체 어디서부터 시작?
- 복잡도 분석
    - 시간: O(V+E)
        - adj list 만드는 데 드는 시간 O(E)
        - in-degree가 0인 노드(key)가 생길 때마다 돌면서 그 노드를 선행 요건으로 갖는(value) 노드들의 in-degree 값을 줄여나감
            - 최악의 경우 모든 노드를 돌 때마다 decrement every outging edge once - 각자 달고 있는 노드들이 겹치지 않는 경우 → O(V+E)
    - 공간: O(V+E)
        - adj list : O(E)
        - 각 노드의 in-degree 저장하는 데 드는 공간: O(V)
        - 큐는 최대 V개의 노드 저장할 수도 있음 → O(V)