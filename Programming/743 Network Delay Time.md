# 743. Network Delay Time

Status: in progress, with help
Theme: graph
Created time: December 22, 2023 3:34 PM
Last edited time: December 22, 2023 6:46 PM

- 문제 이해
    
    starting point is given
    
    Return *the **minimum** time it takes for all the* `n` *nodes to receive the signal*.
    
    → 각 node로의 최소 시간은 구할 수 있는데. 동시 다발적으로 신호가 간다고 생각하면 여기서 최대 시간을 구하면 되겠지? (맞다) ~~아닌가? 합계인가?~~ 
    
- Editorial
    - Overview
        
        ![Untitled](Untitled%2092.png)
        
        - 서로 다른 시간대에 서로 다른 노드로부터 시그널을 받을 수 있다
        - 노드 a가 timestamp 1에 k로부터 신호를 받고, timestamp 2에 b로부터 신호를 받는 상황
            - 두 신호는 동일하다
            - 그래서 어떤 노드가 신호를 받는 timestamp는 그 노드에 처음으로 도달한 신호에 따라 결정
            
            → 노드 a 기준으로 보면 위 상황에서 신호를 받는 timestamp는 1 
            
        
        ⇒ 각 노드가 신호를 받는 시간을 구한 뒤, 그 중 maximum을 취한 것이 우리가 찾는 답 
        
    - DFS
        - Intuition
            - cur_node = starting node k, cur_time  = 0에서 시작
            - 현재 node가 신호를 받는 시간을 기록 (`signalReceivedAt[currNode] = currTime]`)
            - 현재 노드의 이웃에 대해 updated timestamp와 함께 DFS 시작
                - cur_time + 현재 node ~ 이웃 노드 걸리는 시간
            - 하나의 노드에 대해 여러 곳에서 신호가 들어올 수 있고, 우리는 그중 가장 먼저 도착하는 것에 관심 → `cur_time < signalReceivedAt[cur_node]`일 때만 DFS 수행
                - 위의 부등식이 성립하지 않으면 이미 cur_node에 신호가 도달된 상태를 의미
        - 알고리즘
            1. adjacency list 생성 
                - `adj[source]` : source node로부터 신호가 향할 수 있는 모든 목적지 노드를 포함. 각 목적지 노드에 대해 `(time, dest)` 정보 저장
            2. 모든 노드에 대해 각자 연결된 edge들을 weight 오름차순으로 정렬
            3. 모든 노드에 대해 `signalReceivedAt` 초기화-아직 신호를 받은 적이 없으면 양의 무한대로 설정
            4. cur_node = k, cur_time = 0으로 DFS 시작
                - 각 재귀호출에서 아래의 내용 수행
                    - `signalReceivedAt[currNode]` ≤ `cur_time` 이면 그대로 호출 종료 (return)
                    - 그렇지 않으면`signalReceivedAt[currNode]` 을`cur_time`로 갱신. 여기서 다시 updated timestamp 사용해서 DFS 수행
            5. `signalReceivedAt` 에서 최대값을 찾는다. 여기서 최대값이 아직도 3.에서 설정한 양의 무한대이면 신호를 받지 못한 노드가 있다는 것이므로 return -1. 
        - trial 놓친 점
            - 재귀적으로 호출하는 함수에서 수신 시간 어레이를 update 하는 기준을 잘못 설정해서 한참 걸림 ;;
        - 복잡도 분석
            - 시간: O((V-1)! + ElogE)
                - (V-1)!
                    - V 개의 노드와 V * (V-1)개의 directed edge로 이루어진 complete graph
                        - 제일 시간이 많이 걸리는 경우를 설명하기 위해 edge, node 수 max인 상황을 가정한 듯
                    - 이런 경우 모든 가능한 길이의 모든 가능한 path를 traverse 할 수 있다
                        
                        → 총 path 개수는 $\sum_{len=1}^{N} \binom{N}{len} * len!$
                        
                        - len: 1부터 N까지 path 길이
                        - 이걸 하나로 $e.N!$이라고 표현
                        - 이 수는 number of arrangements for N elements 와 동일
                    - 우리 문제의 경우 첫번째 원소는 K로 고정되어 있으므로 전체 원소에서 하나뺀 개수 V-1의 number of arrangements = $e.(V-1)!$
                - ElogE
                    - 각 node에 대해 edge sorting. edge들이 쫌쫌따리로 각 node에 대해 나눠져있지만(시작 노드 기준으로), 결국 모든 edge 개수는 E = 정렬 대상도 E개
                    - 그리고 뭐 아래와 같은 부등식이 있다고 함
                        
                        $xlogx+ylogy≤(x+y)log(x+y)$
                        
                        → 이걸 우리식에 대입하면 각 node에 대해 x+y가 결국 E이기 때문에 ElogE를 넘을 수 없음 
                        
                - O(V)
                    - 마지막 수신 시간 array에서 최대값 찾는대 걸리는 시간
            - 공간: O(V+E)
                - adjacency list 만드는 데 O(E)
                - DFS call stack이 최대 V개의 재귀콜 쌓을 수 있으므로 O(V)
    - BFS
        - Intuition
            - queue는 노드 담당, 수신 시간은 별도의 어레이에 저장
            - 현재 node로부터 나오는 신호는 연결된 모든 노드에 도달
            - 큐에 이웃 노드 추가하는 기준
                - 현재 node를 통해서 신호를 도달 받는 시간(`cur_time` blah blah) 이 지금까지 이웃 노드에 도달한 어떤 신호를 받는 시간(`수신 시간[이웃 노드]`)보다 짧을 때
        - 알고리즘
            - DFS와 동일하게 adjacency list 생성 및 수신 시간 array 초기화
            - 큐에 시작 노드를 집어넣고, 큐에 원소가 있는 한
                - 가장 들어간지 오래된 노드를 pop 하고
                - 그 노드의 이웃 노드를 돌면서 위에서 설명한 기준 충족하면 수신 시간 array 해당 값 업데이트하고, 이웃 노드 큐에 추가
            - DFS와 마찬가지로 최대값 확인
        - 복잡도 분석
            - 시간: O(N * E)
                - 큐에서 모든 노드가 나올 수 있고, complete graph 같은 경우 나온 노드 하나 당 모든 edge에 대해 다 돌기 때문에 N * E
            - 공간: O(N * E)
                - adjacency list 만드는데 O(E) 필요 하고, 큐 만드는 데 O(N * E) 필요하기 때문에 둘 중에 더 큰 O(N * E)
    - 이 문제에서 DFS, BFS는 왜 visited set을 사용하지 않아도 풀리는가?
        - tracking the earliest signal reception time at each node.
        - If a node is visited again with a signal time later than what has already been recorded, the visit is skipped, as it won't contribute to a shorter path.
        - This mechanism inherently prevents unnecessary revisits, making a separate visited set redundant.
    - 다익스트라 알고리즘
        - Intuition
            - 목표: k로부터 다른 모든 node 사이의 최단 경로를 찾는 것 → single source shortest path algorithm
            - BFS와 유사
                - k로부터 시작해서 연결된 이웃 노드 탐색
                - BFS-큐를 사용해서 선입선출로 방문된 노드들에 신호를 동시 송출(broadcast)
            - 여기서는 priority queue 사용
                - 도달하는 데 걸리는 시간이 짧은 노드부터 먼저 순회 - 각 iteration에서 가장 짧은 시간을 가진 노드가 다음 목적지로 선택된다는 뜻
        - 알고리즘
            1. DFS, BFS와 동일하게 adjacency list 생성 및 수신 시간 리스트 초기화 
            2. Priority queue 초기화 
                - 원소: (k, 0) # node, dist
                - dist는 수신 시간 리스트에 저장
            3. PQ에 원소가 있는 한 
                1. heappop 해서 cur node 꺼낸다 
                2. cur node의 이웃 노드를 모두 돈다 
                3. 수신 시간 리스트에 저장된 기존 이웃 노드의 시간보다 현재 노드 거쳐서 가는 시간이 더 짧으면 업데이트 한 뒤 PQ에 넣는다 
            4. 수신 시간 리스트 최대값 가지고 최종 답 return 
        - 복잡도 분석
            - 시간 : O(V + ElogV)
                - 다익스트라 알고리즘이 기본적으로 O(ElogN)
                - 마지막 수신 시간 리스트에서 최대값 찾는게 O(V)
                - PQ에 추가될 수 있는 최대 노드의 개수 E → push, pop operation O(log E)
                - E는 최대 V(V-1)개가 될 수 있음 → O(logE) = O(log V(V-1) = O(2logV) → O(log V) = TC for PQ ops
                - 근데 PQ에 최대 E개의 노드가 들어갈 수 있다고 해도, (최소값을 갖는 경우는 1개씩이라서?) 각 노드는 한번씩만 방문하게 될 것
                    - 만약 같은 노드를 두번째로 방문하면 curtime이 이미 수신시간 리스트에 저장된 값보다 클 것-왜냐면 PQ니까.
                    - 저장된 값보다 큰 curtime일 경우 그냥 continue
                - 그래서 전체 E개의 edge가 순회될 것이고, 각 edge 당 한번의 PQ insertion operation이 발생할 것 ⇒ E * log(V)
                
                ⇒ 최종적으로 수신 시간 리스트 최대값 관련 O(V) + PQ 관련 O(ElogV) 합하면 시간 복잡도
                
            - 공간 : O(V+E)
                - 수신 시간 리스트 노드 개수만큼 있어야 하니까 O(V)
                - adjacency list 만들 때 O(E) 필요
                - 다익스트라 알고리즘도 PQ에 O(E) 필요
- AC 코드
    - DFS
        
        ```python
        class Solution:
            def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
                stack = [] # do we need visited set? 
                received_time = [float('inf')] * (n+1)
                #received_time[0] = -1 # warning 
                graph = {}
                for s, e, w in times:
                    if s not in graph:
                        graph[s] = [] 
                    # time, dest
                    graph[s].append((w, e)) 
                for key in graph:
                    graph[key].sort() # based on the first element of each tuple.
        
                def dfs_recur(cur_node, cur_time):
                    if received_time[cur_node] <= cur_time:
                        return 
                    # update 
                    received_time[cur_node] = cur_time
                    # recursive call 
                    if cur_node not in graph: # keyerror check
                        return 
                    for pair in graph[cur_node]: 
                        adj_time, next_node = pair
                        dfs_recur(next_node, cur_time + adj_time)
        
                dfs_recur(k, 0)
                max_time = max(received_time[1:]) # can include 0th element cuz it is negative 
                print(received_time)
                if max_time == float('inf'):
                    return -1
                return max_time
        ```
        
    - BFS - 졸빠름
        
        ```python
        from collections import deque
        class Solution:
            def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
                stack = [] # do we need visited set? 
                received_time = [float('inf')] * (n+1)
                received_time[0] = -1 # warning 
                graph = {}
                for s, e, w in times:
                    if s not in graph:
                        graph[s] = [] 
                    # key: src, value: (weight, trg)
                    graph[s].append((w, e)) 
                for key in graph:
                    graph[key].sort() 
        
                queue = deque()
                queue.append(k)
                received_time[k] = 0
        
                while queue:
                    cur_node = queue.popleft()
                    cur_time = received_time[cur_node]
                    if cur_node not in graph:
                        continue
                    for pair in graph[cur_node]:
                        adj_time, neighbor = pair
                        so_far_fastest = received_time[neighbor]
                        new_time = cur_time + adj_time 
                        if new_time < so_far_fastest:
                            queue.append(neighbor)
                            received_time[neighbor] = new_time 
          
                max_time = max(received_time) 
                if max_time == float('inf'):
                    return -1
                return max_time
        ```
        
    - 다익스트라 - 졸빠름 22
        - BFS와 거의 동일
        
        ```python
        import heapq
        class Solution:
            def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
                stack = [] # do we need visited set? 
                received_time = [float('inf')] * (n+1)
                received_time[0] = -1 # warning 
                graph = {}
                for s, e, w in times:
                    if s not in graph:
                        graph[s] = [] 
                    # key: src, value: (weight, trg)
                    graph[s].append((w, e)) 
                for key in graph:
                    graph[key].sort() 
        
                priority_queue = []
                heapq.heappush(priority_queue, (k, 0))
                received_time[k] = 0
        
                while priority_queue:
                    cur_node, cur_time = heapq.heappop(priority_queue)
                    if cur_node not in graph:
                        continue
                    for pair in graph[cur_node]:
                        adj_time, neighbor = pair
                        so_far_fastest = received_time[neighbor]
                        new_time = cur_time + adj_time 
                        if new_time < so_far_fastest:
                            heapq.heappush(priority_queue, (neighbor, new_time))
                            received_time[neighbor] = new_time 
          
                max_time = max(received_time) 
                if max_time == float('inf'):
                    return -1
                return max_time
        ```