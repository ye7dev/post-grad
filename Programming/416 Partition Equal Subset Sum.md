# 416. Partition Equal Subset Sum

Status: done, in progress
Theme: DP, Knapsack
Created time: January 30, 2024 4:44 PM
Last edited time: January 30, 2024 5:59 PM

- progress
    - 한 원소당 a, b 두 가지 state
        - 2^n 중에 합이 같은 경우가 있는지
- AC 코드
    - Brute force (TLE)
        - solution 자체는 맞는데 TLE
        
        ```python
        class Solution:
            def canPartition(self, nums: List[int]) -> bool:
                n = len(nums)
                subset_sum = sum(nums) / 2
        
                def recur(left_sum, idx):
                    # base case 
                    if left_sum == 0:
                        return True
                    if left_sum < 0 or idx == n:
                        return False
        
                    # recurrence case
                    if recur(left_sum-nums[idx], idx+1) or recur(left_sum, idx+1):
                        return True
                    return False 
                
                return recur(subset_sum, 0)
        ```
        
    - Top-down(memo)
        - 더 빠르게 한 요소
            1. total_sum이 2로 안 나눠질 경우 early exit 
            2. subset_sum을 // 연산으로 구해서 정수로 떨어지게 함 
            3. memoization
            4. 재귀식에서 두 경우에 대해 각각 변수를 부여하지 않고 하나의 조건문 안에 두 재귀식 다 때려넣으니까 훨씬 빨라짐 
                - python or 조건문 특성에 기인. or에 바로 재귀함수 두개 다 넣으면, 둘 중에 앞에서 True 나오자 마자 뒤의 함수 진입 안하고 바로 return True 해버림
        
        ```python
        class Solution:
            def canPartition(self, nums: List[int]) -> bool:
                n = len(nums)
                total_sum = sum(nums)
                memo = {}
                if total_sum % 2 != 0:
                    return False
                subset_sum = total_sum // 2
        
                def recur(left_sum, idx):
                    # base case 
                    if left_sum == 0:
                        return True
                    if left_sum < 0 or idx == n:
                        return False
        
                    # check memo
                    if (left_sum, idx) in memo:
                        return memo[(left_sum, idx)]
        
                    # recurrence case
                    if recur(left_sum-nums[idx], idx+1) or recur(left_sum, idx+1):
                        memo[(left_sum, idx)] = True
                    else:
                        memo[(left_sum, idx)] = False 
                    return memo[(left_sum, idx)] 
                
                return recur(subset_sum, 0)
        ```
        
    - Top-down (lru_cache, faster)
        
        ```python
        class Solution:
            def canPartition(self, nums: List[int]) -> bool:
                memo = {}
                n = len(nums)
                if sum(nums) % 2 != 0:
                    return False
                subset_sum = sum(nums) // 2 
        
                @lru_cache(maxsize=None)
                def recur(i, left_sum):
                    # base case
                    if left_sum == 0:
                        return True 
                    if left_sum < 0 or i == n:
                        return False
        
                    # recurrence relation
                    if recur(i+1, left_sum-nums[i]) or recur(i+1, left_sum):
                        return True
                    return False
                
        
                return recur(0, subset_sum)
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def canPartition(self, nums: List[int]) -> bool:
                n = len(nums)
                total_sum = sum(nums)
                if total_sum % 2 != 0:
                    return False
                subset_sum = total_sum // 2
        
                dp = [[False] * (subset_sum+1) for _ in range(n+1)]
                # base case
                dp[0][0] = True
        
                # recurrence relation
                for i in range(1, n+1):# 1~n
                    cur_val = nums[i-1]
                    for value in range(1, subset_sum+1):
                        if cur_val > value: # value-cur_val < 0
                            if dp[i-1][value]:
                                dp[i][value] = True
                        else:
                            if dp[i-1][value] or dp[i-1][value-cur_val]:
                                dp[i][value] = True
                
                return dp[-1][-1]
        ```
        
- Trial
    - Top-down: 68/141 memory limit exceeded
        
        ```python
        class Solution:
            def canPartition(self, nums: List[int]) -> bool:
                memo = {}
                n = len(nums)
        
                def recur(i, a, b):
                    # base case
                    if i == n:
                        if a == b: 
                            return True
                        return False 
                    
                    # check memo
                    if (i, a, b) in memo:
                        return memo[(i, a, b)]
        
                    # recurrence relation
                    group_a = recur(i+1, a+nums[i], b)
                    group_b = recur(i+1, a, b+nums[i])
                    if group_a or group_b:
                        memo[(i, a, b)] = True
                    else:
                        memo[(i, a, b)] = False
                    return memo[(i, a, b)]
                
                return recur(0, 0, 0)
        ```
        
    - Top-down: 83/141 memory limit exceeded
        
        ```python
        class Solution:
            def canPartition(self, nums: List[int]) -> bool:
                memo = {}
                n = len(nums)
                subset_sum = sum(nums) / 2 
        
                def recur(i, left_sum):
                    # base case
                    if left_sum == 0:
                        return True 
                    if left_sum < 0 or i == n:
                        return False
                    
                    # check memo
                    if (i, left_sum) in memo:
                        return memo[(i, left_sum)]
        
                    # recurrence relation
                    group_a = recur(i+1, left_sum-nums[i])
                    group_b = recur(i+1, left_sum)
                    if group_a or group_b:
                        memo[(i, left_sum)] = True
                    else:
                        memo[(i, left_sum)] = False
                    return memo[(i, left_sum)]
                
                return recur(0, subset_sum)
        ```
        
    - Bottom-up: 28/141
        - state: dp[i][value]
            - nums[:i]까지의 원소를 고려해서 (current 원소: nums[i-1]) value를 만들 수 있는지 여부
        - base case
            - nums[:0] = None. 아무 원소 없이 0 만들 수 있으므로 dp[0][0] = True
        - current 원소가 만들어야 하는 value보다 큰 경우
            - value에서 current 원소를 빼면 음수가 나오기 때문에, 한 가지 경우만 고려하면 된다
            - current 원소를 고려하지 않을 때 value를 만들 수 있는지
        
        ```python
        class Solution:
            def canPartition(self, nums: List[int]) -> bool:
                n = len(nums)
                total_sum = sum(nums)
                if total_sum % 2 != 0:
                    return False
                subset_sum = total_sum // 2
        
                dp = [[False] * (subset_sum+1) for _ in range(n+1)]
                # base case
                dp[0][0] = True
        
                # recurrence relation
                for i in range(1, n+1):# 1~n
                    cur_val = nums[i-1]
                    for value in range(1, subset_sum+1):
                        if cur_val > value: # value-cur_val < 0
                            if dp[i-1][value]:
                                dp[i][value] = True
                        else:
                            if dp[i-1][value] or dp[i-1][value-cur_val]:
                                dp[i][value] = True
                
                return dp[-1][-1]
        ```
        
- Editorial
    - Overview
        - knapsack 문제와 비슷
            - sum(array) = subset_sum * 2 → subset_sum = total_sum / 2
                - sum(array)는 항상 even 해야
            - 문제는 이제 합의 값이 subset_sum과 같아지는 subset을 찾을 수 있느냐로 바뀜
    - Brute Force
        - 가능한 모든 subset을 만든 다음 required sum을 갖는 경우가 있는지 확인
        - array 원소 하나 당 두 개의 가능성 존재
            1. 원소가 subset sum에 포함되는 경우 
                - subSetSum = subSetSum - x
            2. 원소가 subset sum에 포함되지 않는 경우 → previous sum을 그대로 들고감 
                - subSetSum = subSetSum
        - DFS 사용해서 맨 끝 원소까지 갔을 때 두 경우 중 하나에서 subset_Sum이 0에 도달하는지 확인
            - 재귀함수 파라미터 : 남은 subset sum, 원소 index
    - **Approach 2: Top Down Dynamic Programming - Memoization**
    - **Approach 3: Bottom Up Dynamic Programming**
        - Algorithm
            - base case
                - dp[0][0] = True
            - state: dp[i][value]
                - nums[:i+1] 까지의 원소를 고려할 때, 얘네로 value를 만들 수 있으면 True
                - True인 경우들
                    1. nums[i]까지 포함해서 value를 만드는 경우
                        - dp[i-1][value-nums[i]] = True
                    2. nums[i] 없이 value를 만드는 경우 
                        - dp[i-1][value] = True