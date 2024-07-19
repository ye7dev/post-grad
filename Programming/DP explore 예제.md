# DP explore 예제

Status: in progress
Theme: DP
Created time: January 3, 2024 4:01 PM
Last edited time: January 4, 2024 11:29 AM

- **House Robber** [[**198. House Robber**](https://leetcode.com/problems/house-robber/solutions/846002/python-dynamic-programming-easy-solution-faster-than-95/?envType=study-plan-v2&envId=dynamic-programming)](198%20House%20Robber%20d44dfd89aff84bde8814b45e00a22820.md)
    
    ```python
    class Solution:
        def rob(self, nums: List[int]) -> int:
            if len(nums) == 1:
                return nums[0]
    
            # array
            dp = [0] * len(nums)
    
            # base case
            dp[0] = nums[0]
            dp[1] = max(nums[0], nums[1])
    
            # recurrence relation
            for i in range(2, len(nums)):
                dp[i] = max(dp[i-1], dp[i-2]+nums[i])
            
            return dp[-1]
    ```
    
- **Min Cost Climbing Stairs [[**746. Min Cost Climbing Stairs**](https://leetcode.com/problems/min-cost-climbing-stairs/description/?envType=study-plan-v2&envId=dynamic-programming)](746%20Min%20Cost%20Climbing%20Stairs%209e2034f086494531bfa2b26efb2acf1d.md)**
    
    [점화식은 제대로 찾았는데 base case가 tricky](%E1%84%8C%E1%85%A5%E1%86%B7%E1%84%92%E1%85%AA%E1%84%89%E1%85%B5%E1%86%A8%E1%84%8B%E1%85%B3%E1%86%AB%20%E1%84%8C%E1%85%A6%E1%84%83%E1%85%A2%E1%84%85%E1%85%A9%20%E1%84%8E%E1%85%A1%E1%86%BD%E1%84%8B%E1%85%A1%E1%86%BB%E1%84%82%E1%85%B3%E1%86%AB%E1%84%83%E1%85%A6%20base%20case%E1%84%80%E1%85%A1%20tricky%20d93bbff433f94e15b871be803f168b66.md)
    
    - dp array 초기값 관련 팁
        - For problems where you accumulate a value from a known starting point (like zero in this case), initializing to that starting value is appropriate.
        - In contrast, for problems where you are looking for a minimum value out of possibilities that are initially unknown, starting with **`float('inf')`** is the correct approach.
    
    ```python
    class Solution:
        def minCostClimbingStairs(self, cost: List[int]) -> int:
            # array
            n = len(cost)
            dp = [0] * (n+1) # known starting values
    
            # base case - dp[0], dp[1]
    
            # recurrence relation
            for i in range(2, n+1):
                dp[i] = min(dp[i-1]+cost[i-1], dp[i-2]+cost[i-2])
            
            return dp[-1]
    ```
    
- **N-th Tribonacci Number**
    
    ```python
    class Solution:
        def tribonacci(self, n: int) -> int:
            if n == 0:
                return 0
            if n == 1 :
                return 1 
            if n == 2 :
                return 1
            # array
            dp = [0] * (n+1)
            # base case 
            dp[1] = 1
            dp[2] = 1
    
            for i in range(3, n+1):
                dp[i] = dp[i-3] + dp[i-2] + dp[i-1]
            
            return dp[n]
    ```
    

[**740. Delete and Earn**](740%20Delete%20and%20Earn%20444c662c4acb438e913553154b275d58.md)