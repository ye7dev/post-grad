# 269. Alien Dictionary

Status: in progress
Theme: graph
Created time: December 30, 2023 2:42 PM
Last edited time: January 8, 2024 4:18 PM

- [ ]  복잡도 분석
- [ ]  khan’s algorithm(BFS)로 쫙 풀어보기
- [ ]  DFS로 쫙 풀어보기
- 문제 이해
    
    input: a list of strings 
    
    이 string들이 새 언어의 알파벳 순으로 정렬된 상태라고 한다?
    
    이 주장이 틀렸고 words에 있는 string의 순서가 어떤 letter에도 상응되지 않으면 return “” 
    
    그렇지 않으면 unique letter들을 연결한 string을 return 해라 
    
    이 unique letter들은 lexicographically increasing order로 정렬된 상태 
    
    하나의 단어 안에서 정렬된 상태는 아님
    
    ["wrt","wrtkj"] 이 경우 w → r → t도 맞는 건가? 아님 t → k 만 valid? 
    
- topological sorting에서는 큐를 사용한다
    - 왜냐면 먼저 in-degree가 0이 된 노드부터 처리해야 하기 때문에
    - 선입선출 개념이 필요한 모든 경우에 큐를 사용한다
- Editorial
    - Overview
        - 하나의 단어 안에서 문자 배열은 상대적인 순서랑 전혀 관련 없음
            - 단어가 kite라고 해서 i가 k보다 먼저 온다는 법은 없음
        - prefix인 단어가 리스트 상에서 더 뒤에 올 수도 있음
            - abcd가 먼저 오고 ab가 다음에 오는 경우 → invalid한 case이므로 코드에서 잡아낼 수 있어야 함.
            - valid case에서는 ab(prefix)가 늘 그것을 포함한 단어(abcd)보다 앞에 와야 함
        - valid한 case가 하나 이상일 수 있음
        - 문제를 세 단계로 난루 수 있음
            1. input에서 dependency rule (뭐가 뭐보다 앞에 와야 하는지) 추출 
            2. dependency rule을 그래프(adj_list)에 넣는다 (letter → node, dependency → edge) 
            3. topologically sorting the graph node 
    - BFS (Khan’s algorithm)
        - Extracting Information → a set of pair order
            - 각 단어의 첫번째 letter를 모아서 중복 제거
            - 첫번째 letter가 같은 경우, 두번째 letter 순서에 따라 정렬
                - wxqkj, whgg 이면, w가 같기 때문에 x가 h보다 빨리 온다는 것을 알 수 있음
                - 세번째 letter부터는 relative ordering에 아무 영향을 주지 않는다
            - 확실하게 알 수 있는 순서들끼리 모아서 fragment를 만듦(?)
                
                ![Untitled](Untitled%2074.png)
                
            
            ⇒ 두 단어가 나란히 있는 경우, first difference between them을 봐야 함 → 이 difference가 두 letters 사이의 relative order를 알려줌 
            
        - Assembling a Valid Ordering
            - prerequisite이 없는 letter들부터 최종 순서에 넣는다
                - 아마 여기서 variation이 생길 수 있는 것 같음
                - 각자로 존재하는 애들은 뭐가 먼저 오던 상관 없기 때문에
            - 위의 letter들을 선행조건으로 갖는 애들은 이제 선행 조건이 충족된 상태 → 이 상태에서 다시 prerequisite이 없어진 애들이 누군지 보고, 얘네를 다시 최종 순서에 넣는다 (여기서도 variation 생길 수 있음)
        - Code
            
            ```python
            from collections import defaultdict, Counter, deque
            
            def alienOrder(self, words: List[str]) -> str:
                
                # Step 0: create data structures + the in_degree of each unique letter to 0.
                adj_list = defaultdict(set)
                in_degree = Counter({c : 0 for word in words for c in word})
                        
                # Step 1: We need to populate adj_list and in_degree.
                # For each pair of adjacent words...
                for first_word, second_word in zip(words, words[1:]):
                    for c, d in zip(first_word, second_word):
                        if c != d:
                            if d not in adj_list[c]:
                                adj_list[c].add(d)
                                in_degree[d] += 1
                            break
                    else: # Check that second word isn't a prefix of first word.
                        if len(second_word) < len(first_word): return ""
                
                # Step 2: We need to repeatedly pick off nodes with an indegree of 0.
                output = []
                queue = deque([c for c in in_degree if in_degree[c] == 0])
                while queue:
                    c = queue.popleft()
                    output.append(c)
                    for d in adj_list[c]:
                        in_degree[d] -= 1
                        if in_degree[d] == 0:
                            queue.append(d)
                            
                # If not all letters are in output, that means there was a cycle and so
                # no valid ordering. Return "" as per the problem description.
                if len(output) < len(in_degree):
                    return ""
                # Otherwise, convert the ordering we found into a string and return it.
                return "".join(output)
            ```
            
        - 복잡도 분석
            - N: input list에 있는 단어 개수
            - C: input list 에 있는 단어를 모두 하나로 합쳤을 때, 그 단어의 길이-전체 letter 수
            - U: alien alphabet에 있는 unique letter의 개수. 문제 서술에서 26개로 제한된다고 줬지만, 만약 이런 제약이 없는 경우 시간복잡도에 어떻게 영향을 주는지 알 수 있어야
            - 시간: O(C)
                - 알고리즘 세 가지 파트 요약: 1) 관계 파악 2) adj_list에 넣기 3) valid ordering
                - 최악의 경우 1), 2)는 모든 단어의 모든 letter를 확인해야 할 수도 (연속된 두 단어의 차이가 맨 마지막 letter에서만 확인되는 경우)
                - 3) BFS cost : O(V+E)
                    - 그럼 우리 문제에서의 노드 수, edge 수는 무엇?
                    - 노드 수: C에서 unique letter 수 → maximum의 U → O(U)
                    - edge 수
                        - 각 edge는 두 개의 연속된 단어를 비교하는 과정에서 생성됨
                            - N개의 단어가 있을 때, adjacent pair는 N-1개
                            - 각 pair에서 생성될 수 있는 edge는 한개 (first difference from first word → first difference from second word)
                            
                            → N-1개의 edge 생성 가능 
                            
                        - each pair of nodes 사이에서 하나 이상의 edge가 나올 순 없음. upper bound으로 U개의 node가 존재할 때, U^(U-1) /2 $(uC2)$개의 pair가 나올 수 있음
                        
                        ⇒ N-1 vs U^2 두 개의 upper bound 중에 더 작은 것을 선택 
                        
                    
                    ⇒ O(V+E) = O(U + min(N-1, U^2)) = O(U + min(N, U^2))
                    
                - 1), 2), 3)을 다 합치면 O(C + U + min(U^2, N))
                    - N < C (각 단어가 최소 한개의 문자로 이루어져있으므로, 단어 개수 < 전체 Letter 개수)
                    - U < C (C에서 중복제거한 게 U일테니)
                        
                        → O(C + U + min(U^2, N)) ⇒ O(C + min(U^2, N)) 
                        
                    - U^2 < N 이면 min(U^2, N) = U^2
                        
                        → O(C + min(U^2, N)) → O(C + U^2)) 
                        
                        U^2 < N < C ⇒ O(C)  
                        
                    - U^2 > N 이면 min(U^2, N) = N
                        
                        N < C ⇒ O(C) 
                        
                    
                    ⇒ 모든 경우에서 C > min(U^2, N) → O(C) 
                    
            - 공간: O(1) or O(U + min(U^2, N))
                - adj list → O(V+E)
                    - node 개수: U
                    - edge 개수: min(U^2, N)
                    
                    ⇒ O(V+E) = O(U + min(U^2, N))
                    
                - 만약 U가 26으로 고정이라고 하면,
                    - O(U) = O(1)
                    - min(26^2, N) = 26^2  → O(26^2) = 1
                    
                    ⇒ O(V+E) = O(1) 
                    
    - DFS
        - Intuition
            - in_degrees map 사용 안함
            - DFS 특성
                - 더 전진할 링크가 남아 있지 않거나, 모든 outgoing link가 방문된 상태면 returned
                
                → node가 return되는 순서는 reverse of a valid alphabet order
                
        - 알고리즘
            - reverse adj_list를 만든다
                - incoming edge가 없는 노드(선행 조건이 없는 노드)는 outgoing edge가 없는 노드가 된다
                
                → start of the alphabet이 가장 먼저 return 될 것 
                
            - cycle 주의
                - directed graph에서는 그래프 색칠하는 방법으로 사이클 감지
                    - 노드가 흰색 ⇒ 방문 하고 나서는 회색 ⇒ 이웃들까지 모두 방문되면 검은 색
                    - 현재 회색인 노드에 enter 하면 cycle이 있는 것
                        - stack에 들어 있는 노드들은 회색이고, 들어갔다가 나온 애들은 모두 검은색이다
            - BFS에서는 선행조건이 없는 노드들부터 먼저 처리하지만(그 노드들에게서 나온 다음 탐색 노드들은 큐의 마지막에 추가되는데, BFS에서는 First in First out 이라서 앞에서 선행조건이 없어서 추가된 노드들보다 늦게 처리된다
            - DFS에서는 선행조건이 없는 노드들이 먼저 stack에 들어가더라도, 첫번째로 추출된 노드의 자식들이 큐에 마지막에 추가되었다면, 그 자식들이 먼저 탐색된다 → 그 노드들로부터 자식과 손자 등등 끝까지 갈 수 있는 만큼 간 다음 → 쭉 return 하면서 올라와서 그제서야 선행조건이 없는 두번째 노드를 탐색하게 되는 것
        - Trial
            - 근데 여기서 어떻게 x 다음에 h로 넘어가지?
                
                ![Untitled](Untitled%2075.png)
                
            - 예제 하나만 통과
                
                ```python
                class Solution:
                    def alienOrder(self, words: List[str]) -> str:
                        # extract information 
                        pair_set = set()
                        letter_set = Counter({c:0 for word in words for c in word})
                        for first_word, second_word in zip(words, words[1:]):
                            for c, d in zip(first_word, second_word):
                                if c != d:
                                    pair_set.add((c, d))
                                    break
                            else:
                                if len(first_word) > len(second_word):
                                    return ""
                                # ? case: the first word is the prefix of the second word
                        
                        # create a graph
                        graph = {}
                        for a, b in pair_set:
                            if b not in graph:
                                graph[b] = []
                            graph[b].append(a)
                        
                        stack = [l for l in letter_set if l not in graph]
                        
                        # dfs
                        color = {l:'w' for l in letter_set}
                        for l in stack:
                            color[l] = 'g'
                        order = []
                
                        while stack:
                            cur_node = stack.pop()
                            color[cur_node] = 'b' # marking on pop 
                            added = False
                            for key in graph:
                                if cur_node in graph[key]:
                                    graph[key].remove(cur_node)
                                    if len(graph[key]) == 0:
                                        stack.append(key)
                                        color[key] = 'g'
                                        added = True
                            if not added:
                                order.append(cur_node)
                
                        for node in color:
                            if color[node] != 'b':
                                return ""
                                
                        return "".join(order)
                ```
                
            - 헷갈렸던 점
                - 각 단어의 제일 첫번째 letter에 대해 뭘 할 필요는 없다
                - pair set → graph 따로 단계로 하지 말고, pair 만날 때마다 바로 그래프 때려버림
                - # ? case: the first word is the prefix of the second word
                    - 따로 할 일 없다
                - reversed adj list 에서 Key는 후행 조건, value는 선행 조건
                - DFS 코드
                    - 어떤 노드가 이미 까만색이면 방문이 완료되었으므로 상위 단계로 return True→ 그 다음 이웃 노드를 탐색하겠지? (for loop에서 이번 node에서는 early exit 없이 넘어갔기 때문에)
                    - 어떤 노드가 흰색이면 아직 방문한 적이 없으므로
                        - 회색으로 표시하고 그 이웃들을 탐방
                        - 이웃 한 명씩 끝까지 잡아 족친다
                        - 만약 중간에 False가 나오는 경우가 있으면 early exit
                        - early exit 없이 모든 이웃을 다 족쳤으면 검은색으로 처리하고, 최종 결과값에도 추가한 뒤  return True
                    - 어떤 노드가 회색이면, 그 이웃 노드의 후손들을 끝까지 간다 진행 중인 것
                        - 근데 이번에 pop된 노드가 회색이다? 이웃 노드 후손을 따라 가다가다 보니 다시 원 노드가 나온 것 → cycle → return False 하는 유일한 경우
                    - 주어진 그래프를 따라서 탐색을 쭉 할 때 그래프의 노드 각각을 다 방문할 수 있으면 성공-순회한 순서대로 최종 결과 담아둔 list를 Join 해서 return
- 집념의 AC 코드 (느리고 untidy 하지만…!)
    
    ```python
    class Solution:
        def alienOrder(self, words: List[str]) -> str:
            letter_set = set("".join(words))
            graph = {}
            num_prereq = {}
            for i in range(len(words)):
                if words[i][0] not in graph:
                    graph[words[i][0]] = []
                for j in range(i+1, len(words)):
                    if words[j][0] == words[i][0]:
                        continue
                    if words[j][0] not in graph[words[i][0]]:
                        graph[words[i][0]].append(words[j][0])
                        if words[j][0] not in num_prereq:
                            num_prereq[words[j][0]] = 0
                        num_prereq[words[j][0]] += 1 
            
            for idx in range(len(words)-1):
                cur_word, next_word = words[idx], words[idx+1]
                cur_len, next_len = len(cur_word), len(next_word)
                i, j = 0, 0
                while i < cur_len and j < next_len:
                    if cur_word[i] != next_word[j]:
                        break
                    i += 1
                    j += 1
                if i == cur_len and j == next_len: # same 
                    continue
                if i < cur_len and j == next_len: # prefix 
                    return ""
                if i == cur_len: 
                    i -= 1 
    
                if cur_word[i] not in graph:
                    graph[cur_word[i]] = []
                graph[cur_word[i]].append(next_word[j])
                if next_word[j] not in num_prereq:
                    num_prereq[next_word[j]] = 0
                num_prereq[next_word[j]] += 1 
    
            start = []
            for l in letter_set:
                if l not in num_prereq:
                    start.append(l)
    
            queue = collections.deque(start)
            ordered = []
            while queue:
                cur_node = queue.popleft()
                ordered.append(cur_node)
                if cur_node in graph:
                    for child in graph[cur_node]:
                        num_prereq[child] -= 1
                        if num_prereq[child] == 0:
                            queue.append(child)
                        
            if len(ordered) == len(letter_set):
                return "".join(ordered)
            else:
                return ""
    ```
    
- Review
    - BFS
        - trial 1
            - 예제 2/3
                
                ```python
                class Solution:
                    def alienOrder(self, words: List[str]) -> str:
                        letter_set = set([c for word in words for c in word])
                        graph = {c:set() for c in letter_set}
                        in_degree = {c:0 for c in letter_set}
                        # extract information & save to graph
                        for first, second in zip(words, words[1:]):
                            for c, d in zip(first, second):
                                if c != d:
                                    if d not in graph[c]:
                                        graph[c].add(d)
                                        in_degree[d] += 1 
                            else:
                                # edge case: prefix comes latter
                                if len(first) > len(second): 
                                    return ""
                        
                        # order
                        order = []
                        start = [c for c in in_degree if in_degree[c] == 0]
                        queue = collections.deque(start)
                        while queue:
                            cur_node = queue.popleft()
                            order.append(cur_node)
                            for child in graph[cur_node]:
                                in_degree[child] -= 1 
                                queue.append(child)
                 
                        # check output
                        if len(order) == len(letter_set):
                            return "".join(order)
                        else:
                            return ""
                ```
                
            
        - revisited points
            - 두 개의 consecutive words에 대해, first difference만 기록하고 넘어가야 한다. break 필수
            - cur_node의 child에 대해, in_degree 하나 빼준 다음, 그 때의 in_degree가 0일 때만 큐에 child를 추가해준다! (제일 중요한 조항을 실수로 누락해서는 아니되오🧙🏻)
            - 큐에서 나온 char이 이미 order에 들어 있는지는 안봐도 되나?
                - 예를 들어 c의 선결조건이 a, b 두 개인 경우
                - a에 대해 child로서 c를 한번 방문하긴 하지만, in_degree가 0이 아니기 때문에 이때는 큐에 append 되지 않는다
                - 즉 선결조건이 여러 개더라도, 마지막 선결조건이 해소되는 순간에서만 큐에 추가 되기 때문에, 두 번 추가될 일은 없다 (아마도…?)
        - AC code
            
            ```python
            class Solution:
                def alienOrder(self, words: List[str]) -> str:
                    letter_set = set([c for word in words for c in word])
                    graph = {c:set() for c in letter_set}
                    in_degree = {c:0 for c in letter_set}
                    # extract information & save to graph
                    for first, second in zip(words, words[1:]):
                        for c, d in zip(first, second):
                            if c != d:
                                if d not in graph[c]:
                                    graph[c].add(d)
                                    in_degree[d] += 1 
                                break 
                        else:
                            # edge case: prefix comes latter
                            if len(first) > len(second): 
                                return ""
                    
                    # order
                    order = []
                    start = [c for c in in_degree if in_degree[c] == 0]
                    queue = collections.deque(start)
                    while queue:
                        cur_node = queue.popleft()
                        order.append(cur_node)
                        for child in graph[cur_node]:
                            in_degree[child] -= 1 
                            if in_degree[child] == 0:
                                queue.append(child)
             
                    # check output
                    if len(order) == len(letter_set):
                        return "".join(order)
                    else:
                        return ""
            ```
            
        
    - DFS
        - trial 1
            - DFS 코드가 기억이 안남
                
                ```python
                class Solution:
                    def alienOrder(self, words: List[str]) -> str:
                        letter_set = set([c for word in words for c in word])
                        graph = {c:set() for c in letter_set}
                        # extract information & save to graph
                        for first, second in zip(words, words[1:]):
                            for c, d in zip(first, second):
                                if c != d:
                                    if c not in graph[d]: # reverse adj list 
                                        graph[d].add(c)
                                    break 
                            else:
                                # edge case: prefix comes latter
                                if len(first) > len(second): 
                                    return ""
                        
                        # order
                        color = {} # False for gray, True for black
                        order = []
                
                        def dfs(node):
                            if node in color:
                                return color[node]
                            
                            color[node] = False
                            for parent in graph[node]:
                
                                res = dfs()
                                
                            
                
                            color[node] = True
                
                 
                        # check output
                        if len(order) == len(letter_set):
                            return "".join(order)
                        else:
                            return ""
                ```
                
            
        - trial 2
            
            ```python
            class Solution:
                def alienOrder(self, words: List[str]) -> str:
                    letter_set = set([c for word in words for c in word])
                    graph = {c:set() for c in letter_set}
                    # extract information & save to graph
                    for first, second in zip(words, words[1:]):
                        for c, d in zip(first, second):
                            if c != d:
                                if c not in graph[d]: # reverse adj list 
                                    graph[d].add(c)
                                break 
                        else:
                            # edge case: prefix comes latter
                            if len(first) > len(second): 
                                return ""
                    
                    # order
                    visited = {c:'yet' for c in letter_set} # False for gray, True for black
                    order = []
            
                    def dfs(node):
                        # base case 
                        if visited[node] == 'ongoing':
                            return False # cycle 
                        elif visited[node] == 'done':
                            return True 
                        
                        visited[node] = 'ongoing'
                        for prereq in graph[node]:
                            if dfs(prereq) is False:
                                return False
                        
                        visited[node] = 'done'
                        order.append(node)
            
                    # iterate over all the nodes
                    for l in graph:
                        if not dfs(l):
                            return ""
                            
                    return "".join(order)
            ```
            
        - revisited points
            - 왜 reverse adj list는 value 자료 구조가 set이 아니고 list인가? 중복 값이 들어가도 되는 이유?
                - 왜냐면 일단 한번 탐색이 완료된 상태면, 늘 True로 return 될 것이니까. 사실상 color에  저장해놓은 탐색 여부 결과를 가져오기만 하면 돼서 어렵지 않다
            - dfs 에서는 시작 노드를 따로 먼저 구해놓지 않는다-아무 노드나 시작
            - dfs 코드 하는 일
                1. 노드 탐색 여부 확인-탐색 중이거나 탐색 완료된 노드면 그 상태를 return
                2. 만약 탐색이 한 번도 안 된 노드면 탐색 시작 - 탐색 중이라는 상태 마킹
                3. 노드의 선행 조건들을 돌면서 (reverse adj list 니까) 탐색 여부 체크 
                    - 만약 탐색 중인 노드이면 cycle이 있다는 거니까 return False
                        
                        ↳ 실제로 dfs 코드가 사용되는 맥락은 이렇다: 모든 노드를 돌면서 하나라도 False가 나오면 그대로 return “” 
                        
                        ↳ 따라서 dfs 함수 내에서 cycle을 발견했다고 해도 바로 return “” 하지 않고 False를 내보내야 맥락에 맞다 
                        
                    - 노드가 탐색이 안되었다가 탐색을 완료한 상태거나 혹은 이미 탐색을 완료한 상태면 return True → 다음 선행 조건으로(for loop 이어서) 진행
                4. 선행 조건이 모두 True로 나왔다면 현재 노드도 실행할 수 있다는 의미
                    1. 탐색 완료 표시 
                    2. output에 추가 
                    3. return True 
        - AC 코드
            
            ```python
            class Solution:
                def alienOrder(self, words: List[str]) -> str:
                    letter_set = set([c for word in words for c in word])
                    graph = {c:set() for c in letter_set}
                    # extract information & save to graph
                    for first, second in zip(words, words[1:]):
                        for c, d in zip(first, second):
                            if c != d:
                                if c not in graph[d]: # reverse adj list 
                                    graph[d].add(c)
                                break 
                        else:
                            # edge case: prefix comes latter
                            if len(first) > len(second): 
                                return ""
                    
                    # order
                    visited = {c:'yet' for c in letter_set} # False for gray, True for black
                    order = []
            
                    def dfs(node):
                        # base case 
                        if visited[node] == 'ongoing':
                            return False # cycle 
                        elif visited[node] == 'done':
                            return True 
                        
                        visited[node] = 'ongoing'
                        for prereq in graph[node]:
                            if dfs(prereq) is False:
                                return False
                        
                        visited[node] = 'done'
                        order.append(node)
                        return True 
            
                    # iterate over all the nodes
                    for l in graph:
                        if not dfs(l):
                            return ""
            
                    return "".join(order)
            ```