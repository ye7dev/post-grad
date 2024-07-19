# 133. Clone Graph

Status: done, in progress, with help
Theme: graph
Created time: December 15, 2023 9:05 PM
Last edited time: December 15, 2023 10:06 PM

- 과정
    - input, output이 좀 까다로움
    - 내가 짠 코드 (not AC)
        
        ```python
        """
        # Definition for a Node.
        class Node:
            def __init__(self, val = 0, neighbors = None):
                self.val = val
                self.neighbors = neighbors if neighbors is not None else []
        """
        
        from typing import Optional
        class Solution:
            def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
                if not node: 
                    return node
                def dfs(cur_node):
                    new_node = Node(cur_node.val)
                    if not cur_node.neighbors:
                        return new_node
        
                    for neighbor in cur_node.neighbors:
                        new_neighbor = dfs(neighbor)
                        cur_node.neighbors.append(new_neighbor)
        
                    return new_node
        
                return dfs(node)
        ```
        
- Editorial
    - DFS
        - intuition
            - graph → 한 node가 몇 개의 이웃 node를 가지고 있을지 모르기 때문에 list로 표현됨
            - graph 돌면서 cycle에 갖히면 안됨 - undirected edge는 directed edge 2개를 만드는 것과 동일
                
                → 이미 복사한 node를 기록해두고 다시 지나가지 않도록 한다 
                
        - 알고리즘
            1. 주어진 node로부터 그래프를 순회하기 시작한다
            2. hash map `visited` 를 이용해서 이미 방문/복사된 node들의 복사본의 Reference를 저장한다 
                - key: original graph의 node / value: cloned graph에서의 상응하는 node
                - 이미 `visited` 에 있는 node의 경우 저장된 reference of the cloned node를 return 한다
                - node A가 이웃들로 넘어가기 전 이미 복사본을 생성한 경우, B에 와서 이웃 중에 A가 있더라도 다시 방문하지 않고 `visited`에 저장된 A의 복사본ㅇ르 가져와서 추가한다. 그럼 사이클이 생기지 않음
            3. `visited` 에 찾고자 하는 node가 없을 경우, 복사본을 생성해서 추가한다. 
                - 중요한 점은 node copy를 만들어서 사전에 추가한 후에 재귀에 들어가야 한다는 점이다 - 그렇지 않으면 또 cycle 걸린다
            4. node의 이웃들에 대해 재귀 함수 호출
                - 각 재귀함수 호출은 이웃 node의 복사본을 반환해야 한다
                - 반환되어 올 이웃 복사본들을 담을 list를 하나 준비
- AC 코드
    
    ```python
    """
    # Definition for a Node.
    class Node:
        def __init__(self, val = 0, neighbors = None):
            self.val = val
            self.neighbors = neighbors if neighbors is not None else []
    """
    
    from typing import Optional
    class Solution:
        def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
            if not node:
                return node 
    
            visited = {}
            def dfs(cur_node):
                if cur_node in visited:
                    return visited[cur_node]
                clone = Node(cur_node.val)
                visited[cur_node] = clone
                neighbors = [] 
                for neighbor in cur_node.neighbors:
                    cloned_neighbor = dfs(neighbor)
                    if cloned_neighbor not in clone.neighbors:
                        cloned_neighbor.neighbors.append(clone)
                        clone.neighbors.append(cloned_neighbor)
                return clone 
            
            return dfs(node)
    ```