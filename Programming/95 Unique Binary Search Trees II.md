# 95. Unique Binary Search Trees II

Status: done, in progress
Theme: DP, On Trees
Created time: January 22, 2024 5:49 PM
Last edited time: January 23, 2024 11:58 AM

- Progress
    
    [[**96. Unique Binary Search Trees**](https://leetcode.com/problems/unique-binary-search-trees/description/?envType=study-plan-v2&envId=dynamic-programming)](96%20Unique%20Binary%20Search%20Trees%20fb5b77cfb6844bd9873c48736f20a99b.md) 은 개수를 return 하는 거였는데, 이건 나무 자체를 return 
    
    top-down으로 짤 때는 parameter를 큰 수부터 넣어주는 게 좋을 듯 
    
    각 수가 한번씩 root node가 된다
    
    그리고 같은 root에서도 배열이 바뀜 
    
    예를 들어 2, 3이 있으면 [2, 3]도 있을 수 있고 [3, 2]도 있을 수 있음 
    
- AC 코드
    - Top-down (⚡️)
        - root값을 바꿔가면서 left, right를 붙이는 부분 자체가 재귀 함수 안에서 이루어짐
        - base case에서 start, stop이 같은 경우는 따로 만들 필요 없음
            - 재귀 구문에서 root에는 무조건 하나 짜리 값의 node가 배정되기 때문에, left와 right subtree가 하나도 없는 경우 root만 return 되고, base case로 다룰 때와 동일한 결과가 나옴
            - 재귀 구문에 이 부분을 넣을 경우 memoization도 같이 이루어지기 때문에 더 효율적
        - left, right subtree가 여러 개씩 나오는데 어떻게 하냐 → list로 다 받아놨다가 각 left, right 조합이 모두 나올 수 있도록 nested for loop으로 root node에 붙인다
        - 주의점: permutation list에 붙일 때, root 노드는 같은 값이 더라도, left, right subtree가 다른 경우 별도의 tree이기 때문에 별도의 root node가 생성되어야 한다
            - 그렇지 않으면, 같은 root가 여러번 추가되는데, 결국 마지막 left, right의 상태가 앞서 추가된 같은 root들에게 모두 적용되기 때문에 - 애초에 앞에서 추가된 것들도 모두 같은 object를 가리키고 있으므로 - 같은 BST만 여러개 남게 된다
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        
                memo = {}
                def recur(start, stop):            
                    # base case 
                    if start > stop:
                        return [None]
                    # check memoized
                    if (start, stop) in memo:
                        return memo[(start, stop)]
                    # recurrence
                    permutations = []
                    for val in range(start, stop+1):
                        left_subs = recur(start, val-1)
                        right_subs = recur(val+1, stop)
                        for left in left_subs:
                            for right in right_subs:
                                root = TreeNode(val)
                                root.left = left
                                root.right = right
                                permutations.append(root)
                    memo[(start, stop)] = permutations
                    return memo[(start, stop)]
        
                
                return recur(1, n)
        ```
        
- Trial
    - start, stop 구간으로 할 때
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
                memo = {}
                # function
                def recur(start, stop):
                    # base case
                    if start > stop:
                        return 
                    if start == stop:
                        return TreeNode(start)
                    # check memoized
                    if (start, stop) in memo:
                        return memo[(start, stop)]
                    root = TreeNode(start)
                    root.left = recur(start)
                    memo[(start, stop)] = root
                    return memo[(start, stop)]
                
                ans = []
                for i in range(n, 0, -1):
                    root = TreeNode(i) # n -> 1
                    root.left = recur(1, i-1) # n-1 -> 0
                    root.right = recur(i+1, n) # n+1 -> 2
                    ans.append(root)
                return ans
        ```
        
    - 가능한 subtree들을 모두 list에 저장해뒀다가 왼쪽, 오른쪽에 붙이는 점 반영
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        
                memo = {}
                def recur(start, stop):            
                    # base case 
                    if start > stop:
                        return [None]
                    if start == stop:
                        return [TreeNode(start)]
                    # check memoized
                    if (start, stop) in memo:
                        return memo[(start, stop)]
                    # recurrence
                    permutations = []
                    for val in range(start, stop+1):
                        root = TreeNode(val)
                        left_subs = recur(start, val-1)
                        right_subs = recur(val+1, stop)
                        for left in left_subs:
                            for right in right_subs:
                                root.left = left
                                root.right = right
                                permutations.append(root)
                    memo[(start, stop)] = permutations
                    return memo[(start, stop)]
        
                
                return recur(1, n)
        ```
        
- Editorial
    - **Approach 1: Recursive Dynamic Programming**
        - Intuition
            - 1~n 중 하나의 node(i)를 root로 고정 → 나머지 n-1 개의 노드를 양쪽에 가능한 모든 방법으로 분배
            - `left(right)SubTree` 왼(오른)쪽 subtree가 될 수 있는 가능한 모든 BST를 담음. 사실은 a list of node
            - 두 list를 돌면서 each node pair를 만듦 (내가 놓친 부분)
                - leftSubTree, rightSubTree에서 각각 node 하나씩을 꺼내둠
                - value i 각각을 가지고 root node로 만든 뒤 각 left, right를 붙여서, 다시 i로 만들 수 있는 모든 BST 저장 공간에 추가
        
- 참고
    
    ```python
    from collections import deque
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
    
    def serialize(root):
        if not root:
            return []
    
        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)
    
        # Removing trailing None values to match the format
        while result and result[-1] is None:
            result.pop()
    
        return result
    root_store = []
    one_root = TreeNode(5)
    root_store.append(one_root)
    temp = []
    for node in root_store:
        temp.append(serialize(node))
    print(temp)
    # add left
    one_root.left = TreeNode(1)
    root_store.append(one_root)
    temp = []
    for node in root_store:
        temp.append(serialize(node))
    print(temp)
    # add right
    one_root.right = TreeNode(7)
    root_store.append(one_root)
    temp = []
    for node in root_store:
        temp.append(serialize(node))
    print(temp)
    ```