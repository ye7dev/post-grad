# 337. House Robber III

Status: done, in progress, 🏋️‍♀️
Theme: DP, On Trees
Created time: January 23, 2024 1:44 PM
Last edited time: January 23, 2024 4:51 PM

<aside>
🪸 로직이 모든 경우의 수를 커버해야 한다 
class Node로 생성된 node는 모두 개별 Object

</aside>

- Progress
    - root돈을 먹는 경우, 안 먹는 경우
    - root에서 내 높이가 홀수인 경우 짝수인 경우 두 가지만 있으려나?
    - dfs로 타고 가면서 해야하겠지?
    - memo에 키로 뭘 넣으면 될까?
        - node, parent? “each house has one and only one parent house”
        - 홀수짝수로 해야 하려나? height?
        - 아님 level 별로 해야 하려나?
    - bfs에다가 Len(queue)로 구하는 방법이 떠오르는데…
    - 높이별로 가로 합을 구한 다음에 높이에 대해 dp를 하자
        - bfs시에 binary tree라서 방문 여부 따로 표시 안해도 될 듯. 어떤 노드에 도달할 수 있는 유일한 방법은 부모를 통해서 뿐이기 때문에
    - house robber 재귀식이 헷갈림
        
        [[**198. House Robber**](https://leetcode.com/problems/house-robber/solutions/846002/python-dynamic-programming-easy-solution-faster-than-95/?envType=study-plan-v2&envId=dynamic-programming)](198%20House%20Robber%20d44dfd89aff84bde8814b45e00a22820.md) 
        
    - binary tree에서는 중복 값을 허용하는데 도대체 키를 뭐로 함 ;;
        - 각 노드는 서로 다른 Object라서 Key로 사용 가능
- Trial
    - top-down, 60/124
        - 세대를 번걸아가며 구했는데 반례가 있네
            - 최대값은 root + leaf = 4+3 = 7
                
                ![Untitled](Untitled%2056.png)
                
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def rob(self, root: Optional[TreeNode]) -> int:
                memo = {}
                # function
                def recur(node, parent):
                    # base case
                    if not node:
                        return 0
                    # check memo
                    if (node, parent) in memo:
                        return memo[(node, parent)]
                    # recurrence relation
                    if parent: # skip this gen
                        memo[(node, parent)] = recur(node.left, False) + recur(node.right, False)
                        
                    else: # include this gen
                        memo[(node, parent)] = node.val + recur(node.left, True) + recur(node.right, True)
                    return memo[(node, parent)]
                return max(recur(root, True), recur(root, False))
        ```
        
    - bfs + bottom-up, 64/124
        - 같은 level에 있는 node는 무조건 더해져서 하나의 값으로 들어간다고 생각했는데 아니었음
        - 아래와 같은 반례
            - 왼쪽 subtree의 leaf와 오른쪽 subtree의 leaf의 합이 최대값 (4+3=7)
            
            ![Untitled](Untitled%2057.png)
            
        
        ```python
        from collections import deque
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def rob(self, root: Optional[TreeNode]) -> int:
                if not root.left and not root.right:
                    return root.val
                # get value sum of the same height
                level_sum = []
                def bfs(node):
                    queue = deque([node])
                    while queue:
                        num_neighbors = len(queue)
                        cur_sum = 0
                        for _ in range(num_neighbors):
                            cur_node = queue.popleft()
                            cur_sum += cur_node.val
                            if cur_node.left:
                                queue.append(cur_node.left)
                            if cur_node.right:
                                queue.append(cur_node.right)
                        level_sum.append(cur_sum) 
                
                bfs(root)
                print(level_sum)
                n = len(level_sum)
                dp = [0] * n
        
                # base case
                dp[0] = level_sum[0]
                dp[1] = max(level_sum[1], level_sum[0])
        
                # iteration
                for i in range(2, n):
                    dp[i] = max(dp[i-1], dp[i-2]+level_sum[i])
                print(dp)
                return dp[-1]
        ```
        
    - top down2, under 60/124
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def rob(self, root: Optional[TreeNode]) -> int:
                memo = {}
        
                # function
                def recur(node, height, skip):
                    # base case
                    if not node:
                        return 0
                    # check memoized
                    if (node, height, skip) in memo:
                        return memo[(node, height, skip)]
                    # iteration
                    if skip:
                        left_child = recur(node.left, height+1, False)
                        right_child = recur(node.right, height+1, False)
                        memo[(node, height, skip)] = left_child + right_child
                    else:
                        memo[(node, height, skip)] = node.val + recur(node.left, height+1, True) + recur(node.right, height+1, True)
                    
                    return memo[(node, height, skip)]
                
                return max(recur(root, 0, True), recur(root, 0, False))
        ```
        
- AC 코드
    - with `skip` version
        - skip은 현재 node를 건너 뛸 것인가 안 건너뛸 것인가를 의미
        - 현재 노드에 대한 결정을 parameter로 아예 넣어버리면, 모든 경우 중에 커버 못하는 경우가 발생하게 됨
            - 특히 현재 집을 터는 경우 - skip parameter가 False인 경우, children house를 무조건 털게 되는 시나리오만 고려했음
            - 물론 현재 집 기준으로는 모든 경우의 수를 고려한 것 같지만, 자식 집 기준으로는 부모집을 안 털고 자식집만 터는 경우의 수가 고려되지 못한 것임
            - 따라서 skip parameter를 살리면서 모든 경우의 수를 커버하는 로직을 짜면 counter-intuitive 하게 되고 원래의 skip parameter의 목적도 애매해짐
            
            ```python
            # Definition for a binary tree node.
            # class TreeNode:
            #     def __init__(self, val=0, left=None, right=None):
            #         self.val = val
            #         self.left = left
            #         self.right = right
            class Solution:
                def rob(self, root: Optional[TreeNode]) -> int:
                    memo = {}
            
                    # function
                    def recur(node, skip):
                        # base case
                        if not node:
                            return 0
                        # check memoized
                        if (node, skip) in memo:
                            return memo[(node, skip)]
                        # iteration
                        if skip:
                            # two option
                            rob_child = recur(node.left, False) + recur(node.right, False)
                            no_rob_child = recur(node.left, True) + recur(node.right, True)
                            memo[(node, skip)] = max(rob_child, no_rob_child)
                        else:
                            # one option
                            no_rob_child = node.val + recur(node.left, True) + recur(node.right, True)
                            not_rob_this = recur(node.left, False) + recur(node.right, False)
                            memo[(node, skip)] = max(not_rob_this, no_rob_child)
                        
                        return memo[(node, skip)]
                    
                    return max(recur(root, True), recur(root, False))
            ```
            
    - clean and neat version
        
        ```python
        # Definition for a binary tree node.
        # class TreeNode:
        #     def __init__(self, val=0, left=None, right=None):
        #         self.val = val
        #         self.left = left
        #         self.right = right
        class Solution:
            def rob(self, root: Optional[TreeNode]) -> int:
                memo = {}
        
                # function 
                def recur(node, can_rob):
                    # base case
                    if not node:
                        return 0 
                    
                    # check memoized
                    if (node, can_rob) in memo:
                        return memo[(node, can_rob)]
        
                    # recurrence relation
                    if can_rob: 
                        # wheter rob or not 
                        rob_now = node.val + recur(node.left, False) + recur(node.right, False)
                        rob_later = recur(node.left, True) + recur(node.right, True)
                        memo[(node, can_rob)] = max(rob_now, rob_later)
                    else:
                        rob_later = recur(node.left, True) + recur(node.right, True)
                        memo[(node, can_rob)] = rob_later
                    return memo[(node, can_rob)]
                
                return max(recur(root, True), recur(root, False))
        ```
        
- Editorial
    - **Approach 1: Recursion**
        - Intuition
            - 이런 류의 문제에 대한 뼈대 수도 코드
                
                > The pseudo code of the common structure to solve recursive problems is as below:
                > 
                
                ```
                function helper(node, other_information) {
                    // basic case, such as node is null
                    if node is null:
                        return things like 0 or null
                    else:
                        do something relates to helper(node.left) and helper(node.right)
                }
                function answerToProblem(root) {
                    return helper(root, other_information)
                }
                
                ```
                
                > 
                > 
            - 우리의 recur 함수는 무엇을 return 할 것인가?
                - input node에서 시작해서 도둑질 할 수 있는 최대 금액
                
                ```
                function helper(node) { // return the maximum by starting from this node
                    if node is null: // basic case
                        return 0
                    else:
                        two choices: rob this node or not?
                        if not rob... we have: helper(node.left) + helper(node.right)
                
                        what if rob? we get node.val!
                        what about node.left and node.right? we can not rob them.
                        Hmm... maybe we need to touch node.left.left and its other siblings... troublesome!
                }
                ```
                
            - input node의 손자 노드까지 다루는 건 복잡함 - 자식 노드에서 자동으로 손자 노드를 다루도록 하면 좋음
                - 자식 노드로 하여금 부모 노드가 방문되었는지 안되었는지 알게끔 하는 것
                
                ```
                function helper(node, the parent is robbed or not?) {
                    // return the maximum by starting from this node
                    tackle basic case...
                
                    if the parent is robbed:
                        we can not rob this node.
                        return helper(node.left, False) + helper(node.right, False)
                
                    if the parent is not robbed:
                        two choices: rob this node or not?
                        calculate `rob` and `not_rob`...
                        return max(rob, not_rob)
                }
                ```
                
            - recur 함수가 너무 많이 불리는 문제 - 왼쪽, 오른쪽 자식 노드에 대해 각각 따로 호출하는 경우
                - 하나의 input node에 대해 부모 노드가 방문된 경우, 안된 경우를 모두 구하도록 함
                - max if rob의 경우 left[0]+right[0], max_if_not_rob는 left[1]+right[1] 이런 식으로 구하려나?
                
                ```
                function helper(node) {
                    // return original [`helper(node.left, True)`, `helper(node.left, False)`]
                    tackle basic case...
                    left = helper(node.left)
                    right = helper(node.right)
                    some calculation...
                    return [max_if_rob, max_if_not_rob]
                }
                ```
                
                - memoization이나 dp는 뒤에 나옴
        - 알고리즘
            - `not_rob = max(left) + max(right)`
                - 이번 집을 안터는 경우, 자식 집을 털 수 도 있고 안 털 수 도 있기 때문에 둘 중에 max를 구하면 됨
                - 반대로 이번 집을 터는 경우 무조건 자식집을 털지 말아야 함
            
            ```python
            class Solution:
                def rob(self, root: TreeNode) -> int:
                    def helper(node):
                        # return [rob this node, not rob this node]
                        if not node:
                            return (0, 0)
                        left = helper(node.left)
                        right = helper(node.right)
                        # if we rob this node, we cannot rob its children
                        rob = node.val + left[1] + right[1]
                        # else we could choose to either rob its children or not
                        not_rob = max(left) + max(right)
                        return [rob, not_rob]
            
                    return max(helper(root))
            ```
            
    - **Approach 2: Recursion with Memoization**
        - 알고리즘
            - 이집에서 시작하되 터는 경우와 안 터는 경우를 구분해서 저장하는 것이 좋음
- 뭔가 text 이해의 문제가 얽혀있음
    - parameter 시점을 잘 이해해야 함
    - can_rob = True
        - 현재 집을 털 수도 있고 안 털 수도 있고 내 마음
        - 두 가지 옵션이 있음
        - 나의 잘못된 생각
            
            이번 집을 턴다는 선언형이라서 당연히 다음 집을 못 털기 때문에 옵션이 하나라고 생각함 
            
    - can_rob = False
        - 현재 집은 못 턴다. 다음 집에 가서야 털거나 안 털 수 있음
        - 나의 잘못된 생각
            
            이번 집은 안 털고 넘어가기 때문에 다음 집을 털 수도 있고 안 털 수도 있다고 생각함