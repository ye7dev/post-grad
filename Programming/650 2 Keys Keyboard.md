# 650. 2 Keys Keyboard

Created time: May 17, 2024 2:51 PM
Last edited time: May 17, 2024 3:32 PM

- scratch
    
    for loop을 어떤 순으로 돌아야 할지 모르겠다 
    
    우선 copy 해둔 char 수가 1개일 때~n-1개일 때의 상태를 보자 
    
    ```python
    if num_char == prev_copy + 1:
      dp[num_char] = dp[num_char-prev_copy] + 2
    else:
      dp[num_char] = dp[num_char-prev_copy] + 1 
    ```
    
    prev_copy = 1 
    
    dp[2] = dp[2-1] + 2 = dp[1] + 2 = 2
    
    dp[3] = dp[3-1] + 1 = dp[2]+1 = 3 
    
    dp[4] = dp[4-1] + 1 = 4
    
    prev_copy = 2
    
    dp[3] = dp[3-2] + 2?
    
    - 이건 성립 안되지 않나 어떻게 문자가 하나일 때 prev_copy가 2일 수가
    
    ```python
    if num_char - copied_char < copied_char:
        continue 
    if num_char - copied_char = copied_char:
        dp[num_char] = min(dp[num_char], dp[copied_char] + 2)
    else:
        dp[num_char] = min(dp[num_char], dp[num_char-copied_char] + 1)
    ```
    
    num_char = 3, copied_char = 2
    
    num_char - copied_char = 1 < 2 → continue ok 
    
    num_char = 3, copied_char = 1
    
    dp[3] = min(dp[3], dp[3-1]+1) = dp[2]+1 = 3 
    
- Trial
    - 예제 통과 + 5/126
        
        ```python
        class Solution:
            def minSteps(self, n: int) -> int:
                dp = [float('inf')] * (n+1)
                # base case
                dp[1] = 0
                # recursive case
                for copied_char in range(1, n):
                    for num_char in range(2, n+1):
                        if num_char - copied_char < copied_char:
                            continue 
                        if num_char - copied_char == copied_char:
                            dp[num_char] = min(dp[num_char], dp[copied_char] + 2)
                        else:
                            dp[num_char] = min(dp[num_char], dp[num_char-copied_char] + 1)
                return dp[-1]
        ```
        
        - 반례: dp[5] = 5
            - dp[5] = dp[3] + 2 가능?
                - 불가능 왜냐면 dp[3]은 aa + a 그러니까 last copy가 a 하나 짜리인데
                - 여기서 불쑥 aa가 last copy가 될 수 없기 때문이지
            - copy를 하나 했으면 하나로 쭉 가고, 두개 했으면 두 개로 쭉 가야 할 듯
            - dp[6] = dp[4] + 1
            - dp[4] = dp[2] + 2
            - dp[n] = dp[n//2] + 2
            - dp[8] = dp[4] + 2 or dp[6] + 1
    - 118/126
        
        ```python
        class Solution:
            def minSteps(self, n: int) -> int:
                dp = [float('inf')] * (n+1)
                # base case
                dp[1] = 0
                # recursive case
                for copied_char in range(1, n):
                    for num_char in range(2, n+1):
                        if num_char % copied_char != 0:
                            continue 
                        if num_char // copied_char == 2:
                            dp[num_char] = min(dp[num_char], dp[copied_char] + 2)
                        else:
                            dp[num_char] = min(dp[num_char], dp[num_char-copied_char] + 1)
                return dp[-1]
        ```
        
- AC code
    - chat GPT
        
        ```python
            dp = [0] * (n + 1)
            for i in range(2, n + 1):
                dp[i] = i  
                for j in range(1, i):
                    if i % j == 0:
                        dp[i] = min(dp[i], dp[j] + (i // j))
        
            return dp[n]
        
        ```
        
    - Editorial
        
        ```python
        class Solution(object):
            def minSteps(self, n):
                ans = 0
                d = 2 **# 필요한 동작 수. copy 하는 단어 수가 아님** 
                while n > 1: # n = i 
                    while n % d == 0: 
                        ans += d
                        n /= d
                    d += 1
                return ans
        ```
        
        - 예- n이 12이고, d가 2라면
            - 동작 수 2개로 12를 만든다는 뜻
            - 그럼 dp[6]상태에서, 복사 1번 + 붙여넣기 1번 하면 dp[12]가 됨
            - n//d = 12//2 = 6 ← 나머지 작업의 크기
        - 예-n이 6, d가 2
            - 동작 수 2개로 6을 만든다는 뜻
            - 복사 1번 + 붙여넣기 1번 해서 6이 되려면 dp[3]를 1번 복사하고 붙여넣기 2번 하는 것을 의미
            - n//d = 6 // 2 =3 → 3이 나머지 작업의 크기
        - 예-n이 3, d가 2 → 나머지가 0으로 떨어지지 않기 때문에 d를 하나 키운다
            - d= 3 → 1번의 복사와 2번의 붙여넣기로 dp[3]을 만든다는 뜻
            - dp[1]을 1번 복사하고 두번 붙여넣으면 dp[3]
            - 3//3 = 1 → 나머지 작업의 크기
        - n = 1이 되면서 outer while loop break
        - 답은 2 + 2 + 3 = 7