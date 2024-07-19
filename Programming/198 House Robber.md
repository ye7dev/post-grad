# 198. House Robber

Status: done
Theme: DP
Created time: November 12, 2023 11:28 AM
Last edited time: November 12, 2023 11:36 AM

- 많이 다뤄본 문제라 쉽게 풀 줄 알았는데 의외로 아니었음
    - 코드
        
        ```python
        class Solution:
            def rob(self, nums: List[int]) -> int:
                if len(nums) == 1:
                    return nums[0]
                elif len(nums) == 2:
                    return max(nums)
        
                money = [0] * len(nums)
                money[0] = nums[0]
                money[1] = max(nums[1], nums[0])
        
                for i in range(2, len(nums)):
                    money[i] = max(money[i-1], money[i-2]+nums[i])
        
                return money[-1]
        ```
        
- 어디서 테케를 틀렸냐…
    - input array 길이가 1인 경우 → edge case 처리
    - dp[1]의 경우. 무조건 두번째 집을 털었을 때의 금액이 X
        1. 첫번째 집을 털고 두번째집을 안터는 경우
        2. 첫번째 집을 안털고 두번째 집을 터는 경우 
        
        둘 중 더 max 값이 dp[1]
        
    - 헷갈렸던 경우의 수
        
        nums = [2, 1, 1, 2]
        
        - dp[i] = max(dp[i-1], dp[i-2] + nums[i])
            - dp[2] = max(dp[1], dp[0] + nums[2])
                - dp[1] = max(dp[1], dp[0]) 이었는데 dp[0]이 더 컸다면? → dp[1] = dp[0]
                
                → dp[2] = max(dp[0], dp[0] + nums[2])를 비교하는 셈 
                
            - dp[3] = max(dp[2], dp[1] + nums[3])
                - dp[1] = dp[0]이라면 dp[3] = max(dp[0] + nums[2], dp[0] + nums[3])
        - 점화식에서는 바로 전 두 집만 보는 것 같지만, 거슬러 가다보면 첫번째 + 세번째, 첫번째 + 네번째 같은 조합도 확인하게 되더라