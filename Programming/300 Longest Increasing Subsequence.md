# 300. Longest Increasing Subsequence

Status: done, in progress, with help
Theme: DP
Created time: January 8, 2024 4:55 PM
Last edited time: January 8, 2024 9:42 PM

- [ ]  복잡도 분석
- 문제 이해
    
    subsequence: 주어진 input에서 순서 변경 없이 일부 혹은 0개의 원소를 지움으로써 만들 수 있는 array
    
- Trial
    - base case: 자기 혼자라도 increasing subsequence를 구성할 수 있다 → 길이 1인 subsequence인 것
    - 예제 통과 + 35/55까지 통과 - bottom up
        
        ```python
        class Solution:
            def lengthOfLIS(self, nums: List[int]) -> int:
                dp = [1] * len(nums)
                # dp[i]: LIS from up to nums[:i+1]
                # base case
                ## each letter is its own LIS of length 1
                ## dp[0] -> nums[0:1] -> single num -> 1
        
                for i in range(len(nums)):
                    cur_num = nums[i]
                    for j in range(i):
                        if nums[j] < cur_num:
                            dp[i] = max(dp[i], 1 + dp[j])
                
                return dp[-1]
        ```
        
        - `if nums[j] < cur_num:` 여기가 잘못된 것 같은데
            
            dp[j]의 max 값을 어디 저장해 둬야 하나? 
            
            → 아니다. 그저 return 값이 잘못 되었을 뿐. return max(dp)를 했어야 함 
            
        - i 앞의 모든 j에 대해 nums[j]와 nums[i]를 비교
            
            → dp[j]에 해당하는 LIS가 i앞에 있는 index 중 어디서 마지막으로 끝나는지 몰라도, 일단 i보다 앞에 있으면서 값이 nums[i]보다 작은 모든 숫자와 비교를 하기 때문에 하나는 걸리게 되어 있는 듯?
            
            - The algorithm considers every **`j < i`** because the longest subsequence ending at **`i`** could be an extension of any subsequence ending before **`i`**. We don't know in advance which **`j`** will give the longest extension, so we check all possibilities.
    - 35/55 문제에서 wrong - top down
        
        ```python
        class Solution:
            def lengthOfLIS(self, nums: List[int]) -> int:
                memo = {}
                
                # function
                def recur(i):
                    if i == 0: # nums[0:1]
                        return 1 
                    
                    # iteration of the recurrence relation
                    max_len = 1
                    for j in range(i):
                        if nums[j] < nums[i]:
                            max_len = max(max_len, 1 + recur(j))
                    
                    memo[i] = max_len
                    return memo[i]
                
                recur(len(nums)-1)
                return max(memo.values())
        ```
        
- AC 코드
    - Bottom-up
        
        ```python
        class Solution:
            def lengthOfLIS(self, nums: List[int]) -> int:
                dp = [1] * len(nums)
                # dp[i]: LIS from up to nums[:i+1]
                # base case
                ## each letter is its own LIS of length 1
                ## dp[0] -> nums[0:1] -> single num -> 1
        
                for i in range(len(nums)):
                    cur_num = nums[i]
                    for j in range(i):
                        if nums[j] < cur_num:
                            dp[i] = max(dp[i], 1 + dp[j])
                
                return max(dp)
        ```
        
    - Top-down (🐌)
        
        ```python
        class Solution:
            def lengthOfLIS(self, nums: List[int]) -> int:
                memo = {}
                
                # function
                def recur(i):           
                    # check memoization
                    if i in memo:
                        return memo[i]
        
                    # iteration of the recurrence relation
                    max_len = 1 # base case
                    for j in range(i):
                        if nums[j] < nums[i]:
                            max_len = max(max_len, 1 + recur(j))
                    
                    memo[i] = max_len
                    return memo[i]
                
                for i in range(len(nums)):
                    recur(i)
                    
                return max(memo.values())
        ```
        
        - 왜 모든 range에 대해 recur(i) 실행?
            - LIS 문제는 본질적으로 마지막 element에 관한 것이 아님. LIS는 nums i의 어느 위치에나 나올 수 있음
            - recur(len(nums)-1)을 하면 반드시 마지막 element = nums[len(nums)-1]을 포함하는 LIS만 구해짐. 그러나 overall LIS는 다른 값일 수도 있음
            - 반례
                
                Consider the array **`nums = [10, 9, 2, 5, 3, 7, 101, 18]`**.
                
                - If you only compute **`recur(len(nums) - 1)`**, which is **`recur(7)`**, the function will consider subsequences that must include the last element **`18`**.
                - The LIS that includes **`18`** is **`[2, 3, 7, 18]`**, with a length of 4.
                - However, the actual LIS in the entire array is **`[2, 3, 7, 101]`**, which does not include the last element **`18`**. This LIS has a length of 4 as well, but it's a different subsequence.
                
                By only computing **`recur(7)`**, the algorithm would miss the chance to consider the LIS **`[2, 3, 7, 101]`**, since it stops including elements after it reaches the last element **`18`**.