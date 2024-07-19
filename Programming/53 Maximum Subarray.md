# 53. Maximum Subarray

Status: done
Theme: DP
Created time: November 17, 2023 2:27 PM
Last edited time: November 17, 2023 3:14 PM

[Kadane’s algorithm](Kadane%E2%80%99s%20algorithm%208c3c89f804b64469b548e58e4349628f.md) 전형 문제. 

- 코드
    
    ```python
    class Solution:
        def maxSubArray(self, nums: List[int]) -> int:
            max_ending_here = 0
            max_so_far = -float('inf')
            for n in nums:
                if max_ending_here < 0:
                    max_ending_here = n 
                else:
                    max_ending_here += n 
                max_so_far = max(max_so_far, max_ending_here)
            return max_so_far
    ```
    
- 중간에 특정 원소를 뺀 부분 합은 아님. 왜냐면 subarray는 contiguous 예를 들어 `nums = [-2,1,-3,4,-1,2,1,-5,4]` 에서 양수만 골라낸 합이 최대일 것 같지만 정답은 `[4,-1,2,1]`