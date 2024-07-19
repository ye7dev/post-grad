# 100. Same Tree

Status: done, in progress
Theme: recursive
Created time: December 5, 2023 5:32 PM
Last edited time: December 5, 2023 6:05 PM

[[Recursion II](https://leetcode.com/explore/learn/card/recursion-ii/) ](Recursion%20II%20295b3c8068a5427a847db92fc8561127.md) 예시 중 하나. easy 

- 코드 (iterative)
    
    ```python
    from collections import deque
    # Definition for a binary tree node.
    # class TreeNode:
    #     def __init__(self, val=0, left=None, right=None):
    #         self.val = val
    #         self.left = left
    #         self.right = right
    class Solution:
        def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
            def check_node(a, b):
                if a is None and b is None:
                    return True 
                if a is None or b is None:
                    return False
                if a.val == b.val:
                    return True 
    
            dq = deque()
            dq.append([p, q])
            while dq:
                a, b = dq.popleft() # q -> first in first out 
                if not check_node(a,b):
                    return False
                if a:
                    dq.append([a.left, b.left])
                    dq.append([a.right, b.right])
            return True
    ```