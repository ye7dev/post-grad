# 332. Reconstruct Itinerary

Status: done, in progress, with help
Theme: DFS
Created time: November 15, 2023 4:29 PM
Last edited time: December 15, 2023 11:05 PM

- priority queue에서 알파벳 순서도 적용이 되나?
    - yes
        
        ```python
        >>> x = ['m', 'a', 't', 'b', 'o', 'm', 'e']
        >>> heapq.heapify(x)
        >>> x
        ['a', 'b', 'e', 'm', 'o', 'm', 't']
        ```
        
- 시행착오
    - ["JFK","ATL","ATL","JFK","SFO","ATL"]
        - ATL에서 JFK도 갈 수 있고 SFO도 갈 수 있는데
        - 알파벳 순서로 따지면 jfk가 먼저가 아닌가?
        - 아 혹시 도착지랑 출발지를 반대로 둬야 하나?
    - [['ATL', 'JFK'], ['JFK', 'SFO'], ['ATL', 'SFO']]
        - 여기서 ATL JFK pop 되고, ATL에 res에 append 되고
        - JFK로 시작하는 티켓은 이미 힙큐에 들어와 있으므로 더 append 할 것은 없음
        - 그럼 그 다음 while loop에서 힙큐의 상태는 [['ATL', 'SFO'], ['JFK', 'SFO']]
            - 여기서 다시 알파벳 순으로 pop 하니까 당연히 ATL이 빠져나옴
    - 티켓 : `[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]`
    - while loop 돌 때마다 journey를 빈 힙큐로 만들어서 예제는 통과했는데 `[["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]` 이런 건 어떻게?
        - 왜냐면 K가 N보다 알파벳 상으로는 먼저지만, KUL은 더 이상 경로가 없고
        - JKF → NRT → JFK → KUL이어야 함
- 애초에 heapq를 쓰는 게 아니었다…
- 가이드
    1. ticket을 정렬
        - reverse True → 출발지 알파벳 뒤에 나오는 순으로, 같은 출발지 일때는 도착지 알파벳이 뒤에 나오는 순서대로 저장
            
            ```python
            x = [['abc', 'bca'], ['abc', 'mcu'], ['jfk', 'atl'], ['jfk', 'cdg']]
            >>> sorted(x, reverse=True)
            [['jfk', 'cdg'], ['jfk', 'atl'], ['abc', 'mcu'], ['abc', 'bca']]
            ```
            
    2. 그래프를 만든다 
        - 사전으로. 각 sublist를 돌면서 graph[dep] = [arr1, arr2…]
        - 이 때 원래 list에서 같은 출발지 일때 목적지 알파벳이 뒤에 있는 것부터 앞으로 정렬했기 때문에
            
            → graph[출발지] 에서도 목적지 알파벳이 뒤쪽에 있는 것부터 value list에 앞쪽에 위치하게 된다 
            
            → pop을 하면 알파벳 순서상 앞에 있는 목적지부터 pop되고, route에도 추가된다 
            
    3. route = [] 생성
    4. dfs(’JFK’)
        - dfs 함수 정의
            - 출발지가 input으로 들어오면, 그에 따른 목적지가 있는 동안 graph에서 pop 하고, 다시 dfs 보냄
            - 목적지가 없는 혹은 다 떨어진 출발지가 들어온 출발지 그대로 route에 추가됨
                
                → 목적지 갈 수 있는데까지 다 간 다음에 마지막으로 출발지가 추가되는 것. 그래서 route에도 거꾸로 집어넣어야 함 
                
            - 예시
                
                ```python
                tickets= [["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]
                >>> sorted(tickets,reverse=True)
                [['NRT', 'JFK'], ['JFK', 'NRT'], ['JFK', 'KUL']]
                >>> graph
                {'NRT': ['JFK'], 'JFK': ['NRT', 'KUL']}
                dfs('JFK') 
                ```
                
                | key | dfs input | route |
                | --- | --- | --- |
                | JFK | JFK |  |
                |  | KUL | [KUL] |
                |  | NRT |  |
                |  | JFK | [KUL, JFK] |
                |  |  | [KUL, JFK, NRT] |
                |  |  | [KUL, JFK, NRT, JFK] |
                
                → route 뒤집으면 [JFK, NRT, JFK, KUL] 
                
                - 위의 예시에서 [JFK, ATL]을 추가하면 ['JFK', 'NRT', 'JFK', 'KUL', 'ATL']로 나온다
                    - 그러니까 결국 가능한 route를 한번씩 다 돌면서 모든 여정을 하나의 string으로 붙였을 때 가장 알파벳 순으로 빠른 걸 구하는 거다
                    - 그래서 ATL이 두번째로 나올 수 없는 이유가 JFK-ATL을 먼저 돌았다가는 다음 목적지로 이어지지 않아서 가능한 티켓을 모두 한번씩 사용할 수 없기 때문이다
    5. return route[::-1] 
        - 뒤집어서 return
- 코드
    
    ```python
    from collections import defaultdict
    class Solution:
        def findItinerary(self, tickets: List[List[str]]) -> List[str]:
            graph = defaultdict(list)
            route = []
    
            for dep, arr in sorted(tickets, reverse=True):
                graph[dep].append(arr)
            
            def dfs(a):
                while graph[a]:
                    dfs(graph[a].pop())
                route.append(a)
    
            dfs('JFK')
            return route[::-1]
    ```
    
- DFS로 재방문
    - 여기까지 짜보았는데 18/81
        
        ```python
        class Solution:
            def findItinerary(self, tickets: List[List[str]]) -> List[str]:
                graph = collections.defaultdict(list)
                itinerary = ['JFK']
                visited = {}
                for s, e in tickets:
                    graph[s].append([e, False])
                for key in graph:
                    graph[key].sort()
                
                def dfs(node):
                    if not graph[node]:
                        return 
                    complete = sum([x[1] for x in graph[node]])
                    if complete == len(graph[node]):
                        return 
                    for neighbor in graph[node]:
                        if neighbor[1] is False:
                            itinerary.append(neighbor[0])
                            neighbor[1] = True
                            dfs(neighbor[0])
                            
        
                dfs("JFK")
                return itinerary
        ```
        
    - DFS로 AC 받으려면 이렇게 했어야 (chat gpt helped)
        
        ```python
        from collections import defaultdict
        
        class Solution:
            def findItinerary(self, tickets: List[List[str]]) -> List[str]:
                graph = defaultdict(list)
        
                # Create a graph, each edge is unique
                for start, end in sorted(tickets, reverse=True):
                    graph[start].append(end)
        
                itinerary = []
        
                def dfs(airport):
                    while graph[airport]: 
                        next_airport = graph[airport].pop()
                        dfs(next_airport)
                    itinerary.append(airport) # post order DFS
        
                dfs('JFK')
                return itinerary[::-1]  # reverse to get the correct order
        
        # Example usage
        solution = Solution()
        tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
        print(solution.findItinerary(tickets))
        ```
        
        - why `itinerary[::-1]` ?
            - JFK → ATL, ATL → SFO,  SFO → LAX 라고 하면
            - JKF input → ABC가 먼저 Pop 되고, dfs(ABC) → dfs(SFO) → dfs(LAX)
            - LAX는 더 갈 곳이 없으니까 itinerary에 추가되고 [LAX]
            - SFO도 LAX 말고 더 갈 곳이 없으니까 itinerary에 추가되고 [LAX, SFO]
            - ATL도 SFO 말고 더 갈 곳이 없으니까 itinerary에 추가되고 [LAX, SFO, ATL]
            - JFK도 ATL 말고 더 갈 곳이 없으니까 itinerary에 추가되면 [LAX, SFO, ATL, JFK]
            
            ⇒ 이래서 reverse를 마지막에 해줘야 한다 
            
        
        🥊 근데 아래와 같은 예시에서는 우리의 직관과 반대인 답이 나와버린다 - 근데 뭐 그게 솔루션이라고 하니까..
        
        ```python
        solution = Solution()
        tickets = [["JFK", "MUC"],["JFK", "ATM"], ["JFK", "SFO"]]
        print(solution.findItinerary(tickets)) # ['JFK', 'SFO', 'MUC', 'ATM']
        ```
        
    - heapq 쓰면 더 빨라진다
        
        ```python
        from collections import defaultdict
        from heapq import heappush, heappop
        
        class Solution:
            def findItinerary(self, tickets):
                # Create a graph using a dictionary of priority queues (min-heaps)
                flights = defaultdict(list)
                for departure, arrival in tickets:
                    heappush(flights[departure], arrival)
        
                path = []
                
                def dfs(departure):
                    arrivals = flights[departure]
                    while arrivals:
                        # Pop the next destination from the min-heap
                        next_destination = heappop(arrivals)
                        dfs(next_destination)
                    path.append(departure)
        
                # Start DFS from 'JFK'
                dfs("JFK")
                return path[::-1]
        ```