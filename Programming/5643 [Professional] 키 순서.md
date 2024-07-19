# 5643. [Professional] 키 순서

Created time: May 16, 2024 2:13 PM
Last edited time: May 16, 2024 5:33 PM

- scratch
    
    ![Untitled](Untitled%2090.png)
    
    (2)의 경우, 4가 나와야 하는데 (5)→(4) 연결 때문에 답이 5가 나온다 
    
- Trial
    - 예제 통과
        
        ```python
        import sys
        sys.stdin = open('temp_input/sample_input.txt')
        from collections import deque
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            M = int(input())
            to_node = {i:[] for i in range(1, N+1)} # i-> next node
            from_node = {i:[] for i in range(1, N+1)} # prev node -> i
            for _ in range(M):
                a, b = map(int, input().split())
                to_node[a].append(b)
                from_node[b].append(a)
        
            ans = 0
            for target in range(1, N+1):
                connected = [0] * (N+1)
                for prev in from_node[target]:
                    dq = deque(from_node[target])
                    while dq:
                        cur_prev = dq.popleft()
                        if connected[cur_prev]:
                            continue
                        connected[cur_prev] += 1
                        for prev_prev in from_node[cur_prev]:
                            if not connected[prev_prev]:
                                dq.append(prev_prev)
                if len(to_node[target]) + sum(connected) == N-1:
                    ans += 1
            print(f'#{t} {ans}')
        
        ```
        
- 남의 풀이 세가지
    - [x]  adjacency matrix
    - [x]  bfs/dfs
    - [x]  floyd-warshall
- floyd-warshall 알고리즘 복습
    - 모든 node pair 간의 최단 경로를 찾는 알고리즘
    - 음수 가중치 그래프에서도 동작
    - 시간 복잡도 : O(V**3)
    - DP 사용하여 점진적으로 최단 경로 개선
        - 모든 pair에 대해 직접 경로 가중치를 초기화
        - 중간 경로를 거치는 모든 가능한 경로를 고려하여 최단 경로 갱신
    - 알고리즘
        1. 초기화 
            - 거리 행렬 초기화. dist[i][j]
                - edge 가중치. 경로가 없으면 무한대로 설정 (매트릭스 초기값은 모두 무한대)
            - 자기 자신에 대한 거리는 0 (dist[i][i])
        2. 경로 갱신
            - 모든 정점 k를 중간 정점으로 사용하여 거리 행렬 갱신
                - dist[i][j] > dist[i][k] + dist[k][j] 이면 후자로 갱신
- 남의 코드 플로이드 와샬
    - 가중치가 없는 상황이라 엣지가 있으면 dist[i][j]=1, 없으면 초기값인 float(’inf’), 자기자신에 대한 거리는 0
    - 플로이드 3중 for loop 돈다
        - i,j가 직접적이 아니더라도 연결이 되어 있으면 어쨌든 inf 값이 아니게 될 것
    - 각 row, col 돌면서 i,j 가 서로 다른 값이고 float(’inf’) 값이 아니면, row, col cnt를 하나씩 늘린다
        - rowcnt는 i에 대해 += 1 ← i보다 큰 노드의 개수
        - colcnt는 j에 대해 += 1 ← j보다 작은 노드의 개수
    - 최종 답은 total cnt
- AC 코드
    
    ![Untitled](Untitled%2091.png)
    
    - 속도는 dfs가, 메모리는 bfs가 1등
    - 재귀(dfs) + adj_matrix
        
        ```python
        def get_taller(node, visited):
            global num_taller
            visited[node] = 1
            for i in range(1, N+1):
                if not visited[i] and adj_mat[node][i]:
                    num_taller += 1
                    get_taller(i, visited)
        def get_smaller(node,visited):
            global num_smaller
            visited[node] = 1
            for i in range(1, N+1):
                if not visited[i] and adj_mat[i][node]:
                    num_smaller += 1
                    get_smaller(i, visited)
        
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            M = int(input())
            # adjacency matrix
            adj_mat = [[0] * (N+1) for _ in range(N+1)]
            for _ in range(M):
                a, b = map(int, input().split())
                adj_mat[a][b] = 1  # a < b
            ans = 0
            for target in range(1, N+1):
                num_taller, num_smaller = 0, 0
                get_taller(target, [0] * (N + 1))
                get_smaller(target, [0] * (N + 1))
                if num_taller + num_smaller == N-1:
                    ans += 1
            print(f'#{t} {ans}')
        
        ```
        
    - bfs + adj_matrix
        
        ```python
        import sys
        sys.stdin = open('temp_input/sample_input.txt')
        from collections import deque
        
        def get_taller(node, visited):
            dq = deque([node])
            visited[node] = 1
            res = 0
            while dq:
                curr = dq.popleft()
                for i in range(1, N+1):
                    if not visited[i] and adj_mat[curr][i]:
                        res += 1
                        visited[i] = 1
                        dq.append(i)
            return res
        
        def get_smaller(node,visited):
            dq = deque([node])
            visited[node] = 1
            res = 0
            while dq:
                curr = dq.popleft()
                for i in range(1, N + 1):
                    if not visited[i] and adj_mat[i][curr]:
                        res += 1
                        visited[i] = 1
                        dq.append(i)
            return res
        
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            M = int(input())
            # adjacency matrix
            adj_mat = [[0] * (N+1) for _ in range(N+1)]
            for _ in range(M):
                a, b = map(int, input().split())
                adj_mat[a][b] = 1  # a < b
            ans = 0
            for target in range(1, N+1):
                num_taller = get_taller(target, [0] * (N + 1))
                num_smaller = get_smaller(target, [0] * (N + 1))
                if num_taller + num_smaller == N-1:
                    ans += 1
            print(f'#{t} {ans}')
        
        ```
        
    - floyd-warshall
        
        ```python
        import sys
        sys.stdin = open('temp_input/sample_input.txt')
        
        def floyd_warshall():
            for i in range(1, N+1):
                for j in range(1, N+1):
                    if i == j:
                        continue
                    for k in range(1, N+1):
                        if dist[i][j] > dist[i][k] + dist[k][j]: # i < k < j
                            dist[i][j] = dist[i][k] + dist[k][j]
        
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            M = int(input())
            # dist matrix
            dist = [[float('inf')] * (N+1) for _ in range(N+1)]
            for _ in range(M):
                a, b = map(int, input().split())
                dist[a][b] = 1
            for i in range(1, N+1):
                dist[i][i] = 0
        
            floyd_warshall()
            ans = 0
            taller_count, shorter_count = [0] * (N+1), [0] * (N+1)
            for i in range(1, N+1):
                for j in range(1, N+1):
                    # dist[i][j]: i < j
                    if i != j and dist[i][j] != float('inf'):
                        taller_count[i] += 1
                        shorter_count[j] += 1
        
            for i in range(1, N+1):
                if taller_count[i] + shorter_count[i] == N-1:
                    ans += 1
        
            print(f'#{t} {ans}')
        
        ```