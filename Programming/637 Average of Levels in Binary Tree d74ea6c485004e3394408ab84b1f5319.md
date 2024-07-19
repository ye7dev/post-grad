# 637. Average of Levels in Binary Tree

Status: done
Theme: BFS
Created time: November 21, 2023 12:32 AM
Last edited time: November 21, 2023 11:18 AM

- 몸풀기 easy level
- 코드
    
    ```python
    class Solution:
        def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
            value_dict = {}
            def get_average(height, node):
                if node is None: return 
                if height not in value_dict:
                    value_dict[height] = [node.val] 
                else:
                    value_dict[height].append(node.val)
                
                get_average(height+1, node.left)
                get_average(height+1, node.right)
    
            get_average(0, root)
            ans = [] 
            for key in value_dict:
                ans.append(sum(value_dict[key])/len(value_dict[key]))
            return ans
    ```