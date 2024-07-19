# 1646. Get Maximum in Generated Array

Status: done, in progress
Theme: DP
Created time: November 23, 2023 10:37 PM
Last edited time: November 23, 2023 10:59 PM

- 몸풀기 easy
- 마지막 return 값을 여느때처럼 dp[-1]로 했는데 max(dp)로 해야 하는 거였음;;
- 코드
    
    ```python
    class Solution:
        def getMaximumGenerated(self, n: int) -> int:
            if n <= 1: return n
            nums = [0] * (n+1)
            nums[1] = 1 
            
            for i in range(2, n+1):
                if i % 2 == 0:
                    nums[i] = nums[i//2]
                else:
                    nums[i] = nums[(i-1)//2] + nums[(i-1)//2+1]
            return max(nums)
    ```