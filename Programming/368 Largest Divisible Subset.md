# 368. Largest Divisible Subset

Status: done, in progress
Theme: DP
Created time: February 22, 2024 6:02 PM
Last edited time: February 22, 2024 6:37 PM

- 문제 이해
    - every pair of subset이 아래의 조건 만족하는 longest subset 구하라
        - `answer[i] % answer[j] == 0`, or
        - `answer[j] % answer[i] == 0`
            
            → 어느 한쪽이 다른 한쪽의 배수여야 한다는 뜻
            
        - 근데 모든 pair에 대해 그것이 성립해야 하니까
    - input array에는 중복이 없다
        - 다 1보다 크거나 같은 숫자만 있다
- 과정
    - 개수나 길이가 아니라 subset 자체를 return 하는 경우 state를 어떻게 정의해야 할지?
    - 그냥 top-down으로 푸는 게 이로울 듯
    - 문제 category에 sorting이 있어서 우선 sorting을 하고 본다
- AC 코드
    - Bottom-up(🪇)
        
        ```python
        class Solution:
            def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
                nums.sort()
                n = len(nums)
                # array
                dp = [[nums[i]] for i in range(n)]
        
                # base case
                max_idx = 0
                for i in range(1, n):
                    temp =[]
                    for j in range(i):
                        if nums[i] % nums[j] == 0:
                            if len(temp) < len(dp[j]):
                                temp = dp[j]
                    dp[i] += temp 
                    if len(dp[i]) > len(dp[max_idx]):
                        max_idx = i
                return dp[max_idx]
                
        ```