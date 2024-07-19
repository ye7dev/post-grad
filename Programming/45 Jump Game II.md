# 45. Jump Game II

Status: done, in progress
Theme: DP
Created time: March 8, 2024 10:24 PM
Last edited time: March 9, 2024 12:03 AM

- 문제 이해
    - nums array: 0-indexed, length n
    - 처음 위치는 nums[0]
    - 각 element nums[i]: index i로부터 forward jump 한번 해서 이동할 수 있는 최대 길이를 의미
        - nums[i]에 있으면 nums[max(n, i+nums[i])]이 최대로 갈 수 있는 거리
        - nums[n-1]로 이동할 수 있는 최소한의 Jump 수를 계산하라
- AC 코드
    - Bottom-up (🪇🐌)
        
        ```python
        class Solution:
            def jump(self, nums: List[int]) -> int:
                n = len(nums)
                dp = [float('inf')] * n
                # base case: start from n-1
                dp[n-1] = 0
                for i in range(n-2, -1, -1):
                    max_move = nums[i]
                    for j in range(max_move+1):
                        next_idx = min(n-1, j+i)
                        dp[i] = min(dp[i], 1+dp[next_idx])
                return dp[0]
        ```
        
    - Greedy(faster)
        
        ```python
        class Solution:
            def jump(self, nums: List[int]) -> int:
                end, far = 0, 0
                n = len(nums)
                ans = 0
                for i in range(n-1):
                    cur_far = min(n-1, i+nums[i])
                    far = max(far, cur_far)
                    if i == end:
                        end = far
                        ans += 1 
                return ans
        ```
        
- Editorial
    - Greedy 알 수 없는 rule
        - end: 갈 수 있는 가장 먼 starting index
            - i == end 일 때만 update 하고, 그럴 때만 answer이 증가한다
            - update 되는 값은 far. 그래서 far을 먼저 구하고 그 다음에 i == end인지 확인
                - 갈 수 있는 가장 먼 reachable index에 도달해서 jump를 수행한 것으로 count 하는 듯
        - far: 갈 수 있는 가장 먼 reachable index
            - 모든 index를 돌면서 최대값 far만 취한다
            - 나중에 end가 된다
        - i가 n-1에 도착하면 ans return