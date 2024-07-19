# 5. Longest Palindromic Substring

Status: done, in progress
Theme: DP
Created time: November 13, 2023 4:48 PM
Last edited time: November 14, 2023 10:09 AM

- 여러번 했던 건 데 또 헷갈려서 슬프네
- edge case가 length = 1, 2였던 건 기억이 남
- 근데 dp[i][i] = True인지 dp[i][i+1] = True 헷갈림
- 헷갈렸던 점
    1. dp table 크기 : (n+1) * (n+1)로 했다. 그래야 dp[i][i+1]로 s[i]를 표현할 수 있다 
    2. edge case에 length=2는 왜 필요한가? 왜냐면 for loop transition 때는 dp[i+1][i+length-1]=True인지 봐야 하는데 length가 2이면 dp[i+1][i+2-1] = dp[i+1][i+1] = False가 되어서 실패 
    3. 점화식 length 범위, i 범위 설정 
        - len(s[i:i+length]) = length
            - s[i], s[i+1], … s[i+length-1] → 0부터 length-1개 = 1부터 length 개
        - dp current cell(update 대상) : dp[i][i+length]
        - i+length는 n을 넘을 수 없다 (dp table column 최대 index: n)
            - i + length ≤ n → i ≤ n-length → i < n-length+1
            - i = 0 일 때 i+length ≤ n → length ≤ n → length < n+1
- 코드 - 좀 느리지만 직관적
    
    ```python
    class Solution:
        def longestPalindrome(self, s: str) -> str:
            n = len(s)
            dp = [[False] * (n+1) for _ in range(n+1)]
            max_len = 1
            start = 0
            # edge case 1) len = 1 
            for i in range(n):
                dp[i][i+1] = True # exclusive of right index 
            # edge case 2) len = 2
            for i in range(n-1): # i+1 = n-1 -> i = n-2 -> range(n-1)
                if s[i] == s[i+1]:
                    start = i
                    max_len = 2 
                    dp[i][i+2] = True 
            for length in range(3, n+1): # 0+k = n -> k = n -> range(n+1)
                for i in range(n-length+1): # x+k-1 = n-1 -> x = n-k -> range(n-k+1)
                    if s[i] == s[i+length-1] and dp[i+1][i+length-1]:
                        dp[i][i+length] = True 
                        if length > max_len:
                            start = i 
                            max_len = length
            return s[start:start+max_len]
    ```