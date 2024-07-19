# 787. Cheapest Flights Within K Stops

Status: done, in progress, with help
Theme: graph
Created time: December 26, 2023 10:57 PM
Last edited time: February 7, 2024 5:50 PM

- 문제 이해
    - k번의 제약이 있으므로 DP로 풀어야만 한다
    - 근데 가중치가 모두 양수라 다익스트라로 풀어도 된다
    
- Trial
    - 다익스트라로 시도했는데 안 풀림
    
    ```python
    from collections import deque
    class Solution:
        def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
            travel = {}
            for s, t, cost in flights:
                if s not in travel:
                    travel[s] = []
                travel[s].append((cost, t))
            for key in travel:
                travel[key].sort() # increasing cost order 
    
            visited = set()
    
            min_dist = [float('inf')] * n
            min_dist[src] = 0
            prev_node = [-1] * n
    
            queue = deque([src])
            while queue:
                cur_node = queue.popleft()
                if cur_node not in travel:
                    visited.add(cur_node)
                    continue
    
                for neigh_cost, neighbor in travel[cur_node]:
                    if neighbor in visited:
                        continue
                    # cur_node~neighbor + source~cur_node
                    new_dist = neigh_cost + min_dist[cur_node] 
                    if new_dist < min_dist[neighbor]:
                        min_dist[neighbor] = new_dist
                        prev_node[neighbor] = cur_node
    
                visited.add(cur_node)
                temp_min_dist = float('inf')
                cand = None
                for node in range(n):
                    if node == src or node in visited:
                        continue
                    if min_dist[node] < temp_min_dist:
                        cand = node
                        temp_min_dist = min_dist[node]            
                queue.append(cand)          
                
            return min_dist[dst]
    ```
    
- Editorial
    - k stops라는 제약이 있을 때 src → dst 최단 경로 구하는 문제
    - BFS
        - Intuition
            - unweighted graph에서 최단 경로 찾기에 좋은 알고리즘
            - 어떤 노드가 traversal 중에 처음으로 도달되면, 그 때의 거리가 최단 거리 (The first time a node is reached during the traversal, it is reached at the minimum distance from the source.)
                - a particular discovery of a node would give us the cheapest path to that node
                - weigthed graph에 대해서는 edge가 더 많이 들어간 path라고 해서 더 비싼(path weight sum이 더 큰)이 path라고 할 수 없음
            - BFS에서는 최단 경로를 찾기 위해 그래프 전체를 돌면서 src → dst 최단 거리 경로를 기록해 나가야 함
            - 주어진 문제에서는 거쳐 가야 하는 정류장이 최대 k개로 제약 → BFS 사용 가능. because the number of levels to be explored by the algorithm is bounded by k.
            - level-wise iteration over nodes
                - 현재 level에 위치한 모든 node를 탐험한 다음, next level에 있는 node들로 이동
                - 여기서의 level이 k로 제한된 number of stops에 해당
                - 최대 k개의 stop 허용 = src node에서 dst 도달하기 위해 최대 k+1 높이만큼 올라갈 수 있다
            - array `dist`
                - 각 노드에 도달하기 위한 최소 가격을 저장
                - 어떤 노드로 이동하고자 할 때, 현재 dist에 저장된 dist[node]보다 traversing the edge 하고 난 이후의 total price가 더 적은 edge들만 고려
            
        - 알고리즘
            1. adjacency list 생성. `adj[x]` : x의 모든 이웃과 그 이웃으로 이동하기 위한 가격 저장 
            2. `dist` array 초기화. `dist[x]`: src에서 출발해서 x에 도달하기 위한 최소 비용. 초기화는 양의 무한대 값으로 
            3. queue 초기화. 원소 : (node, distance) 쌍. 초기화는 (src, 0)
            4. stops 변수 생성. 초기값은 0 
            5. BFS 수행: queue가 비거나 stops가 k보다 크면 중지 
                1. 특정 level의 모든 node를 돈다 
                    
                    = starting a nested loop and visiting all the nodes currently present in the queue 
                    
                2. (node, dist) pair가 하나 큐에서 추출되면, node의 모든 이웃을 돌면서 dist[neighbor] 이 dist + neighbor~node보다 작으면 **update 하고, (이웃, 이웃의 새 거리)를 큐에 추가** 
                3. 현재 level의 모든 node를 다 돌았으면 stops를 하나 늘린다 
            6. BFS 수행 중단하는 조건에 이르면, dist[dst]가 정답
                - 그런데 이 때 dist[dst]가 초기값에서 변하지 않았으면 도달한 적이 없다는 것이므로 -1 return
                
        - trial
            - 코드
                
                ```python
                class Solution:
                    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
                        travel = {}
                        for dep, arr, cost in flights:
                            if dep not in travel:
                                travel[dep] = []
                            travel[dep].append((arr, cost))
                        
                        min_dist = [float('inf')] * n
                        min_dist[src] = 0 
                        num_stops = 0
                        queue = [(src, 0)]
                
                        while queue or num_stops <= k:
                            num_same_level = len(queue)
                            for _ in range(num_same_level):
                                cur_node, cur_price = queue.pop()
                                if cur_node not in travel:
                                    continue
                                for neighbor, move_price in travel[cur_node]:
                                    new_price = cur_price + move_price
                                    if new_price < min_dist[neighbor]:
                                        min_dist[neighbor] = new_price
                                        queue.append((neighbor, new_price))
                            num_stops += 1 
                        
                        if min_dist[dst] == float('inf'):
                            return -1
                        else:
                            return min_dist[dst]
                ```
                
            - 개선사항
                - BBQ → BFS는 deque를 사용하는 거여서 import deque 하고, pop을 popleft method로 변경
                - min_dist[src] 라인을 삭제-BFS 들어가서 똑같은 것 하는 듯?
                - 제일 중요: queue에 원소가 있고, 그리고 num_stop ≤ k. OR이 아니고 AND임!!!
        - AC 코드(짱빠름)
            
            ```python
            from collections import deque
            class Solution:
                def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
                    travel = {}
                    for dep, arr, cost in flights:
                        if dep not in travel:
                            travel[dep] = []
                        travel[dep].append((arr, cost))
                    
                    min_dist = [float('inf')] * n
                    num_stops = 0
                    queue = deque([(src, 0)])
            
                    while queue and num_stops <= k:
                        num_same_level = len(queue)
                        for _ in range(num_same_level):
                            cur_node, cur_price = queue.popleft()
                            if cur_node not in travel:
                                continue
                            for neighbor, move_price in travel[cur_node]:
                                new_price = cur_price + move_price
                                if new_price < min_dist[neighbor]:
                                    min_dist[neighbor] = new_price
                                    queue.append((neighbor, new_price))
                        num_stops += 1 
                    
                    if min_dist[dst] == float('inf'):
                        return -1
                    else:
                        return min_dist[dst]
            ```
            
        - 복잡도 계산
            - 시간: O(N + E*K)
                - depending on improvements in the shortest distance for each node, we may process each edge multiple times = 어떤 노드가 다른 노드의 이웃으로서 순회되면서 최단 거리를 갱신하면, 큐에 다시 추가된다
                    - 하나의 edge가 처리될 수 있는 최대 횟수는 K로 제한됨
                    - worst case 시에 O(E*K)
                - adjacency list 초기화할 때도 모든 edge 한번씩 돌기 때문에 O(E)
                - dist array는 각 node에 대해 한 칸씩 갖고 있으므로 O(N)
            - 공간: O(N + E * K)
                - 최대 E개의 edge 각각을 K번씩 processing 하기 때문에 큐는 최대 O(E*K) 의 공간을 차지 할 수 있다
                - adjacency list O(E), dist array O(N)
    - Bellman Ford
        - Intuition
            - weighted graph에서 src → all other nodes의 최단 경로를 찾기 위해 사용
            - 최단 경로를 cycle을 가질 수 없기 때문에 최대 N-1개의 edge들을 포함한다
            - input: directed weighted graph, a starting node
            - output: starting node로부터 그래프에 있는 다른 모든 노드들로 향하는 최단 경로
            - 각 edge를 N-1번 돈다
            - **relaxing an edge**
                - 이전에 저장된 dist[node] 보다 더 적은 weight를 가지면서 node를 지나는 edge를 발견하면, dist[node]값을 update
                - 짧게 말하면 path 길이가 더 길어져도 path weight sum이 더 적은 edge를 찾으면, 그 edge로 얻을 수 있는 path weight sum으로 dist[node] 값을 update 한다는 뜻
            - 최대 사용 edge 수를 늘려가면서 최단 거리 계산
                - 어떤 simple path(negative cycle이 아닌)도 최대 N-1개의 edge를 가질 수 있기 때문에 N-1번의 iteration을 수행하는 것
        - 알고리즘
            1. `dist` array 초기화 
                - src → node min price 저장. 초기화는 양의 무한대
                - dist[src] = 0
            2. outer loop `k+1` 로 setting 
            3. 각 iteration에서
                1. `dist` copy 생성 - `temp`
                2. loop over all the edges in the graph trying to relax each one of them 
                    - src → x에 도달하는 cost(=dist[x]) + (x~y edge의 cost = x에서 y에 도달하는 cost) < src → y price보다 작으면 temp[y] 값을 update = x,y edge를 relaxing
                    - 여기서처럼 distance from the previous iteration (dist에 저장된 정보)가 변하지 않도록 temp라는 별도의 array를 사용하는 것
                    - 근데 이때 이미 dist[x]가 inf면 그대로 continue 한다-굳이 덧셈하고 비교하는 게 의미 없으므로
            4. iteration이 모두 끝나면 temp array를 dist array로 copy 
            5. 우리의 최종 답은 `dist[dst]` 에서 확인 가능-초기값과 변화 없으면 도달한 적이 없다는 것이므로 return -1 
        - Trial
            - edge 순회 순서가 영향을 미친다고 했는데 우선은 그냥 돌려보자
            - previous랑 current 교체 위치는 outer for loop 안
            - cost 비교 시에 update 대상인 node 쪽에는 current, relaxing 하는 쪽은 previous
                - 즉 previous[cur_node] + cost(cur_node~neighbor) vs. current[neighbor]
        - AC 코드
            
            ```python
            class Solution:
                def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
                    previous = [float('inf')] * n
                    previous[src] = 0
                
                    for i in range(k+1):
                        current = previous.copy()
                        for dep, arr, cost in flights:
                            if previous[dep] == float('inf'):
                                continue
                            if previous[dep] + cost < current[arr]:
                                current[arr] = previous[dep] + cost 
                        previous = current.copy()
            
                    if previous[dst] == float('inf'):
                        return -1
                    return previous[dst]
            ```
            
        - 좀 더 최적화해보자
            - P = C → break (AC)
                
                ```python
                class Solution:
                    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
                        previous = [float('inf')] * n
                        previous[src] = 0
                    
                        for i in range(k+1):
                            current = previous.copy()
                            for dep, arr, cost in flights:
                                if previous[dep] + cost < current[arr]:
                                    current[arr] = previous[dep] + cost 
                            if previous == current:
                                break 
                            previous = current.copy()
                
                        if previous[dst] == float('inf'):
                            return -1
                        return previous[dst]
                ```
                
            - 위에 거 받고 SPFA
                - BFS랑 비슷한데 visited가 추가되는 듯. 근데 k에 대한 제약이 어디서 적용될 수 있는지 모르겠음
                - trial-not accepted
                    
                    ```python
                    class Solution:
                        def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
                            travel = {}
                            for dep, arr, price in flights:
                                if dep not in travel:
                                    travel[dep] = []
                                travel[dep].append((arr, price))
                    
                            visited = [False] * n
                            min_dist = [float('inf')] * n 
                            min_dist[src] = 0 
                            queue = collections.deque([(src, 0)])
                            visited[src] = True 
                    
                            while queue:
                                cur_node, cur_cost = queue.popleft()
                                visited[cur_node] = False 
                                if cur_node not in travel:
                                    continue 
                                for neighbor, neighbor_cost in travel[cur_node]:
                                    if cur_cost + neighbor_cost < min_dist[neighbor]:
                                        min_dist[neighbor] = cur_cost + neighbor_cost 
                                        if not visited[neighbor]:
                                            queue.append((neighbor, min_dist[neighbor]))
                                            visited[neighbor] = True 
                            
                            if min_dist[dst] == float('inf'):
                                return -1
                            else:
                                return min_dist[dst]
                    ```
                    
    - Dijkstra
        - Intuition
            - 핵심
                - src → all the other nodes
                - weighted graph. 모든 edge weight가 양수
                - heap(priority queue) 사용 → 어떤 edge 사용할지 결정
            - 다음으로 조사할 노드를 그리디하게 선택
                - priority queue 사용 → 현재 가장 낮은 가격의 노드를 선택
                - 이전 접근법: `dist` array 사용 → dist[x]를 더 낮은 숫자로 개선할 수 있는 edge만 순회
            - 다익스트라: `stops` array 사용 → min price(distance) 대신에 각 node에 도달하기 위해 거쳐야 하는 중간 노드의 최소 숫자 사용
                - x가 이미 더 적은 수의 stops를 거쳐서(?) 방문되지 않았을 때만 x로 향하는 edge 순회
            - 그때 그때 가장 price가 낮은 노드를 선택하기 때문에(greedily choosing), `dst` 노드에 처음으로 도달하는 순간이 가장 적은 cost로 방문하는 순간임 - 뒤에건 더 볼 필요 없다
            - 제약사항 -  number of stops at most to k+1
                - 각 노드에 대해 current number of stops 저장
                - level by level로 iteration 하는 게 아니기 때문(?)
        - 알고리즘
            1. ADJ list 생성 
            2. stops array 생성. `stops[node]` : src → node path에서 필요한 step 수 저장. 초기값은 모두 양의 무한대-아직 어떤 노드에도 도달하지 않은 상태이기 때문
            3. min-heap 초기화. 
                - 원소: `(dist_from_src_node, node, number_of_stops_from_src_node)`
                - 초기원소: (0, src, 0)
            4. heap에 원소가 없어질 때까지 다익스트라 수행
                1. heappop → `(dist, node, step)`
                2. step vs. `stops[node]` 
                    - 지금 이 노드를 더 적은 step을 거쳐 방문한 적이 있다는 것이므로 current triplet 무시하고 continue
                3. step vs. k+1
                    - k+1보다 더 크면 너무 많은 중간 단계가 있는 상태라서 current triplet 또 무시하고 전진
                4. b.랑 c.모두 조건에 부합해서 중간에 continue 되지 않았다면, 현재 노드가 목적지인지 확인 → 만약 목적지면 그대로 return dist 
                5. **목적지도 아니면 우선 step < stops[node]는 부합하기 때문에 stops[node] update**
                6. node의 이웃들을 확인해 봐야 하기 때문에 각 이웃에 대해 heap에 새로운 triplet 만들어서 추가 (`dist + cost btw node~neighbor, neighbor, step+1`)
            5. heap 다 돌고도 return 하지 못했으면 목적지에 도달하지 못했다는 것이므로 -1 return 
        - Trial
            - 47/53에서 TLE
            - 빠진 것: heappop 한 다음 여러 edge case 피하고 dst도 아니라면, stops를 update 해줘야 하는데 그부분이 누락됨
            
            ```python
            import heapq
            class Solution:
                def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
                    travel = {}
                    for dep, arr, price in flights:
                        if dep not in travel:
                            travel[dep] = []
                        travel[dep].append((arr, price))
            
                    num_stops = [float('inf')] * n 
            
                    heap = [(0, src, 0)]
            
                    while heap:
                        cur_dist, cur_node, cur_step = heapq.heappop(heap)
                        if cur_step > num_stops[cur_node]:
                            continue
                        if cur_step > k+1:
                            continue
                        if cur_node == dst:
                            return cur_dist 
                        if cur_node in travel:
                            for neighbor, neigh_dist in travel[cur_node]:
                                triplet = (cur_dist + neigh_dist, neighbor, cur_step+1)
                                heapq.heappush(heap, triplet)
                    return -1
            ```
            
        - AC 코드 - 빠름 ⚡️
            
            ```python
            import heapq
            class Solution:
                def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
                    travel = {}
                    for dep, arr, price in flights:
                        if dep not in travel:
                            travel[dep] = []
                        travel[dep].append((arr, price))
            
                    num_stops = [float('inf')] * n 
            
                    heap = [(0, src, 0)]
            
                    while heap:
                        cur_dist, cur_node, cur_step = heapq.heappop(heap)
                        if cur_step > num_stops[cur_node]:
                            continue
                        if cur_step > k+1:
                            continue
                        if cur_node == dst:
                            return cur_dist 
                        # update the stops! 
                        num_stops[cur_node] = cur_step
                        if cur_node in travel:
                            for neighbor, neigh_dist in travel[cur_node]:
                                triplet = (cur_dist + neigh_dist, neighbor, cur_step+1)
                                heapq.heappush(heap, triplet)
                    return -1
            ```
            
    - 복잡도 분석
        - 시간: O(N+ E*K*log(E*K))
            - 이번 iteration에서 heappop 된 node가 A라고 할 때
                - stops[A] < step 이면 이미 node A를 더 적은 수의 중간 노드로 방문을 완료한 상태이기 때문에 A의 이웃을 돌지 않음
                - 반대 경우면 A의 이웃을 돈다 - which can be true K times
                    - `A` can be popped the first time with `K` steps, followed by `K-1`steps, and so on until `1` step.
                
                → 각 edge는 K 번만 처리될 수 있고, 그래서 O(E * K)
                
            - PQ에서 O(E * K) element 들을 처리하는 데 드는 시간은
                - O(E * K * log(E* K))
            - stops array 사용해서 O(N) 시간 든다
                - 길이 N의 array를 생성하는데 O(N) 걸림
        - 공간: O(N+ E * K)
            - adj list → 모든 edge가 하나의 element 형성(pair). O(E)
            - stops array → 모든 노드가 한칸씩 갖고 있음. O(N)
            - PQ는 O(E * K)개의 원소 가질 수 있음