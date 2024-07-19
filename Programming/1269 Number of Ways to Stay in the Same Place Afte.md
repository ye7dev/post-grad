# 1269. Number of Ways to Stay in the Same Place After Some Steps

Status: done, in progress
Theme: DP
Created time: February 14, 2024 6:28 PM
Last edited time: February 15, 2024 4:25 PM

- 문제 이해
    - 0에서 시작해서 왼쪽으로 한칸 가거나 오른쪽으로 한칸 가거나 같은 자리에 머물 수 있음
    - step 수가 주어질 때, 그 step 뒤에 정확히 다시 0에 있을 수 있는 방법의 가지수를 구하라
    - [[**629. K Inverse Pairs Array**](https://leetcode.com/problems/k-inverse-pairs-array/description/)](629%20K%20Inverse%20Pairs%20Array%20de3231059d394d299eb1188c0b830e37.md) 문제처럼 indices랑 value랑 혼동하지 말 것
- Trial
    - Brute force(?) → 6/33
        
        ```python
        class Solution:
            def numWays(self, steps: int, arrLen: int) -> int:
                mod = 10 ** 9 + 7
                # dp[n][k]: # of ways with k steps in n length array
                dp = [[0] * (steps+1) for _ in range(arrLen+1)]
        
                # base case
                # empty arr or zero steps -> no way 
                for i in range(arrLen):
                    dp[i][1] = 1 # single step -> stay 
                for j in range(steps):
                    dp[1][j] = 1 # single element -> stay 
        
                # recurrence relation
                for cur_len in range(2, arrLen+1):
                    for cur_step in range(2, steps+1):
                        target = [0]
                        ways = 1 
                        coord = set()
                        for s in range(cur_step-1, 1, -1):
                            coord = set()
                            while target:
                                t = target.pop()
                                if 0 <= t-1 < cur_len:
                                    coord.add(t-1)
                                coord.add(t)
                                if 0 <= t+1 < cur_len:
                                    coord.add(t+1)
                            ways *= len(coord)
                            ways %= mod
                            target = list(coord)
                            coord = set()
                    dp[cur_len][cur_step] = ways
        
                return dp[arrLen][steps] * 2
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def numWays(self, steps: int, arrLen: int) -> int:
                mod = 10 ** 9 + 7
                
                ''' 
                dp[remain_step][idx]
                : ways to end at zero 
                : current position is idx
                : and remaining steps is remain_step
                '''
                dp = [[0] * arrLen for _ in range(steps+1)]
        
                # base case 
                dp[0][0] = 1 
                dp[1][0] = 1 # [0] -> stay 
                dp[1][1] = 1 # [1] -> left 
                '''
                2-> 2, 1, 3
                dp[3][2] = dp[2][2] + dp[2][1] + dp[2][3]
                1 -> 1, 0
                dp[2][1] = dp[1][1] + dp[1][2] + dp[1][0] = 2 
                2 -> 0, 1
                dp[2][2] = dp[1][0] + dp[1][1] = 2
        
                dp[2][2]
                '''
                # recurrence relation
                for remain in range(2, steps+1):
                    for end in range(arrLen): # 0~arrLen-1
                        if end + 1 < arrLen: # 1~arrLen
                            dp[remain][end] = (dp[remain][end] + dp[remain-1][end+1]) % mod
                        if end - 1 >= 0: # -1~arrLen-2
                            dp[remain][end] = (dp[remain][end] + dp[remain-1][end-1]) % mod
                        dp[remain][end] = (dp[remain][end] + dp[remain-1][end]) % mod
                
                ways = 0
                for i in range(arrLen):
                    ways = (ways + dp[steps][i]) % mod
                return ways
        ```
        
- AC 코드
    - Bottom-up
        - 놓친 점
            1. state 정의까지 잘 했는데, 마지막 return 값에서 정의에서 약간 벗어나 버림 
                - dp[remain][idx]: if current position is idx, number of ways to end at zero with remain steps
                - 문제에서는 steps를 가지고 0에서 시작하기 때문에 current position = 0인 셈이다
            2. Valid 계산 범위 설정
                - 1만 수정해도 27/33까지는 풀리지만 28번째 문제에서 TLE 나옴
                - 왜냐면 계산할 필요가 없는 부분까지 계산하기 때문에
                - 현재 위치가 4라고 해도 남은 step 수가 2이면 0에 도달할 수 있는 방법이 없다
                - 결국 방법이 존재하는 max 현재 위치는 남은 step의 개수만큼이다
                    - steps = 4 → 4에서 왼쪽으로 4번 오면 0.
                        - 4→3→2→1→0 에서 화살표 개수가 step이기 때문에 4개
                - index가 0에서 시작하는 것을 고려할 때, steps가 되려면 steps+1개의 원소가 존재해야 함 → dp table 생성 시에 반영
            3. 더 간단하게 계산할 수 있는 부분 
                - dp[remain][end] = (dp[remain][end] + dp[remain-1][end]) % mod
                    - 이 부분을 제일 먼저 계산하면 dp[remain][end]는 0에서 시작하기 때문에
                    - dp[remain][end] = dp[remain - 1][end]  등호 처리로 간단하게 가능
                - mod 연산 위치
                    - 더할 때마다 하지 말고
                    - 다 더한 다음 마지막에 한번만 한다
        
        ```python
        class Solution:
            def numWays(self, steps: int, arrLen: int) -> int:
                mod = 10**9 + 7
                
                # Initialize DP table
                dp = [[0] * min(steps + 1, arrLen) for _ in range(steps + 1)]
                dp[0][0] = 1  # Base case
                
                # Fill DP table
                for remain in range(1, steps + 1):
                    for end in range(min(arrLen, remain + 1)):  # Only iterate through reachable positions
                        dp[remain][end] = dp[remain - 1][end]  # Stay in place
                        if end > 0:
                            dp[remain][end] += dp[remain - 1][end - 1]  # Move left
                        if end + 1 < arrLen and end < remain:  # Check if moving right is possible
                            dp[remain][end] += dp[remain - 1][end + 1]  # Move right
                        dp[remain][end] %= mod
                
                return dp[steps][0]  # Return ways to end at start position
        ```