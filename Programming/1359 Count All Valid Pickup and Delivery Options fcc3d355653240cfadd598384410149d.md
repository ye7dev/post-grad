# 1359. Count All Valid Pickup and Delivery Options

Status: done, in progress
Theme: DP
Created time: February 15, 2024 4:52 PM
Last edited time: February 15, 2024 5:14 PM

- 문제 이해
    - n개의 주문이 있을 때, 각 주문은 Pickup과 delivery로 구성되어 있다 (p_i, d_i)
    - d_i가 늘 p_i 뒤에 있도록 하는 pickup, delivery sequence의 개수를 구하라
- Trial
    - Bottom-up → 예제 통과
        
        ```python
        import math
        class Solution:
            def countOrders(self, n: int) -> int:
                # early exit
                if n == 1:
                    return 1 
                if n == 2:
                    return 6 
        
                mod = 10 ** 9 + 7
                dp = [0] * (n+1)
        
                # base case
                dp[1] = 1
                dp[2] = 6
        
                # recurrence relation
                for i in range(3, n+1):
                    two_spot = math.comb(2*n, 2)
                    dp[i] = dp[i-1] * two_spot
                    dp[i] % mod
                
                return dp[n]
        ```
        
- AC 코드
    - Bottom-up
        - i가 늘어날 때마다 자리를 두 칸 더 찾아야 한다는 힌트는 사실 보고 시작했음
        - math.comb method
        - 두 자리를 찾으면 나머지는 이전 조합에 두 자리 추가하는 거니까. 그리고 두 자리 안에서는 순서가 정해져있으니까. 이전 조합 * 이번 두 자리 찾기 하면 답이 나오는 것
        - 실수 유의 %=에서 = 빼먹지 말것
        
        ```python
        import math
        class Solution:
            def countOrders(self, n: int) -> int:
                # early exit
                if n == 1:
                    return 1 
                if n == 2:
                    return 6 
        
                mod = 10 ** 9 + 7
                dp = [0] * (n+1)
        
                # base case
                dp[1] = 1
                dp[2] = 6
        
                # recurrence relation
                for i in range(3, n+1):
                    two_spot = math.comb(2*i, 2)
                    dp[i] = dp[i-1] * two_spot
                    dp[i] %= mod
                
                return dp[n]
        ```