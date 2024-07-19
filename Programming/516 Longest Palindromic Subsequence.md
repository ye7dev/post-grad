# 516. Longest Palindromic Subsequence

Status: done
Theme: DP
Created time: November 14, 2023 11:36 AM
Last edited time: November 14, 2023 3:21 PM

- 가능한 subsequence 길이로 접근해야 함
- 제일 edge 부분 두 letter가 같을 때, 그 사이 부분을 어떻게 처리해야 할지 헷갈림
    - True/False 이면 모르겠는데 그게 아님
    - 예를 들어 acbbda라고 할 때, 양 끝 a는 맞지만, dp[2:5]는 2일텐데 그렇다고 dp[:n]을 4이라고 하는 것도 말이 안됨 → 되는 것 같다 왜냐면 by deleting some or no elements. 사이에 cd 빼면 4다
- 포인트는 뭐가 먼저 계산되는지 계산 방향을 잡는 것
    - baa : i(도착점)=2, j(시작점)=0 일 때, 우선 b와 a는 서로 다름 → 근데 사람 눈으로 보면 aa가 palindrome이라서 dp[j+1][i]를 그대로 가져오는 게 한가지 답일 수 있음 → 이 경우 j가 순방향으로 진행하면 j+1은 아직 계산이 되어 있지 않음 → j를 역방향으로 가져오는 게 신의 한 수
    - aab : 여기는 반대로 aa가 dp[j][i-1] 즉 시작점이 하나 당겨진 상태. 근데 우리가 for loop을 돌 때 하나의 i에 대해 모든 j를 다 싹 돌고, 그리고 나서 다음 i+1로 넘어감. 즉 j의 값과 상관없이 i-1로 끝나는 칸의 값들은 이미 모두 계산이 된 상태
    - 그래서 결국 마지막 처음 letter가 다른 경우에는, 앞에서 부터 순방향(도착점 i가 당겨진 상태)와 뒤에서부터 역방향(j가 한칸 미뤄진 상태)의 최대값을 가져가면서 이전의 최적 상태를 유지해나가는 전략을 사용해야 함
- 뿌듯 코드
    
    ```python
    class Solution:
        def longestPalindromeSubseq(self, s: str) -> int:
            n = len(s)
            dp = [[0]*n for _ in range(n)]
            for i in range(n):
                dp[i][i] = 1 # column index inclusive
            for i in range(1, n):
                for j in range(i-1, -1, -1):
                    if s[i] == s[j]:
                        if i-j == 1: dp[j][i] = 2 
                        else: dp[j][i] = dp[j+1][i-1] + 2 
                    else:
                        dp[j][i] = max(dp[j+1][i], dp[j][i-1])
                
            return max(dp[0])
    ```