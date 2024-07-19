# 276. Paint Fence

Status: done, in progress
Theme: DP
Created time: January 9, 2024 4:33 PM
Last edited time: January 10, 2024 11:19 AM

- Progress
    - state variable: n, k
        - dp[i]: i번째 post까지를 제약사항 지키면서 칠할 수 있는 유니크한 방버의 개수
    - 최대 두 개를 연속으로 같은 색깔 칠할 수 있음
    - count dp
        - base case
            - 최대 두 개는 겹쳐도 되니까 첫 두 post에는 제약이 없는 것과 마찬가지
            - 첫번째 포스트는 k개의 옵션, 두번째 포스트까지는 k*k개
    - n= 3의 경우 2 * 2 + 2인 것 같은데
        - 아 n=3부터는 합으로 들어오나보다
        - 앞의 두 컬러가 같은 경우, 다른 경우 두 가지 경우의 수가 있겠군
        - 앞의 두 컬러가 같은 경우 → 나는 K-1개의 옵션이 있고
        - 앞의 두 컬러가 다른 경우 → 나는 k개의 옵션이 있네
    - n의 최소값은 1, k의 최소 값도 1
        - k가 1이고 n이 3보다 크면 제약을 어기게 되는데 늘 valid input이 들어온다고 가정하면 되려나?
    - current가 consecutive면
        - i-2, i-1이 같다는 의미
        - i-3과 i-2도 같을까? 그건 모르지
            - 아니 알지. i-2와 i-1이 같은데 i-3도 i-2랑 같으면 restriction 위배 → i-3은 반드시 i-2와 달라야함
- Trial
    - Top-down 예제 2/3
        
        ```python
        class Solution:
            def numWays(self, n: int, k: int) -> int:
                memo = {}
        
                # function
                def recur(i):
                    # base case
                    if i == 0:
                        return k
                    if i == 1:
                        return k * k 
                    # check memoized
                    if i in memo:
                        return memo[i]
                    # iteration of the recurrence relation
                    consecutive = k * (k-1)
                    free = (recur(i-1) - k) * k
                    memo[i] = consecutive + free
                    return memo[i]
                
                return recur(n-1)
        ```
        
    - Top-down 예제 1/3
        
        ```python
        class Solution:
            def numWays(self, n: int, k: int) -> int:
                memo = {}
        
                def recur(i):
                    # base case
                    if i == 0:
                        return k
                    if i == 1:
                        return k + (k * k-1)
                    # check memoized
                    if i in memo:
                        return memo[i]
                    # iteration of the recurrence relation
                    same = recur(i-2) * (k-1)
                    different = recur(i-1) 
                    memo[i] = same + different 
                    return memo[i]
                
                return recur(n-1)
        ```
        
- AC 코드
    - Top-down
        - 예제 결과에서 index를 오해하는 바람에 좀 더 길어짐
        
        ```python
        class Solution:
            def numWays(self, n: int, k: int) -> int:
                memo = {}
        
                def recur(i):
                    # base case
                    if i == 0:
                        return k
                    if i == 1:          
                        return k * k
                    # check memoized
                    if i in memo:
                        return memo[i]
                    # iteration of the recurrence relation
                    same = recur(i-2) * (k-1) # i-2 + two same color blocks(color option: k-1. different from the i-2th)
                    different = recur(i-1) * (k-1) # i-1 + one different color block (color option: k-1. diffent from the i-1th)
                    memo[i] = same + different
                    return memo[i]
                
                return recur(n-1)
        ```
        
    - Bottom-up(⚡️)
        
        ```python
        class Solution:
            def numWays(self, n: int, k: int) -> int:
                if n == 1:
                    return k
                # array
                dp = [0] * n
        
                # base case
                dp[0] = k
                dp[1] = k * k
                
                # recurrence relation
                for i in range(2, n):
                    same = dp[i-2] * (k-1)
                    diff = dp[i-1] * (k-1)
                    dp[i] = same + diff
                    
                return dp[-1]
        ```