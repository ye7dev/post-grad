# 5686. [Professional] 게임

Created time: May 10, 2024 3:08 PM
Last edited time: May 13, 2024 2:36 PM

- 답을 볼 수 없는 문제인데 과연 풀 수 있을까…? 1시간 해보고 안되면 GG 하자
- scratch
    - 모든 칸을 돌면서 합을 구하고 그 중 최대 합을 구해보자
    - 근데 댓글에는 DP 풀었는데 시간 초과 나왔다고 함;; DP로도 시간 초과면…?
    - 아님 전체 매트릭스 합에서 각 칸을 선택할 때의 마이너스 값을 dict에 저장해볼까
    - 매트릭스는 최대 10**5 크기인데 4초 안에 문제를 풀어야 함
    - dp로 푼다고 하면 현재 cell에 올 수 있게 만드는 다른 cell들의 위치를 찾아보는 것?
    - backtracking
- 문제가 어려우니 backtracking으로 구현해보고 안되면 GG 하고 다음 문제 넘어가자. backtracking으로 어떻게 4초 안에 푸니!
- Trial
    - DFS-예제도 오답이 나와서 왜 그런가 했더니 base case에서 backtrack 처리를 안해줘서 그런것
        
        ```sql
        import sys
        sys.stdin = open('temp_input/sample_input.txt')
        
        def dfs(x, y, num_visited, acc_sum, allowed):
            
            if num_visited == M * N:
                return acc_sum
        
            cur_sum, cur_visited = 0, 0
            cur_sum += matrix[x][y]
            cur_visited += 1
            allowed[x][y] = 2
            upper, lower, left, right = 0, 0, 0, 0
            if x - 1 >= 0:
                cur_visited += M
                for j in range(M):
                    allowed[x-1][j] = 0
                upper = 1
            if x + 1 < N:
                cur_visited += M
                for j in range(M):
                    allowed[x+1][j] = 0
                lower = 1
            if y - 1 >= 0:
                cur_visited += 1
                allowed[x][y-1] = 0
                left = 1
            if y + 1 < M:
                cur_visited += 1
                allowed[x][y+1] = 0
                right = 1
        
            temp = -1
            for i in range(N):
                for j in range(M):
                    if i == x and j == y: continue
                    if not allowed[i][j]: continue
                    if cur_sum + matrix[i][j] < ans: continue
                    temp = max(temp, dfs(i, j, num_visited + cur_visited, acc_sum + cur_sum, allowed))
        
            if upper:
                for j in range(M):
                    allowed[x-1][j] = 1
            if lower:
                for j in range(M):
                    allowed[x+1][j] = 1
            if left:
                allowed[x][y-1] = 1
            if right:
                allowed[x][y+1] = 1
        
            return temp
        
        T = int(input())
        for t in range(1, T+1):
            N, M = map(int, input().split())
            matrix = []
            for _ in range(N):
                row = list(map(int, input().split()))
                matrix.append(row)
        
            ans = -1
            can_visit = [[1] * M for _ in range(N)]
            for i in range(N):
                for j in range(N):
                    ans = max(ans, dfs(i, j, 0, 0, can_visit))
            print(f'#{t} {ans}')
        ```
        
    - DFS-예제는 통과한 코드
        
        ```sql
        import sys
        sys.stdin = open('temp_input/sample_input.txt')
        
        def dfs(x, y, num_visited, acc_sum, allowed):
            allowed[x][y] = 0
            backtrack = [(x, y)]
        
            if x - 1 >= 0:
                for j in range(M):
                    if allowed[x-1][j]:
                        allowed[x - 1][j] = 0
                        backtrack.append((x - 1, j))
        
            if x + 1 < N:
                for j in range(M):
                    if allowed[x+1][j]:
                        allowed[x+1][j] = 0
                        backtrack.append((x + 1, j))
        
            if y - 1 >= 0:
                if allowed[x][y-1]:
                    allowed[x][y-1] = 0
                    backtrack.append((x, y-1))
        
            if y + 1 < M:
                if allowed[x][y+1]:
                    allowed[x][y+1] = 0
                    backtrack.append((x, y+1))
        
            cur_visited = len(backtrack)
            if num_visited + cur_visited == M*N:
                for b in backtrack:
                    i, j = b
                    allowed[i][j] = 1
                return acc_sum + matrix[x][y]
        
            temp = -1
            for i in range(N):
                for j in range(M):
                    if allowed[i][j] == 0: continue
                    temp = max(temp, dfs(i, j, num_visited + cur_visited, acc_sum + matrix[x][y], allowed))
        
            for b in backtrack:
                i, j = b
                allowed[i][j] = 1
        
            return temp
        
        T = int(input())
        for t in range(1, T+1):
            N, M = map(int, input().split())
            matrix = []
            for _ in range(N):
                row = list(map(int, input().split()))
                matrix.append(row)
        
            ans = 0
            can_visit = [[1] * M for _ in range(N)]
            for i in range(N):
                for j in range(M):
                    ans = max(ans, dfs(i, j, 0, 0, can_visit))
            print(f'#{t} {ans}')
        
        ```
        
- 힌트를 얻었다
    
    문제가 뭔지 궁금해서 한번 살펴봤더니 dfs 는 아니고 dp 문제 같습니다.
    
    House Robber dp 알고리즘을 모든 행에 대해 적용하고, 모든 행의 결과 값 배열에 대해 다시 한 번 House Robber 를 적용하면 쉽게 풀 수 있습니다.
    
    릿코드의 House Robber 문제 링크입니다: https://leetcode.com/problems/house-robber/
    
    제가 작성한 dp 알고리즘은 아래와 같습니다.
        static int dp(int[] arr) {
            int N = arr.length;
            
            if (N == 0) {
                return 0;
            }
            
            int[] maxSum = new int[N + 1];
            
            maxSum[N] = 0;
            maxSum[N - 1] = arr[N - 1];
            
            for (int i = N - 2; i >= 0; --i) {
                maxSum[i] = Math.max(maxSum[i + 1], maxSum[i + 2] + arr[i]);
            }
            return maxSum[0];
        }
    
- House robber 문제 복습
    - nums[i]: i번째 집에 있는 돈
    - 붙어 있는 두 집을 연속으로 털지는 못함
    
    ```python
    class Solution:
        def rob(self, nums: List[int]) -> int:
            if len(nums) == 1: # 집이 한 집이면
                return nums[0] # 그 집것만 털어나온다 
    
            # array
            dp = [0] * len(nums) # 집의 길이는 최소 1
    
            # base case
            dp[0] = nums[0]
            dp[1] = max(nums[0], nums[1]) # 0,1 둘 중에 한 집만 털 수 있음 
    
            # recurrence relation
            for i in range(2, len(nums)):
    		        # 직전집까지 턴 금액 그대로 vs. 전전집까지 턴 금액 + 이번집 턴 금액 
                dp[i] = max(dp[i-1], dp[i-2]+nums[i])
            
            return dp[-1]
    
    ```
    
- 힌트 실행해보기
    - House Robber dp 알고리즘을 모든 행에 대해 적용하고,
        - 나란한 두 column도 못턴다
        - 나란한 두 row는 같이 못턴다
    - 모든 행의 결과 값 배열에 대해 다시 한 번 House Robber 를 적용하면 쉽게 풀 수 있습니다.
- AC 코드
    
    ```python
    import sys
    sys.stdin = open('temp_input/sample_input.txt')
    
    def house_rob(nums):
        # early exit
        if len(nums) == 1:
            return nums[0]
    
        dp = [0] * len(nums)
    
        # base case
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
    
        # recurrence relation
        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    
        return dp[-1]
    
    T = int(input())
    for t in range(1, T+1):
        N, M = map(int, input().split())
        matrix = []
        for _ in range(N):
            row = list(map(int, input().split()))
            matrix.append(row)
    
        res_rows = []
        for i in range(N):
            cur_row = [matrix[i][j] for j in range(M)]
            cur_res = house_rob(cur_row)
            res_rows.append(cur_res)
        ans = house_rob(res_rows)
    
        print(f'#{t} {ans}')
    
    ```