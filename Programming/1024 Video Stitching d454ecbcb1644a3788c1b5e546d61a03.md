# 1024. Video Stitching

Status: done, in progress
Theme: DP
Created time: March 15, 2024 3:41 PM
Last edited time: March 15, 2024 4:12 PM

- AC 코드
    - Bottom-up (🪇)
        - edge case 조심할 것
        
        ```python
        class Solution:
            def videoStitching(self, clips: List[List[int]], time: int) -> int:
                clips.sort()
                if clips[0][0] > 0:
                    return -1 
                
                n = len(clips)
                dp = [101] * (time+1)
                # base case 
                dp[0] = 0
                
                t = 0
                cidx = 0
                while t <= time:
                    s, e = clips[cidx]
                    if s <= t <= e:
                        dp[t] = min(dp[t], 1 + dp[s])
                        t += 1 
                    else:
                        cidx += 1 
                        if cidx == n:
                            break 
                return dp[-1] if dp[-1] != 101 else -1 
        
        ```