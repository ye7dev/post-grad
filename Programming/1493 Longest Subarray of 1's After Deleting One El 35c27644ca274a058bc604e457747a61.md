# 1493. Longest Subarray of 1's After Deleting One Element

Status: done, in progress
Theme: DP
Created time: February 28, 2024 12:12 PM
Last edited time: February 28, 2024 12:25 PM

- AC 코드 (⚡️🪇)
    
    ```python
    class Solution:
        def longestSubarray(self, nums: List[int]) -> int:
            n = len(nums)
            if n == 1:
                return 0
            if max(nums) == 0:
                return 0 
            if min(nums) == 1:
                return len(nums)-1
    
            reduced = [0]
            for i in range(n):
                if nums[i] == 0:
                    reduced.append(0)
                else:
                    if reduced[-1] != 0:
                        reduced[-1] += 1
                    else:
                        reduced.append(1)
            reduced.append(0)
            ans = 0
            for i in range(1, len(reduced)-1):
                if reduced[i] == 0:
                    ans = max(reduced[i-1]+reduced[i+1], ans)
            return ans
                    
                    
            
    ```