# 1155. Number of Dice Rolls With Target Sum

Status: done, in progress
Theme: DP
Created time: January 15, 2024 5:09 PM
Last edited time: January 15, 2024 5:56 PM

[](Untitled%206ad005a244354b0ebe8420a7cbea2944.md)

- Progress
    
    주사위를 순차적으로 던진다고 생각하자 
    
    target 값 기준으로 dp를 만들어야 하려나…
    
- Trial
    - 예제 1개 통과
        
        ```python
        class Solution:
            def numRollsToTarget(self, n: int, k: int, target: int) -> int:
                mod = 10 ** 9 + 7
                
                # array
                ## state dp[i][val]: number of ways to make up value val with i number of dices
                dp = [[0] * (target+1) for _ in range(n+1)]
                
                # base case - auto covered
                # no dices can make up value of zero
                # one dice can make value until k 
                for value in range(1, min(k+1, target+1)):
                    dp[1][value] = 1
                
                # iteration
                for i in range(2, n+1):
                    for value in range(i, target+1):
                        for face in range(1, k+1):
                            if value - face > 0:
                                dp[i][value] = dp[i-1][value-face]
        
                return dp[-1][-1] % mod
        ```
        
- AC 코드
    - by myself Bottom-up
        - 모든 face에 대해 value를 누적하는 것이 포인트였음
        
        ```python
        class Solution:
            def numRollsToTarget(self, n: int, k: int, target: int) -> int:
                mod = 10 ** 9 + 7
                
                # array
                ## state dp[i][val]: number of ways to make up value val with i number of dices
                dp = [[0] * (target+1) for _ in range(n+1)]
                
                # base case - auto covered
                # no dices can make up value of zero
                # one dice can make value until k 
                dp[0][0] = 1
                for value in range(1, min(k+1, target+1)):
                    dp[1][value] = 1
                
                # iteration
                for i in range(2, n+1):
                    for value in range(i, target+1):
                        for face in range(1, k+1):
                            if value - face > 0:
                                dp[i][value] += dp[i-1][value-face]
        
                return dp[-1][-1] % mod
        ```