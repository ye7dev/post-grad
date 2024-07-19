# 1218. Longest Arithmetic Subsequence of Given Difference

Status: done, in progress, with help
Theme: DP, Longest Increasing Subsequence
Created time: January 18, 2024 3:30 PM
Last edited time: January 18, 2024 4:45 PM

- Trial
    - n-1에서 내려오는 식으로 했는데 TLE 나버림
        - 1에서 n-1까지 올라가는 식으로 해도 TLE 남
        
        ```python
        class Solution:
            def longestSubsequence(self, arr: List[int], difference: int) -> int:
                n = len(arr)
                # every single element is the LAS 
                dp = [1] * n
                max_len = 1
                for i in range(n-1, -1, -1):
                    for j in range(i+1, n):
                        if arr[j] - arr[i] == difference:
                            dp[i] = max(dp[i], dp[j]+1)
                    max_len = max(max_len, dp[i])
                
                return max_len
        ```
        
- AC code
    - post-editorial bottom-up
        
        ```python
        class Solution:
            def longestSubsequence(self, arr: List[int], difference: int) -> int:
                n = len(arr)
                # base case: first element 
                # every single element is the LAS 
                dp = {arr[0]:1}
                max_len = 1
        
                for i in range(1, n):
                    cur_element = arr[i]
                    prev_element = arr[i] - difference
        
                    if prev_element in dp:
                        prev_max_len = dp[prev_element]
                    else: 
                        prev_max_len = 0
                    
                    dp[cur_element] = prev_max_len + 1 
        
                    max_len = max(max_len, dp[cur_element])
                
                return max_len
        ```
        
- Editorial
    - Intuition
        
        ![Untitled](Untitled%20118.png)
        
        - dp[arr[i]]: arr[i]로 끝나는 arithmetic subsequence 중 가장 길이가 긴 것의 길이
            - key가 index가 아니라 arr[i]
            - 초기값은 0
            - array가 아니라 hashmap으로 만듦
        - arr[i]-difference가 이미 dp에 있는지 확인
            - LIS에서는 arr[i]보다 작기만 하면 뭐든 올 수 있었지만, 여기서는 정확히 올 수 있는 값이 정해져있음
            - before_a는 기존 dp[arr[i]-diff] 값을 의미하는 듯
            - arr[i]-diff가 dp에 없는 경우
                - every single element is the LAS에 따라 0
                - 아예 arr에 없거나 arr[i] 뒤에 있는 경우
                    
                    c.f. 5-7은 -2지만, subsequence 순서상 5→7은 +2에 해당 
                    
                
                ![Untitled](Untitled%20119.png)
                
            - arr[i] - diff가 dp에 있는 경우
                - arr[i]-diff까지의 subseq에 arr[i]를 붙이는 상황이기 때문에 dp[arr[i]] = dp[arr[i]-diff] + 1
                
                ![Untitled](Untitled%20120.png)