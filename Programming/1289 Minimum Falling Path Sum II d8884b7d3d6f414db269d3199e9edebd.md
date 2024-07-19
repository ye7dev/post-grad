# 1289. Minimum Falling Path Sum II

Status: done, in progress
Theme: DP
Created time: March 15, 2024 4:12 PM
Last edited time: March 15, 2024 4:57 PM

- AC 코드
    - Top-down(🪇🐌)
        
        ```python
        class Solution:
            def minFallingPathSum(self, grid: List[List[int]]) -> int:
                nrows, ncols = len(grid), len(grid[0])
                memo = {}
                def recur(r, c):
                    # check memo
                    if (r, c) in memo:
                        return memo[(r, c)]
                    # check base case
                    if r == nrows-1:
                        return grid[r][c]
                    # recursive case 
                    min_sum = float('inf')
                    for i in range(ncols):
                        if i == c:
                            continue 
                        min_sum = min(min_sum, recur(r+1, i))
        
                    memo[(r, c)] = min_sum + grid[r][c]
                    return memo[(r, c)]
                
                ans = float('inf')
                for c in range(ncols):
                    ans = min(ans, recur(0, c))
                return ans
                    
        ```
        
    - Bottom-up(🪇🐢)
        
        ```python
        class Solution:
            def minFallingPathSum(self, grid: List[List[int]]) -> int:
                nrows, ncols = len(grid), len(grid[0])
                dp = [[float('inf')] * ncols for _ in range(nrows)]
        
                # base case: r == 0
                for c in range(ncols):
                    dp[0][c] = grid[0][c]
        
                # iterative relation 
                for r in range(1, nrows):
                    for c in range(ncols):
                        cur_val = grid[r][c]
                        for prev_c in range(ncols):
                            if c == prev_c:
                                continue
                            dp[r][c] = min(dp[r][c], cur_val + dp[r-1][prev_c])
                            
                return min(dp[nrows-1])
        ```
        
    - Bottom-up(Editorial, ⚡️)
        - heapq를 사용해서 바로 윗 열에서 최소 값 두 개 뽑는다
            - 더 앞에 있는게 더 작은 값
        - 현재 row의 모든 열을 돌면서 같은 열, 이전 row 값이 더 작은 값이면,
            - 위에서 나온 두 개 중 더 큰 쪽을 현재 값에 더한다
        - 첫번째 열은 자기 자신 그대로 사용하면 되고
        - 두번째 열부터는 앞선 열들의 값을 누적해서 갖게 된다
        
        ```python
        import heapq
        class Solution:
            def minFallingPathSum(self, grid: List[List[int]]) -> int:
                nrows, ncols = len(grid), len(grid[0])
        
                # iterative relation 
                for r in range(1, nrows):
                    # former two candidates
                    c1, c2 = heapq.nsmallest(2, grid[r-1])
                    for c in range(ncols):
                        # if current row is the same as the previous row 
                        if c1 == grid[r-1][c]:
                            grid[r][c] += c2 
                        else:
                            grid[r][c] += c1
                            
                return min(grid[nrows-1])
        ```
        
    - Bottom-up(별도 dp 공간 사용)
        
        ```python
        import heapq
        class Solution:
            def minFallingPathSum(self, grid: List[List[int]]) -> int:
                nrows, ncols = len(grid), len(grid[0])
                dp = [[float('inf')] * ncols for _ in range(nrows)]
        
                # base case
                for c in range(ncols):
                    dp[0][c] = grid[0][c]
                # iterative relation 
                for r in range(1, nrows):
                    # previous candidates
                    c1, c2 = heapq.nsmallest(2, dp[r-1])
                    for c in range(ncols):
                        # if current row is the same as the previous row 
                        if c1 == dp[r-1][c]:
                            dp[r][c] = grid[r][c] + c2 
                        else:
                            dp[r][c] = grid[r][c] + c1
                            
                return min(dp[nrows-1])
        ```