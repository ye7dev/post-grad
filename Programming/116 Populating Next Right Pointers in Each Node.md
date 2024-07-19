# 116. Populating Next Right Pointers in Each Node

Status: done, in progress
Theme: BFS
Created time: December 18, 2023 5:12 PM
Last edited time: December 18, 2023 5:21 PM

- 문제 이해
    - right next node이면 같은 level. parent node의 같은 자식들이니까 BFS지
- AC 코드
    
    ```python
    """
    # Definition for a Node.
    class Node:
        def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
            self.val = val
            self.left = left
            self.right = right
            self.next = next
    """
    
    class Solution:
        def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
            if not root:
                return root
            start = root
            queue = collections.deque([root])
    
            while queue:
                prev = None
                for i in range(len(queue)):
                    cur_node = queue.popleft()
                    if prev is not None:
                        prev.next = cur_node
                    if cur_node.left is not None:
                        queue.append(cur_node.left)
                    if cur_node.right is not None:
                        queue.append(cur_node.right)
                    cur_node.next = None
                    prev = cur_node
            return start
    ```