# 712. Minimum ASCII Delete Sum for Two Strings

Status: done, in progress
Theme: DP
Created time: November 14, 2023 4:15 PM
Last edited time: November 14, 2023 5:35 PM

- [[**72. Edit Distance**](https://leetcode.com/problems/edit-distance/description/?envType=study-plan-v2&envId=dynamic-programming)](72%20Edit%20Distance%20fb0cf18fea83455e885dcee6a3b35ae4.md) 랑 비슷한 문제 같음. transition 식만 다르지
    - 마냥 비슷하지 않다. 그 문제의 transition 식을 엄청 정확히 이해하고 있어야 응용 가능
        - 이해했다 헤헤
    - 그리고 이문제에서는 삭제만 가능
- ord(’l’) → l에 해당하는 아스키 숫자 돌려줌
- 아스키 숫자는 알파벳 순서상 앞에 있을 수록 숫자가 작다
- 그리고 delete와 leet 사이의 답(let)를 보듯이 순서를 임의로 바꾸는 것은 안됨
- 코드
    
    ```python
    class Solution:
        def minimumDeleteSum(self, s1: str, s2: str) -> int:
            m, n = len(s1), len(s2)
            dp = [[float('inf')] * (n+1) for _ in range(m+1)]
            dp[0][0] = 0
            for i in range(1, m+1):
                dp[i][0] = sum([ord(char) for char in s1[:i]])
            for j in range(1, n+1):
                dp[0][j] = sum([ord(char) for char in s2[:j]])
            
            for i in range(1, m+1): # 1-> m
                for j in range(1, n+1): # 1-> n
                    if s1[i-1] == s2[j-1]:
                        dp[i][j] = dp[i-1][j-1]
                    else:
                        dp[i][j] = min(dp[i-1][j] + ord(s1[i-1]),
                                    dp[i][j-1] + ord(s2[j-1]),
                                    dp[i-1][j-1] + ord(s1[i-1]) + ord(s2[j-1]))
            return dp[-1][-1]
    ```