# 1035. Uncrossed Lines

Status: done, in progress
Theme: DP, Longest Common Subsequence
Created time: January 22, 2024 3:46 PM
Last edited time: January 22, 2024 4:55 PM

- Process
    - dp 만들 때 empty string 을 base case로 잡는가? → 아닌 것 같은데?
        - [x]  It turns out to be…
        - n+1, m+1로 initialize 해야 한다
- Trial
    - 예제 2/3
        
        ```python
        class Solution:
            def maxUncrossedLines(self, nums1: List[int], nums2: List[int]) -> int:
                m, n = len(nums1), len(nums2)
        
                dp = [[0] * n for _ in range(m)]
        
                # base case
                for i in range(m):
                    if nums1[i] == nums2[0]:
                        dp[i][0] = 1 
                for j in range(n):
                    if nums1[0] == nums2[j]:
                        dp[0][j] = 1
                
                # iteration
                for i in range(1, m):
                    for j in range(1, n):
                        if nums1[i] == nums2[j]:
                            dp[i][j] = dp[i-1][j-1] + 1
                        else:
                            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                return dp[-1][-1]
        ```
        
    - AC 코드
        - DP size of m+1 by n+1 (index high → low, ⚡️)
            
            ```python
            class Solution(object):
                def maxUncrossedLines(self, nums1, nums2):
                    m, n = len(nums1), len(nums2)
                    
                    # array
                    dp = [[0] * (n+1) for _ in range(m+1)]
                    # base case
                    # i = n, j = m -> no valid char -> no common -> len = 0
            
                    # iteration
                    for i in range(m-1, -1, -1):
                        for j in range(n-1, -1, -1):
                            if nums1[i] == nums2[j]:
                                # bottom up에서 equation 오른쪽은 이미 계산 완료된 부분 
                                dp[i][j] = 1 + dp[i+1][j+1]
                            else:
                                dp[i][j] = max(dp[i+1][j], dp[i][j+1])
                    
                    return dp[0][0]
            ```
            
        - index low → high
            
            ```python
            class Solution:
                def maxUncrossedLines(self, nums1: List[int], nums2: List[int]) -> int:
                    m, n = len(nums1), len(nums2)
            
                    dp = [[0] * (n+1) for _ in range(m+1)]
            
                    # base case - auto covered
                    ## emptry string vs. any string -> common is zero
                    ## dp[0][j]: nums1[:0] vs nums2[:j]
            
                    for i in range(1, m+1):
                        for j in range(1, n+1):
                            if nums1[i-1] == nums2[j-1]:
                                dp[i][j] = 1 + dp[i-1][j-1]
                            else:
                                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                    
                    return dp[-1][-1]
            ```
            
- Editorial
    - 코드 흐름은 같으나 dp initialization에서 차이
        - state definition
        
        [[**1143. Longest Common Subsequence**](https://leetcode.com/problems/longest-common-subsequence/description/)](1143%20Longest%20Common%20Subsequence%2006fdbe2b7c1e4d6e9d1832737d94dffc.md) 와 동일한가? → 동일
        
    -