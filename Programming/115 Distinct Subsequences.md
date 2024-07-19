# 115. Distinct Subsequences

Status: done, in progress
Theme: DP
Created time: November 14, 2023 5:35 PM
Last edited time: November 15, 2023 11:12 AM

- [x]  코드로 구현해서 풀기
- hard라 해설봄~
- 코드
    
    ```python
    class Solution:
        def numDistinct(self, s: str, t: str) -> int:
            m, n = len(s), len(t)
            # dp[i][j] string[:i] includes how many target[:j]
            dp = [[0]*(n+1) for _ in range(m+1)]
            # base case - empty string can be part of any substring 
            for i in range(m+1):
                dp[i][0] = 1 
            # transition
            for i in range(1, m+1):
                for j in range(1, n+1):
                    dp[i][j] = dp[i-1][j]
                    if s[i-1] == t[j-1]:
                        dp[i][j] += dp[i-1][j-1]
            return dp[-1][-1]
    ```
    
- 해설 한글로 옮기기
    - state: dp[i+1][j+1] (exclusive)
        - `S[0..j]` contains `T[0..i]`that many times as distinct subsequences.
        - column이 S, row가 T
        - substring s[:j+1]이 target substring t[:i+1]을 서로 다른 방식으로 몇 번 포함하는지
    - end: dp[len(t)+1][len(s)+1]
    - row-by-row로 채워감
    - base case
        - state를 다시 생각하면 dp[row][col]일 때, string[:col]이 target[:row]를 포함하고 있는 횟수
        - empty string은 empty string을 포함하고 있다
            - 사실 이런 게 헷갈리고 어떨 때 이런 가정을 하는지 확실히 모르겠지만 우선 이 문제에서는 그렇게 한다
            - dp[0][0] = 1
        - col이 0인 경우: string[:0] = “” empty string → 어떤 char도 포함할 수 없다
            - for i in range(1, len(t)+1): dp[i][0] = 0
        - row가 0인 경우: target[:] = “” empty string → 어떤 substring에도 포함될 수 있다 (한번씩)
            - for j in range(1, len(s)+1): dp[0][j] = 1
    - transition
        - current index의 string[col-1]이 target[row]과 같지 않은 경우(row-by-row)
            - 이전 상태의 값 유지 dp[i][j] = dp[i][j-1] (가로로)
        - 같은 경우
            - 이전에 subsequence 개수 dp[i][j-1] + 한 letter씩 둘다 물러난 거에 이번 거 같아서 subsequence 만드는 경우 dp[i-1][j-1]