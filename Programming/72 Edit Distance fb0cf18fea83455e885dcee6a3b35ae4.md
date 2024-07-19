# 72. Edit Distance

Status: done, in progress
Theme: DP
Created time: November 14, 2023 3:22 PM
Last edited time: November 14, 2023 4:12 PM

- 최소값을 구할 때 dp table 초기 cell 값은 양의 무한대로 설정한다
- 식은 대충 안다 min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1 인데 각각의 경우가 헷갈려서 그런다
    - word2 → word1으로 방향을 잡는 다고 하면
        - dp[i-1][j] +1 → word2에서 letter 한 개를 지우고(+1) word1을 만드는 상황
        - dp[i-1][j-1] +1  word2에서 마지막 letter를 word1의 마지막 letter로 replacement(+1)
        - dp[i][j-1] + 1 → word2에서 word1[:-1]까지 만들고 word1의 마지막 letter를 추가(+1)
- i-m-row, j-n-col 익숙해져있어서 여기 맞춰서 짜는게 안전함
- 코드
    
    ```python
    class Solution:
        def minDistance(self, word1: str, word2: str) -> int:
            m, n = len(word1), len(word2)
            dp = [[501] * (n+1) for _ in range(m+1)]
    
            # base case
            dp[0][0] = 0
            for i in range(1, m+1): # 1 -> m
                dp[i][0] = len(word1[:i])
            for j in range(1, n+1): # 1 -> n
                dp[0][j] = len(word2[:j])
            
            # transition
            for i in range(1, m+1): # 1 -> m
                for j in range(1, n+1):
                    if word1[i-1] == word2[j-1]:
                        dp[i][j] = dp[i-1][j-1]
                    else:
                        dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1 
            return dp[-1][-1]
    ```