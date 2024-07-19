# 530. Minimum Absolute Difference in BST

Status: done, in progress
Theme: Tree
Created time: November 27, 2023 10:29 AM
Last edited time: November 27, 2023 10:59 AM

- 몸풀기 easy
- 생각보다 시간이 더 걸렸음
    - 처음에는 min val 찾는 걸로 짰는데 그것도 어쩐지 이상하고?
    - 다음에는 노드 하나 만날 때마다 vals에 있는 두 값과 비교하도록 했는데 답이 맞지 않았다. 이유를 모르겠음
- 코드
    - 느려서 개선 여지
    
    ```python
    # Definition for a binary tree node.
    # class TreeNode:
    #     def __init__(self, val=0, left=None, right=None):
    #         self.val = val
    #         self.left = left
    #         self.right = right
    class Solution:
        def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
            vals = []
            def recur(node):
                if not node:
                    return
                vals.append(node.val)
                recur(node.left)
                recur(node.right)
            recur(root)
            min_diff = float('inf')
            for i in range(len(vals)):
                for j in range(i+1, len(vals)):
                    min_diff = min(min_diff, abs(vals[i]-vals[j]))
                        
            return min_diff
    ```
    
    - 공식 답안을 봤을 때도-이제 프리미엄이라 실컷 볼 수 있다 야호- 나랑 같은 접근법 씀. dfs로 모든 노드 값 추가한 다음, 그 리스트에서 최소 차이 찾기
    - 다만 이렇게 했더니 속도가 훨씬 빨라졌다
        - vals에서 sort를 먼저 쫙하고
        - 그다음에 i를 range(1,len(vals))에서 돌린 뒤, vals[i]-vals[i-1] 차이와 min_diff를 비교해나간다
    - 별로 차이 안날 것 같지만 의외로 효과가 크다
        
        ```python
        vals.sort()
        for i in range(1, len(vals)):
            min_diff = min(min_diff, vals[i]-vals[i-1])
        ```
        
    
    ++ extra: 만약 tree 크기가 정렬되어 있는 경우 아래와 같이 in-traversal 하면 마지막에 vals.sort() 안해도 됨 
    
    ```python
    def in_order_traverse(node):
        if not node:
            return
        in_order_traverse(node.left)
        vals.append(node.val)
        in_order_traverse(node.right)
    ```