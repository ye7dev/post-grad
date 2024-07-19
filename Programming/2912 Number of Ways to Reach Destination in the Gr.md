# 2912. Number of Ways to Reach Destination in the Grid

Status: done, in progress, 🏋️‍♀️
Theme: DP
Created time: November 23, 2023 11:01 PM
Last edited time: November 24, 2023 12:52 PM

- [ ]  더 최적화할 여지가 많은 것 같음.
    - 예를 들어 이 코드 - matrix를 안 쓰고 이전 상태를 저장하는 변수들만 사용
        
        ```python
        class Solution {
         public:
          int numberOfWays(int R, int C, int k, vector<int>& source, vector<int>& dest) {
            long MOD = 1000000007L;
            long center = 1, samer = 0, samec = 0, other = 0;
            while (k-- != 0) {
              long prev_center = center;
              long prev_samer = samer;
              long prev_samec = samec;
              long prev_other = other;
              center = (prev_samer * (C - 1) + prev_samec * (R - 1)) % MOD;
              samer = (prev_samer * (C - 2) + prev_center + prev_other * (R - 1)) % MOD;
              samec = (prev_samec * (R - 2) + prev_center + prev_other * (C - 1)) % MOD;
              other = (prev_other * (C - 2) + prev_other * (R - 2) + prev_samec + prev_samer) % MOD;
            }
            if (source[0] == dest[0] && source[1] == dest[1]) return center;
            if (source[0] == dest[0]) return samer;
            if (source[1] == dest[1]) return samec;
            return other;
          }
        };
        ```
        
        - python translated
            
            ```python
            class Solution:
                def numberOfWays(self, R, C, k, source, dest):
                    MOD = 1000000007
                    center, samer, samec, other = 1, 0, 0, 0
                    
                    while k != 0:
                        k -= 1
                        prev_center = center
                        prev_samer = samer
                        prev_samec = samec
                        prev_other = other
                        
                        center = (prev_samer * (C - 1) + prev_samec * (R - 1)) % MOD
                        samer = (prev_samer * (C - 2) + prev_center + prev_other * (R - 1)) % MOD
                        samec = (prev_samec * (R - 2) + prev_center + prev_other * (C - 1)) % MOD
                        other = (prev_other * (C - 2) + prev_other * (R - 2) + prev_samec + prev_samer) % MOD
                    
                    if source[0] == dest[0] and source[1] == dest[1]:
                        return center
                    if source[0] == dest[0]:
                        return samer
                    if source[1] == dest[1]:
                        return samec
                    return other
            ```
            

프리미엄 전용 문제. grid는 오랜만이라 어려울 꺼니까 못풀어도 의기소침 말자. 

- 과정
    
    col, row 변경 횟수 합이 k가 되도록 이동했을 때 target에 도달하는 방법
    
    ```
    - [1,2] -> [1,1] -> [1,3] -> [2,3] : col -1, col +2, row +1 => 변화량 합 2
    - [1,2] -> [1,1] -> [2,1] -> [2,3] : col -1, row +1, col +2 => 변화량 합 2
    - [1,2] -> [1,3] -> [3,3] -> [2,3] : col +1, row +2, row -1 => 변화량 합 2
    - [1,2] -> [1,4] -> [1,3] -> [2,3] : col +2, col -1, row +1 => 변화량 합 2
    - [1,2] -> [1,4] -> [2,4] -> [2,3] : col +2, row +1, col -1 => 변화량 합 2
    - [1,2] -> [2,2] -> [2,1] -> [2,3] : row +1, col -1, col +2 => 변화량 합 2
    - [1,2] -> [2,2] -> [2,4] -> [2,3] : row +1, col +2, col -1 => 변화량 합 2
    - [1,2] -> [3,2] -> [2,2] -> [2,3] : row +2, row -1, col +1 => 변화량 합 2
    - [1,2] -> [3,2] -> [3,3] -> [2,3] : row +2, col +1, row -1 => 변화량 합 2
    ```
    
    3칸에 
    
    col col row 아니면 row row 
    
    ```python
    dp = {i:set() for i in range(0, k+1)}
            mod = 10**9+7
            dp[0].add(tuple(source))
            for i in range(1, n+1):
                if i == source[0]: continue
                dp[1].add((i, source[1]))
            for j in range(1, m+1):
                if j == source[1]: continue
                dp[1].add((source[0], j))
                
            if k == 1:
                if tuple(dest) in dp[1]: return 1
                else: 0
    
            if k == 2:
                count = 0
                for i in range(1, n+1):
                    if i == dest[0]: continue
                    if (i, dest[1]) in dp[1]:
                        count += 1
                for j in range(1, m+1):
                    if j == dest[1]: continue
                    if (dest[0], j) in dp[1]:
                        count += 1 
                return count
    
            dp[k].add(tuple(dest))
            for i in range(1, n+1):
                if i == dest[0]: continue
                dp[k-1].add((i, dest[1]))
            for j in range(1, m+1):
                if j == dest[1]: continue
                dp[k-1].add((dest[0], j))
            
            for idx_k in range(1, k-1):
                for cell in dp[idx_k-1]:
                    for j in range(1, m+1):
                        if j == cell[1]: continue
                        dp[idx_k].add((cell[0], j))
                    for i in range(1, n+1):
                        if i == cell[0]: continue
                        dp[idx_k].add((i, cell[1]))
            
            count = 0
            for cell in dp[k-2]:
                for j in range(1, m+1):
                    if j == cell[1]: continue
                    if (cell[0], j) in dp[k-1]:
                        count += 1 
                for i in range(1, n+1):
                    if i == cell[0]: continue
                    if (i, cell[1]) in dp[k-1]:
                        count += 1
            print(dp)
            return count
    ```
    
- 남의 풀이
    
    노션 이미지 업로드 너무 안된다 
    
    난 이성을 잃고 안자고 문제를 이해하겠다는 우를 범한다
    
- 같은 크기의 2차원 matrix에 넣는 값을 다르게 할 경우 변수 사이즈가 차이날까
    
    → 차이가 난다. 왜냐면 숫자 하나 당 갖는 크기가 엄청 다르기 때문 
    
    ```python
    >>> from sys import getsizeof
    >>> a = 42
    >>> getsizeof(a)
    12
    >>> a = 2**1000
    >>> getsizeof(a)
    146
    ```
    
    → 그래서 그렇게 모듈러 연산을 쓰는 거다. matrix 안에 있는 숫자의 크기를 줄여서 memory exceed를 방지하지만 결과는 같게 얻을 수 있으므로
    
    → 모듈러 연산 revisited
    
    $(a+b) \mod n  = [(a \mod n) + (b \mod n)] \mod n$
    
    $(a * b) \mod n = [(a \mod n) * (b \mod n)] \mod n$
    
- 내가 구운 코드~🍪
    
    ```python
    class Solution:
        def numberOfWays(self, n: int, m: int, k: int, source: List[int], dest: List[int]) -> int:
            # dp[k][0]: k번의 이동으로 목적지에 도달하는 방법의 가지 수 
            # dp[k][1]: k번의 이동으로 목적지와 같은 row에 도달하는 방법의 가지 수
            # dp[k][2]: k번의 이동으로 목적지와 같은 col에 도달하는 방법의 가지 수 
            # dp[k][3]: k번의 이동으로 목적지와 row도 다르고 col 도 다른 어느 cell에 도달하는 방법의 가지 수
            dp = [[0] * 4 for _ in range(k+1)] 
            if source == dest:
                dp[0][0] = 1 
            elif source[0] == dest[0]: 
                dp[0][1] = 1 # same row without any step
                dp[1][0] = 1 
            elif source[1] == dest[1]: 
                dp[0][2] = 1 # same col without any step
                dp[1][0] = 1 
            else:
                dp[0][3] = 1 
            if k == 1: return dp[1][0]
    
            mod = 10 ** 9 + 7
            for i in range(1, k+1):
                # dp[i-1][1]: i-1 step에 목적지와 같은 row에 도달하는 모든 방법의 가짓수
                # 그 방법들이 모두 한 번만 이동하기만 하면 목적지 도달 가능이니까 단순합 
                dp[i][0] = (dp[i-1][1] + dp[i-1][2]) % mod 
                # i-1에 목적지 도달 -> i에 목적지 제외한 같은 row에 있는 m-1개 셀에 도착 가능 
                # i-1에 같은 row 도착 -> 자기 자신이랑 목적지 제외한 m-2개 cell에 도착 가능 
                # i-1에 목적지와 다른 col, 다른 row에 도착 -> row만 이동해서 목적지 row에 맞춤. 
                # dp[i-1][3] 방법 하나 당 도착 가능한 cell도 하나. col은 이동 불가, row도 하나로 정해짐
                dp[i][1] = (dp[i-1][0] * (m-1) + dp[i-1][1] * (m-2) + dp[i-1][3]) % mod  
                # i-1에 목적지 도달 -> i에 목적지 제외한 같은 col에 있는 n-1개 cell에 도착 가능
                # i-1에 목적지와 같은 col 도달 -> 자기 자신과 목적지 제외한 n-2개 cell에 도착 가능 
                # i-1에 목적지와 다른 col, 다른 row에 도착
                #   -> col만 이동해서 목적지 col에 맞춤. 여기도 row 이동 불가, col 고정 
                dp[i][2] = (dp[i-1][0] * (n-1) + dp[i-1][2] * (n-2) + dp[i-1][3]) % mod 
                # i-1에 목적지와 같은 row에 도달 -> row 이동 시켜서 row, col 둘다 목적지와 다르게 
                #   -> row는 자기 시작점=목적지 row 1개 빼고 어디든 갈 수 있으므로
                # i-1에 목적지와 다른 row, 다른 col에 도착
                # i에 row나 col 둘 중에 하나만 이동 가능
                # row 이동 시 전체 n개에서 자기 자신과 목적지 두 개 제외 -> n-2
                # col 이동 시 전체 m개에서 자기 자신과 목적지 두 개 제외 -> m-2
                # 두 경우를 합하면 n+m-4  
                dp[i][3] = (dp[i-1][1] * (n-1) + dp[i-1][2] * (m-1) + dp[i-1][3] * (n+m-4)) % mod 
            return dp[k][0]
    ```
    
    깔꼼쓰 버전
    
    ```python
    class Solution:
        def numberOfWays(self, n: int, m: int, k: int, source: List[int], dest: List[int]) -> int:
            dp = [[0] * 4 for _ in range(k+1)] 
            if source == dest:
                dp[0][0] = 1 
            elif source[0] == dest[0]: 
                dp[0][1] = 1 
            elif source[1] == dest[1]: 
                dp[0][2] = 1
            else:
                dp[0][3] = 1 
    
            mod = 10 ** 9 + 7
            for i in range(1, k+1):
                dp[i][0] = (dp[i-1][1] + dp[i-1][2]) % mod 
                dp[i][1] = (dp[i-1][0] * (m-1) + dp[i-1][1] * (m-2) + dp[i-1][3]) % mod  
                dp[i][2] = (dp[i-1][0] * (n-1) + dp[i-1][2] * (n-2) + dp[i-1][3]) % mod 
                dp[i][3] = (dp[i-1][1] * (n-1) + dp[i-1][2] * (m-1) + dp[i-1][3] * (n+m-4)) % mod 
            return dp[k][0]
    ```
    
- 또 다른 남의 풀이
    
    #dp[i][0] number of ways to destination with i steps
    
    #dp[i][1] number of ways to same row with destination with i steps
    
    #dp[i][2] number of ways to same column with destination with i steps
    
    #dp[i][3] number of ways to the others with i steps
    
    ```python
    class Solution:
        def numberOfWays(self, n: int, m: int, k: int, source: List[int], dest: List[int]) -> int:
            MOD = 10**9 + 7
            dp = [[0]*4 for _ in range(k+1)]
            if source == dest:
                dp[0][0] = 1
            elif source[0] == dest[0]:
                dp[0][1] = 1
            elif source[1] == dest[1]:
                dp[0][2] = 1
            else:
                dp[0][3] = 1
            for i in range(1, k+1):
                dp[i][0] = (dp[i-1][1] + dp[i-1][2])%MOD
                dp[i][1] = (dp[i-1][0]*(m-1) + dp[i-1][1]*(m-2) + dp[i-1][3])%MOD
                dp[i][2] = (dp[i-1][0]*(n-1) + dp[i-1][2]*(n-2) + dp[i-1][3])%MOD
                dp[i][3] = (dp[i-1][1]*(n-1) + dp[i-1][2]*(m-1) + dp[i-1][3]*(m+n-4))%MOD
            return dp[k][0]
    ```