# 429. N-ary Tree Level Order Traversal

Status: done, in progress
Theme: graph
Created time: December 20, 2023 3:23 PM
Last edited time: December 20, 2023 3:30 PM

- 문제 이해
    
    어차피 트리니까 순환이 없을 거고, 그러면 visited set 안 써도 되겠지?
    
- AC 코드 🪇
    
    ```python
    """
    # Definition for a Node.
    class Node:
        def __init__(self, val=None, children=None):
            self.val = val
            self.children = children
    """
    from collections import deque
    class Solution:
        def levelOrder(self, root: 'Node') -> List[List[int]]:
            ans = []
            if not root:
                return ans
            dq = deque([root])
            while dq:
                num_nodes = len(dq)
                level_nodes = []
                for _ in range(num_nodes):
                    cur_node = dq.popleft()
                    level_nodes.append(cur_node.val)
                    for ch in cur_node.children:
                        dq.append(ch)
                ans.append(level_nodes)
            return ans
    ```