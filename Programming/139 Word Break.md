# 139. Word Break

Status: done, in progress, incomplete
Theme: DP
Created time: November 13, 2023 6:51 PM
Last edited time: November 14, 2023 11:23 AM

- i, j, k 나눠서 하는 건 상관 없는데 dp table을 2차원으로 만들 필요는 없다. 왜냐하면 index 0부터 시작해서 하나라도 막히면 뒤에는 무조건 false이고, 중간부터 시작해서 되는 경우에 true를 줄 수 없기 때문
- [ ]  dp를 n+1이 아니라 n으로 두고 풀 수 있는 방안 탐구-특히 wordDict를 iterate 하면서…
- 내가 푼 코드(개선 여지 있음)
    
    ```python
    class Solution:
        def wordBreak(self, s: str, wordDict: List[str]) -> bool:
            dp = [False] * (len(s) +1)
            dp[0] = True 
            for i in range(1, len(s)+1):
                for j in range(i):
                    if dp[j] and s[j:i] in wordDict:
                        dp[i] = True 
                        break 
            return dp[-1]
    ```