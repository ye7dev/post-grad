# 377. Combination Sum IV

Status: done, in progress
Theme: DP
Created time: November 22, 2023 10:21 PM
Last edited time: November 22, 2023 10:32 PM

왠 일로 두 번만에 맞추는 기염을 토했다? 미디엄인데? 🪇

- 코드
    
    ```python
    class Solution:
        def combinationSum4(self, nums: List[int], target: int) -> int:
            dp = [0] * (target+1)
            for n in nums:
                if n <= target:
                    dp[n] += 1 
            for i in range(1, target+1):
                for n in nums:
                    dp[i] += dp[max(0, i-n)] 
            return dp[-1]
    ```