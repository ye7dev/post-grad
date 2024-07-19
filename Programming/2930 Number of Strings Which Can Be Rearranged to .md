# 2930. Number of Strings Which Can Be Rearranged to Contain Substring

Status: done, in progress, incomplete, 🏋️‍♀️
Theme: DP
Created time: November 27, 2023 11:08 AM
Last edited time: November 28, 2023 10:28 AM

- [x]  다시 한번 풀기
- [ ]  cache decorator 없이 풀 수 있는 solution 읽어보기
- 통과한 코드
    
    ```python
    class Solution:
        def stringCount(self, n: int) -> int:
            mod = 10 ** 9 + 7
    				# LEET
            L = 0b1000
            first_E = 0b0100
            second_E = 0b0010
            T = 0b0001
    				# empty/full
            empty = 0b0000
            complete = 0b1111
            
            @cache
            def count_ways(i, mask):
                if i == n:
                    return int(mask == complete)
                ways = count_ways(i+1, mask | L) 
                ways += count_ways(i+1, mask | T)
                if mask & first_E:
                    ways += count_ways(i+1, mask | second_E)
                else:
                    ways += count_ways(i+1, mask | first_E)
                ways += 23 * count_ways(i+1, mask)
                
                return ways % mod
            
            
            return count_ways(0, empty)
    ```
    
- 과정
    
    ```python
    class Solution:
        def stringCount(self, n: int) -> int:
            if n < 4:
                return 0 
            mod = 10 ** 9 + 7
            dp = [0] * (n+1) 
            dp[4] = 12
            for i in range(5, n+1):
                dp[i] = ((dp[i-1] % mod) * (i % mod) * 26) % mod
            return dp[-1]
    ```
    
    - 난 이거라고 생각했는데 왜 도저히 답이 안되는지 모르겠다
    - 4개로 leet를 만들 수 있는 방법은 정해져있고, 
    📦ㅣ📦 e 📦 e 📦 t 📦 총 5자리 중 하나에 26개 알파벳 중 하나를 넣어 만들면 된다고 생각했는데?
    - aleet로 넘어가면 📦a📦l📦e📦e📦t📦
        - 아 중복인 경우가 있구나 예를 들어 두번째 박스에 l을 넣으면 alleet인데 세번째 box에 l을 넣어도 alleet임
    - factorial을 써서 앞에서 사용한 Letter를 뒤에서는 못 쓰게 해볼까 만약에 알파벳이 6 자리면 6*5*4*3*2 = 6! / (6-5) !
    - 만약에 칸수가 26을 넘어가면? 📦ㅣ📦 e 📦 e 📦 t 📦 인데 알파벳은 2 자리라고 하면? 5C3 = 10
    
    ⇒ thinking process는 비슷했지만…ㅎㅎ 
    
- 남의 답안 이해하기 - DP
    
    <aside>
    🌟 1. 필요한 상태(leet letter 각각)를 이진법으로 표기 
    2. LEET 돌아가면서 현재 상태에 하나씩 더한 argument로 함수 하나씩 돌려서 return 되는 값 더해지도록 함 -E는 중복되지 않도록 앞의 E를 먼저 채운 경우에만 두번째 E를 붙여서 들어가도록 분기 
    3. LET 말고 나머지 알파벳 (26-3=23개) 중 하나를 더해서 argument로 삼고 새로운 함수 진입
    
    </aside>
    
    - 제약: 최종 string에 순서 상관없이 l 1개, t 1개, e 2개가 들어있기만 하면 됨
    - bit mask 이용
    - state (i, mask) : i번째 string, mask→ `leet` 중에서 우리가 선택한 게 뭐뭐 있는지 저장 ?
    - 모든 인덱스에 대해 다음과 같은 선택지
        - l, t 선택
        - 첫번째 e 혹은 두번째 e (leet에서)를 선택
        - 다른 아무 letter 선택
    - Bit mask 해석
        - 1111: 우리의 current string에서 LEET를 만드는 데 필요한 모든 letter가 선택된 상태
        - 1001: 우리의 current string에서 L과 T만 선택된 상태
    - 시간 복잡도
        - l은 0 또는 1개, e는 0, 1, 2 개 중 하나, t는 0 또는 1개 → 총 2*3*2=12개의 state 존재-at each position of the n length string
    - 배경지식
        - 0b0010 → ‘0b’ : 어떤 숫자가 이진법으로 쓰여있다는 것을 의미 + ‘0010’ : 이진법으로 표현하고자 하는 값
            
            ![Untitled](Untitled%20115.png)
            
            - 이미지와 상응하는 이진법 표기
                
                ```python
                EMPTY = 0b0000
                LEET = 0b1111
                L = 0b1000
                FIRST_E = 0b0100
                SECOND_E = 0b0010
                T = 0b0001
                ```
                
        - `@cache`
            - 어떤 함수 위에 decorator로 붙이면, 특정 argument 값에 대한 함수 계산 결과를 저장해뒀다가, 다음 번에 동일한 argument가 또 들어오면 처음부터 계산하는 대신 전에 저장해둔 값을 가져다가 바로 return 해서 속도 빨라지게 함
        - bit operation `mask | L`
            - mask랑 L 모두 둘다 이진법으로 표현된 변수
            - 각 bit 자리를 돌면서 둘 중에 하나라도 1이면 Return 1 else 0
            - L은 첫번째 자리만 1이고 나머지는 0
            - 기존 mask의 첫번째 자리가 0이었으면 = current string에 L이 없었으면, `mask | L` 연산으로 첫번째 자리가 1이 되고, current string에 L을 하나 추가한 상태를 의미
            - string index도 하나 들어서 추가한 L 다음 자리를 가리키도록 함
        - 계산 따라해보기
            
            
            | i | mask  | ways |
            | --- | --- | --- |
            | 0 | 0000 | dp(1, 1000) + dp(1, 0001) + dp(1, 0100) + 23*dp(1, 1000)  |
            | 1 | 1000 | dp(2, 1000) + dp(2, 1001) + dp(2, 1100) + 23*dp(2, 1000) |
            | 2 | 1000 | dp(3, 1000) + dp(3, 1001) + dp(3, 1100) + 23*dp(3, 1000)  |
            | 3 | 1000 | dp(4, 1000)  + dp(4, 1001) + dp(4, 1100) + 23*dp(4, 1000) 
            = 0 + 0 + 0 + 0 = 0  |
            | 4 | 1000, 1001, 1010, 1000 | mask ≠ leet → return 0  |
            | 1 | 0001 | dp(2, 1001) + dp(2, 0001) + dp(2, 0101) + 23*dp(2, 0001) |
            | 2 | 0001 | dp(3, 1001) + dp(3, 0001) + dp(3, 0101) + 23*dp(3, 0001)  |
            | 3 | 0001 | dp(4, 1001)  + dp(4, 0001) + dp(4, 0101) + 23*dp(4, 0001) 
            = 0 + 0 + 0 + 0 = 0  |
            | 1 | 0100 | dp(2, 1100) + dp(2, 0101) + dp(2, 0110) + 23*dp(2, 0100) |
            | 2 | 0100 | dp(3, 1000) + dp(3, 0101) + dp(3, 0110) + 23*dp(3, 0100)  |
            | 3 | 0100 | dp(4, 1000)  + dp(4, 1001) + dp(4, 1100) + 23*dp(4, 1000) 
            = 0 + 0 + 0 + 0 = 0  |
        
        하다 보니까 combination 만드는 거랑 비슷해서 풀러왔음