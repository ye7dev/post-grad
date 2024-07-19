# 2369. Check if There is a Valid Partition For The Array

Status: in progress, with help
Theme: DP
Created time: November 29, 2023 12:41 PM
Last edited time: November 30, 2023 3:44 PM

- [ ]  처음부터 끝까지 쫙 짜보기
- 과정
    - subarray 길이가 3일 때 두 가지 state가 생긴다-증가해서 True인지, 아니면 값이 같아서 True인지
- Editorial
    - Top-down
        - recursive function `prefixIsValid(i)`
            - subarray nums[0..i]에서 valid parition이 존재하는지
            - 최종적으로 return 해야 하는 값 `prefixIsValid(n-1)`
            - check `prefixIsValid(i)` at every index i
                - base case: i가 0보다 작으면 `prefixIsValid(i)` = True
                    - 비어 있는 subarray는 늘 valid partition
                1. 마지막 두 원소가 같은 경우: nums[i] == nums[i-1] → `prefixIsValid(i-2)` 가 True이면 `prefixIsValid(i)` 도 True 
                2. 마지막 세 원소가 같은 경우: nums[i] == nums[i-1] == nums[i-2] → `prefixIsValid(i-3)` 가 True이면 `prefixIsValid(i)` 도 True 
                3. 마지막 세 원소가 오름차순인 경우: nums[i]-nums[i-1] == nums[i-1]-nums[i-2] == 1 → `prefixIsValid(i-3)` 가 True이면 `prefixIsValid(i)` 도 True 
    - Bottom-up
        - init table : `dp = [False] * (n+1)`
            - no valid partition is found yet
        - state: `dp[i]` : nums[0..i-1]이 valid partition인지. `prefixIsValid(i-1)`
        - base case: `dp[0] = True`
            - `prefixIsValid(0-1) = prefixIsValid(-1) = True`
        - transition: dp랑 nums의 index 체계가 다름 주의
            - dp_index = nums_index + 1
            - dp에서는 i가 exclusive라서
            
            → dp[i+1]: nums[0..i]까지가 valid parition인지 
            
        - end: return dp[n]
- Editorial 보고 짠 코드
    - top-down (더 빠름)
        
        ```python
        class Solution:
            def validPartition(self, nums: List[int]) -> bool:
                @cache
                def dp(i):
                    # empty string = valid partition
                    if i < 0: return True 
                    if nums[i] == nums[i-1] and dp(i-2):
                        return True 
                    if nums[i] == nums[i-1] == nums[i-2] and dp(i-3):
                        return True 
                    if nums[i] == nums[i-1] +1 == nums[i-2] + 2 and dp(i-3):
                        return True
                    return False
                return dp(len(nums)-1)
        ```
        
    - bottom-up
        
        ```python
        class Solution:
            def validPartition(self, nums: List[int]) -> bool:
                n = len(nums)
                # init table
                dp = [False] * (n+1)
                # base case
                dp[0] = True
                # transition: start at the farthest from the desired
                for i in range(1, n):
                    dp_index = i+1 # dp_index-3 = i-2 -> i=0이면 0. empty array 
                    if nums[i] == nums[i-1] and dp[dp_index-2]:
                        dp[dp_index] = True 
                    if i > 1:
                        if nums[i] == nums[i-1] == nums[i-2] and dp[dp_index-3]:
                            dp[dp_index] = True 
                        elif nums[i] == nums[i-1] + 1 == nums[i-2]+2 and dp[dp_index-3]:
                            dp[dp_index] = True 
                    # no update for else case: retain False
        
                # end
                return dp[n]
        ```