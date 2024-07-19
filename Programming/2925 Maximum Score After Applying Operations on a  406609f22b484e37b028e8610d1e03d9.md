# 2925. Maximum Score After Applying Operations on a Tree

Status: in progress, incomplete, 🏋️‍♀️
Theme: DP
Created time: November 27, 2023 3:59 PM
Last edited time: November 28, 2023 12:55 PM

- [ ]  다시 보고 이해하기
- [ ]  처음부터 다시 짜보기
- 문제 이해
    
    node, value, edge가 주어질 때 어떤 oper를 하고 싶은 만큼 하고 나서도 tree가 stay healthy 할 수 있는 최대 점수를 구하라
    
    - 어떤 oper를 할 때마다 node의 value 만큼의 점수가 더해진다
    - tree가 stay healthy 하려면 → root에서 다른 모든 leaf node까지 도달한다고 할 때 Path sum이 0이상이어야.
        - → 각 path 마다 leaf node 전까지 최소 1개의 node가 0이 아닌 채로 값이 유지되어야.
        - 이 때 internal node만 0이 아니고 leaf node가 0인 경우는 healthy 하지 않게 됨?
            - 아니다 그래도 leaf node까지 edge가 연결되어 있으면 도달 가능하고, leaf에서 0이더라도 그 전에 어떤 값이 하나 있으면 전체 path sum은 0이 아니게 된다
        - root의 value가 0이 아니면 나머지 모든 node에 대해 operation을 해서 점수를 최대로 얻고 node value는 0으로 만들어 버려도 됨
            - 혹은 root의 value가 엄청 크면 root에 대해 operation을 하고 path 당 최소 1개의 node에 대해 value를 살려 둬도 됨
- 과정
    - 내 접근법을 요약하자면…
        - node를 돌면서 node가 속한 path를 구하고, node value를 빼도 path sum이 0을 넘으면 node value를 score에 더하고, 이 node의 value를 0으로 만든다
        - 아닐 경우에는 이전 상태를 그대로 유지하거나 아님 이전 상태를 초기화-앞에서 0이 됐던 value 값을 다시 원래 value 값으로 복귀-하고 현재 node의 값만 score로 데려간다
        - as far as i go
            
            ```python
            from collections import defaultdict
            class Solution:
                def maximumScoreAfterOperations(self, edges: List[List[int]], values: List[int]) -> int:
                    num_nodes = len(values)
                    dp = [0] * (num_nodes)
                    child_tree = {i:[] for i in range(num_nodes)}
                    parent_tree = {i:[] for i in range(num_nodes)}
                    value_dict = {i: values[i] for i in range(num_nodes)}
            
                    for e in edges:
                        parent, child = e
                        child_tree[child].append(parent)
                        parent_tree[parent].append(child)
            
                    dp[0] = values[0]      
                    values[0] = 0
            
                    def get_path(node):
                        path_sum = 0
                        parent = node
                        child = node
                        # upward
                        while parent != 0:
                            parent = child_tree[parent][0]
                            path_sum += values[parent]
                        # node == 0
                        path_sum += values[0]
            
                        
                        return path_sum
            
                    for i in range(1, num_nodes):
                        path_sum = get_path(i)
                        if path_sum > 0:
                            dp[i] = dp[i-1] + values[i]
                            values[i] = 0
                        else:
                            if dp[i-1] > values[i]:
                                dp[i] = dp[i-1]
                            else:
                                dp[i] = values[i]
                                values[i] = 0 
                                # 나머지는 다 0이 아니게 해야 함 
                                for j in range(i):
                                    values[j] = value_dict[j]
                    return dp[-1]
            ```
            
- 더 나은 남의 코드 번역
    
    1) edge를 graph(matrix)로 재구성
    
    ```python
    class Solution:
        def dfs(self, tree, values, node, parent):
            candidate, score = 0, 0
    				current = values[node]
            for c in tree[node]:
                if c == parent: continue
                s, c = self.dfs(tree, values, c, node)
                score += s
                candidate += c
    
            if candidate != 0: 
                score += max(candidate, current) # 값이 더 큰 거 
    						candidate = min(candidate, current) # 더 작은 거
            else: # 현재 node가 leaf이면 score은 0으로, 자기 value는 후보로 올려둠 
    						candidate = current
    
            return taken, leftout
    
        def maximumScoreAfterOperations(self, edges, values):
            tree = [[] for _ in range(len(values))]
            for e in edges:
                tree[e[0]].append(e[1])
                tree[e[1]].append(e[0])
            
            return self.dfs(tree, values, 0, -1)[0] # taken 
    ```
    
- 남의 코드 번역 (이해하기 어려워서 다른 걸로 pass)
    - `dp[node]` : 모든 path가 생존 가능한 상태에서 얻을 수 있는 최대 점수
    - dfs function: path에서 max sum, min sum을 return
    
    ```python
    # Creating adj
    n = len(values)
    adj = [[] for _ in range(n+1)]
    dp = [-1] * (n+1)
    vis = [0] * (n+1)
    for e in edges:
    		parent, child = e
    		adj[parent] = child
    		adj[child] = parent
    
    def dfs(node):
    		if dp[node] != -1: 
    				return [0, 0]
    		dp[node] = 0
    		child_sum = 0 #sum of all the children nodes
    		min_child_sum = 0 # min node seen in the path
    		
    		for item in adj[node]:
    				if dp[item] == -1:
    						next = dfs(item)
    						child_sum += next[0]
    						min_child_sum += next[1]
    		
    		val = values[node]
    		if min_child_sum == 0: # current node 가 leaf node
    				dp[node] = 0 # 현재 node의 value를 0으로 만들었다가는 tree unhealthy
    				return [val, val] # path에서 최대값도 최소값도 cur node value 
    		if min_child_sum >= val: # path에서 현재 node의 값이 가장 작기 때문에 혼자만 살린다 
    				dp[node] = child_sum # 현재 node 빼고 나머지를 다 score에 더하고
    		else: # 현재 node 값이 더 크면 child path에서 가장 작은 애만 살리고(score에 안 더하고) 현재 node 값을 score에 더해준다 
    				dp[node] = child_sum - min_child_sum + val 
    		return [child_sum + val, min(min_child_sum, val)]
    
    dfs(0)
    return dp[0]
    ```