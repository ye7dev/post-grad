# 55. Jump Game

Status: done, in progress
Theme: DP
Created time: February 3, 2024 11:13 AM
Last edited time: February 3, 2024 11:52 AM

- Progress
    - 문제 이해
        - array의 첫번째 index에 위치. 각 element 는 그 자리에서 할 수 있는 최대 jump length를 나타낸다
        - 마지막 index에 닿을 수 있으면 true, 아니면 false를 return 하라
    - 과정
        - 예전에 삼성에서 풀었던 문제 같다.
        - index가 아니라 jump length를 저장해야 할 것 같기도
- AC 코드
    - Bottom-up (🪇)
        - i는 작은 값부터 채워짐
        - j는 i보다 작은 값임. 그래서 j는 큰 값에서 작은 값으로 순회해도 이미 값이 다 채워져 있음
        - i에서 더 가까운 j, 즉 더 큰 j부터 시작해서 찾는게 더 빨리 찾을 수 있음
        
        ```python
        class Solution:
            def canJump(self, nums: List[int]) -> bool:
                n = len(nums)
                dp = [False] * n
                # base case
                dp[0] = True
        
                for i in range(1, n):
                    for j in range(i-1, -1, -1):
                        if dp[j] and j + nums[j] >= i:
                            dp[i] = True
                            break
                return dp[-1]
        ```
        
    - Bottom-up (editorial version)
        
        ```python
        class Solution:
            def canJump(self, nums: List[int]) -> bool:
                n = len(nums)
                dp = [False] * n
                # base case
                dp[-1] = True
        
                for i in range(n-2, -1, -1):
                    furthest_jump = min(i + nums[i], n-1)
                    for j in range(i+1, furthest_jump+1):
                        if dp[j]:
                            dp[i] = True 
                            break
                return dp[0]
        ```
        
- Trial
    - Bottom-up → 107/172
        
        ```python
        class Solution:
            def canJump(self, nums: List[int]) -> bool:
                n = len(nums)
                dp = [False] * n
                # base case
                dp[0] = True
        
                for i in range(1, n):
                    for j in range(i):
                        if dp[j] and j + nums[j] >= nums[i]:
                            dp[i] = True
                            break
                return dp[-1]
        ```
        
    - Bottom-up → 143/172 (TLE)
        - j + nums[j]가 nums[i]가 아닌 index i보다 도달 가능!
        
        ```python
        class Solution:
            def canJump(self, nums: List[int]) -> bool:
                n = len(nums)
                dp = [False] * n
                # base case
                dp[0] = True
        
                for i in range(1, n):
                    for j in range(i):
                        if dp[j] and j + nums[j] >= i:
                            dp[i] = True
                            break
                return dp[-1]
        ```
        
- Editorial
    - **Approach 3: Dynamic Programming Bottom-up**
        - jump는 왼쪽에서 오른쪽으로만 이루어짐
        - array의 오른쪽에서 시작하면, 우리의 오른쪽에 있는 위치를 query 하면, 그 위치는 이미 True, False가 정해져 있을 것 → 더 recurse 할 필요 없다
        - dp[i]: i th index에서 n-1 도달 가능한지
        - 예) [2, 3, 1, 1, 4], n = 5
            - dp = [False, False, False, False, True]
            - i = 3 → nums[i] = 1 → furthest jump = min(1+3, 4) = 4
                - for j in range(4, 5) → j = 4
                    - dp[4] = True → dp[3] = True
                
                ⇒ 3에서 4가 도달 가능하고, 4가 도달 가능한 상태니까 3에서도 도달 가능하다 
                
            - i = 2 → nums[i] = 1 → furthest jump = min(2+1, 4) = 3
                - for j in range(3, 5) → j = 3, 4
                    - dp[3] = True → dp[2] = True → break
                
                ⇒ 2에서 4가 도달 가능하고, 4가 end까지 도달 가능한 상태니까 2에서도 도달 가능하다 
                
            - i = 1 → nums[i] = 2 → furthest_jump = min(1+2, 4) = 3
                - for j in range(3, 5) → j = 3, 4
                    - dp[3] = True → dp[1] = True