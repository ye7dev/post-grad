# 1326. Minimum Number of Taps to Open to Water a Garden

Status: done, in progress, with help
Theme: DP
Created time: November 28, 2023 6:36 PM
Last edited time: November 29, 2023 12:37 PM

- [ ]  처음부터 쫙 짜보기
- 과정
    
    dp[i] : i번째 호스까지 고려했을 때 커버할 수 있는 가장 넓은 넓이 
    
    dp[-1]이 주어진 범위 포함하면 return 아니면 -1 
    
    호스가 있는 곳은 커버해야 할 범위 내부임 
    
- Editorial
    - state dp[i]: 0부터 i까지의 영역을 커버하기 위한 최소 tap 수
        - i inclusive → 우리가 구해야 하는 건 dp[n] → n을 Index로 쓰기 위해서는 n+1까지의 칸이 필요
        - 최소 상태를 update 해야 하므로 default는 positive infinity
    - base case: dp[0] = 0
        - 0에서 0까지의 넓이를 커버하기 위해서는 아무 호스도 틀 필요가 없다
        - [x]  transition 부터 이어서…
    - Transitions
        - 각 tap에서는 범위를 확인
            - `tap_start = max(0, i-ranges[i])`
                - 어차피 커버해야 하는 범위는 0과 n 사이기 때문에 범위에서 음수까지 진행된다고 해도 쓸 필요 없음
                - ranges[i]의 범위와 ranges의 length를 고려할 때 i-ranges[i]의 범위
                    - i는 index라서 0부터 n (len(ranges) == n+1)
                    - ranges[i]의 최소값은 0
                    
                    → i-ranges[i]의 최대값은 0-0 = 0
                    
                    아 근데 i=n이고, ranges[i]가 0이면 i-ranges = n이라서 더 커질 수 있네 ;; 
                    
            - `tap_end = min(n, i+ranges[1])`
                - 아무리 호스로 커버할 수 있는 범위가 넓어도 n보다 더 커질 필요는 없음
        - dp[j] + 1
            - dp[j]: 0부터 j까지 커버 ← 이 때 j는 0부터 ith tap이 커버할 수 있는 범위 내의 임의의 지점
            - dp[j] + 1 : 0부터 tap_end(ith tap이 커버할 수 있는 rightmost boundary)까지 커버하기 위해 필요한 tap 수
            - j=0이고  ith tap의 leftmost boundary가 0보다 작거나 같으면 tap 하나로도 충분
                - dp[j] = dp[0] → dp[0]+1 = 0+1 = 1 (base case 활용)
        - each tap이 커버하는 범위 내에 있는 position(0과 n 사이)을 각각 돌면서 → 각 position j에서 `dp[j]+1`과 `dp[tap_end]` 비교. 둘 중에 더 작은 게 `dp[tap_end]`
    - end
        - dp[-1] 값이 초기값인 infinity이면 주어진 범위를 커버할 수 없다는 거니까 -1. 유한한 숫자이면 그게 최소로 필요한 tap 수
        
- 코드
    - 유의할 점
        - j는 0와 tap_end 사이에 있는 값이 아니라, ith tap이 커버할 수 있는 범위 즉 tap_start ~ tap_end 사이에 있는 지점이어야
        - 이 때 tap_end는 ith tap의 커버 범위에서 inclusive → j에 대한 range 줄 때 tap_end + 1이 마지막값
    
    ```python
    class Solution:
        def minTaps(self, n: int, ranges: List[int]) -> int:
            # dp init
            dp = [float('inf')] * (n+1) # len(ranges) == n+1
            # base case
            dp[0] = 0
            # transition
            for i in range(n+1):
                tap_start = max(0, i - ranges[i])
                tap_end = min(n, i + ranges[i])
                for j in range(tap_start, tap_end+1):
                    dp[tap_end] = min(dp[tap_end], dp[j]+1)
            # end 
            if dp[-1] == float('inf'):
                return -1
            else:
                return dp[-1]
    ```