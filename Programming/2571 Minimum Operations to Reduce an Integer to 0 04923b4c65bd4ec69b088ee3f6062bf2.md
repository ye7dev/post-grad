# 2571. Minimum Operations to Reduce an Integer to 0

Status: done, in progress
Theme: DP
Created time: February 14, 2024 3:36 PM
Last edited time: February 14, 2024 6:26 PM

- 문제 이해
    - 정수 n이 주어질 때, 아래의 operation을 얼마든지 할 수 있다. n을 0으로 만들기 위한 operation의 최소 횟수를 구하라
        - operation: n에서 2의 승수를 빼거나 더한다
            - 2^0 = 1을 뺄 수도 있음 주의
- Trial
    - Top-down
        
        ```python
        class Solution:
            def minOperations(self, n: int) -> int:
                memo = {}
        
                # function
                def recur(num):
                    # check memo
                    if num in memo:
                        return memo[num]
                    # check base case
                    if num == 0:
                        return 0
                    if num < 0:
                        return float('inf')
                    # recurrence relation
                    pwr = 0
                    while num > (1 << pwr):
                        pwr += 1 
                    ans = float('inf')
                    for i in range(pwr):
                        ans = min(ans, 1 + recur(num-(2**i)))
        
                    memo[num] = ans
                    return memo[num]
                
                return recur(n)
        ```
        
    - Bottom-up
        
        ```python
        import math
        class Solution:
            def minOperations(self, n: int) -> int:
                pwr = 0
                while n > (1 << pwr):
                    pwr += 1 
                
                # array
                dp = [pwr] * (n+1)
                # dp[i]: min num of opers to make i -> 0
        
                # base case
                dp[0] = 0
                for i in range(pwr):
                    dp[(1 << i)] = 1
        
                # early exit
                if dp[n] != pwr:
                    return dp[n]
        
                # base case 
                for i in range(3, n+1):
                    for j in range(1, i):
                        left = i - j 
                        if dp[left] != pwr and dp[j] != pwr:
                            dp[i] = min(dp[i], 2)
                        elif dp[left] != pwr:
                            dp[i] = min(dp[i], dp[j]+1)
                        elif dp[j] != pwr:
                            dp[i] = min(dp[i], dp[left]+1)
                        
                return dp[n]
        ```
        
- AC 코드
    - Bottom-up(**🐢**)
        
        ```python
        import math
        class Solution:
            def minOperations(self, n: int) -> int:
                pwr = 0
                # first bigger power of 2
                while n >= (1 << pwr):
                    pwr += 1 
                
                # dp[i]: min num of operations to make i -> 0
                dp = [i for i in range(n+1)]
                # base case
                dp[0] = 0
                for i in range(pwr):
                    dp[(1 << i)] = 1 
                
                # iteration
                high_pwr = 2
                for i in range(3, n+1):
                    if 2 ** high_pwr < i:
                        high_pwr += 1 
                    low_pwr = high_pwr - 1
                    dp[i] = min(dp[i], dp[i - (1<< low_pwr)] + 1, dp[(1<< high_pwr)-i] +1)
                return dp[n]
        ```
        
    - Top-down solution (⚡️)
        - rightmost set bit를 계속 더하거나 빼면(숫자를 Update 해나가면서), 결국 2의 승수에 닿게 된다
        - 2의 승수에 닿으면 어떤 식으로든 1이 return 된다
        
        ```python
        import math
        class Solution:
            def minOperations(self, n: int) -> int:
                memo = {}
        
                # function
                def recur(num):
                    # check memo
                    if num in memo:
                        return memo[num]
                    # base case
                    if num == 0:
                        return 0
                    if (num & (num-1)) == 0: # num == 2**sth?
                        return 1 
                    
                    # recurrence relation
                    lsb = (num & -num) # finding the rightmost set bit(1)
                    next_big = recur(num + lsb)
                    next_small = recur(num - lsb)
                    # 1 : either adding or subtracting
                    memo[num] = min(next_big, next_small) + 1 
                    return memo[num]
        
                return recur(n)
        ```