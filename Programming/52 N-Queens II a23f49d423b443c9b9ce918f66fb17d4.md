# 52. N-Queens II

Status: in progress, with help
Theme: backtracking
Created time: December 4, 2023 4:20 PM
Last edited time: December 5, 2023 12:58 PM

- [ ]  속도 빠른 코드로 풀어보기
- [x]  처음부터 다시 풀어보기
- backtracking 실습 hard 문제
- 과정
    - 뼈대 코드에서 직관적이지 않은 부분
        - row가 n-1이면 count += 1
            - n개의 queen을 n개의 row에 하나씩 세웠다는 의미에서 그런 것 같은데
            - row 하나를 지나칠 때마다 퀸을 반드시 하나 세우고 넘어간다는 부분이 어딘지 안 다가옴
        - row는 input이고, col이 for loop
        - 만약에 현재 cell에 놓기 어려운 것으로 판명되면, row+1 해서 재귀호출
        - remove_queen은 현재 cell에 놓던 놓지 않던 실행 → 왜?
- 가이드 보고 짠 코드
    
    ```python
    class Solution:
        def totalNQueens(self, n: int) -> int:
            if n == 1: return 1 
            taken = []
            def backtrack_nqueen(row=0, count=0):
                for col in range(n):
                    if is_not_under_attack(row, col):
                        place_queen(row, col)
                        if row + 1 == n:
                            count += 1 
                    else:
                        count = backtrack_nqueen(row+1, count)
                    remove_queen(row, col)
                return count 
            def is_not_under_attack(row, col):
                if (row, col) in taken: return False
                for queen in taken:
                    q_row, q_col = queen
                    # same col or row
                    if q_row == row or q_col == col:
                        return False
                    # on diagonal 
                    if abs(row-q_row) == abs(col-q_col):
                        return False
                return True
            def place_queen(row, col):
                taken.append((row, col))
            def remove_queen(row, col):
                taken.pop()
        
            return backtrack_nqueen()
    ```
    
    - Editorial
        - queen을 하나씩 놓고, 모든 가능성이 소진되면 하나의 queen을 제거함으로써 backtrack → 그걸 다른 곳에 둔다
        - backtracking 구현
            - 현재 상태에 변화를 주고 → backtrack 함수 재귀로 다시 호출 → call이 return 되고 나면 맨 처음에 주었던 변화를 다시 취소한다
                
                ```python
                for col in range(n):
                  if is_not_under_attack(row, col):
                			# 현재 상태에 변화 
                      place_queen(row, col)
                      if row + 1 == n:
                          count += 1 
                  else:
                			# 재귀 호출 
                      count = backtrack_nqueen(row+1, count)
                	# count return 되고 나면 맨 처음에 주었던 변화를 undo
                  remove_queen(row, col)
                ```
                
        - encoding state
            - row 당 queen이 하나만 들어가도록 하기 위해, integer argument to the function `row`
                - 이번 row에 queen이 놓이면 다음 함수 콜은 무조건 row+1의 argument를 받는다
            - col 당 하나의 queen을 놓기 위해 set을 사용
                - queen을 놓으면 놓은 col index를 set에 추가
            - 대각선 경우 처리
                - 대각선에 놓인 사각형들은 row-col 차(difference) 값이 모두 같다
                    
                    ![Untitled](Untitled%20113.png)
                    
                - anti-대각선에 놓인 사각형들은 row+col 합이 상수다
                    - 우상(0, 7)에서 시작하는 경우, (1, 6)으로 한 칸 내려오면 row는 +1, col은 -1 → 서로 상쇄되어 합은 이전과 동일
                    
                    ![Untitled](Untitled%20114.png)
                    
                - queen을 하나 놓을 때마다 그 퀸이 속한 대각선, 반대대각선을 계산해야 한다
                - column 처럼 대각선들에 대해서도 각각의 set을 운용
                    - [ ]  column처럼 index가 있는 것도 아닌데 set 안에 어떤 값을 추가하지?
        - 알고리즘
            - `backtrack` function
                - board state를 유지하기 위해 4개의 argument 받음
                - `row` : 이번에 퀸을 놓을 row
                - `col_set`, `diag_set`, `anti_diag_set` : 이미 퀸을 놓은 자리를 표시하기 위해
            1. current row가 n보다 크면 solution을 찾은 것이니 1을 return 
            2. `solutions=0` 으로 local variable 초기화 
                
                ↳ current board state로 얻을 수 있는 가능한 solution의 개수 표현 
                
            3. current row(argument로 받아옴)의 column iteration
                - 각 col에서 cell (row, col)에 queen 놓기 위한 시도
                - cell이 속한 diagonal, anti-diagonal 계산
                - current col, diagonal, anti-diagonal에 queen이 없는 것으로 확인되면 cell에 queen을 놓는다
                - 그럴 수 없으면 현재 column skip 하고 다음 column으로 넘어간다
            4. queen을 놓는데 성공하면 세 가지 set을 update 한 뒤, `row+1` 의 argument로 함수를 재귀적으로 다시 부른다 
            5. board에 3번에서 새롭게 놓인 퀸을 포함한 상태에서 4번의 재귀콜이 들어간다. 4번의 재귀콜이 끝나고 나면, 3번의 자리에서 퀸을 다시 제거함으로써 backtracking - 4에서 update 했던 set들도 원복 
    - Editorial 보고 짠 코드
        
        ```python
        class Solution:
            def totalNQueens(self, n: int) -> int:
                if n == 1: return 1 
                col_set, diag_set, anti_diag_set = set(), set(), set()
                def backtrack_nqueen(row=0, count=0):
                    for col in range(n):
                        if is_not_under_attack(row, col):
                            place_queen(row, col)
                            if row + 1 == n:
                                count += 1 
                        else:
                            count = backtrack_nqueen(row+1, count)
                        remove_queen(row, col)
                    return count 
                def is_not_under_attack(row, col):
                    if col in col_set: return False
                    if (row, col) in diag_set or (row,col) in anti_diag_set:
                        return False
                    return True
                def place_queen(row, col):
                    col_set.add(col)
                    # calculate diagonal 
                    diff, comb = row-col, row+col
                    for r in range(n):
                        for c in range(n):
                            if r-c == diff: 
                                diag_set.add((r, c))
                            if r+c == comb:
                                anti_diag_set.add((r, c))
                def remove_queen(row, col):
                    if col in col_set:
                        col_set.remove(col)
                    diff, comb = row-col, row+col
                    for r in range(n):
                        for c in range(n):
                            if r-c == diff and (r,c) in diag_set:
                                diag_set.remove((r, c))
                            if r+c == comb and (r,c) in anti_diag_set:
                                anti_diag_set.remove((r, c))
                return backtrack_nqueen()
        ```
        
    - Editorial 재구성해서 통과한 코드
        
        ```python
        class Solution:
            def totalNQueens(self, n: int) -> int:
                if n == 1: return 1 
                col_set, diag_set, anti_diag_set = set(), set(), set()
                def backtrack_nqueen(row=0, count=0):
                    for col in range(n):
                        if is_under_attack(row, col):
                            continue
                        else:
                            place_queen(row, col)
                            if row + 1 == n:
                                count += 1 
                                
                        count = backtrack_nqueen(row+1, count)
                        remove_queen(row, col)
                    return count 
                def is_under_attack(row, col):
                    if col in col_set: return True
                    diff, comb = row - col, row + col
                    if diff in diag_set or comb in anti_diag_set:
                        return True
                    return False
                def place_queen(row, col):
                    col_set.add(col)
                    diff, comb = row-col, row+col
                    diag_set.add(diff)
                    anti_diag_set.add(comb)
                def remove_queen(row, col):
                    col_set.remove(col)
                    diff, comb = row-col, row+col
                    diag_set.remove(diff)
                    anti_diag_set.remove(comb)
                return backtrack_nqueen()
        ```
        
        - if-continue 관련하여
            - 아래와 같이 돌리면 에러 난다
                
                ```python
                def test(num):
                    if num < 3:
                        continue
                    else:
                        print('num is over 3')
                    print('Would you be able to see this message?')
                ```
                
                ```python
                SyntaxError: 'continue' not properly in loop
                ```
                
                - 근데 위의 코드는 어떻게 돌아간거지? → 왜냐면 for loop이 윗단에 있었으니까
    - 더 깔끔한 코드
        
        ```python
        class Solution:
            def totalNQueens(self, n: int) -> int:
                if n == 1: return 1 
                col_set, diag_set, anti_diag_set = set(), set(), set()
        
                def backtrack_nqueen(row=0, count=0):
                    for col in range(n):
                        if not is_under_attack(row, col):
                            place_queen(row, col)
                            if row + 1 == n:
                                count += 1 
                            count = backtrack_nqueen(row+1, count)
                            remove_queen(row, col)
                    return count 
        
                def is_under_attack(row, col):
                    if col in col_set: return True
                    diff, comb = row - col, row + col
                    if diff in diag_set or comb in anti_diag_set:
                        return True
                    return False
        
                def place_queen(row, col):
                    col_set.add(col)
                    diff, comb = row-col, row+col
                    diag_set.add(diff)
                    anti_diag_set.add(comb)
        
                def remove_queen(row, col):
                    col_set.remove(col)
                    diff, comb = row-col, row+col
                    diag_set.remove(diff)
                    anti_diag_set.remove(comb)
        
                return backtrack_nqueen()
        ```
        
    - chat gpt가 수도 코드에 맞춰서 짜준 코드(통과함)
        - 이전 코드
            - 위에는 추가 메모리 set 3개 사용
            - invalid option(if under attack)에서 아무것도 안 함
        - 이번 코드
            - board라는 길이 n짜리 메모리 하나 사용
                - board[row] = 해당 row에서 queen이 위치한 col. 해당 row에 queen이 없으면 -1
            - invalid option 시에 명시적으로 범위 좁혀서 다음으로 넘어감
        
        ```python
        class Solution:
            def totalNQueens(self, n: int) -> int:
        
                def is_not_under_attack(row, col):
                    for prev_row in range(row):
                        # Check column and diagonal attacks
                        if board[prev_row] == col or \
                           board[prev_row] - prev_row == col - row or \
                           board[prev_row] + prev_row == col + row:
                            return False
                    return True
        
                def place_queen(row, col):
                    board[row] = col
        
                def remove_queen(row, col):
                    board[row] = -1
        
                def backtrack(row=0, count=0):
                    for col in range(n):
                        if is_not_under_attack(row, col):
                            place_queen(row, col)
                            if row + 1 == n:
                                count += 1
                            else:
                                count = backtrack(row + 1, count)
                            remove_queen(row, col)
                    return count
        
                # Initialize the board
                board = [-1] * n
                return backtrack()
        ```
        
    
- 다시 풀 때 막혔던 점
    - UnboundLocalError: local variable 'count' referenced before assignment
        - backtrack_nqueen 함수 밖의 함수에서 count 선언해서 읽어올 줄 알았는데 아니었음
        - argument로 넣어주니까 되었음
    - template에 잘 맞지만 속도는 좀 느림
        - 코드
            
            ```python
            class Solution:
                def totalNQueens(self, n: int) -> int:
                    board = [-1] * n
                    def backtrack_nqueen(row=0, count=0):
                        for col in range(n):
                            if is_not_under_attack(row, col):
                                place(row, col)
                                if row + 1 == n:
                                    count += 1 
                                else:
                                    count = backtrack_nqueen(row+1, count)
                                remove(row, col)
                        return count 
                    
                    def is_not_under_attack(row, col):
                        for prev_row in range(row):
                            prev_col = board[prev_row]
                            if prev_col == col:
                                return False
                            # on diagonal
                            if prev_row - prev_col == row - col:
                                return False
                            # on anti-diagonal
                            if prev_row + prev_col == row + col:
                                return False
                        return True 
                    
                    def place(row, col):
                        board[row] = col 
                    
                    def remove(row, col):
                        board[row] = -1 
            
                    return backtrack_nqueen()
            ```
            
    - 속도 빠른 코드 : set 세 개 사용하는 버전
        
        ```python
        class Solution:
            def totalNQueens(self, n: int) -> int:
                if n == 1: 
                    return 1
                
                col_set, diag_set, anti_diag_set = set(), set(), set()
        
                def backtrack(row=0, count=0):
        						# base case 
                    if row == n:
                        return count + 1
        
                    for col in range(n):
        								# is_not_under_attack
                        if col in col_set or (row - col) in diag_set or (row + col) in anti_diag_set:
                            continue
        								
        								# place 
                        col_set.add(col)
                        diag_set.add(row - col)
                        anti_diag_set.add(row + col)
        								
        								# base case를 위로 빼내서 여기에서는 따로 조건문 필터링 x
        								## row가 끝까지 갔던 아니던 전진 
                        count = backtrack(row + 1, count)
        								
        								# remove 
                        col_set.remove(col)
                        diag_set.remove(row - col)
                        anti_diag_set.remove(row + col)
        
                    return count
        
                return backtrack()
        ```