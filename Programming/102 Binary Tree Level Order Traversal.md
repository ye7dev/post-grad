# 102. Binary Tree Level Order Traversal

Status: done, in progress
Theme: recursive
Created time: December 6, 2023 12:48 AM
Last edited time: December 6, 2023 3:00 PM

[[Recursion II](https://leetcode.com/explore/learn/card/recursion-ii/) ](Recursion%20II%20295b3c8068a5427a847db92fc8561127.md) unfold the recursion 예제

- all by myself code
    
    ```python
    # Definition for a binary tree node.
    # class TreeNode:
    #     def __init__(self, val=0, left=None, right=None):
    #         self.val = val
    #         self.left = left
    #         self.right = right
    from collections import deque
    class Solution:
        def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
            if not root: return []
            ans = []
            prev_level = 0
            dq = deque([[root, 0]])
            temp = []
            while dq:
                cur_node, level = dq.popleft()
                if not cur_node:
                    continue
                if prev_level != level:
                    ans.append(temp)
                    temp = [cur_node.val]
                    prev_level = level
                else:
                    temp.append(cur_node.val)
                if cur_node.left:
                    dq.append([cur_node.left, level+1])
                if cur_node.right:
                    dq.append([cur_node.right, level+1])
            ans.append(temp)
            return ans
    ```
    
- [x]  해설 코드 확인
- Editorial double check
    
    level length가 핵심 
    
    ```python
    from collections import deque
    class Solution:
        def levelOrder(self, root):
            """
            :type root: TreeNode
            :rtype: List[List[int]]
            """
            ans = []
    				# base case 필수 
            if not root:
                return ans
            
            level = 0
            queue = deque([root,])
            while queue:
                cur_level = []
                level_length = len(queue) # 1, 2, 4...
                
    						# 같은 높이에 있는 node 개수만큼 부모 노드 빼고, 자식 노드 넣는다 
                for _ in range(level_length): 
    								# 부모노드 빼고 
                    node = queue.popleft()
                    cur_level.append(node.val)
    				        # 자식노드 모두 넣는다 
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
                
    						# 이번 레벨에 대한 마무리
    						ans.append(cur_level)
                level += 1
            
            return ans
    ```
    
    | node | queue | levels[level] | levels | len(queue) | level |
    | --- | --- | --- | --- | --- | --- |
    |  | [root] | [] | [ [] ] | 1 | 0 |
    | root | [] | [1] |  |  |  |
    |  | [2, 3]  | [] | [[1], []] | 2 | 1 |
    | 2 | [3] | [2] | [[1]], [2]] |  |  |
    |  | [3, 4, 5] |  |  |  |  |
    | 3 | [4, 5] | [2, 3] | [[1]], [2,3]] |  |  |
    |  | [4, 5, 6, 7] |  |  | 4 |  |