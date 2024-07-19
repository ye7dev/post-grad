# 1136. Parallel Courses

Status: in progress
Theme: graph
Created time: January 2, 2024 5:35 PM
Last edited time: January 2, 2024 9:50 PM

- [ ]  복잡도 분석
- 문제 이해
    
    직전 학기에 선수과목이 완료된 과목에 대해서는 이번 학기에 개수 제한 없이 들을 수 있음 
    
    모든 과목을 끝내기 위해 필요한 학기 수를 구해라. 만약 모든 과목을 듣는 게 불가능하다면-아마도 cycle detection- -1 return 
    
- AC 코드 🪇(심지어 빠르기까지 후후)
    
    ```python
    class Solution:
        def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
            graph = {i:[] for i in range(1, n+1)}
            in_degree = {i:0 for i in range(1, n+1)}
            for prev_course, next_course in relations:
                graph[prev_course].append(next_course)
                in_degree[next_course] += 1 
            
            num_semester = 0
            start = [c for c in range(1, n) if in_degree[c] == 0]
            taken = 0
            queue = collections.deque(start)
            while queue:
                num_courses = len(queue)
                taken += num_courses
                for _ in range(num_courses):
                    cur_course = queue.popleft()
                    for neighbor in graph[cur_course]:
                        in_degree[neighbor] -= 1 
                        if in_degree[neighbor] == 0:
                            queue.append(neighbor)
                
                num_semester += 1
            
            if taken == n:
                return num_semester
            else:
                return -1
    ```