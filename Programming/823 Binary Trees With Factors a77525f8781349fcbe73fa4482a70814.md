# 823. Binary Trees With Factors

Status: done, in progress
Theme: DP
Created time: February 5, 2024 11:21 AM
Last edited time: February 5, 2024 1:51 PM

- Progress
    - 문제 이해
        - 중복 숫자가 없는 arr. 모든 element가 1보다 크다
        - 이 숫자로 binary tree 생성 - 각 element는 몇 번이고 사용될 수 있음
        - non-leaf node의 값은 children value의 product와 같아야 함
        - 만들 수 있는 binary tree의 개수를 구하라 - 모듈로 연산
        - non-leaf node가 없는 경우 = 하나의 원소만 존재하는 경우는 하나의 valid tree가 될 수 있음
        - index 대신 값으로 state 저장해두는 게 좋을 듯
- Trial
    - bottom-up → 예제 1
        - 재귀식만 좀 어떻게 하면 될 듯
        
        ```python
        class Solution:
            def numFactoredBinaryTrees(self, arr: List[int]) -> int:
                mod = 10 ** 9  + 7
                dp = {num:1 for num in arr}
                
                for num in arr:
                    for q in arr:
                        if num == q:
                            continue 
                        if num % q == 0 and num // q in arr:
                            ways = (dp[num] * dp[num // q]) % mod 
                            if q != (num // q):
                                ways *= 2 
                                ways %= mod 
                            dp[num] += ways 
                print(dp)
                return sum(dp.values()) % mod
        ```
        
    - bottom-up → 32/48
        - inner for loop 돌면서 q가 left일 때도 더해지고, num // q 가 left일 때도 알아서 더해지기 때문에 곱하기 2는 어디에도 필요 없다
        
        ```python
        class Solution:
            def numFactoredBinaryTrees(self, arr: List[int]) -> int:
                mod = 10 ** 9  + 7
                dp = {num:1 for num in arr}
                
                for num in arr:
                    for q in arr:
                        if num == q:
                            continue 
                        if num % q == 0 and num // q in arr:
                            ways = (dp[q] * dp[num // q]) % mod 
                            dp[num] += ways 
                print(dp)
                return sum(dp.values()) % mod
        ```
        
- AC 코드
    - Bottom-up (🪇🐌)
        
        ```python
        class Solution:
            def numFactoredBinaryTrees(self, arr: List[int]) -> int:
                mod = 10 ** 9  + 7
                arr.sort()
                dp = {num:1 for num in arr}
                
                for num in arr:
                    for q in arr:
                        if num <= q:
                            continue 
                        if num % q == 0 and num // q in arr:
                            ways = (dp[q] * dp[num // q]) % mod 
                            dp[num] += ways 
                        
                return sum(dp.values()) % mod
        ```