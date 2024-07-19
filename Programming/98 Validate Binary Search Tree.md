# 98. Validate Binary Search Tree

Status: done, in progress
Theme: Tree
Created time: December 1, 2023 9:53 PM
Last edited time: December 2, 2023 11:13 AM

- [ ]  Iterative Inorder Traversal로 다시 짜보기
- 과정
    - 이렇게 풀었는데 75/83에서 막힘
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def isValidBST(self, root: Optional[TreeNode]) -> bool:
                # base case
                if root is None: return True
                if root.left is None and root.right is None: return True 
                # condition check
                if root.left and root.left.val >= root.val: return False
                if root.right and root.right.val <= root.val: return False
                # split
                if self.isValidBST(root.left) and self.isValidBST(root.right):
                    return True
        ```
        
        - subtree에 있는 값은 root보다 다 크거나 작아야 함.
        - 
        
        ![Untitled](Untitled%20220.png)
        
    - 이렇게 고쳤는데 81/83에서 막힘
        
        ```python
        class Solution:
            def isValidBST(self, root: Optional[TreeNode]) -> bool:
                def check_node(root, min_val, max_val):
                    # base case
                    if root is None: return True
                    if root.val < min_val or root.val > max_val: return False
                    if root.left is None and root.right is None: return True 
                    # condition check
                    if root.left and root.left.val >= root.val: return False
                    if root.right and root.right.val <= root.val: return False
                    # split
                    if check_node(root.left, min_val, root.val) and check_node(root.right, root.val, max_val):
                        return True 
                return check_node(root, -float('inf'), float('inf'))
        ```
        
        - 맨 마지막에 3은 나오면 안됨. 3보다 작은 node들만 subtree에 올 수 있는데. 그니까 결국 min,max val update 부분에서 잘못되었다는 이야기
            
            ![스크린샷 2023-12-02 오전 9.08.29.png](%25EC%258A%25A4%25ED%2581%25AC%25EB%25A6%25B0%25EC%2583%25B7_2023-12-02_%25EC%2598%25A4%25EC%25A0%2584_9.08.29.png)
            
    - 경계값에 등호로 걸릴 때도 False로 빼줘야 했음
- 코드
    
    ```python
    # Definition for a binary tree node.
    # class TreeNode:
    #     def __init__(self, val=0, left=None, right=None):
    #         self.val = val
    #         self.left = left
    #         self.right = right
    class Solution:
        def isValidBST(self, root: Optional[TreeNode]) -> bool:
            def check_node(root, min_val, max_val):
                # base case
                if root is None: return True
                if root.val <= min_val or root.val >= max_val: return False
                if root.left is None and root.right is None: return True 
                # condition check
                if root.left and root.left.val >= root.val: return False
                if root.right and root.right.val <= root.val: return False
                # split
                upper_limit = min(max_val, root.val)
                lower_limit = max(min_val, root.val)
                if check_node(root.left, min_val, upper_limit) is False: return False
                if check_node(root.right, lower_limit, max_val) is False: return False
                return True 
            return check_node(root, -float('inf'), float('inf'))
    ```
    
- Editorial (풀이4가지)
    - **Approach 1: Recursive Traversal with Valid Range**
        - 내 풀이랑 가장 가까운데 코드가 더 짧음
            
            ```python
            class Solution:
                def isValidBST(self, root: TreeNode) -> bool:
            
                    def validate(node, low=-math.inf, high=math.inf):
                        # Empty trees are valid BSTs.
                        if not node:
                            return True
                        # The current node's value must be between low and high.
                        if node.val <= low or node.val >= high:
                            return False
            
                        # The left and right subtree must also be valid.
                        return (validate(node.right, node.val, high) and
                               validate(node.left, low, node.val))
            
                    return validate(root)
            ```
            
    - **Approach 2: Iterative Traversal with Valid Range**
        - DFS & stack 사용
        - 코드
            
            ```python
            class Solution:
                def isValidBST(self, root: TreeNode) -> bool:
                    if not root:
                        return True
            
                    stack = [(root, -math.inf, math.inf)]
                    while stack:
                        root, lower, upper = stack.pop()
                        if not root:
                            continue
                        val = root.val
                        if val <= lower or val >= upper:
                            return False
                        stack.append((root.right, val, upper))
                        stack.append((root.left, lower, val))
                    return True
            ```
            
    - **Approach 3: Recursive Inorder Traversal**
        - BST에서 inorder traversal을 하면 node 값이 담기는 list에서 이전 element에 비해 항상 더 큰 값이 담기게 됨
            - left → self → right 순으로 값이 커지니까
        - 근데 이 list를 다들고 있을 필요는 없고 바로 전 값만 들고 있으면 된다. 바로 전에 비해 같거나 작은 값 나오는 순간 바로 return False
        
        ```python
        class Solution:
            def isValidBST(self, root: Optional[TreeNode]) -> bool:
                self.prev = -float('inf')
                def inOrderTraversal(node):
                    if not node: 
                        return True 
        						# 첫번째 재귀콜 
                    if not inOrderTraversal(node.left): 
                        return False
        						# 실질적으로 한 node에 대해 하는 작업
                    if self.prev >= node.val: 
                        return False
                    self.prev = node.val
        						# 두번째 재귀콜
                    return inOrderTraversal(node.right)
                
                return inOrderTraversal(root)
        ```
        
    - **Approach 4: Iterative Inorder Traversal**
        - left에서 self로 가려면 한 단계 위로 가야하는데 이 경우 어떻게 진행되는지를 잘 외우는게 중요할 듯
        
        ```python
        class Solution:
            def isValidBST(self, root: TreeNode) -> bool:
                stack, prev = [], -math.inf # 두 가지 변수 운용 
                while stack or root: 
        						# 왼쪽으로 왼쪽으로 
                    while root: # 갈 수 있는 한 가장 왼쪽으로 이동 
                        stack.append(root) # 도중에 만난 node들은 모두 쌓아둠
                        root = root.left
        
        						# 전 단계에서 None이었던 root를 새로운 node로 update
                    root = stack.pop() 
        						
        						# 한 node에 대해 실제로 하는 일 
                    if root.val <= prev:
                        return False
                    prev = root.val
        
        						# 오른쪽
                    root = root.right
        
                return True
        ```