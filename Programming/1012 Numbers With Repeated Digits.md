# 1012. Numbers With Repeated Digits

Status: done, in progress
Theme: DP
Created time: March 6, 2024 2:11 PM
Last edited time: March 7, 2024 5:45 PM

- Editorial
    - intuition
        - repeated digit 없는 숫자들을 구해서, n에서 뺀다
        - dp state
    - skills
        - python `permutations(iterable, num_pick)` method
            
            ```python
            >>> from itertools import permutations
            >>> x = [i for i in range(1, 10)]
            >>> x
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> permutations(x, 2)
            <itertools.permutations object at 0x1049433b0>
            >>> list(permutations(x, 2))
            [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (5, 1), (5, 2), (5, 3), (5, 4), (5, 6), (5, 7), (5, 8), (5, 9), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8), (6, 9), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 8), (7, 9), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 9), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)]
            >>> len(list(permutations(x, 2)))
            72
            ```
            
        - 여러 자리 수 N을 각 자리별로 분리해서 리스트에 넣어주기
            1. 숫자를 string 화 한다 
            2. map 함수를 통해 string 각 char 마다 int 함수 적용한다
            3. 리스트로 감싼다 
            
            ```python
            >>> N = 7896
            >>> L = list(map(int, str(N)))
            >>> L
            [7, 8, 9, 6]
            ```
            
        - math.perm(n, r)
            - n개에서 r개를 선택해서, 순서를 고려할 때, 만들 수 있는 조합의 개수
            
            ```python
            >>> from math import perm
            >>> perm(9, 1)
            9
            >>> perm(9, 2)
            72
            ```
            
    - Solution code
        
        ```python
        def numDupDigitsAtMostN(self, N):
        		# N보다 1 큰 숫자를 자리수별로 분리  
            L = list(map(int, str(N + 1)))
            n = len(L) 
        		# res: N보다 자릿수가 작은 수 중에서 without repeated digit 개수
            res = sum(9 * perm(9, i) for i in range(n - 1))
            s = set()
            for i, x in enumerate(L):
        				# i == 0: True면 1, 아니면 False
        				# 첫번째 자리 수는 0이 나올 수 없기 때문에 1에서부터 시작
                for y in range(i == 0, x):
                    if y not in s: 
                        res += perm(9 - i, n - i - 1)
                if x in s: break
                s.add(x)
            return N - res
        ```
        
- Trial
    - Bottom-up → 107(TLE) / 130
        
        ```python
        class Solution:
            def numDupDigitsAtMostN(self, n: int) -> int:
                if n < 11:
                    return 0
                # dp[i]: i is repeated num or not 
                dp = [False] * (n+1) 
                # base case: 0~10 -> covered        
                for i in range(11, n+1):
                    num = i
                    digits = []
                    while num:
                        q, r = divmod(num, 10)
                        if dp[q] or r in digits:
                            dp[i] = True
                            break
                        else: 
                            digits.append(r)
                            num = q 
        
                return sum(dp)
        
        ```
        
- review1
    - False code
        
        ```python
        from math import perm
        class Solution:
            def numDupDigitsAtMostN(self, n: int) -> int:
                # digit separation
                nums = list(map(int, str(n+1)))
                num_len = len(nums) # 99 -> 100 (3)
                res = 0
                # n보다 하나 작거나 같은? 자릿 수 
                for i in range(num_len-1): # 0, 1
                    # Q. perm(9, 0)은 뭘 의미? 1부터 시작해야 하나?
                    res += 9 * perm(9, i)
                # n과 같은 자리면서 n보다 작은 수들
                for i in range(num_len):
                    x = nums[i]
                    for candidate in range((i==0), 
                    # 숫자 하나 골랐기 때문에, 남은 건 num_len-1-i
                    res += (x-1) * perm(9-x, num_len-i-1)
                return res
                
        ```
        
    - AC code
        
        ```python
        from math import perm
        class Solution:
            def numDupDigitsAtMostN(self, n: int) -> int:
                # digit separation
                nums = list(map(int, str(n+1)))
                num_len = len(nums) # 99 -> 100 (3)
                res = 0
                # n보다 하나 작거나 같은? 자릿 수 
                for i in range(num_len-1): # 0, 1
                    # Q. perm(9, 0)은 뭘 의미? 1부터 시작해야 하나?
                    res += 9 * perm(9, i)
                # n과 같은 자리면서 n보다 작은 수들 
                digit_set = set()
                for i in range(num_len):
                    # i: num에서 몇 번째 자리에 위치한 숫자를 가리킬 것인지 
                    x = nums[i]
                    # candidate: 우리가 i 자리에 넣으려고 하는 값. x를 넘을 순 없음 
                    for candidate in range((i==0), x):
                        # 이미 앞에서 나온 숫자면 선택할 수 있는 option이 아님 -> continue 
                        if candidate not in digit_set:                     
                            # 숫자 하나 골랐기 때문에(candidate), 남은 건 num_len-1-i
                            # 9-i: 앞에서 고른 숫자의 개수 제외하고 남는 option 수 
                            res += perm(9-i, num_len-i-1)
                    if x in digit_set:
                        break 
                    digit_set.add(x)
                return n-res
                
        ```
        
    - perm(9, 0)
        - 앞에서 9를 곱해줌 - 1의 자리에서 취할 수 있는 옵션 수 (1~9)
        - 한 자리 수에 대한 계산은 그걸로 끝나기 때문에 곱하기 1을 해줄 뿐. 마침 그게 perm(9, 0)
        - 같은 의미로 perm(9, 1)의 경우 앞에서 1의 자리는 골랐고, 10의 자리에 대한 옵션 수를 의미
    - 빠진 부분
        - 같은 자리 수에 대한 경우의 수를 구할 때, set 활용을 잊었음
    - `if x in s: break`
        - 1332의 경우
            - 그보다 작은 1302 등등은 유의미하기 때문에 중복 조건 체크하기 전에 for loop을 먼저 돌지만
        - 일단 중복된 숫자가 나타났다고 하면 그보다 더 크면서 중복이 없는 숫자는 만들 수 없음
            - 예) 773
                - 771, 772는 이미 탈락
            - 예) 18865
                - 188XX는 모두 탈락
                - 그보다 작은 187XX는 앞선 for loop에서 이미 다 count 완료
    - `nums = list(map(int, str(n+1)))`
        - 왜 더하고 시작하는가
        - 나중에 nums의 각 자리수를 가지고 그보다 작은 숫자까지만 허용이 되는데
            - 원래 숫자가 98인 경우 그대로 쓰면
                - nums = [9, 8]이고, x = nums[i] = 8
                - 그럼 unique digit으로만 구성된 숫자에 원래 숫자 98은 들어갈 수가 없음
                    - 왜냐면 마지막 자리에서 y가 x보다 하나 작은 숫자까지만 돌기 때문에. 97까지만 고려
                    - 그럼 98을 따로 구해야 하는데 그럼 귀찮으니까
            - 98+1 해서 99로 쓰면
                - nums = [9, 9] 이고, x = nums[i] =9라서 y는 8까지 가능
                - 98도 커버 가능
            - 근데 +1을 해서 자릿수가 바뀌는 경우
                - nums = 99 → +1 하면 100
                - nums = [1, 0, 0]
                    - range(1, 1), range(0, 0), range(0, 0) 나와서 더해지는 경우의 수 없음