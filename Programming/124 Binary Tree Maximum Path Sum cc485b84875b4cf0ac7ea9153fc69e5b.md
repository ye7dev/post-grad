# 124. Binary Tree Maximum Path Sum

Status: done, in progress, 🏋️‍♀️
Theme: DP, On Trees
Created time: January 23, 2024 5:24 PM
Last edited time: January 24, 2024 2:01 PM

- Process
    - each pair of adjacent nodes in the sequence
        - sum에 들어가는 모든 node가 하나의 path 위에 놓여야 함 - branch는 허용되지 않음
- 정리
    - 하나의 node에게 허락된 직접 연결은 최대 2개
    - non local 변수 : 부모랑 연결을 끊고 자기가 new root가 되어 자식을 최대 둘 다 데리고 가는 경우
    - return 결과 값: 부모랑 연결을 유지하면서 자식을 최대 하나만 들고 가는 경우
- AC 코드
    - recursive (⚡️)
        - 재귀 호출 할 때, `gain_from_subtree(node.left)`
            - 현재 node 기준 left subtree는 left child node도 포함되어야 함
            - 그래서 함수의 return 값에 node.val이 더해져서 들어가는 것
            - 그리고 node.left는 이미 현재 노드와 연결된 상태
                - 여기서 다시 node.left의 두 자식과 모두 연결한다면, node.left는 총 세 개의 연결을 갖게 됨 → invalid
                - 따라서 왼쪽 자식, 오른쪽 자식 중 하나로 결정해야 하므로
                    
                    `max(left_gain + node.val, right_gain + node.val)`
                    
                - 또 이 호출 시에 max_path_sum update 연산을 통해 부모(node)와 연을 끊고 자신(node.left)을 root로 두 자녀와 모두 연결된 상태가 최대값을 만들진 않는지 확인하는 과정을 거침
        - 결국 재귀함수의 return 값의 역할과 non local 변수의 역할이 분리된 경우임. return 값은 다른 재귀함수에서 호출됐을 때 들고 가야할 값이고, non local 변수의 역할은 전체 문제의 답을 구하는데 주목
            - 그렇기 때문에 max path sum에서는 세 가지를 다 더한 값이랑 비교하는 것이고, return 에서는 두 가지 값만 더한 결과를 비교하는 것임
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def maxPathSum(self, root: Optional[TreeNode]) -> int:
                max_path_sum = -float('inf')
                def gain_from_subtree(node):
                    nonlocal max_path_sum
                    # base case
                    if not node:
                        return 0
                    # check memoized?
        
                    # recurrence relation
                    left_gain = gain_from_subtree(node.left)
                    right_gain = gain_from_subtree(node.right)
        
                    left_gain = max(left_gain, 0)
                    right_gain = max(right_gain, 0)
        
                    max_path_sum = max(max_path_sum, node.val+left_gain+right_gain)
        
                    return max(left_gain + node.val, right_gain + node.val)
        
                gain_from_subtree(root)
                return max_path_sum
        ```
        
- Editorial
    - Overview
        - a path
            - 하나의 path 안에서 starting, ending node를 제외하고는 모든 node가 sequence 내에서 다른 두 개의 node와 연결되어 있음 - 두 경우 중 하나
                - 왼쪽, 오른쪽 child
                - 하나는 child, 하나는 parent
            - 어떤 노드도 seuquence 안에서 두 개 이상의 연결을 가질 수 없다
                - 아래 그림에서 5의 경우 밑의 두 자식이랑 부모 노드까지 연결되어 있어서 총 3개의 노드가 연결된 상태
            - 그림
                
                ![Untitled](Untitled%20203.png)
                
                ![Untitled](Untitled%20204.png)
                
    - **Approach: Post Order DFS**
        - **Intuition**
            - brute-force : 가능한 모든 path를 구하고, 각 path sum을 구한 뒤 그중에서 최대값을 찾는 방법 → O(n^2)
            - hightest sum path가 root를 반드시 포함하는 경우의 4가지 가능성
                1. path가 root에서 시작해서 root의 left child를 지나는 경우 
                    
                    ![Untitled](Untitled%20205.png)
                    
                2. path가 root에서 시작해서 root의 right child를 지나는 경우 
                    
                    ![Untitled](Untitled%20206.png)
                    
                3. path가 왼쪽, 오른쪽 child를 모두 포함하는 경우
                    
                    ![Untitled](Untitled%20207.png)
                    
                4. 아무 child도 포함하기 않고 root itself로 존재 
                    
                    ![Untitled](Untitled%20208.png)
                    
                - root는 무조건 path에 포함된다는 사실을 알고 있으므로, 초기에는 path sum이 root.val
                - path sum에 gain이 있을 때만 path가 왼쪽이나 오른쪽 subtree로 연장됨
                    - subtree의 값이 음수이면 무시
            - 왼쪽, 오른쪽 subtree에 의해 path sum에 얻는 이익 계산 → contribution에 포함할지 말지 결정
                - children에 대해 먼저 처리한 다음, current node를 처리해야 함
                
                → post-order traversal 
                
                - contribution에 포함 여부 결정 시나리오는 크게 네 가지
                    - Include the left subtree's gain only.
                    - Include the right subtree's gain only.
                    - Include both the left and right subtree's gains.
                    - Include neither, especially if both gains are negative.
            - 재귀 함수 구현
                - input: root of the subtree (왼쪽이나 오른쪽 자식) → output: path sum gain contributed by the subtree (자식이 가져다 주는 이익)
                - path sum gain을 계산하기 위해 왼쪽, 오른쪽 자식에 대해 재귀적으로 함수 호출
                - maximum sum path가 root를 지나지 않는 경우를 커버하기 위해 함수에 추가해야 할 부분
                    
                    ![Untitled](Untitled%20209.png)
                    
                    - output에서 path sum gain만 return 하는 것이 아니라, maximum path sum도 keep track - 새로운 maximum sum이 나올 때마다 update
            - `gain_from_subtree`
                - input: root의 subtree
                - 두 가지 역할
                    1. input으로 들어온 subtree로 얻게 되는 path sum gain 계산 
                        - 최대 root의 하나의 child만 포함하는 path로부터 계산되어야 (child를 포함하기 않거나 왼쪽/오른쪽 둘 중 하나만 포함)
                        - 양쪽 children을 모두 포함할 수 없는 이유 - make a fork at the root
                            - root는 이미 자기 부모랑 연결되어 있기 때문에(?) 두 자식까지 연결시키면 해당 노드는 총 3개의 연결을 갖게 되므로 valid path가 될 수 없다
                        - left, right gain을 비교해서 그 중 더 큰 것만 root value에 더한다
                            - 이 때 subtree gain은 음수인 경우 0으로 간주됨
                    2. maximum path sum을 기록한다 
                        - max path sum이 subtree의 root를 통과하는 경우 4가지 가능성 존재
                            1. left subtree 통과
                            2. right subtree 통과
                            3. left, right subtree 둘 다를 통과 
                            4. left, right subtree 둘 다 배제 
                        - left, right gain 구한 뒤 양수이면 root value에 더해줌 - 이 sum을 so far max path sum과 비교한 뒤 더 큰 값이 되었으면 update