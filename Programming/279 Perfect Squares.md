# 279. Perfect Squares

Status: done, in progress
Theme: DP, Knapsack
Created time: January 24, 2024 2:02 PM
Last edited time: January 24, 2024 3:27 PM

- Progress
    - 12보다 작은 square
        
        3^2 = 9
        
        2^2 = 4
        
        12에 루트 씌운 다음에 정수화해서 그 수부터 시작해서 제해가기?
        
    - [[322. Coin Change(🪂)](https://leetcode.com/problems/coin-change/description/)](322%20Coin%20Change(%F0%9F%AA%82)%205c6b4477702548109d532dd506b1bbf3.md) revisited
- Trial
    - 569/588
        
        ```python
        import math
        class Solution:
            def numSquares(self, n: int) -> int:
                root = math.ceil(math.sqrt(n))
                if root == math.sqrt(n):
                    return 1 
                    
                dp = [float('inf')] * (n+1)
                
                # base case
                for denom in range(1, root):
                    dp[denom**2] = 1
        
                for num in range(1, n+1):
                    for denom in range(1, root):
                        new_num = num - (denom**2)
                        dp[num] = min(dp[num], dp[new_num]+1)
                
                return dp[-1]
        ```
        
- AC 코드
    - base case dp[0] = 0 핵심
    - `dp[num] = min(dp[num], dp[new_num]+1)`
        - break 문이 있으면 쓸모없는 계산을 끊어주니까 편하긴 하지만 없더라고
        - new_num이 음수일 경우 아직 계산이 안된 array의 뒷부분에서 값을 가져올 것이기 때문에 양의 무한대를 가져오겜 됨 → 여기에 min 연산을 적용하면 아무 변화도 없게 되는 것
    
    ```python
    import math
    class Solution:
        def numSquares(self, n: int) -> int:
            root = int(math.sqrt(n)) +1
            
            dp = [float('inf')] * (n+1)
            
            # base case
            dp[0] = 0
    
            for num in range(1, n+1):
                for denom in range(1, root):
                    if denom ** 2 > num:
                        break
                    new_num = num - (denom**2)
                    dp[num] = min(dp[num], dp[new_num]+1)
            
            return dp[-1]
    ```