# 329. Longest Increasing Path in a Matrix

Status: done, in progress
Theme: DP
Created time: February 22, 2024 6:38 PM
Last edited time: February 25, 2024 7:24 AM

- 문제 이해
    - 이동 가능한 방향은 위아래좌우 총 4개
    - top-left → right-bottom이 아니다. 각 cell이 모두 start cell이 될 수 있음
- Trial
    - Top-bottom (maximum recursion depth error)
        
        ```python
        from collections import deque
        class Solution:
            def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
                m, n = len(matrix), len(matrix[0])
                memo = {}
                max_val = 0
                for i in range(m):
                    for j in range(n):
                        max_val = max(max_val, matrix[i][j])
        
                # function
                def recur(r, c):
                    # check memo
                    if (r, c) in memo:
                        return memo[(r, c)]
                    # base case
                    if matrix[r][c] == max_val:
                        return 1 
                    # recurrence relation 
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    temp = 0
                    for d in directions:
                        new_r, new_c = r+d[0], r+d[1]
                        if 0 <= new_r < m and 0 <= new_c < n:
                            if matrix[new_r][new_c] > matrix[r][c]:
                                temp = max(recur(new_r, new_c), temp)
                    memo[(r, c)] = temp+1 
                    return memo[(r, c)]
        
                for i in range(m):
                    for j in range(n):
                        recur(i, j)
                
                return max(memo.values())
        ```
        
- 과정
    - base case hit 하지 않는 중간 단계에서 서로가 서로를 호출하는 일이 발생
        - `Usually, in DFS or BFS, we can employ a set visited to prevent the cells from duplicate visits. We will introduce a better algorithm based on this in the next section." but I did not find which part in the article explains why we don't have to maintain such a visited set. My guess is because the path is increasing, we will never visit a node with smaller value.`
- AC 코드
    - Bottom-up
        
        ```python
        from collections import deque
        class Solution:
            def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
                m, n = len(matrix), len(matrix[0])
                memo = {}
                max_val = 0
                for i in range(m):
                    for j in range(n):
                        max_val = max(max_val, matrix[i][j])
        
                # function
                def recur(r, c):
                    # check memo
                    if (r, c) in memo:
                        return memo[(r, c)]
                    # base case
                    if matrix[r][c] == max_val:
                        return 1 
                    # recurrence relation 
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                    temp = 0
                    for d in directions:
                        new_r, new_c = r+d[0], c+d[1]
                        if 0 <= new_r < m and 0 <= new_c < n:
                            if matrix[new_r][new_c] > matrix[r][c]:
                                temp = max(recur(new_r, new_c), temp)
                    memo[(r, c)] = temp+1 
                    return memo[(r, c)]
        
                ans = 0
                for i in range(m):
                    for j in range(n):
                        ans = max(ans, recur(i, j))
                
                return ans
        ```