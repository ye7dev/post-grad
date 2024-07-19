# 108. Convert Sorted Array to Binary Search Tree

Status: done, in progress
Theme: Divide & Conquer
Created time: November 20, 2023 11:04 AM
Last edited time: November 30, 2023 11:04 PM

- 문제 이해
    
    모든 node의 자식 tree들의 깊이가 하나 이상 차이 나지 않는다 
    
- 이렇게 푸는 게 아니라고 생각했는데 빠른 시간으로 풀림 ;;
    
    ```python
    class Solution:
        def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
            def recur(subarray):
                if isinstance(subarray, int):
                    return TreeNode(val=subarray)
                elif len(subarray) == 1:
                    return recur(subarray[0])
                elif len(subarray) == 2:
                    parent = recur(subarray[1])
                    child = recur(subarray[0])
                    parent.left = child 
                    return parent 
                else:
                    mid = (0 + len(subarray)) // 2 
                    root = TreeNode(subarray[mid])
                    left = recur(subarray[:mid])
                    right = recur(subarray[mid+1:])
                    root.left = left
                    root.right = right 
                    return root 
            return recur(nums)
    ```
    
- python indexing(point) vs. slicing(range)
    - 원소가 하나일 때
        - x = [10] → x[0] : 10 (type: integer) vs. x[:1] = [10] (type: array)
    - 범위를 벗어났을 때
        - x = [10] → x[1] : 가챠 없이 error vs. x[1:] = [] 에러 없음
- 모범답안
    
    ```python
    # Definition for a binary tree node.
    # class TreeNode:
    #     def __init__(self, val=0, left=None, right=None):
    #         self.val = val
    #         self.left = left
    #         self.right = right
    
    class Solution:
        def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
            total_nums = len(nums)
            if not total_nums:
                return None
    
            mid_node = total_nums // 2
            return TreeNode(
                nums[mid_node], 
                self.sortedArrayToBST(nums[:mid_node]), self.sortedArrayToBST(nums[mid_node + 1 :])
            )
    ```
    
    - nums array가 원소 1개인 경우
        
        total_nums = 1 → mid_node = 0
        
        → nums[0]의 left: nums[:0] = None, nums[0]의 right: nums[1:] → None 
        
        ```python
        >>> x = [9]
        >>> x[1:]
        []
        >>> x[:0]
        []
        ```
        
        ⇒ 자동으로 left, right가 None인 root node만 return 
        
    - nums array 원소가 없는 경우
        
        total_nums = 0 → mid = 0 
        
        nums[0] → index out of range error 남. 
        
        ```python
        >>> y = []
        >>> y[0]
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        IndexError: list index out of range
        # 참고로 빈 array y에 대해 not y를 하면 True가 나온다 
        ```
        
        그러나 이 경우는 걱정할 필요가 없음 
        
        1.  `1 <= nums.length <= 104`
        2. 바로 return None이 되게 되어 있음
    - [-10, -3, 0, 5, 9]
        
        len(nums) = 5 → 5 // 2 = 2 → mid: 0 
        
        left : nums[:2] = [-10, -3], right = nums[2+1:] = [5, 9]
        
        val: 0, left: (val: -10, left: None, right t: (val: -3, left: None, right None))
        
        ---
        
        [-10, -3] 
        
        len(nums) = 2 → 2// 2= 0 → mid : 0
        
        left : nums[:0] = [], right = nums[0+1:] = [-3] 
        
        ⇒ val: -10, left: None, right t: (val: -3, left: None, right None)
        
        ---
        
        [-3]
        
        len(nums) = 1 → 1//2 = 0 → mid: 0
        
        left = nums[:0] = [], right = nums[0+1:] = []
        
        빈 list은 한 단계 더 내려가자마자 None으로 return 
        
        ⇒ val: -3, left: None, right None