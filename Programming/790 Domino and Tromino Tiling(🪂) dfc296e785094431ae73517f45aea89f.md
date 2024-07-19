# 790. Domino and Tromino Tiling(🪂)

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP
Created time: January 15, 2024 5:56 PM
Last edited time: January 16, 2024 1:05 PM

- Process
    - 이게 무슨 말인지 모르겠음
        
        In a tiling, every square must be covered by a tile. Two tilings are different if and only if there are two 4-directionally adjacent cells on the board such that exactly one of the tilings has both squares occupied by a tile.
        
        → 대충 이렇게 이해하고 넘어가자 
        
        - 모두 같아야 같은 배치이고 하나라도 다르면 서로 다른 배치 방법이다
        - chat 선생님
            - Consider that each tile might cover more than one square. For example, think of a tile as a domino that covers two squares.
            - Two tilings are considered different if you can find at least one pair of adjacent squares (side by side, up and down, not diagonal) where a single tile covers both squares in one tiling, but in the other tiling, two different tiles are covering these two squares.
    
    n의 최소 값은 1 
    
    점화식 찾으려고 n = 5까지 그려보았으나 못 찾았다 
    
- AC 코드
    - Top-down
        
        ```python
        class Solution:
            def numTilings(self, n: int) -> int:
                f_cache, p_cache = {}, {}
                mod = 10 ** 9 + 7
        
                # two transition function
                def f_recur(k):
                    # base case
                    if k == 1:
                        return 1
                    if k == 2 :
                        return 2
                    # check memoized
                    if k in f_cache:
                        return f_cache[k]
                    # recurrence relation & save the result
                    f_cache[k] = f_recur(k-1) + f_recur(k-2) + 2 * p_recur(k-1)
                    # return the result
                    return f_cache[k] % mod
                
                # two transition function
                def p_recur(k):
                    # base case
                    if k == 2:
                        return 1
                    # check memoized
                    if k in p_cache:
                        return p_cache[k]
                    # recurrence relation & save the result
                    p_cache[k] = p_recur(k-1) + f_recur(k-2)
                    # return the result
                    return p_cache[k] % mod
        
                return f_recur(n)
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def numTilings(self, n: int) -> int:
                mod = 10 ** 9 + 7
                if n == 1:
                    return 1 
        
                # array
                f_cache = [0] * (n+1)
                p_cache = [0] * (n+1)
                
                # base case
                f_cache[1] = 1
                f_cache[2] = 2
                p_cache[2] = 1 
        
                # iteration
                for i in range(3, n+1):
                    f_cache[i] = (f_cache[i-1] + f_cache[i-2] + 2 * p_cache[i-1]) % mod
                    p_cache[i] = (f_cache[i-2] + p_cache[i-1]) % mod
               
                return f_cache[n]
        ```
        
- Editorial
    - Overview
        - 너비가 k인 보드에 대해, 가능한 타일링 방법 중 일부는 two previous fully covered boards로부터 구할 수 있다
            
            ![Untitled](Untitled%20216.png)
            
            - 그림에서 각각 노란색은 k=1일 때, 하늘색은 k=2, 핑크색은 k=3 일 때 사용된 bar
            - k와 k-1 사이의 관계
                - 세로로 domino 1개를 붙인다
                
                ![Untitled](Untitled%20217.png)
                
            - k와 k-2 사이의 관계
                - 가로로 눕힌 domino 2개를 붙인다
                
                ![Untitled](Untitled%20218.png)
                
        - 또 다른 일부 타일링 방법은 partially covered boards with a width of k-1로부터 구할 수 있다
            - partially covered board
                - 아래 그림에서 k= k-1 인 board에 기역자 타일을 올리면 부분 커버 - 좌하단 모서리 한 칸은 커버되지 않은 상태
                - 여기서 L shape tromino를 하나 더 붙이면 k board를 채울 수 있다
                
                ![Untitled](Untitled%20219.png)
                
        - 정의
            - fully covered board: 보드 위의 모든 타일이 도미노나 트로미노로 덮혀 있는 상태
            - partially covered board: fully covered board와 같지만, 우상단 혹은 우하단 모서리의 타일 하나?는 덮히지 않은 상태
                - 그러나 어느 모서리가 덮히지 않은 상태인지는 keep track 하지 않는다. 대칭이므로?
            - f(k): 너비가 k인 보드를 fully cover 하는 방법의 수
            - p(k): 너비가 k인 보드를 partially cover 하는 방법의 수
        - 위의 정의를 이용하면 너비가 k인 보드를 fully 덮는 방법의 수(f(k))를 결정할 수 있음
            - f(k-1)를 구한 다음, 각 방법의 타일링에다가 1 vertical domino를 하나 얹어서 k를 fully cover
            - f(k-2)를 구한 다음, 각 방법의 타일링에다가 2 horizontal dominos를 붙여서 k를 fully cover
                - 주의: 2 vertical dominos는 필요하지 않다. f(k-1)에서 vertical 하나 붙일 때 이 경우가 커버될 것이므로, 여기서 또 세버리면 중복 카운팅 발생
            - p(k-1)을 구한 다음 L자 모양 tromino를 붙여서 k를 fully cover
                - p(k-1) 가지 수에 곱하기 2를 한다
                    - horizontally symmetrical tiling 까지 고려
                        - 우하단 모서리가 하나 비어 있는 상태에서 (↱) 좌우반전한 L자 tromino(↵)를 붙인다고 생각
                        - 우상단 모서리가 하나 비어 있는 상태에서 테트리스 하듯이 ㄱ자 모양 tromino를 붙인다고 생각하는 경우
                        - 우하단 모서리는 상하반전(위로 접어 올린다고 생각)하면 우상단이 되어버림
            
            ⇒ f(k) = f(k-1) + f(k-2) + 2 * p(k-1)
            
        - 위의 정의를 이용하여 너비가 k인 보드를 partially 덮는 방법의 수(p(k))도 구할 수 있음
            - fully covered 너비 k-2 보드에 tromino 하나 붙이기
            - partially covered 너비 k-1 보드에 horizontal domino 하나 붙이기
            
            ⇒ p(k) = f(k-2) + p(k-1)
            
        - current state에 도달하는 방법의 수가 previous state에 도달하는 방법의 수에 의존 → DP!
    - **Approach 1: Dynamic Programming (Top-down)**
        - recurrence relation가 2개, memo도 2개
        - Algorithm
            1. f(n)에서 시작, n을 작게 해나가다가 base case에 도달 : f(1), f(2), p(2)
            2. f와 p에 대한 정의 사용
                - f(k): 너비 k인 보드를 fully cover 하는 방법의 수
                - p(k): 너비 k인 보드를 partially cover 하는 방법 수
            3. base case & results of subproblems → recursion call → final result (f(n))
                - stop condition: base case k ≤ 2
                - base case에 대한 값은 추가적인 재귀 호출 없이 바로 return
                    - f(1) = 1
                    - f(2) = 2
                    - p(2) = 1
                - memoization
                    - f_cache, p_cache 따로 만들어서 사용하거나 `@cache` wrapper 사용
            4. k≥2 인 경우 transition function에 따라 재귀 호출
                - f(k) = f(k-1) + f(k-2) + 2 * p(k-1)
                - p(k) = p(k-1) + f(k-2)
            5. 모든 재귀호출이 끝나면 f(n)의 값을 얻을 수 있다 
- modular 연산의 적용과 관련하여
    - 보통은 재귀식에서 적용하고 넘어가는 게 일반적이라고 함
    - 그리고 그 결과를 dp array에 저장하고 마지막엔 그걸 return 하기만 하니까 마지막엔 안 넣어도 된다
    - 재귀식 연산 종류에 따른 mod 연산적용 방식
        - 덧셈
            
            ```python
            result = (result + new_value) % mod
            ```
            
        - 뺄셈 - result가 음수가 안되게 조심
            
            ```python
            result = (result - value_to_subtract + mod) % mod
            ```
            
        - 곱셈
            
            ```python
            result = (value1 % mod * value2 % mod) % mod
            ```