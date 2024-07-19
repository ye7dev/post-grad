# 96. Unique Binary Search Trees

Status: done, in progress
Theme: DP, On Trees
Created time: January 22, 2024 5:18 PM
Last edited time: January 22, 2024 5:48 PM

- Process
    - root를 돌아가면서로 만드는 듯…?
    - DP 문제인 걸로 봐서 n=1 일 때 1, n=2 일 때 2
- AC 코드
    - Top-down (🪇)
        
        ```python
        class Solution:
            def numTrees(self, n: int) -> int:
                memo = {}
        
                # function
                def recur(num):
                    # base case
                    if num <= 1:
                        return 1 
                    elif num == 2:
                        return 2
                    # check memoized
                    if num in memo:
                        return memo[num]
                    # recursive case
                    num_trees = 0
                    for i in range(num): # 0 -> num-1
                        left = recur(i)
                        right = recur(num-1-i) # num-1 -> 0
                        num_trees += (left * right)
                    memo[num] = num_trees
                    return memo[num]
                
                return recur(n)
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def numTrees(self, n: int) -> int:
                if n <= 2:
                    return n
        
                dp = [0] * (n + 1)       
                # base case
                dp[0] = 1
                dp[1] = 1
                dp[2] = 2 
        
                # iteration
                for i in range(3, n+1):
                    for j in range(i):
                        dp[i] += dp[j] * dp[i-1-j]
                
                return dp[-1]
        ```