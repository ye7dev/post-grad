# 343. Integer Break

Status: done, in progress
Theme: DP
Created time: January 31, 2024 9:26 AM
Last edited time: January 31, 2024 1:32 PM

- Progress
    - 숫자 n을 k개로 쪼개야 함 k는 2보다 크고 n보다 작음
        - 숫자 n을 n으로 나누면 1…1
        - 숫자 n을 n-1으로 나누면 1….2
        - 숫자 n을 n-2개로 나누면
            - 5 → 3 : 1 1 3 = 3 vs. 1 2 2 = 4
        - 숫자 n을 n//2 개로 나누면
            - n 짝수 → 2 … 2
            - n 홀수 → 2 … 3
        
        각 k에 대해 max product 구하고
        
        다시 거기서 max 구하면 되려나 
        
        K=3일때 max product 구하는 법?
        
        10을 3으로 나누면 나머지 1
        
        10을 2로 나누면 5 
        
        5 5 = 25
        
        10을 4로 나누면 나머지 2
        
        2 2 2 4 = 32
        
        2 3 3 2 = 36
        
        10을 5로 나누면
        
        2 2 2 2 2 = 32
        
        10 
        
        5 5 = 25
        
        3 4 3 = 36
        
        2 3 3 2 = 36
        
        2 2 2 2 2 = 32
        
        1 2 2 2 2 1 = 16
        
        12
        
        6 6 = 36
        
        4 4 4 = 64
        
        3 3 3 3 = 81
        
        2 2 3 3 2 = 72
        
        2 2 2 2 2 2 = 64
        
- Trial
    - Top-down : 14/50
        - 왜 5에서 6이 아니고 5가 나오지
            
            recur(5) 
            
            i = 2 → tmp = 2* recur(3) = 2 * 2 * 1 = 4 
            
        
        ```python
        class Solution:
            def integerBreak(self, n: int) -> int:
                # edge cases
                if n < 4: # 2, 3
                    return n-1 
        
                memo = [0] * (n+1)
                # function
                def recur(num):
                    # check memo
                    if num in memo:
                        return memo[num]
                    # base case
                    if num == 1:
                        return 1
                    if num <= 3:
                        return num-1
                    # recurrence relation
                    # no split
                    ans = num
                    for i in range(2, num):
                        tmp = i * recur(num-i)
                        ans = max(ans, tmp)
                    memo[num] = ans
                    return memo[num]
        
                return recur(n)
        ```
        
    - Top-down: 27/50
        
        ```python
        class Solution:
            def integerBreak(self, n: int) -> int:
                # edge cases
                if n < 4: # 2, 3
                    return n-1 
        
                memo = [0] * (n+1)
                # function
                def recur(num):
                    # check memo
                    if num in memo:
                        return memo[num]
                    # base case
                    if num <= 3:
                        return num
                    # recurrence relation
                    # no split
                    ans = num
                    for i in range(2, num):
                        tmp = i * recur(num-i)
                        ans = max(ans, tmp)
                    memo[num] = ans
                    return memo[num]
        
                return recur(n)
        ```
        
- Hint
    - 7~10까지 쪼개보면 규칙을 발견할 수 있다
        - 7
            - 7을 1개로 나누면 7
            - 2개 → 3 * 4 = 12
            - 3개 → 2 * 2 * 3 = 12
            - 4개 → 2 * 2 * 2 * 1 = 8
            - 5개 → 1 * 1 * 1 * 2 * 2 = 4
            - 6개 → 1 … 1 2 = 2
            - 7개 → 1
        - 8
            - 8
            - 4 * 4 = 16
                - 8//2 = 4
                - 2 ** 4 * 1
            - 2 * 2 * 4 = 16 < 3 * 3 * 2 = 18
                - 8//3 = 2, 8 % 3 = 2
                - 3**(8//3) * (8%3)
            - 2 2 2 2
                - 8 // 4 = 2
            - 2 2 2 1 1
                - 8 // 5 = 1
                - 8 % 5 = 3
        - 10
            - 10
            - 5 * 5 = 25
                - 10 // 2 = 5
            - 3 3 4
                - 10 // 3 = 3
                - 10 % 3 = 1
            - 10 // 4 = 2, 10 % 4 = 2
                - 2 2 2 2
                - 2 2 3 3 = 36
- AC 코드
    - DP는 아닌 것 같은데?
        
        ```python
        class Solution:
            def integerBreak(self, n: int) -> int:
                max_prod = 1
                for k in range(2, n+1):
                    q, r = divmod(n, k)
                    temp = [q] * k
                    cur_prod = 1
                    for i in range(k):
                        if i < r:
                            temp[i] += 1 
                        cur_prod *= temp[i]
                    max_prod = max(max_prod, cur_prod)       
                        
                return max_prod
        ```
        
    - Top-down
        - memo를 array로 써서 check memo 부분을 수정해야 했음. 사전에서 하는 것처럼 if num in memo 하면 array에서 값을 찾게 될 것
        - 그리고 input 숫자 자체가 2나 3이면 split 했을 때의 최대값을 return 해야하지만, 재귀 함수 들어오고 나서는 그 숫자 자체로 return 되어야 함
        
        ```python
        class Solution:
            def integerBreak(self, n: int) -> int:
                # edge cases
                if n < 4: # 2, 3
                    return n-1 
        
                memo = [0] * (n+1)
                # function
                def recur(num):
                    # check memo
                    if memo[num] != 0:
                        return memo[num]
                    # base case
                    if num <= 3:
                        return num
                    # recurrence relation
                    # no split
                    ans = num
                    for i in range(2, num):
                        tmp = i * recur(num-i)
                        ans = max(ans, tmp)
                    memo[num] = ans
                    return memo[num]
        
                return recur(n)
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def integerBreak(self, n: int) -> int:
                if n <= 3:
                    return n-1
                
                dp = [0] * (n+1)
                # base case
                for i in range(1, 4):
                    dp[i] = i
                
                for i in range(4, n+1):
                    for j in range(i):
                        dp[i] = max(dp[i], j * dp[i-j])
                
                return dp[-1]
        ```
        
- Editorial
    - Top-down
        - Intuition
            - num → 2개의 정수 i, num-i로 나누는 상황 가정
                - highest product: i * BEST
                - BEST : num-i를 쪼개서 얻을 수 있는 highest product
                    - original problem with a different input
            - dp(num)
                - return: num을 쪼개서 얻을 수 있는 highest possible product
            - base case (in general, no constraint)
                - num == 1 → return 1
                    - 숫자를 쪼갤 수 없으므로
                - num == 2 → return 2
                    - 숫자를 쪼개면 1 * 1 = 1만 되어서 쪼개지 않는 편이 나음
                - num == 3 → return 3
                    - 숫자를 쪼개면 1 * 2 = 2만 되어서 쪼개지 않는 편이 나음
                
                ⇒ if num < 4 → return num 
                
            - recurrence relation
                - 숫자를 쪼개지 않는 경우 → ans = num 촉화
                - 숫자를 쪼개는 경우
                    - 모든 가능한 split 시도. i : 2 → num(exclusive)
                        - 왜냐면 dp(0)이면 num이랑 0으로 나눈 건데, 그건 말이 안됨
                    
                    → ans = i * dp(num-i)가 더 크면 그걸로 update 
                    
            - recurrence relation 들어가기 전에 검사하라는데
                - base case랑 다른 건가? 다른 건 아니고 base case에서 constraint 적용한 후의 결과인듯.
                - num == 2 → return 1, num == 3 → return 2