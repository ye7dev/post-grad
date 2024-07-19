# 218. The Skyline Problem

Status: done, in progress, incomplete, 🏋️‍♀️
Theme: recursive
Created time: December 7, 2023 5:50 PM
Last edited time: December 11, 2023 5:15 PM

- 문제 이해
    
    input:  빌딩의 높이(y좌표 인듯) 와 위치. 위치는 왼쪽 경계로부터 몇 칸 떨어져있는지, 오른쪽 경계로부터 몇 칸 떨어져 있는지 (left, right, height)
    
    skyline은 키포인트들의 리스트로 표현-키포인트들은 x좌표 기준으로 정렬된 상태
    
    각 키포인트들은 horizontal segment의 왼쪽 끝점 - 마지막 점만 제외하고
    
    ![Untitled](Untitled%2031.png)
    
    마지막 점은 무조건 제일 오른쪽에 위치한 건물의 우하단 끝점. 무조건 높이는 0
    
    제일 왼쪽, 제일 오른쪽 건물 사이에 있는 지표면-건물이 없는 부분-은 무조건 스카이라인의 
    
    무조건 뒤의 빌딩의 left는 앞의 빌딩의 left보다 크다 
    
- 과정
    - 언제 stack에서 pop 하냐 → 이번 직사각형으로 만들어지는 endpoint를 모두 다 만들었을 때.
    - endpoint는 언제 만들어지냐? 내 좌상단 좌표로 만들어지는 수평선이 끝나고 높이 변경이 생길 때
    - minheap 쓰면 안되나? 그리고 우상단 좌상단을 따로 좌표에 넣어주는 방법이 있을 듯
    - 1시간 비몽사몽 고민해서 만든 솔루션-그러나 13/42가 최선…
        
        ```python
        from collections import deque
        class Solution:
            def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                endpoints = [[buildings[0][0], buildings[0][2]]]
                stack = [[buildings[0][1], buildings[0][2]]] # right, left
        
                for i in range(len(buildings)):
                    prev_right, prev_height = stack[-1]
                    cur_left, cur_right, cur_height = buildings[i]
                    if cur_left > prev_right:
                        endpoints.append([prev_right, 0])
                        endpoints.append([cur_left, cur_height])
                    elif cur_left == prev_right:
                        if cur_height != prev_height:
                            endpoints.append([cur_left, cur_height])
                    else:
                        if cur_height > prev_height:
                            endpoints.append([cur_left, cur_height])
                        elif cur_height < prev_height:
                            endpoints.append([prev_right, cur_height])
                    stack.append([cur_right, cur_height])
                endpoints.append([cur_right, 0])
        
                return endpoints
        ```
        
    
- 돈 값 하는 프리미엄 Editorial
    - **Brute Force I**
        - 요약
            - get unique positions
            - init heights
            - update heights
            - get endpoints
        - 그림
            
            ![Untitled](Untitled%2032.png)
            
            ![Untitled](Untitled%2033.png)
            
        - 설명
            - 왼쪽, 오른쪽 edge를 모두 모은다 - endpoint가 생성될 수 있는 후보들
            - 높이 h의 빌딩이 index `x_i`부터 `x_j` 까지 커버한다면, `x_i`부터 `x_j` (right edge exclusive) 사이의 x index들은 최소 h의 높이를 가진다
            - `heights` : index가 x좌표, heights[i]가 y 좌표
                - len(heights) : unique position 개수
                - 초기값은 0
                - update: 빌딩을 돌면서 하나의 빌딩이 커버하는 구간에 대해 height 값을 빌딩 높이로 갱신. 더 높은 높이의 빌딩이 커버하게 되면 더 높은 값으로 update. maximum height
            - `heights` 를 돌면서 height change가 발생하는 위치를 endpoint에 추가
        - 코드 🪇
            - positions랑 heights의 index를 연동하는게 좀 헷갈렸다
            - 시간 복잡도: O(n^2). n=len(buildings)
            
            ```python
            class Solution:
                def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                    # get unique positions
                    positions = []
                    for b in buildings:
                        left, right, h = b
                        if left not in positions:
                            positions.append(left)
                        if right not in positions:
                            positions.append(right)
                    positions.sort()
                    len_unique = len(positions)
            
                    # init heights
                    heights = [0] * len_unique 
            
                    # update heights
                    for b in buildings:
                        left, right, h = b 
                        left_idx, right_idx = positions.index(left), positions.index(right)
                        for idx in range(left_idx, right_idx):
                            if heights[idx] < h:
                                heights[idx] = h 
            
                    # get endpoints 
                    endpoints = []
                    prev = 0
                    for i in range(len(heights)):
                        if heights[i] != prev:
                            endpoints.append([positions[i], heights[i]])
                            prev = heights[i]
                    #endpoints.append([positions[-1], 0])
                    return endpoints
            ```
            
    - **Brute Force II, Sweep Line**
        - 요약
            - get coordinates sorted by x values
            - iterate all the coordinates
            - keep track of endpoints following small rules (right exclusive, change only)
        - 그림
            
            ![Untitled](Untitled%2034.png)
            
            ![스크린샷 2023-12-08 오후 5.35.09.png](%25EC%258A%25A4%25ED%2581%25AC%25EB%25A6%25B0%25EC%2583%25B7_2023-12-08_%25EC%2598%25A4%25ED%259B%2584_5.35.09.png)
            
            ![Untitled](Untitled%2035.png)
            
        - 설명
            - 오른쪽 edge는 exclusive임 주의
            - 무한한 길이의 수직선이 왼쪽으로 오른쪽으로 → 바닥을 쓸어넘기는 양상
                - 건물의 각 edge마다 멈추며, 수직선과 교차하는 모든 건물 중 가장 높은 높이를 기록
            - 높이가 변할 때마다 skyline(endpoint)에 current position 추가
                - 높이가 안 변하면 edge라도 추가 X
            - 알고리즘
                - `edge_set` : buildings의 모든 distinct edge 저장
                - iterate over the sorted `positions`
                    - 특정 position이 어떤 빌딩의 left, right 범위 사이에 있으면 가상의 수직선과 빌딩이 교차하는 것
                - `max_height`
                    - position에서 교차하는 빌딩들의 높이 중 가장 높은 것. 아무 빌딩이랑도 교차하지 않으면 0.
                - 이전 position에서와 max_height 값이 달라지면 end point에 넣기
        - 코드
            - 시간 복잡도는 O(n^2)로 동일
            - 내가 짠 버전
                
                ```python
                class Solution:
                    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                        edge_set = set()
                        for left, right, h in buildings:
                            edge_set.add(left)
                            edge_set.add(right)
                        edge_set = sorted(list(edge_set))
                        
                        height_dict = {i:0 for i in edge_set}
                        prev = 0
                        endpoints = [] 
                        
                        for pos in height_dict:
                            for left, right, h in buildings:
                                if left <= pos < right:
                                    height_dict[pos] = max(h, height_dict[pos])
                            if height_dict[pos] != prev:
                                endpoints.append([pos, height_dict[pos]])
                                prev = height_dict[pos]
                
                        return endpoints
                ```
                
    - **Sweep Line + Priority Queue**
        - 복기
            - edge와 building 중 어디를 iteration 하고 있는 건지 잘 생각해야 한다.
            
            ```python
            # edges 생성
            	- index associated 
            	- left, right both
              - sort by x value 
            # 필요한 자료구조, 변수 생성
            	- dq, endpoints, top_height
            # iteration
            	- edges를 도는 커다란 while 문
            		-- 새로운 edge가 들어오면 기준 x value update (⬅︎)
            			--- 여기서는 아래 while loop을 실행하기 위한 x value 기준값 설정만 한다
            		-- x value가 같은 edge들을 한번에 모두 처리하고 넘어가기 위한 둘째 while문
            			--- 같은 x value더라도 left, right에 따라 역할이 달라짐
            			--- left 이면 현재 dq의 top의 x value를 보고 아직 live이면 heappush
            					---- default가 minheap이라 height는 네가티브로 넣어줘야 
            			--- x value가 안 겹치는 top이 나올 때까지 pop 지속
            			--- left, right 각자의 할일을 마쳤으면 index를 하나 뒤로 민다
            					---- 다음 차례 인덱스에 관한 일은 다음 while loop에서 이루어진다 
            					----- 다음 인덱스의 x가 직전 x와 값이 같으면 inner while loop
            					----- 다르면 outer while loop으로 넘어가고 거기서 기준 x 값 변경 
            		-- height 확정
            			--- index는 하나 뒤로 가있지만, (⬅︎)에서 설정한 기준 x value에 대한 청산
            			--- 현재 상태: 기준 x value에서 취할 수 있는 최대 높이가 큐 탑에 위치
            			--- edge case: 큐가 비어 있는 경우 -> 높이는 0 
            		-- endpoint 추가
            				---- 마지막으로 추가한 ep의 높이와 현재 높이가 다르면 새로운 ep 추가 
            				---- edge case: ep가 비어 있는 경우 -> 바로 추가 
            return endpoins 	
            ```
            
            - 코드
                
                ```python
                import heapq
                class Solution:
                    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                        N = len(buildings)
                        edges = [] # index associated
                        for i in range(N):
                            left, right, height = buildings[i]
                            edges.append([left, i, True])
                            edges.append([right, i, False])
                        edges.sort() # default key: element[0]
                
                        pq, endpoints = [], []
                        top_height = 0 
                
                        # iteration 
                				M = len(edges)
                        idx = 0
                        while idx < M:
                            cur_x, _, _ = edges[idx] # landmark
                            # process all the edges with the same x value as the landmark
                            while idx < M and edges[idx][0] == cur_x:
                                x_val, sub_idx, is_left = edges[idx]
                                # left only
                                if is_left:
                                    _, right, height = buildings[sub_idx]
                                    heapq.heappush(pq, [-height, right])
                                # remove past buildings  
                                while pq and pq[0][1] <= cur_x:
                                    heapq.heappop(pq)
                                # marking this edge is done 
                                idx += 1 
                            # fix height
                            top_height = pq[0][0] * (-1) if pq else 0
                            # check endpoint
                            if not endpoints or endpoints[-1][1] != top_height:
                                endpoints.append([cur_x, top_height])
                        return endpoints
                ```
                
        - 설명
            - 기본 내용
                - 특정 position의 높이는 그 position이 속해있는 범위를 밑변으로 하는 빌딩 중 가장 높은 것의 높이가 됨
                - 한 position에 대해 모든 빌딩을 돌 필요 없이 바로 tallest live building을 얻게 하는 것이 목표
                - each intersecting building을 priority queue `live`에 push → 특정 position에 대해 가장 큰 tallest live building을 얻을 수 있다. pq의 top result를 확인하면 되는 것. 만약 pq가 비어 있으면 높이는 0.
                - 오른쪽 edge 처리의 경우
                    - 이론적으로는 오른쪽 edge를 만나면 그 건물은 pq에서 제외
                    - 이미 이 건물을 지나쳤으므로 더 이상 endpoint에 기여하지 않음(?)
                    - 가장 높은 빌딩이 live에 있는 한, 이미 지나친 좀 낮은 빌딩이 live에 있어도 괜찮음(?)
                    - 중요한 건 가장 큰 빌딩을 지나쳤을 때 그걸 live에서 제거해야 하는 것(?)
                    - 그림
                        
                        ![https://leetcode.com/problems/the-skyline-problem/Figures/218_re/218_sl_exp2.png](https://leetcode.com/problems/the-skyline-problem/Figures/218_re/218_sl_exp2.png)
                        
                        - 두번째 그림에서 building 2가 가장 높은 빌딩이 되었다는 것은, 그 pos에서 가장 높은 높이가 빌딩 2에서 온다는게 아니라,
                        - 현재 pos가 right edge of building3 니까 live pq에서 3의 높이를 제거했는데, 그러고 나니까 top이 2가 되어서 이대로 두면 공식(?)에 따라 max_height를 빌딩 2에서 가져올 판이다
                        - 근데 그건 틀린 답이니까 얼른 2를 빼서 현재 pos에서의 max height를 building 1에서 가져오게끔한다는 뜻인듯
                
            - 슬라이드쇼 보고 다시 정리
                - 슬라이드쇼 캡쳐
                    
                    ![Untitled](Untitled%2036.png)
                    
                    ![Untitled](Untitled%2037.png)
                    
                1. 각 빌딩을 돌면서 왼쪽, 오른쪽 경계 좌표를 리스트에 저장
                2. 1.의 경계를 x좌표 기준으로 정렬 
                3. 2.를 돌면서 priority queue에 (높이,  x 좌표) 추가
                    1. 왼쪽 경계를 만난 경우 큐에는 오른쪽 경계를 넣어준다
                    2. 일단 큐에 넣은 뒤 top 요소의 x좌표가 현재 x 좌표보다 크면 큐에 그대로 남겨둔다 
                    3. 그렇지 않으면 b.를 만족하는 요소가 top이 될때까지 큐에서 지속적으로 pop 한다 
                    4. 현재 x 좌표에서의 높이가 새로운 높이면 endpoint에 좌표 추가 
                    5. 큐에 더 이상 원소가 남아있지 않으면 높이는 0
                    
            - 다시 생각해보고 정리
                - queue가 대체하는 역할: 특정 x 좌표에 대해 모든 빌딩을 돌면서 빌딩의 왼쪽 x 좌표(inclusive)와 오른쪽 x 좌표(exclusive) 사이에 있는지 확인하는 작업 → current x좌표가 그 범위 사이에 있으면, 수직선이 왼→ 오 이동 시에 current x에 도착한다면, 어느 어느 빌딩과 교차하는지 알 수 있음 → 그리고 교차하는 빌딩 중에 가장 높이가 높은 빌딩이 스카이라인을 구성하게 될 것
                - 큐에는 오른쪽 좌표만 들어감
                    - 같은 좌표일 때 높이가 더 높은 값이 위 (index 0)에 있도록 하려면 더 작은 값을 앞으로 보내는 min heap(heapq default) 특성 고려하여 height를 음수로 넣어준다
                    - 같은 좌표라서 right, height pair가 큐에 두 개 들어갔을 때, 더 높이가 높은 height가 pop 되고 → 다음 left edge로 넘어가는지 아니면 큐에서 또 pop을 하는지?
                        - 중요한 건 tallest building의 높이가 아직 지나치기 전인지 후인지냐는 거다
                        - 더 낮은 height이기 때문에 굳이 pop을 바로 안하고 다음 pair로 넘어가도 되는듯? → 바로 pop을 하면 어떻게 나오려나?
                - edges에는 왼쪽 좌표만 들어가면 되는거 아닌가? 근데 left edge가 겹치는 경우는 어떻게 되는거지? → record the maximum height among all the buildings that intersect with the line.
                    - 오른쪽 좌표도 넣어야 하는듯?
                    - left edge, right edge 모두 iteration 대상인데, 큐에 뭘 추가하는 건 left edge만이고, 큐 top의 x좌표와 비교해서 우리가 그보다 작은 값에 있는지 확인하는 건 둘다 하는 듯 → 만약 우리의 x좌표와 같은 top이 계속 나오면 Pop 지속 → 그러다가 큐가 비어 버리면 우리의 current height는 0이 되고 그렇게 endpoint에 넣어준다
                - endpoint에 들어가는 높이
                    - 큐의 top 높이인지, 아니면 current height인지-근데 전자일 것 같은게 왼쪽 경계가 동일한 경우를 생각해보자. 그럼 같은 Left 값에 Index만 가지고 비교해야 하는데 그 귀찮음을 덜어주려고 큐가 존재하는 듯?
            - chat 센세 동원해서 다시 정리
                - left, right 말고 start, end로 생각
                1. 각 빌딩의 start, end edge 모은 다음 x 축 값을 기준으로 정렬
                    - 각 edge는 building index와 연결되어 있음
                2. active building을 추적하기 위한 우선순위 큐 사용 
                    - active: buildings that have started but not yet ended
                    - 큐에 저장되는 값: (-height, end)
                3. 각 edge를 돌면서 
                    - start인지, end인지에 따라 하는 역할이 달라짐
                    - start edge → 경계 세우기
                        - 이번에 시작한 빌딩의 높이와 end edge를 큐에 넣어준다
                    - end edge → 경계 지켰는지 확인
                        - 현재 x 좌표보다 큐의 top 값이 작거나 같은 한 이미 지나온 빌딩이라는 뜻이므로 큐에서 이 빌딩에 관한 정보를 pop 해서 제거한다
                4. endpoints 결정
                    - 주어진 x 좌표에서의 각 edge를 처리한 다음, 현재 큐에서 가장 높이가 높은 빌딩을 체크
                    - 이전 point에서와 현재 최고 높이가 다른 값을 가질 경우, 새로운 endpoint 추가
            - 시간 복잡도
                - edge는 최대 2n개 존재하므로 Iteration은 O(2n) = O(n)
                - 각 edge에서 push, pop을 한번씩 다 한다고 하면 O(2n*logn)
                    - push, pop은 한번 하는데 O(log n) 소요
                
                ⇒ O(nlogn)
                
        - 코드
            - 다시 생각해보고 짜봤으나 예제 통과 안됨
                
                ```python
                import heapq
                
                class Solution:
                    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                        endpoints = []
                        # get edges 
                        edges = [] 
                        for i, b in enumerate(buildings):
                            edges.append([True, i, b[0]]) # left
                            edges.append([False, i, b[1]]) # right
                
                        # build a queue
                        pq = []
                        prev_height = 0
                
                        for e in edges:
                            cur_x = e[2]
                            # push
                            if e[0]: # left 
                                cur_idx = e[1] # index
                                left, right, height = buildings[cur_idx]
                                heapq.heappush(pq, [-height, right]) # push right edge 
                     
                            # pop past buildings
                            while pq and pq[0][1] <= cur_x: 
                                heapq.heappop(pq)
                            
                            if not pq: # zero height
                                top_height = 0
                            else: # valid range
                                top_height = pq[0][0] * (-1)
                
                            if prev_height != top_height:
                                endpoints.append([cur_x, top_height])
                                prev_height = top_height 
                            
                        return endpoints
                ```
                
            - for vs. while
                - 동일한 x 좌표에 여러 edge가 있는 경우, 각 edge를 모두 처리하고 다음 index로 넘어가야 한다는데 무슨 말인지 모르겠음 → solution에서는 while을 사용했는데 왜 for 사용하면 안되는지 모르겠음
                - 코드 trial 1
                    
                    ```python
                    import heapq
                    class Solution:
                        def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                            # index related edge 
                            edges = [] # is_left, index, x_coord
                            for i in range(len(buildings)):
                                left, right, _ = buildings[i]
                                edges.append([True, i, left])
                                edges.append([False, i, right])
                            edges.sort(key=lambda x: x[-1]) # sort by x_coord
                    
                            pq = []
                            endpoints = []
                            # iterate edges
                            for edge in edges:
                                is_left, idx, x_coord = edge
                                # check the past buildings 
                                while pq and pq[0][1] <= x_coord:
                                    heapq.heappop(pq)
                    
                                if is_left: # set the boundary for the current building
                                    _, right, height = buildings[idx]
                                    heapq.heappush(pq, [-height, right])               
                    
                                # check current top_height 
                                if pq: 
                                    top_height = pq[0][0] * (-1)
                                else:
                                    top_height = 0
                    
                                # check end points 
                                if not endpoints: 
                                    endpoints.append([x_coord, top_height])
                                else:
                                    if endpoints[-1][1] != top_height:
                                        endpoints.append([x_coord, top_height])
                            
                            return endpoints
                    ```
                    
                    - 예시
                        
                        buildings = `[[0,2,3],[2,5,3]]`
                        
                        edges = `[[True, 0, 0], [False, 0, 2], [True, 1, 2], [False, 1, 5]]`
                        
                        | edge | is_left | pq | top_height | endpoints |
                        | --- | --- | --- | --- | --- |
                        | True, 0, 0 | T | [[-3, 2]] | 3 | [[0,3]] |
                        | F, 0, 2 | F | 2 == 2 → pop | 0 | [[0, 3], [2, 0]] |
                        | True, 1, 2 | T | [[-1, 2]] |  |  |
                        
                        → 오른쪽 경계라서 endpoint에 포함되면 안됨 → 이대로 코드를 유지하려면 endpoint 마지막 값의 x 좌표가 자기랑 일치하는 지 확인하고 또 높이는 그 전전 값이랑 동일하지 않은지까지 확인해야 하는데 구구절절…이걸 해결하고 나면 문제가 풀린다는 보장이 없고…그냥 while loop을 이해하는게 빠를까…졸립다 
                        
                        → 근데 또 그렇다고 오른쪽 경계를 지나치자고 하면 중간에 진짜 나와야 할 right, 0의 endpoint가 안나와버린다 → 그냥 while loop 받아들이자…
                        
                - 코드 trial 2
                    
                    ```python
                    import heapq
                    class Solution:
                        def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                            # index related edge 
                            edges = [] # is_left, index, x_coord
                            for i in range(len(buildings)):
                                left, right, _ = buildings[i]
                                edges.append([True, i, left])
                                edges.append([False, i, right])
                            edges.sort(key=lambda x: x[-1]) # sort by x_coord
                    
                            pq = []
                            endpoints = []
                            # iterate edges
                            i = 0
                            while i < len(edges): 
                                is_left, idx, x_coord = edges[i]
                    
                                if is_left: # set the boundary for the current building
                                    _, right, height = buildings[idx]
                                    heapq.heappush(pq, [-height, right])
                    
                                # check the past buildings 
                                while pq and pq[0][1] <= x_coord:
                                    heapq.heappop(pq)
                                    i += 1 
                    
                                # check current top_height 
                                if pq: 
                                    top_height = pq[0][0] * (-1)
                                else:
                                    top_height = 0
                    
                                # check end points 
                                if not endpoints: 
                                    endpoints.append([x_coord, top_height])
                                else:
                                    if endpoints[-1][1] != top_height:
                                        endpoints.append([x_coord, top_height])
                                i += 1 
                            
                            return endpoints
                    ```
                    
                    - 예시
                        
                        buildings = `[[0,2,3],[2,5,3]]`
                        
                        edges = `[[True, 0, 0], [False, 0, 2], [True, 1, 2], [False, 1, 5]]`
                        
                        | i | edge | is_left | pq | top_height | endpoints |
                        | --- | --- | --- | --- | --- | --- |
                        | 0 | True, 0, 0  | T | [[-3, 2]] | 3 | [[0, 3]] |
                        | 1 | F, 0, 2 | F | 2 == 2 → pop | 0 |  |
                        | 2 | True, 1, 2 | T |  |  |  |
                        
                        → 두번째 while loop 밑으로 1이 증가한 건 좋았지만, 그리고 나서 다시 is_left를 체크할 수 있는 곳으로 가야하는데 바로 top_height 체크하는 곳으로 떨어져 버림 
                        
                - 코드 trial 3
                    
                    ```python
                    import heapq
                    class Solution:
                        def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                            # index related edge 
                            edges = [] # is_left, index, x_coord
                            for i in range(len(buildings)):
                                left, right, _ = buildings[i]
                                edges.append([True, i, left])
                                edges.append([False, i, right])
                            edges.sort(key=lambda x: x[-1]) # sort by x_coord
                    
                            pq = []
                            endpoints = []
                            # iterate edges
                            i = 0
                            while i < len(edges): 
                                is_left, idx, x_coord = edges[i]
                                while i < len(edges) and edges[i][2] == x_coord:
                                    # check the past buildings 
                                    while pq and pq[0][1] <= x_coord:
                                        heapq.heappop(pq)
                                        i += 1 
                    
                                    # set the boundary for the current building
                                    if is_left: 
                                        _, right, height = buildings[idx]
                                        heapq.heappush(pq, [-height, right])
                    										i += 1 # 추가해본다 
                    
                                # check current top_height 
                                if pq: 
                                    top_height = pq[0][0] * (-1)
                                else:
                                    top_height = 0
                    
                                # check end points 
                                if not endpoints: 
                                    endpoints.append([x_coord, top_height])
                                else:
                                    if endpoints[-1][1] != top_height:
                                        endpoints.append([x_coord, top_height])
                            
                            return endpoints
                    ```
                    
                    - 예시
                        
                        buildings = `[[0,2,3],[2,5,3]]`
                        
                        edges = `[[True, 0, 0], [False, 0, 2], [True, 1, 2], [False, 1, 5]]`
                        
                        | i | x_coord | edge | is_left | pq | top_height | endpoints |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | True, 0, 0  | T | [[-3, 2]] |  |  |
                        
                        → is_left 로 해야 할 거 하고 while loop 빠져나와야 하는데 할 수가 없음 
                        
                        → is_left 하고 나서 1 더하면? x_coord랑 값 달라져서 탈출 
                        
                        | i | x_coord | edge | is_left | pq | top_height | endpoints |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | True, 0, 0  | T | [[-3, 2]] |  |  |
                        | 1 |  | False, 0, 2 |  |  | 3 | [[0, 3]] |
                        |  | 2 |  | False | pop  |  |  |
                        | 3 |  |  |  |  |  |  |
                        
                - 코드 trial 4
                    
                    ```python
                    import heapq
                    class Solution:
                        def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                            # index related edge 
                            edges = [] # is_left, index, x_coord
                            for i in range(len(buildings)):
                                left, right, _ = buildings[i]
                                edges.append([True, i, left])
                                edges.append([False, i, right])
                            edges.sort(key=lambda x: x[-1]) # sort by x_coord
                    
                            pq = []
                            endpoints = []
                            # iterate edges
                            i = 0
                            while i < len(edges): 
                                is_left, idx, x_coord = edges[i]
                                while i < len(edges) and edges[i][2] == x_coord:
                                    # set the boundary for the current building
                                    if is_left: 
                                        _, right, height = buildings[idx]
                                        heapq.heappush(pq, [-height, right])
                                    
                                    # check the past buildings 
                                    while pq and pq[0][1] <= x_coord:
                                        heapq.heappop(pq)
                    
                                    i += 1 # move edge index 
                    
                                # check current top_height 
                                if pq: 
                                    top_height = pq[0][0] * (-1)
                                else:
                                    top_height = 0
                    
                                # check end points 
                                if not endpoints or endpoints[-1][1] != top_height:
                                    endpoints.append([x_coord, top_height])
                               
                            return endpoints
                    ```
                    
            - AC 받은 코드
                
                ```python
                import heapq
                class Solution:
                    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                        # index related edge 
                        edges = [] # is_left, index, x_coord
                        for i in range(len(buildings)):
                            left, right, _ = buildings[i]
                            edges.append([True, i, left])
                            edges.append([False, i, right])
                        edges.sort(key=lambda x: x[-1]) # sort by x_coord
                
                        pq = []
                        endpoints = []
                        # iterate edges
                        i = 0
                        while i < len(edges): 
                            is_left, idx, x_coord = edges[i]
                
                            while i < len(edges) and edges[i][2] == x_coord:
                                is_left, idx, x_coord = edges[i]
                                # set the boundary for the current building
                                if is_left: 
                                    _, right, height = buildings[idx]
                                    heapq.heappush(pq, [-height, right])
                                
                                # check the past buildings 
                                while pq and pq[0][1] <= x_coord:
                                    heapq.heappop(pq)
                
                                i += 1 # move edge index 
                
                            # check current top_height 
                            if pq: 
                                top_height = pq[0][0] * (-1)
                            else:
                                top_height = 0
                
                            # check end points 
                            if not endpoints or endpoints[-1][1] != top_height:
                                endpoints.append([x_coord, top_height])
                           
                        return endpoints
                ```
                
    - **Sweep Line + Two Priority Queue**
        - 설명
            - 좆같은 설명
                - sol3에서는 별도의 표시가 필요했음
                    - right,left 구분, building idx를 따로 사용
                    - left edge의 경우 bidx 사용해서 right랑 height 들고 와야 pq에 추가 가능했음
                - sol4에서는 unique index 버리고 빌딩 높이만 저장해서 더 직관적(?)
                    - 빌딩의 left edge 만날 때면, pq에 빌딩 높이를 추가한다
                - 그럼 top building 말고 우리가 이미 지나쳐서 제거해야 할 빌딩은 어떻게 아는가? → 또 다른 pq past를 사용해서 live pq에서 제거되어야 하지만 아직 제거되지 않은 빌딩들을 담는다
                - 이제 live pq는 신용카드와 같은 것(?)
                    - 일시적으로 우리의 외상을 기록
                    - 일단 우리가 빚을 외상갚을 수 있게 되면 live pq에서의 top 빌딩이 past pq에서의 top 빌딩과 일치하게 되는 것이고, past로부터 top 빌딩을 제거한다(?)
                    - 외상이 정산되었기 때문에 past 에서도(?) top 빌딩을 제거한다
                - live와 past 둘 다로부터 top building을 반복적으로 제거한다.언제까지?
                    - past에 아무것도 남아 있지 않을 때까지 = live pq에 있는 모든 빌딩은 live 상태를 가리킨다
                    - live pq에 있는 top 빌딩이 past pq에 있는 top 빌딩보다 더 높을 때 = 제거해야 할 빌딩이 좀 있지만, 걔네 높이가 너무 낮아서 top 빌딩의 높이에 영향을 주지 못한다
            - 슬라이드 보면 좀 나으려나
                - 빈 pq live, past 두 개 초기화. iteration 시작
                
                → 빌딩1~2의 왼쪽 edge 만나면 그 높이만 live pq에 저장 
                
                - height가 변경되었으므로 current position을 skyline에 저장
                
                → 빌딩1의 right edge 만나면 빌딩1의 높이를 past에 넣는다. 
                
                - height 변경 없으므로 move on
                
                → 빌딩3의 왼쪽 edge 만나면 그 높이만 live pq에 저장 
                
                - height가 변경되었으므로 current position을 skyline에 저장
                
                → 빌딩2의 right edge 만나면 빌딩2의 높이를 past에 넣는다 
                
                - height 변경 없으므로 move on
                
                → 빌딩3의 right edge 만나면 빌딩3의 높이를 past에 넣는다.
                
                🌟 live, past pq의 top 빌딩의 높이가 같은 한, 둘 다를 pop 
                
                → pop 할만큼 다 했더니 두 pq가 모두 비게 되어 current height 0으로 update → skyline에 current positions 추가하고 끝 
                
                ![Untitled](Untitled%2038.png)
                
        - chat 센세 추가 설명
            - 늘 헷갈리는 게 왜 같은 x 좌표에 존재하는 서로 다른 edge들을 한꺼번에-최종 height 하나로만 짝지어지게- 처리해야 하는가?
                - 답변
                    
                    1. **Overlapping Buildings**: In scenarios where multiple buildings overlap (i.e., they share the same x-coordinate at some point), processing each edge separately might not correctly reflect the actual skyline. For example, if one building ends and another taller building starts at the same x-coordinate, processing these as separate events could incorrectly introduce a point where the skyline drops to zero before rising again, which doesn't accurately represent the continuous nature of the actual skyline.
                    
                - 오른쪽 edge가 다음 빌딩의 왼쪽 edge와 겹친다고 할 때, skyline은 왼쪽 edge를 갖는 빌딩의 높이에 점이 찍혀야 함(다른 조건 만족한다고 할 때)
                - 그런데 얘네를 따로 처리하게 되면 오른쪽 edge는 exclusive라서 높이 0과 짝지어서 x 좌표값이 endpoint 하나로 짝지어지고, 다음 빌딩의 왼쪽 edge는 inclusive라서 자기 높이랑 짝지어져서 또 다른 endpoint 하나로 짝지어짐. 그러나 우리는 후자만 남기를 바람
                - 따라서 같은 x 좌표에 존재하는 서로 다른 edge들은 무조건 하나의 endpoint로 귀결되어야 함
        - 코드
            - 시간 엄청 빨라짐
            
            ```python
            import heapq 
            
            class Solution:
                def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                    edges = []
                    live, past = [], []
                    endpoints = []
            
                    for left, right, height in buildings:
                        edges.append([left, True, -height])
                        edges.append([right, False, -height])
                    edges.sort()
            
                    edge_idx = 0
                    while edge_idx < len(edges):
                        cur_x, _, _ = edges[edge_idx]
            
                        while edge_idx < len(edges) and edges[edge_idx][0] == cur_x:
                            _, is_left, height = edges[edge_idx]
                            if is_left:
                                heapq.heappush(live, height)
                            else:
                                heapq.heappush(past, height)
            
            		            while past and live[0] == past[0]:
            		                heapq.heappop(live)
            		                heapq.heappop(past)
            
            								edge_idx += 1 
                        
                        cur_height = -live[0] if live else 0 
            
                        if not endpoints or endpoints[-1][-1] != cur_height:
                            endpoints.append([cur_x, cur_height])
                    
                    return endpoints
            ```
            
    - **Union Find**
        - Union-find class definition
            - `init(self, N)`
                - self.root = [i for i in range(N)]
                - root[x]: x의 궁극적인 parent 또는 x가 속한 집합의 대표자
                    - x가 어느 집합에 속했는지를 알려주는 역할
            - `find(self, x)`
                - 효율성을 높이는 path compression을 수행하면서
                    - 각 node를 다이렉트로 root에 연결해서 future 탐색을 용이하게 한다
                    - recursion 수행하는 동안 만난 모든 node들의 parent reference를 root node로 연결
                    - parent refernce: immediate parent를 나타내는 값
                - x의 root를 재귀적으로 확인하고 최종 root를 return 한다
            - `union(self, x, y)`
                - x의 parent reference를 y의 parent reference로 update
        - 설명
            - Brute-force O(n^2) time complexity
                - 새로운 빌딩이 들어올 때마다 이 빌딩으로 커버할 수 있는 모든 인덱스를 돌면서 heights에 적절한 값(max)을 업데이트 했어야 함
            - 이제 아주 작은 높이를 가진 빌딩이 있다고 가정하고, 이 빌딩의 heights 값들이 어떤 더 큰 빌딩들에 의해 이미 update 되었다고 가정 → 이번에는 update 안한다
                
                ![Untitled](Untitled%2039.png)
                
                - 빌딩 2가 빌딩 1보다 늦게 나오는데, 두 빌딩이 같은 edge에 있어서 그 사이 존재하는 position 들도 같은 상태
                - 빌딩1의 높이가 더 높아서 position들의 height list 값이 이미 빌딩1의 높이로 update된 상태이고, 빌딩2의 높이가 max가 아니기 때문에 더 이상 heights의 값들은 update 되지 않는다
            - 위와 같은 불필요한 non-updates(update는 안 일어나지만 코드 상에서 확인은 한번씩 다하고 지나가는…)를 피할 방법은 없을까?
            - 아래와 같은 내용을 일부 index(position)들에게 적용한다고 가정
                - 나로부터 시작하고, XX(나보다 오른쪽에 있는 어떤 index)에서 끝나는 높이는 이미 update 되었다. 이들의 높이는 너네 높이보다 높기 때문에 update 할 꿈도 꾸지 말아라. 그냥 바로 XX(어차피 exclusive라서 previous term에서는 무시됨)로 점프해서 진행해라
            - 각 edge마다 값 하나를 부여 → 이 값은 현재 edge보다 낮지 않은 높이를 가진 연속된 범위에서 가장 오른쪽에 위치한 edge의 값
                - 왜 이런 값들을 부여하고 난리?
                    - 스킵하고 지나갈 수 있는 edge들의 범위를 밝히는 데 도움을 준다
                    
                    ![Untitled](Untitled%2040.png)
                    
                    ↳ x_i index에 대응하는 값은 x_j
                    
                    - 왜 둘이 대응하는가? x_i를 왼쪽 경계로 하는 빌딩의 높이와 같거나 그보다 높은 빌딩의 경계들 중, 가장 오른쪽에 있는 x 좌표 값이 x_j이기 때문.
                    - 왼쪽 그림. x_i로 시작하는 건물은 빨간색. 빨간색 건물보다 높거나 같은 높이에 해당하는 건물은 초록색. 초록색 건물의 오른쪽 경계는 x_j
                    - 오른쪽 그림. x_i로 시작하는 건물은 파란색. 이보다 높거나 같은 높이의 건물은 자기 자신도 있고(!!!), 빨간색도 있고, 초록색도 있다. 이 건물들의 모든 경계를 두고 볼때, x 좌표값이 가장 큰 경우는 자기 자신-파란색 건물-의 오른쪽 경계 x_j이다
                    
                    → [x_i, x_j) 구간 사이의 인덱스들은 모두 x_i와 같거나 그보다 높은 높이 값을 갖는다 
                    
            - Skip의 미덕
                - 모든 index를 다 돌고도 아무것도 update 하지 않는 대신
                - 먼저 `root` 에서 현재 index에 해당하는 값이 있는지 확인 → 값이 있으면 그 값보다 작은 중간 index들은 모두 건너 뛴다.
                    - 건너뛰는 index들의 heights는 이전에 더 높은 빌딩의 높이로 다 update가 된 상태라서 이번 건물의 높이로는 update될리가 없기 때문에 그냥 넘어감으로써 시간을 아끼는 전략
                        
                        ![Untitled](Untitled%2041.png)
                        
            - 앞쪽에 높이가 더 높은 빌딩들을 먼저 보도록 만들어서 스킵해도 되는 구간을 최대로 만들려면 어떻게?
                - 빌딩을 높이 내림차순으로 돈다
                - 그래서 각 빌딩을 돌 차례가 되었을 때, 이미 그보다 높거나 같은 높이의 빌딩은 이미 다 보고 난 뒤라는 것을 보장할 수 있음 → 그래야 이 구간을 스킵하는 게 안전함
            - 어떤 자료 구조를 사용할 것인가?
                - disjoint-set 자료 구조 사용 → 인덱스들 간의 관계를 저장
        - 슬라이드쇼
            - 자료 구조 초기화
                - `root` : a disjoint set of indexes
                - `heights` : 각 index에서의 최고 높이 저장
            - 높이 내림차순으로 빌딩 순회 - 각 빌딩에 대해 아래와 같은 동작 수행
                1. 왼쪽, 오른쪽 edge의 index 체크 
                    
                    ![Untitled](Untitled%2042.png)
                    
                    - root[left_idx] = 3 < root[right_idx] = 5
                        
                        → left_idx로부터 right_idx에 도달할 수 있다는 의미
                        
                        → left_idx의 높이를 1번 건물의 높이로 update 하고 (heights) 
                        
                        → left_idx와 right_idx의 union을 수행 (root)
                        
                    - left_idx와 right_idx(exclusive) 사이에 위치한 모든 indexes들에 대해서도 root, heights array update
                        - left_idx += 1 해서 다음 index로 이동
                        - heights[idx] = h1, root[idx] = right_idx = 5
                2. 두번째 빌딩이 들어왔을 때
                    
                    ![Untitled](Untitled%2043.png)
                    
                    - 빌딩 2의 right_idx = 4 → root[4] = 5 >  root[2] = 2
                        
                        → left_idx (x2)에서 볼 수 있는 최대 높이는 right_idx에 위치한다(???)
                        
                    - 빌딩 2의 left_idx에 대해서 root는 union(root[right_idx] 값으로 update), heights는 빌딩 2의 높이로 update
                    - 2와 4 사이의 모든 index에 대해서도 update
                        - x2에서 left_idx += 1 해서 x3으로 이동
                        
                        ![Untitled](Untitled%2044.png)
                        
                        - 이렇게 root 값이 동일한 경우 left_idx의 높이 즉 heights[3]이 이미 이전에 나온 더 높은 빌딩의 높이로 업데이트가 되었다는 뜻 → skip to the root[3] which is 5 → 5는 마지막 index 이기 때문에 iteration 그만.
                3. 세번째 빌딩이 들어왔을 때
                    
                    ![Untitled](Untitled%2045.png)
                    
                    - left_idx: 1, right_idx: 5 → root 값 비교하면 right_idx가 더 크므로, root[left_idx]를 union, heights를 h3로 update
                    - 그 사이에 있는 index 모두 update 하기 위해
                        - left_idx += 1 → 2. root[2] = 5 → 5 = root[5] → 5로 스킵, 근데 5는 마지막 index라서 iteration 종료
                4. endpoints 채우기 
                    
                    ![Untitled](Untitled%2046.png)
                    
                    - heights array 값 바뀌는 지점에서의 x_value, h를 넣어주기만 하면 된다
        - 코드 trial 1
            
            ```python
            import heapq 
            
            class Solution:
                def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                    buildings.sort(key=lambda x: x[2], reverse=True) # sort by height in descending order
            
                    # edges
                    edges = []
                    for i in range(len(buildings)):
                        left, right, height = buildings[i]
                        if left not in edges:
                            edges.append(left)
                        if right not in edges:
                            edges.append(right)
            
                    edges.sort()
                    N = len(edges)
                    
                    # iteration 
                    root = [i for i in range(N)]
                    heights = [0] * N
                    for i in range(len(buildings)):
                        left, right, height = buildings[i]
                        # better way to retrieve index?
                        left_idx, right_idx = edges.index(left), edges.index(right)
                        while left_idx < right_idx and left_idx < N: 
                            if root[left_idx] < root[right_idx]:
                                # union & update 
                                root[left_idx] = root[right_idx]
                                heights[left_idx] = height
                                left_idx += 1 
                            else:
                                # skip
                                left_idx = root[left_idx]
                    
                    # endpoints
                    endpoints = []
                    for i in range(len(heights)):
                        cur_x = edges[i]
                        cur_height = heights[i]
                        if not endpoints or endpoints[-1][1] != cur_height:
                            endpoints.append([cur_x, cur_height])
            
                    return endpoints
            ```
            
        - AC 코드
            - trial 1에서 root 부분을 union-find class instance로 수정하고, 매번 새로운 left_idx가 들어올 대마다 find 한번씩 실행하는 것으로 수정
            - 근데 속도는 좀 느리다
            
            ```python
            import heapq 
            
            class UnionFind():
                def __init__(self, N):
                    self.root = list(range(N))
                def find(self, x):
                    if self.root[x] != x:
                        self.root[x] = self.find(self.root[x])
                    return self.root[x]
                def union(self, x, y):
                    self.root[x] = self.root[y]
            
            class Solution:
                def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                    buildings.sort(key=lambda x: x[2], reverse=True) # sort by height in descending order
            
                    # edges
                    edges = []
                    for i in range(len(buildings)):
                        left, right, height = buildings[i]
                        if left not in edges:
                            edges.append(left)
                        if right not in edges:
                            edges.append(right)
            
                    edges.sort()
                    N = len(edges)
                    
                    # iteration 
                    #root = [i for i in range(N)]
                    edge_UF = UnionFind(N)
                    heights = [0] * N
                    for i in range(len(buildings)):
                        left, right, height = buildings[i]
                        # better way to retrieve index?
                        left_idx, right_idx = edges.index(left), edges.index(right)
                        while left_idx < right_idx: 
                            left_idx  = edge_UF.find(left_idx)
                            #if root[left_idx] < root[right_idx]:
                            if left_idx < right_idx:
                                # union & update 
                                #root[left_idx] = root[right_idx]
                                edge_UF.union(left_idx, right_idx)
                                heights[left_idx] = height
                                left_idx += 1 
                    
                    # endpoints
                    endpoints = []
                    for i in range(len(heights)):
                        cur_x = edges[i]
                        cur_height = heights[i]
                        if not endpoints or endpoints[-1][1] != cur_height:
                            endpoints.append([cur_x, cur_height])
            
                    return endpoints
            ```
            
        - time complexity
            - 빌딩 높이에 따라 정렬: O(nlogn)
            - n개의 빌딩에 각 2개의 edge 존재 → 빌딩 간 겹치는 부분이 하나도 없으면 최대 2n개의 position 존재
            - UF의 union method는 O(1) → 최대 2n 번 수행되면 O(n)
            - find method는 최악의 경우 O(n) 이지만, collapsing find technique를 사용하면 O(1) with repeated use
                - collapsing find method
                    - input x node로부터 root까지의 path에서 만나게 되는 각 node들의 parent reference를 바로 root로 update
                - amortize
                    - 비싼 operation의 cost를 쪼개서 여러 개의 값싼 operation의 cost에 얹는다. operation 당 평균 비용을 줄이는 방법
                - overall time complexity of O(n)
                    - 각 successful `find()` 수행이 root의 value를 바꿀 것이고, 최대 2n개가 있기 때문에 O(1) * 2n → O(n)
                
                ⇒ 정렬하는데 시간이 젤 많이 걸리므로 최종 시간 복잡도는 O(nlogn)
                
            - 그림
                
                ![Untitled](Untitled%2047.png)
                
                - 빌딩 1 처리하고 난 상태
                - left_idx, right_idx 를 빌딩 2의 edge의 것으로 update 하고 난 상태
                - `left_idx  = edge_UF.find(left_idx)`
                    - left_idx는 skip 해도 되는 구간 모두 점프하고 rightmost edge로 이동한 상태
                - 그림 1:
                    - left_idx: 빌딩 1의 right_edge로 이동한 상태
                    - 여기서부터 빌딩 2의 right_edge가 N-A개의 인덱스로 이루어져있음
                - 그림 2:
                    - 빌딩 2의 left_edge부터 빌딩 1의 left_edge-1까지 처리한 상태 (right_idx로)
                    - 빌딩 1의 left_edge로 오고나면 바로 right_edge로 skip
                    - 빌딩 1의 right_edge부터 빌딩 2의 right_edge까지의 인덱스 처리
                    - ⇒ 총 N-A개 인덱스 처리
                - 그림 3:
                    - left_idx: 이미 skip 해서 빌딩 1의 right_edge 가리킴 > 빌딩 2의 right_idx라서 아무일도 안일어나고 다음 빌딩으로 이동
                    
    - **Divide-and-Conquer**
        - 설명
            - building list를 비슷한 길이의 두 개의 sublist로 divide
            - 각 sublist들로부터 skyline를 얻는다
                - base case: 빌딩이 하나인 경우 바로 skyline을 얻는다
            - 두 개의 skyline을 하나로 합친다
                - 더 쉬운 버전의 sweep 알고리즘
            - 그림
                
                ![Untitled](Untitled%2048.png)
                
        - 슬라이드쇼
            
            ![Untitled](Untitled%2049.png)
            
            - 가장 왼쪽에 있는 endpoint L1부터 시작 → height가 0에서 h_L1로 바뀌었으므로 L1을 skyline에 추가 → 그 다음 leftmost인 L2로 이동 → 해당 x 좌표에서 높이가 h_L2로 바뀌었으므로 skyline에 추가 → L3로 이동
            - L3보다는 R1이 leftmost라서 focus 이동 → 해당 x 좌표에서 높이는 이전 h_L2랑 변동이 없어서 skyline 추가 없이 R2로 이동→ L3가 R2보다 더 왼쪽이라서 focus 이동 …
            
            ![Untitled](Untitled%2050.png)
            
            - 늘 양쪽 skyline의 높이를 비교한다. R이 L보다 먼저 오더라도, L의 높이도 같이 고려된다
            - 첫번째 그림
                - R이 많은 skyline point들을 갖고 있지만, 최종 endpoints에는 하나도 안 들어감. 왜냐면 뒤에 있는 빌딩 L의 높이가 더 높아서 가려질 것이기 때문 → merged skyline’s height는 current point’s height가 반대편보다 더 높지 않는 한 변경되지 않는다
            - 두번째 그림
                - R이 L을 뛰어 넘는 직사각형 한 부분에 대해서만 endpoint가 추가될 것
        - 코드 trial1
            
            ```python
            class Solution:
                def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                    # recursively divde the current buildings 
                    def merge(left, right):
                        endpoints = []
                        i, j = 0, 0
                        h_l, h_r = 0, 0
                        while i < len(left) and j < len(right):
                            if left[i][0] < right[j][0]:
                                cur_x = left[i][0]
                                cur_height = left[i][1]
                                if cur_height > h_r:
                                    h_l = cur_height
                                else:
                                    cur_height = h_r
                                i += 1 
                            elif left[i][0] > right[j][0]:
                                cur_x = right[j][0]
                                cur_height = right[j][1]
                                if cur_height > h_l:
                                    if not endpoints or endpoints[-1][1] != cur_height:
                                        endpoints.append([cur_x, cur_height])
                                        h_r = cur_height
                                else:
                                    cur_height = h_l
                                j += 1 
                            else: # same x value
                                if left[i][1] > right[j][1]:
                                    cur_x = left[i][0]
                                    cur_height = left[i][1]
                                    if cur_height > h_r:
                                        h_l = cur_height
                                    else:
                                        cur_height = h_r 
                                    i += 1 
                                elif left[i][1] < right[j][1]:
                                    cur_x = right[j][0]
                                    cur_height = right[j][1]
                                    if cur_height > h_l:
                                        h_r = cur_height
                                    else:
                                        cur_height = h_r
                                    j += 1 
                                else: # same height
                                    cur_x = left[i][0]
                                    cur_height = left[i][1]
                                    max_height = max(cur_height, h_l, h_r)
                                    if max_height == cur_height:
                                        h_l = cur_height
                                        h_r = cur_height
                                    elif max_height == h_l:
                                        cur_height = h_l
                                    else:
                                        cur_height = h_r
                                    i += 1 
                                    j += 1 
                                    
                            if not endpoints or endpoints[-1][1] != cur_height:
                                    endpoints.append([cur_x, cur_height])
            
                        return endpoints
                    def recur(arr):
                        # conquer
                        if len(arr) == 1:
                            left, right, height = arr[0] 
                            return [[left, height], [right, 0]]
            
                        # divide
                        mid = len(arr) // 2 
                        left = recur(arr[:mid])
                        right = recur(arr[mid:])
                        
                        # combine
                        return merge(left, right)
                    
                    return recur(buildings)
            ```
            
        - AC 코드
            - 역시 merge가 문제였고, x value가 같은 경우가 문제였다
            
            ```python
            class Solution:
                def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
                    # recursively divde the current buildings 
                    def merge(left, right):
                        endpoints = []
                        i, j = 0, 0
                        h_l, h_r = 0, 0
                        while i < len(left) and j < len(right):
                            if left[i][0] < right[j][0]:
                                h_l = left[i][1] 
                                cur_x = left[i][0]
                                cur_height = max(h_l, h_r)
                                i += 1 
                            elif left[i][0] > right[j][0]:
                                h_r = right[j][1]
                                cur_x = right[j][0]
                                cur_height = max(h_l, h_r)
                                j += 1 
                            else: # same x value
                                cur_x = left[i][0] # == right[j][0]
                                h_l, h_r = left[i][1], right[j][1]
                                cur_height = max(h_l, h_r)
                                i += 1 
                                j += 1 
                                    
                            if not endpoints or endpoints[-1][1] != cur_height:
                                    endpoints.append([cur_x, cur_height])
                        
            						# 두 줄로 대체 가능
                        while i < len(left):
                            endpoints.append(left[i])
                            i += 1 
                        while j < len(right):
                            endpoints.append(right[j])
                            j += 1 
            
                        return endpoints
                    def recur(arr):
                        # conquer
                        if len(arr) == 0:
                            return []
                        if len(arr) == 1:
                            left, right, height = arr[0] 
                            return [[left, height], [right, 0]]
            
                        # divide
                        mid = len(arr) // 2 
                        left = recur(arr[:mid])
                        right = recur(arr[mid:])
                        
                        # combine
                        return merge(left, right)
                    
                    return recur(buildings)
            ```