# 935. Knight Dialer

Status: done, in progress
Theme: DP
Created time: February 1, 2024 11:52 AM
Last edited time: February 1, 2024 2:07 PM

- Progress
    - 문제 이해
        - 두 칸 세로로 움직이고 한 칸 가로로 움직이거나
        - 두 칸 가로로 움직이고 한 칸 세로로 움직이기
        - 그림
            
            ![Untitled](Untitled%20129.png)
            
        - chess 나이트 말 하나랑 하나의 핸드폰 패드가 주어짐
            
            ![Untitled](Untitled%20130.png)
            
        - 폰 패드 위에서는 파란색 칸에서만 서있을 수 있음
        - 정수 n이 주어졌을 때, 우리가 걸 수 있는 길이 n의 폰 번호가 서로 다른 몇 개가 나올 수 있는지
            - 시작할 때는 아무 숫자 칸에 말을 놓고, n-1 jump를 수행 → 길이 n의 숫자를 dial
            - 모든 jump는 knight jump 방식에 부합해야
        
    - 과정
        - count DP
        - 각 번호의 좌표 생성
        - 숫자를 다 들고 다녀야 하나?
            - 늘 이런게 어렵다
        - 시작 점 → jump1 → 숫자 1 → jump2 → 숫자 3
            - 두번의 jump로 총 세 자리 번호 완성
        - bottom-up에서는 사전을 거꾸로 뒤집어야 하려나?
- AC 코드
    - Top-down
        - 숫자를 다 들고 다닐 필요 없고 기회가 소진되었는지만 확인하면 됨
        - % mod 연산은 모드에 넣기 전이랑 마지막에 return 전 두 번
        
        ```python
        class Solution:
            def knightDialer(self, n: int) -> int:
                mod = 10**9 + 7
                # set up jump table 
                jump = [[] for _ in range(10)]
                jump[0] = [4, 6]
                jump[1] = [6, 8]
                jump[2] = [7, 9]
                jump[3] = [4, 8]
                jump[4] = [3, 9, 0]
                jump[6] = [7, 1, 0]
                jump[7] = [2, 6]
                jump[8] = [1, 3]
                jump[9] = [4, 2]
        
                memo = {}
                # function
                def recur(remain, square):
                    # check memo
                    if (remain, square) in memo:
                        return memo[(remain, square)]
                    # base case
                    if remain == 0:
                        return 1 
                    # recurrence relation
                    count = 0
                    for next_square in jump[square]:
                        count += recur(remain-1, next_square) 
                    memo[(remain, square)] = count % mod
                    return memo[(remain, square)]
                
                count = 0
                for i in range(10):
                    count += recur(n-1, i) 
                return count % mod
        ```
        
    - Bottom-up(⚡️)
        
        ```python
        class Solution:
            def knightDialer(self, n: int) -> int:
                mod = 10**9 + 7
                # set up jump table 
                jump = [[] for _ in range(10)]
                jump[0] = [4, 6]
                jump[1] = [6, 8]
                jump[2] = [7, 9]
                jump[3] = [4, 8]
                jump[4] = [3, 9, 0]
                jump[6] = [7, 1, 0]
                jump[7] = [2, 6]
                jump[8] = [1, 3]
                jump[9] = [4, 2]
        
                # dp[remain][num]: num에서 remain-1 개의 jump를 끝낼 수 있는 방법의 수
                dp = [[0] * 10 for _ in range(n)]
        
                # base case
                for i in range(10):
                    dp[0][i] = 1
                
                # recurrence case
                for remain in range(1, n):
                    for num in range(10):
                        for next_square in jump[num]:
                            dp[remain][num] += dp[remain-1][next_square]
                        dp[remain][num] %= mod
                
                return sum(dp[-1]) % mod
        ```
        
- Trial
    - Top-down
        - 누적된 번호를 들고 다닐 것인가?
        
        ```python
        class Solution:
            def knightDialer(self, n: int) -> int:
                mod = 10 ** 9 + 7
                phone = []
                # (3,0), (3,2) invalid cells
                for r in range(4):
                    for c in range(3):
                        phone.append((r, c)) 
                memo = {}
                def recur(i, coord, nums):
                    # check memo
                    state = (i, coord, nums)
                    if state in memo:
                        return memo[state]
                    x, y = coord
        
                    # base case 
                    if i == n: 
                        if 0 <= x < 4 and 0 <= y < 3:
                            if x == 3 and y in [0, 2]:
                                return 0 
                            else:
                                return 1 
                        else:
                            return 0 
        
                    two_verti = recur(i+1, (x+2, y+1), nums+[coord])
                    two_hori = recur(i+1, (x+1, y+2), nums+[coord])
        
                    memo[state] = (two_verti % mod) + (two_hori % mod)
                    return memo[state]
        ```
        
- Editorial
    - **Approach 1: Top-Down Dynamic Programming**
        - Intuition
            - 어떤 좌표에서 이동 가능한 다른 좌표를 미리 계산해둔다
                - table
                    
                    
                    | From | Can Jump To |
                    | --- | --- |
                    | 0 | 4(가로1, 세로 2), 6(가로 1, 세로 2) |
                    | 1 | 6(가로 2, 세로 1), 8(가로1, 세로 2) |
                    | 2 | 7(가로 1, 세로 2), 9(가로 1, 세로 2) |
                    | 3 | 4(가로 2, 세로 1), 8(가로 1, 세로 2) |
                    | 4 | 9(가로 2, 세로 1), 0(세로 2, 가로 1), 3(가로 2, 세로 1) |
                    | 5 | - |
                    | 6 | 7(가로 2, 세로 1), 1(가로 2, 세로 1), 0(세로 2, 가로1) |
                    | 7 | 6, 2 |
                    | 8 | 1, 3 |
                    | 9 | 4, 2 |
                - 범위 제한 두고 다 계산하자면
                    - x-2, x+2, x-1, x+1
                    - y-2, y+2, y-1, y+1
                    - 4 * 4 = 16개의 경우의 수 체크해야 함 매번
                    - 그리고 숫자 하나가 아니라 좌표(r,c)로 들고 다녀야 해서 저장공간도 더 필요함
            - 예) 현재 위치한 번호 7 → 5개의 jump 더 해야 하는 경우
                1. 7에서 2로 간 다음 2에서 4개의 jump 더 한다
                2. 7에서 6으로 간 다음 6에서 4개의 jump 더 한다 
                
                ⇒ 같은 문제 with difference square, fewer jumps remaining
                
            - `dp(remain, square)`
                - state definition: square 위치에서 remain 개의 jump를 마치는 방법의 수 return
                - base case: remain = 0
                    - jump를 모두 마쳤기 때문에 return 1
                - recurrence relation
                    - 현재 위치에서 이동할 수 있는 다른 모든 square 확보 (위의 table에서) → dp(remain-1, next_square)
                    - 가능한 모든 option이 내놓는 결과의 합
                - original problem
                    - dp(n-1, any square)
                        - starting square automatically contributes 1 toward our path of length n
                        - each jump will contribute 1 more