# 94. Binary Tree Inorder Traversal

Status: done, in progress
Theme: Tree
Created time: December 2, 2023 9:36 AM
Last edited time: December 6, 2023 2:26 PM

- 몸풀기 easy
- 코드
    
    ```python
    class Solution:
        def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
            ans = []
            def visitNode(node):
                if node is not None:
                    visitNode(node.left)
                    ans.append(node.val)
                    visitNode(node.right)
            visitNode(root)
            return ans
    ```
    

![Untitled](Untitled%20116.png)

- iterative revisited
    - 그림
        
        ![Untitled](Untitled%20117.png)
        
        - Iterative code
            
            ```python
            class Solution:
                def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
                    ans = []
                    cur_node = root 
                    stack = []
                    while stack or cur_node:
                        # farthest left
                        while cur_node is not None:
                            stack.append(cur_node)
                            cur_node = cur_node.left
                        # self 
                        cur_node = stack.pop()
                        ans.append(cur_node.val)
                        # right
                        cur_node = cur_node.right
                    return ans
            ```
            
        - [ ]  위의 그림이랑 코드 보고 순서대로 표 채워보기
            
            
            | cur_node | stack  |
            | --- | --- |
            |  |  |
            |  |  |
            
- iterative로 다시 짜는데 놓친 점
    
    ```python
    from collections import deque
    # Definition for a binary tree node.
    # class TreeNode:
    #     def __init__(self, val=0, left=None, right=None):
    #         self.val = val
    #         self.left = left
    #         self.right = right
    class Solution:
        def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
            ans = []
            stack = []
            cur_node = root
            while stack or cur_node:
                while cur_node:
                    stack.append(cur_node)
                    cur_node = cur_node.left
                cur_node = stack.pop()
                ans.append(cur_node.val)
                if cur_node.right:
                    cur_node = cur_node.right
            return ans
    ```