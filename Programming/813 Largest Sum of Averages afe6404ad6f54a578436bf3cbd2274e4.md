# 813. Largest Sum of Averages

Status: done, in progress
Theme: DP
Created time: March 15, 2024 1:41 PM
Last edited time: March 15, 2024 3:41 PM

- AC 코드
    - Top-down(🪇🐢)
        
        ```python
        class Solution:
            def largestSumOfAverages(self, nums: List[int], k: int) -> float:
                # edge case 
                if k == 1:
                    return sum(nums) / len(nums)
                if k == len(nums):
                    return sum(nums)
        
                memo = {}
                def recur(start, end, left_k):
                    # check memo
                    state = (start, end, left_k)
                    if state in memo:
                        return memo[state]
                    # base case
                    if start == end:
                        return 0
                    if left_k == 1:
                        return sum(nums[start:end]) / (end-start)
                    
                    # recursive case
                    max_avg = 0 
                    for i in range(start+1, end):
                        cur_avg = sum(nums[start:i]) / (i-start)
                        next_avg = recur(i, end, left_k-1)
                        max_avg = max(max_avg, (cur_avg + next_avg))
        
                    memo[state] = max_avg
                    return memo[state]                
        
                return recur(0, len(nums), k)
                
        ```
        
    - Top-down(Editorial)
        - prefix sum 반영
            - index 주의
            - p[i]는 i-1까지의 원소를 담게끔 원소 개수 + 1로 [0] array init
        
        ```python
        class Solution:
            def largestSumOfAverages(self, nums: List[int], k: int) -> float:
                n = len(nums)
        
                prefix_sum = [0] * (n+1) # for better indexing 
                for i in range(n):
                    prefix_sum[i+1] = prefix_sum[i] + nums[i]
        
                memo = {}
        
                def recur(start, left_k):
                    # check memo
                    if (start, left_k) in memo:
                        return memo[(start, left_k)]
                    
                    # base case
                    if left_k == 1:
                        return (prefix_sum[n] - prefix_sum[start]) / (n - start)
                    
                    max_avg = 0
                    # recursive_case
                    for i in range(start, n - left_k + 1): # exclusive end
                        current_avg = (prefix_sum[i] - prefix_sum[start]) / (i - start)
                        max_avg = max(max_avg, current_avg + recur(i, left_k - 1))
                    
                    memo[(start, left_k)] = max_avg
                    return max_avg
        
                return recur(0, k)
        
        ```