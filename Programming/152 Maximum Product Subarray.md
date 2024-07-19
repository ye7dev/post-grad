# 152. Maximum Product Subarray

Status: done, in progress, 👀1
Theme: DP
Created time: February 26, 2024 10:24 PM
Last edited time: February 26, 2024 10:55 PM

- 과정
    - subarray: contiguous, non-empty
- Trial
    - Bottom-up: 186/190 → TLE
        
        ```python
        class Solution:
            def maxProduct(self, nums: List[int]) -> int:
                n = len(nums)
                if n == 1:
                    return nums[0]
                dp = [0] * n 
        
                # base case
                ans = -11
                for i in range(n-1, -1, -1):
                    dp = [0] * (n-i) #i~n-1 -> n-1-i+1 
                    dp[0] = nums[i]
                    running_prod = nums[i]
                    for j in range(i+1, n):
                        running_prod *= nums[j]
                        dp[j-i] = max(running_prod, dp[j-1-i], nums[j])
                    ans = max(max(dp), ans)
                return ans
                
                
        ```
        
- Editorial
    - **Approach 2: Dynamic Programming**
        - combo chain-모든 숫자가 양수면 그냥 누적해서 다 곱하면 되는데
        - 중간에 0이 있는 경우
            - 곱해버리면 combo chain이 0이 됨
            - 그 동안의 결과를 저장해둘 변수 `result` 가 필요
        - 더 높은 결과가 나타날 때마다 result도 update
        - 중간에 음수가 있는 경우
            - 음수 하나로 가장 큰 combo chain이 아주 작은 숫자가 될 수 있음
            - 아직 nums에 negative가 하나 더 있다면 combo chain을 살릴 수 있음
        - max_so_far: 아래 셋 중의 max
            - current number
            - last max_so_far * curr
                - 누적 곱이 꾸준히 중가하는 경우-계속 양수만 나오는 경우 선택될 것
            - last min_so_far * curr
                - 만약 curr이 negative고, combo chain도 음수인 상태인 경우
- AC 코드
    
    ```python
    class Solution:
        def maxProduct(self, nums: List[int]) -> int:
            n = len(nums)
            if n == 1:
                return nums[0]
    
            # base case
            max_so_far = nums[0]
            min_so_far = nums[0] # if next element is negative, multiplying to this can lead the max 
            result = max_so_far
    
            for i in range(1, n):
                curr = nums[i]
                # use previous so_far values 
                temp_max = max(curr, max_so_far * curr, min_so_far * curr)
                # use previous so_far values -> update min_sofar
                min_so_far = min(curr, max_so_far * curr, min_so_far * curr)
                # update max_so_far
                max_so_far = temp_max
                result = max(result, max_so_far)
            
            return result
            
    ```