# 59. Spiral Matrix II

Status: done, in progress
Theme: matrix
Created time: February 19, 2024 11:44 AM
Last edited time: February 19, 2024 12:44 PM

- 문제 이해
    - given : integer n → 1에서 n^2까지 나선 형태로 도는 n * n matrix를 만들어라
- 과정
    - 언제 꺾어야 하는가
- AC 코드
    - Brute-force (🪇)
        
        ```python
        class Solution:
            def generateMatrix(self, n: int) -> List[List[int]]:
                matrix = [[0] * n for _ in range(n)]
                num = 1
                for j in range(n):
                    matrix[0][j] = num
                    num += 1 
                
                if n == 1:
                    return matrix
                
                r, c = 0, j
                directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
                dir_idx = 0 
                for fill in range(n-1, 0, -1):
                    for _ in range(2):
                        cur_dir = directions[dir_idx % 4]
                        for _ in range(fill):
                            r += cur_dir[0]
                            c += cur_dir[1]
                            matrix[r][c] = num
                            num += 1 
                        dir_idx += 1        
                
                return matrix
        ```
        
    - Editorial
        - cnt: value이자 counter. 1에서 시작해야 n^2까지 count 하는게 유효
        - while loop 들어오자마자 값을 넣고 시작
            - 이전 iteration에서 valid next index를 구하면서 끝남
        - validity check 용 임시 index를 먼저 구함
            - 근데 방향 전환 전에 구하는 거기 때문에 valid 범위를 넘을 수도 있어서 % n 연산 넣어서 값이 있는지 없는지 체크
            - 만약 값이 이미 채워진 상태라면
                - 예) 임시 idx (4, 2) → %n → (1, 2) : 앞에서 채워진 값
                - 방향을 전환해서 새로운 idx 구함
                    - 방향 전환 시에는 % 4 연산 필수. 그래야 맨 마지막 방향까지 갔다가 다시 맨 앞으로 올 수 있음
            - 다음 차례에 값을 넣을 r, c 확정해서 다음 iteration으로 보냄
        
        ```python
        class Solution:
            def generateMatrix(self, n: int) -> List[List[int]]:
                matrix = [[0] * n for _ in range(n)]
                r, c = 0, 0
                cnt = 1 # value and counter
        
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                dir_idx = 0 
                
                while cnt <= (n * n):
                    # fill out current cell 
                    matrix[r][c] = cnt 
                    cnt += 1 
        
                    # get next r, c 
                    cur_dir = directions[dir_idx]
                    next_r = r + cur_dir[0]
                    next_c = c + cur_dir[1]
        
                    # check validity of next r, c 
                    if matrix[next_r % n][next_c % n] != 0:
                        # change direction 
                        dir_idx = (dir_idx + 1) % 4 
                        cur_dir = directions[dir_idx]
                        # get valid next r, c
                        next_r = r + cur_dir[0]
                        next_c = c + cur_dir[1] 
                    
                    # update r, c 
                    r = next_r
        ```
        
- Editorial
    - **Approach 2: Optimized spiral traversal**
        - Algorithm
            - 하나의 layer를 만들기 위해 4 방향으로 이동
                - 각 방향을 반영하는 (x,y) 좌표로 구성된 array dir 이용
            - 언제 방향을 바꿔야 하는지를 알 수 있는지?
                - 특정 방향에서의 next row나 column이 non-zero value이면, 이미 traversed된 cell이므로 방향을 바꾼다
                - d: current direction index
                    - 다음 방향으로 갈 때는 (d+1) % 4
                        - 이렇게 해야 방향 1, 2, 3, 4 다 돌고 나서 다시 1로 돌아올 수 있다