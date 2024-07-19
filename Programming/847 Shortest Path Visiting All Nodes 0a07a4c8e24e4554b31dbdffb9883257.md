# 847. Shortest Path Visiting All Nodes

Status: no idea 🤷‍♀️, 🏋️‍♀️
Theme: BFS, DP
Created time: January 30, 2024 9:33 AM
Last edited time: January 30, 2024 4:25 PM

- Trial
    - Top-down - 예제 1/2
        - 모든 이웃을 다 방문하는 게 아니라 방문 처리가 된 노드(해당 자리가 bit 1인) 에 대해 두 가지 분기
            - 왜냐면 이미 방문한 걸 가정할 때는 mask 변화 없이 그대로 넣어주는데, 이 경우 방문 처리가 안되어 있으면 이웃 자리 bit가 0일 것임
            - 방문 안 한 경우는 1을 0으로 뒤집에서 방문하도록 유도
                - 그리고 뒤집는 건 neighbor이 아니라 node 자리의 bit
        
        ```python
        class Solution:
            def shortestPathLength(self, graph: List[List[int]]) -> int:
                n = len(graph)
                ending_mask = (1 << n) - 1
                memo = {}
        
                # function
                def recur(node, mask):
                    # check memoized
                    if (node, mask) in memo:
                        return memo[(node, mask)]
                    # base case - starting point
                    if (mask & (mask-1) == 0):
                        return 0 
                    # infinite cycle prevention
                    memo[(node, mask)] = float('inf')
                    # recurrence relation 
                    cur_min = float('inf')
                    for neighbor in graph[node]:
                        visited = recur(neighbor, mask)
                        # bit flipping
                        new_mask = mask ^ (1 << neighbor)
                        not_visited = recur(neighbor, new_mask)
                        # choose the best
                        temp_min = min(visited, not_visited) + 1 
                        cur_min = min(temp_min, cur_min)
                    memo[(node, mask)] = cur_min
                    return memo[(node, mask)]
        
                # DFS for all nodes 
                min_len = float('inf')
                for i in range(n):
                    cur_len = recur(i, ending_mask)
                    min_len = min(min_len, cur_len)
                return min_len
        ```
        
    - BFS - 예제 통과, 2/51
        - base case (node가 하나거나 없는 경우) handling이랑, next_queue를 reset 하지 않아서 그런 거였음
        
        ```python
        from collections import deque
        class Solution:
            def shortestPathLength(self, graph: List[List[int]]) -> int:
                n = len(graph)
                queue = deque()
                seen = set()
                steps = 0
                ending_mask = (1 << n) - 1 
        
                # base case population
                for i in range(n):
                    queue.append((i, (1 << i)))
                    seen.add((i, (1 << i)))
                
                # queue iteration
                next_queue = deque()
                while queue:
                    for _ in range(len(queue)):
                        cur_node, cur_mask = queue.popleft()
                        for neighbor in graph[cur_node]:
                            next_mask = (cur_mask | (1 << neighbor))
                            if next_mask == ending_mask:
                                return steps + 1 
                            new_element = (neighbor, next_mask)
                            if new_element not in seen:
                                next_queue.append(new_element)
                                seen.add(new_element)
                    steps += 1 
                    queue = next_queue
        ```
        
- AC 코드
    - Top-down (🤷‍♀️)
        - 솔직히 이해가 잘 안간다. 왜 11…11에서 시작하는지도 모르겠고, 왜 neighbor가 아닌 node의 bit를 flippling 하는지도 모르겠고
        - 어쨌든 1111 → 0001로 going backward 한다고 생각하면, neighbor bit이 1이어야 아직 탐험을 안한게 되고, node 자리가 0이어야 탐험을 마친 게 된다
        
        ```python
        class Solution:
            def shortestPathLength(self, graph: List[List[int]]) -> int:
                n = len(graph)
                ending_mask = (1 << n) - 1
                memo = {}
        
                # function
                def recur(node, mask):
                    # check memoized
                    if (node, mask) in memo:
                        return memo[(node, mask)]
                    # base case - starting point
                    if (mask & (mask-1) == 0):
                        return 0 
                    # infinite cycle prevention
                    memo[(node, mask)] = float('inf')
                    # recurrence relation 
                    cur_min = float('inf')
                    for neighbor in graph[node]:
                        # visited neighbor only 
                        if mask & (1 << neighbor):
                            visited = recur(neighbor, mask)
                            # bit flipping (1 -> 0)
                            new_mask = mask ^ (1 << node)
                            not_visited = recur(neighbor, new_mask)
                            # choose the best
                            temp_min = min(visited, not_visited) + 1 
                            cur_min = min(temp_min, cur_min)
                    memo[(node, mask)] = cur_min
                    return memo[(node, mask)]
        
                # DFS for all nodes 
                min_len = float('inf')
                for i in range(n):
                    cur_len = recur(i, ending_mask)
                    min_len = min(min_len, cur_len)
                return min_len
        ```
        
    - BFS(⚡️🏄🏻‍♀️)
        
        ```python
        from collections import deque
        class Solution:
            def shortestPathLength(self, graph: List[List[int]]) -> int:
                n = len(graph)
                if n == 1:
                    return 0
        
                queue = deque()
                seen = set()
                steps = 0
                ending_mask = (1 << n) - 1 
        
                # base case population
                for i in range(n):
                    queue.append((i, (1 << i)))
                    seen.add((i, (1 << i)))
                
                # queue iteration
                while queue:
                    next_queue = deque()
                    for _ in range(len(queue)):
                        cur_node, cur_mask = queue.popleft()
                        for neighbor in graph[cur_node]:
                            next_mask = (cur_mask | (1 << neighbor))
                            if next_mask == ending_mask:
                                return steps + 1 
                            new_element = (neighbor, next_mask)
                            if new_element not in seen:
                                next_queue.append(new_element)
                                seen.add(new_element)
                    steps += 1 
                    queue = next_queue
        ```
        
- Editorial
    - **Approach 1: DFS + Memoization (Top-Down DP)**
        - Overview
            - 왜 DP problem?
                - 최단 경로 요구
                - 그래프를 지나가면서 내리는 결정에 따라 정답이 달라짐
                    - 결정: 어떤 노드를 먼저 방문
                    - 정답: 각 노드에서 어떤 edge를 취해야 하는가(?)
            - 문제 제약 조건
                - 노드 수가 12보다 작거나 같다 ⇒ explore all the possibilities
            - state definition
                - 노드와 edge를 재방문해도 되기 때문에 아래 두 정보만 있으면 됨(?)
                1. 현재 위치한 노드가 어디인지
                2. 어떤 노드들이 이미 방문되었는지 
                    - 어떤 자료 구조에 저장? array도 되지만 caching의 제 1 목적은 반복되는 계산을 안해도 되게끔 하는 것 → array는 mutable이라서 hash table에 key로 들어갈 수 없다 (?)
            - **Bit Manipulation To Encode State**
                - 노드가 n개 있으면, 가능한 state-nodes we have visited so far-은 2^n개
                    - 각 노드마다 방문했거나 안했거나니까
                - 어떤 정수의 i번째 bit가 1로 설정되면, i번째 노드를 방문했다는 뜻
                    - bit: 정수를 binary representation으로 변환했을 때, 각 자리의 binary number
                    - 주의! bit는 오른쪽에서 왼쪽으로 세고, 가장 오른쪽 숫자는 0th bit임
                        
                        ![Untitled](Untitled%2011.png)
                        
                - 두 가지 결정해야 할 사항
                    1. bit mask 상태를 어떻게 바꿀지 (예: 특정 노드를 방문한다고 할 때, 그 자리의 bit를 어떻게 flip 할 것인지) 
                    2. 지금까지 방문한 노드들을 어떻게 알아볼 것인가
                - bit mask 상태 바꾸기
                    - 그림
                        
                        ![Untitled](Untitled%2012.png)
                        
                    1. 숫자 1에서 시작 → i번 left shift → i번째 자리에만 1이 있는 binary number 생성 
                        - 예) 1 << 4  = 16 → binary로 표현하면 10000
                    2. 1에서 생성한 숫자와 우리의 mask를 가지고 XOR 연산
                        - 1 XOR 1 = 0, 1 XOR 0 = 1
                        - 1에서 생성한 숫자는 특정 자리에만 1을 갖고 있음. 우리 mask가 그 자리에
                            - 0을 갖고 있었으면 1로 flip
                            - 1을 갖고 있었으면 0으로 flip
                - 특정 노드의 방문 여부 확인
                    - 그림
                        
                        ![Untitled](Untitled%2013.png)
                        
                    - 예) 7번째 노드가 방문 되었는지 확인하기
                        1. 숫자 1에서 시작 → left shift 7 번 → 1 << 7 = 128 = 10000000
                        2. 1의 숫자와 우리의 mask를 AND 연산 실행
                            - 우리 mask의 7번째 자리 숫자가 1이었으면 1 → visited
                            - 0이었으면 0이 나올 것 → unvisited
        - Intuition
            - state definition (node, mask)
                - node: 우리가 현재 위치한 노드
                - mask: 이미 방문한 노드들은 1로 표시되어 있는 bitmask
            - state transtion
                - node → edge가 있는 노드로만 이동 가능 - neighbors
                - 현재 노드가 1이고 0인 노드로부터 온 경우
                    - 노드 0에서 1로 가기 전, 두 가지 옵션 존재
                        1. 1이 이미 방문된 노드인 경우 1 (1 → 0 → 1)
                            - bitmask 달라질 필요 없음
                        2. 1을 처음으로 방문하는 경우 (0 → 1)
                            - before the move: 01 → after the move: 11
                            - 방문하려는 노드 위치의 bit를 뒤집기
                    - 각 movement가 하나의 step으로 세어지기 때문에, 1.2. 중 더 나은 선택에 1을 더해준다
                - `dp(node, mask) = 1 +`
                    - +1 : 다음 node로 이동하는 step 한 개 count
                    - `for all neighbors in graph[node]`.
                        - 모든 이웃을 방문해야 함
                    - `min(`
                        - `dp(neighbor, mask),`
                            - 이미 neighbor가 방문된 노드인 경우
                        - `dp(neighbor, mask ^ (1 << node))),`
                            - 1 << neighbor
                                - neighbor 위치만 1이고 나머지는 0인 binary representation
                            - mask와 XOR 연산 실행 → neighbor 자리가 0인 경우 1로 flipping
                                - 기존에 1인 경우 0으로 flipping 될텐데?
            - recurrence → 무한 사이클 (undirected graph)
                - 처음으로 어떤 노드를 방문(A, mask)하면, 우선 state value (경로 길이)를 무한대로 caching 해둠
                - 그럼 (A, mask) → (B, mask)로 간 다음에 최소 하나의 새로운 노드를 방문하지 않고는 (mask를 변경시키지 않고는) 다시 A,mask로 돌아갈 수 없음을 의미
                - 재귀식에서 보면 min(이미 방문한 노드로 이동, 처음 방문하는 노드로 이동)이니까 무한대로 설정한 게 어느 쪽인지 모르겠지만, 그 반대쪽만 이동하게 된다 이런 느낌인듯
            - base case
                - 모든 노드를 방문한 경우 return 0
                - no more steps need to be made
                - 혹은 방문 안한 노드가 1개만 남아 있는 경우도 return 0
                    - 다른 모든 노드는 방문한 상태이고, 지금 마지막으로 하나 남은 미방문 노드에 서 있는 상태이기 때문에
            - thinking in backward direction
                - choose the latter option(?)
                - DFS를 top, 즉 모든 노드를 방문한 상태에서 DFS 시작
                    - ending mask: (2^n)-1 or (1 << n) -1
                        - 예) n = 5 → 2^5 = 100000 → -1 = 31 = 11111
                - 여기서 시작해서 가려는 base case? (위의 base case랑은 다름)
                    - 문제에서 어느 노드에서든 시작할 수 있다고 함 → mask에 1인 bit가 하나인 어떤 state든 base case가 될 수 있음 (starting position)
                    - mask에 1인 bit가 한 개인지 확인하는 방법
                        - `mask & (mask-1) == 0`
                            - the least significant bit (제일 오른쪽 1)을 0으로 바꿔줌
                            - mask: 10…000 이런 모양 → mask-1 = 01…111 이런 모양 → 둘에 AND operation 하면 같은 자리에 1인 bit가 없기 때문에 0이 나와버림
            - DFS
                - optimal path는 어느 노드에서나 끝날 수 있기 때문에, 각 노드에 대해 DFS 해야 한다 (???)
        - 알고리즘
            1. 변수 초기화 
                - n, endingMask (`(1 << n) - 1`)
                - memo
                    - key가 bitmask integer인 것 같다
                    - 아니면 node, mask tuple인 것 같기도?
            2. function definition `dp(node, mask)`
                1. 현재 상태 (mask 말하는 거겠지?)가
                    1. 이미 방문된 경우, cached result를 return 
                    2. 방문되지 않은 경우 base case check 
                        - `mask & (mask-1)` 이 0이면 하나의 bit만 1이라는 소리고, 모든 노드를 방문했다는 의미이므로 return 0
                        - 헷갈리는 점 - 현재 노드가 마지막 노드면 내 자리에 와서 모두 0이 되어야 하는게 아닌가? bit가 하나 1로 남겨 져 있으면 그리로 추가 step 하나를 더 밟아야 하는게 아닌가?
                            - intuition block에 따르면, 이미 그 노드는 방문된 상태의 starting point에 다다른 것이므로 추가적인 step이 필요 없다. 우리는 11…111 → 010…0 으로 가는 것과 마찬가지
                    3. memo에도 없고 base case도 아니면, memo에 우선 양의 무한대로 현재 상태를 캐싱해둠 - 재귀식 들어가기 이전에 이 조치를 취해야 무한 사이클 막을 수 있다는 점 주의 
                        - DFS에서 color gray 상태랑 비슷한 듯
                    4. 재귀식 적용 
                        - 현재 node의 모든 이웃에 대해 두 가지 옵션 탐험
                            1. 이웃이 이미 방문된 상태거나 
                                - mask에 변경 없음
                            2. 이웃을 처음으로 방문하는 경우거나 
                                - mask의 이웃 bit를 flipping
                        - 1, 2 중 best option에 1 더해서 memo 값 update
                        - returned the cached result
            3. 각 node에 대해 DFS 수행 - dp(node, endingMask) for all node from 0 → n-1 
                - n개의 결과 중 가장 작은 결과를 return
                
        
    - **Approach 2: Breadth-First Search (BFS) (🏄🏻‍♀️🏄🏻‍♀️🏄🏻‍♀️)**
        - Intuition
            - BFS는 unweighted graph에서 최단 경로를 보장
                - 정답을 찾자마자 그게 optimal이라는 것이 보장됨 ↔ DFS는 모든 노드에 대해 다 해봐야 했음
            - base case (starting bit만 1, 나머지는 0) → ending mask (모두 1)
                - 주어진 state (node, mask)에 대해 모든 이웃의 (neighbor, mask | (1 << neighbor)) traverse
                    - ‘|’ OR 연산 오른쪽은 neighbor 자리가 무조건 1
                    - mask에서 neighbor 자리가 1이더라도 1, 0이더라도 1로 바뀜
        - 알고리즘
            1. 그래프에 노드가 하나면, return 0 
                - 더 이상 step 없이 node 0에서 시작하는 것만으로도 모든 노드 방문한 것이므로
            2. 변수 초기화
                - n, ending mask
                - seen (방문 여부 표시), queue
                - steps: 몇번째 step에 있는지 표시. BFS는 최단 경로를 보장하기 때문에, ending mask와 마주치는 즉시 return steps
            3. queue와 seen에 base case들을 넣어준다 
                - 모든 노드를 starting node로 삼는 경우
                - 모든 i에 대해 (i, 1 << i)
            4. BFS 수행 
                1. `next_queue` 초기화 - current step의 끝에서 queue를 대체
                2. current queue에 대해 iteration 
                    - 각 state (node, mask)에 대해 graph[node] (neighbors) 순회
                    - 각 이웃에 대해 새로운 상태 선언 (neighbor, next_mask)
                        - next_mask = mask | (1 << neighbor)
                        - next_mask가 ending mask이면 이웃 노드로 1개의 step만 더 하면 모든 노드 방문 완료된다는 뜻이므로 return steps + 1
                        - 새로운 state(next_mask)가 아직 방문되지 않았으면, next_queue에 넣어주고 seen에도 넣어준다
                3. current queue에 있는 모든 원소를 다 탐방했으면, steps를 1 증가시키고, queue를 next_queue로 대체한다 
            5. input graph는 언제나 connected이기 때문에 언제나 답이 나올 것 - 그래서 다른 경우는 신경 안써도 된다. return statement에 언제나 도달하게 될 것