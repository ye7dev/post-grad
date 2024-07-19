# 210. Course Schedule II

Status: done, in progress
Theme: graph
Created time: December 28, 2023 9:53 PM
Last edited time: January 2, 2024 5:34 PM

- [ ]  복잡도 분석
- [x]  코드 개선
- AC 코드
    
    ```python
    class Solution:
        def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
            ordered = []
            courses = {}
            visited = [False] * numCourses
            num_prereq = [0] * numCourses
            for a, b in prerequisites:
                if b not in courses:
                    courses[b] = []
                courses[b].append(a)
                num_prereq[a] += 1 
    
            starting = []
            for i in range(numCourses): # zero-index
                if num_prereq[i] == 0:
                    starting.append(i)
            if len(starting) == 0:
                return ordered
    
            queue = collections.deque(starting)
            while queue:
                cur_node = queue.popleft()
                visited[cur_node] = True
                ordered.append(cur_node)
                if cur_node in courses:
                    for c in courses[cur_node]:
                        num_prereq[c] -= 1
                        if num_prereq[c] == 0:
                            queue.append(c)
            
    				if len(ordered) == numCourses:
    		        return ordered
    				else:
    						return []
    ```
    
    - cycle이 있는 경우 어떻게 처리하나 했는데,
        - 칸 알고리즘 다 돌고 나서도 topologically sorted list에 모든 노드가 들어와있지 않으면 그게 cycle이 있다는 의미 → 빈 list return 하라고 문제 써있음