# 37. Sudoku Solver

Status: done, in progress, incomplete, with help, 🏋️‍♀️
Theme: backtracking
Created time: December 5, 2023 1:34 PM
Last edited time: December 6, 2023 2:07 PM

- [x]  처음부터 짜보기
- template
    
    ```python
    보드를 돌면서 
    	# board가 채워진 경우 -> return 변화없이 column 하나 늘려서 다시 함수 들어갔다가 나올 때 값 
    	# board가 빈 경우
    		가능한 모든 후보를 돌면서
    			## validity 체크
    			## 통과했으면 place
    			## return 이 변화된 상태에서 column 하나 늘려서 다시 함수 들어갔다가 나올 때 값 
    			## 아직도 solution 안나왔으면 remove-방금 변화했던 상태를 없애고 원상 복귀 
    			-> 다음 후보로 넘어감
    보드 다 돌고도 solution 안나왔으면 solution 없는 것  
    ```
    
- 과정
    
    현재 cell이 속한 subgrid의 좌표를 찾아야 겠군 
    
    여기는 solution이 하나인듯-방법 자체가 몇 개인지 찾아라 그런게 아니고 
    
    ![Untitled](Untitled%20104.png)
    
    0~2/ 3~5/ 6~8
    
    몫이 크게 0/1/2로 나뉘고, 그 안에서 나머지가 0/1/2로 나뉨
    
    만약에 row로 4가 들어왔다고 하면 4 // 3 = 1 → 3 * 1과 3 * 2 사이 즉 3, 4, 5
    
    col로 7이 들어왔다고 하면 7 // 3 = 2 → 3 * 2와 3 * 3 사이 즉 6, 7, 8
    
- 중간 과정에서 짠 코드
    - 애초에 저 규정을 통과할 수 있는 num이 없는 것 같은데 어떻게 해야 하쥐
    - 전진할 때 좌표를 어떻게 update 해야 하는지 헷갈림
    
    ```python
    class Solution:
        def solveSudoku(self, board: List[List[str]]) -> None:
            def check_subgrid(row, col, num):
                # subgrid
                q_row, q_col == row // 3, col // 3 
                for r in range(3*q_row, 3*(q_row+1)):
                    for c in range(3*q_col, 3*(q_col+1)):
                        if board[r][c] == num:
                            return False
                # column
                for r in range(9):
                    if board[r][col] == num:
                        return False
                # row
                for c in range(9):
                    if board[row][c] == num:
                        return False
    
                return True 
    
            def backtrack_sudoku(row, col):
                # base case
                if row == 9:
                    return 
               
                for r in range(row, 9):
                    for c in range(col, 9):
                        if board[row][col] != '.':
                            for num in range(9):
                                if check_subgrid(row, col, num):
                                    board[row][col] = num
                                    print(num)
                                    if col == 8:
                                        backtrack_sudoku(row+1, 0)
                                    else:
                                        backtrack_sudoku(row, col+1)
                                    board[row][col] == '.'
    
                backtrack_sudoku(0, 0)
    ```
    
- Editorial
    - 생각보다 코드가 많이 다르다 ;;
    - Constrained programming
        - 일단 board에 place a number 하고 나면 → 그 숫자가 같은 행, 열, sub-box에서 사용되지 못하도록 바로 제외
        - 이런 식으로 제약을 넓혀가다 보면 생각해야 할 조합의 수가 줄어듦
    - Backtracking
        - 숫자를 여러 개 놓다보니 막다른 곳에 도달한 경우 → 바로 직전에 board에 놓인 숫자를 바꿔서 다시 전진
    - sub-box indexing tip
        - `box_index = (row // 3) * 3 + column // 3`
            - 예를 들어 4, 7이 들어오면 1*3+2=5 → 5번째 subbox
        - 그림
            
            ![Untitled](Untitled%20105.png)
            
    - 알고리즘
        - `backtrack(row=0, col=0)`
            - cell 단위가 맞군
            - 첫번째 공백이 나올 때까지 전진
            - 빈 자리가 나오면 숫자 1-9까지 돌면서 current num d가 row,col 자리에 들어갈 수 있는 지 확인
                - 들어갈 수 있으면 place
                - d가 current_row, col, box에 있음을 알림
                - 현재 좌표가 (8, 8)이면 푼 거니까 return
                - 아니면 더 전진
                - 다 돌고 나오면 마지막으로 추가했던 숫자를 삭제함
            - invalid num에 대해서는 따로 할 일 없음
        - 여기까지 짜고 와플 사먹으러 간다
            
            ```python
            from collections import defaultdict
            class Solution:
                def solveSudoku(self, board: List[List[str]]) -> None:
                    """
                    Do not return anything, modify board in-place instead.
                    """
                    row_dict = defaultdict(list)
                    col_dict = defaultdict(list)
                    sub_box_dict = defaultdict(list)
            
                    def place(row, col):
                        row_dict[row] = board[row][col]
                        col_dict[col] = board[row][col]
                        sub_box_index = (row // 3) * 3 + (col // 3)
                        sub_box_dict[sub_box_index] = board[row][col]
            
                    def remove(row, col):
                        row_dict[row].remove(board[row][col])
                        col_dict[col].remove(board[row][col])
                        sub_box_index = (row // 3) * 3 + (col // 3)
                        sub_box_dict[sub_box_index].remove(board[row][col])
                
                    def backtrack_sudoku(row, col):
                        if row == 8 and col == 8:
                            return 
                        
                        sub_box_index = (row // 3) * 3 + (col // 3)
            
                        for num in range(1, 10):
                            if num not in row_dict[row] and not in col_dict[col] and not in sub_box_dict[sub_box_index]:
                                row
            
                    for i in range(9):
                        for j in range(9):
                            if board[i][j] != '.':
                                place(i, j)
                            else:
                                backtrack_sudoku(i, j)
                                remove(i, j)
            ```
            
- Editorial 코드 분석
    - 전체 구조
        
        ```python
        # 이미 채워진 숫자는 사전에 넣기  
        for i in range(N):
          for j in range(N):
              if board[i][j] != '.':
        					# 원래는 string으로 들어오기 때문에 int로 전환해야 
                  num = int(board[i][j])
                  place(i, j, num)
        
        sudoku_solved = False # nonlocal
        backtrack()
        ```
        
    - 필요한 자료 구조
        
        ```python
        # dict[row(col)][num] = 1 : existence, 0: non-existence
        row_dict = [defaultdict(int) for _ in range(N)]
        col_dict = [defaultdict(int) for _ in range(N)]
        sub_box_dict = [defaultdict(int) for _ in range(N)]
        ```
        
        - row, col, sub_box 모두 9개씩
        - `defaultdict(int)` 하나의 경우, 아직 값이 없는 key를 넣어서 부르면 keyError 대신 0을 return
            - 그렇다고 해도 사전[key] = 0 인 경우와 사전에 key가 아예 없는 경우는 엄연히 다름
            - 만약 전자의 경우 if key in 사전을 하면 True가 나오지만, 후자는 False가 나옴
    - place
        
        ```python
        def place(row, col, num):
        	  row_dict[row][num] = 1 # why += 1 instead of =1 
        	  col_dict[col][num] = 1
        	  sub_box_index = (row // 3) * 3 + (col // 3)
        	  sub_box_dict[sub_box_index][num] = 1
        	  board[row][col] = str(num) # input cell value type: string
        ```
        
        - += 1로 하나 1로 하나 결과는 같음
        - board에 직접적으로 값을 넣어주는 것까지 여기서 함-이때 변수 type 주의
    - remove (주의)
        
        ```python
        def remove(row, col, num):
            del row_dict[row][num]  # why del instead of -= 1 
            del col_dict[col][num] 
            sub_box_index = (row // 3) * 3 + (col // 3)
            del sub_box_dict[sub_box_index][num] 
            board[row][col] = '.'
        ```
        
        - `del` vs. -= 1 or = 0
            - del의 경우 사전에서 아예 key-value pair를 빼버림 → if key in 사전 하면 False 나옴
            - 후자의 경우 if key in 사전 하면 True 나와서 답이 아예 달라져 버림
    - is_valid
        
        ```python
        def is_valid(row, col, num):
            if num in row_dict[row]: return False
            if num in col_dict[col]: return False
            sub_box_index = (row // 3) * 3 + (col // 3)
            if num in sub_box_dict[sub_box_index]: return False
            return True
        ```
        
        - if num in 사전으로 판단하기 때문에 key가 사전에 있느냐가 상당히 중요함
    - `go_forward` 핵심
        - 역할 1: base case 설정
        - 역할 2: 최종 output 값 변경
        - 역할 3: 재귀 함수 호출
        - 근데 사실 생각해보면 그냥 따로 함수 안 빼고 backtrack 함수 안에 넣어도 되는 부분이 아닌가 싶다…
        
        ```python
        def go_forward(row, col):
            if col == N-1 and row == N-1:
                nonlocal sudoku_solved
                sudoku_solved = True
            else:
                if col == N-1:
                    backtrack(row+1, 0)
                else:
                    backtrack(row, col+1)
        ```
        
    - `backtrack` 핵심
        - board 값이 채워진 거랑 invalid 숫자인거랑은 경우가 엄연히 다르다
        
        ```python
        def backtrack(row=0, col=0):
            if board[row][col] == '.':
                for num in range(1, 10):
        						# invalid input에 대해서는 아무것도 안한다 
                    if is_valid(row, col, num):
        								# board랑 사전들에 값 추가해서 주변에서 해당 숫자 못 사용하게 만듦 
                        place(row, col, num)
        								# 이 함수 들어갔다 나오면서 sudoku_solved 변수 값이 바뀔 수 있음
                        go_forward(row, col) 
        								# board랑 사전들 원상 복구 
                        if not sudoku_solved:
                            remove(row, col,num)
            else: # 이미 input이 채워진 cell이면 비어 있는 칸으로 이동하기 위해 전진 
                go_forward(row, col)
        ```
        
    
    ```python
    from collections import defaultdict
    class Solution:
        def solveSudoku(self, board: List[List[str]]) -> None:
            """
            Do not return anything, modify board in-place instead.
            """
            N = 9
            # dict[row(col)][num] = 1 : existence, 0: non-existence
            row_dict = [defaultdict(int) for _ in range(N)]
            col_dict = [defaultdict(int) for _ in range(N)]
            sub_box_dict = [defaultdict(int) for _ in range(N)]
    
            def place(row, col, num):
                row_dict[row][num] += 1 # why += 1 instead of =1
                col_dict[col][num] += 1
                sub_box_index = (row // 3) * 3 + (col // 3)
                sub_box_dict[sub_box_index][num] += 1
                board[row][col] = str(num) # input cell value type: string
    
            def remove(row, col, num):
                del row_dict[row][num] # why del instead of -= 1 
                del col_dict[col][num] 
                sub_box_index = (row // 3) * 3 + (col // 3)
                del sub_box_dict[sub_box_index][num] 
                board[row][col] = '.'
    
            def is_valid(row, col, num):
                if num in row_dict[row]: return False
                if num in col_dict[col]: return False
                sub_box_index = (row // 3) * 3 + (col // 3)
                if num in sub_box_dict[sub_box_index]: return False
                return True 
    
            def go_forward(row, col):
                if col == N-1 and row == N-1:
                    nonlocal sudoku_solved
                    sudoku_solved = True
                else:
                    if col == N-1:
                        backtrack(row+1, 0)
                    else:
                        backtrack(row, col+1)
    
            def backtrack(row=0, col=0):
                if board[row][col] == '.':
                    for num in range(1, 10):
                        if is_valid(row, col, num):
                            place(row, col, num)
                            go_forward(row, col)
    
                            if not sudoku_solved:
                                remove(row, col,num)
                else:
                    go_forward(row, col)
    
            for i in range(N):
                for j in range(N):
                    if board[i][j] != '.':
                        num = int(board[i][j])
                        place(i, j, num)
            
            sudoku_solved = False
            backtrack()
    ```
    
- 더 간단하다고 주장하는 코드
    
    ```python
    class Solution:
        def solveSudoku(self, board: List[List[str]]) -> None:
            n = len(board)
            rows, cols, boxes = defaultdict(set), defaultdict(set), defaultdict(set)
    
            for r in range(n):
                for c in range(n):
                    if board[r][c] == '.':
                        continue
    								# 사전에 값 추가 
                    num = int(board[r][c])
                    rows[r].add(num)
                    cols[c].add(num)
    								box_id = (r // 3) * 3 + c // 3
                    boxes[box_id].add(num)
    
            def is_valid(r, c, num):
                box_id = (r // 3) * 3 + c // 3
                return num not in rows[r] and num not in cols[c] and num not in boxes[box_id]
    
            def backtrack(r, c):
    						# 함수 들어와서 r,c를 범위에 맞게 재조정 
                if r == n - 1 and c == n:
                    return True
                elif c == n:
                    c = 0
                    r += 1
    
                # current grid has been filled
                if board[r][c] != '.':
    								# 여기서 c가 n-1인지 확인 안하고 그냥 바로 호출하기 때문에 
    								## 함수 들어가서 제일 윗단에서 체크하고 조정 
                    return backtrack(r, c + 1)
    
                box_id = (r // 3) * 3 + c // 3
                for num in range(1, n + 1):
    								# check validity 
                    if not is_valid(r, c, num):
                        continue
    								
    								# place
                    board[r][c] = str(num)
                    rows[r].add(num)
                    cols[c].add(num)
                    boxes[box_id].add(num)
    								
    								# go forward 
                    if backtrack(r, c + 1):
                        return True
    
                    # backtrack-remove
                    board[r][c] = '.'
                    rows[r].remove(num)
                    cols[c].remove(num)
                    boxes[box_id].remove(num)
    
                return False
    
            backtrack(0, 0)
    ```
    
- 복습하면서 또 헷갈린 점
    - backtrack에서 valid num을 못 만난 경우의 진전을 어떻게 해야 하는지 헷갈림
        - invalid num에 대해서는 할 것이 없고, 다만 현재 cell 값이 공백이 아닌 경우 parameter update 해서 재귀 호출 해야 함
- 오롯이 복기 해서 통과한 코드 🪇
    
    ```python
    from collections import defaultdict
    class Solution:
        def solveSudoku(self, board: List[List[str]]) -> None:
            """
            Do not return anything, modify board in-place instead.
            """
            N = 9
            # making dict
            rows = [defaultdict(int) for _ in range(N)]
            cols = [defaultdict(int) for _ in range(N)]
            boxes = [defaultdict(int) for _ in range(N)]
            
            sudoku_solved = False
            
            def box_index(row, col):
                return (row // 3) * 3 + (col // 3)
            
            def is_valid(row, col, num):
                if rows[row][num]: return False 
                if cols[col][num]: return False
                if boxes[box_index(row,col)][num]: return False
                return True 
            
            def place(row, col, num):
                rows[row][num] += 1 
                cols[col][num] += 1
                boxes[box_index(row, col)][num] += 1 
                board[row][col] = str(num) 
            def remove(row, col, num):
                del rows[row][num]
                del cols[col][num]
                del boxes[box_index(row, col)][num]
                board[row][col] = '.'
                
            def backtrack(row, col):
                nonlocal sudoku_solved
                if row == N:
                    sudoku_solved = True 
                    return 
    						# 값이 이미 차있는 경우 
                if board[row][col] != '.':
                    if col < N-1:
                        backtrack(row, col+1)
                    else:
                        backtrack(row+1, 0)
    						# 값이 비어 있는 경우 
                else:
                    for n in range(1, N+1):
                        if is_valid(row, col, n):
                            place(row, col, n)
                            if col < N-1:
                                backtrack(row, col+1)
                            else:
                                backtrack(row+1, 0)
                            if sudoku_solved:
                                return 
                            remove(row, col, n)
    				# 사전 값 채우기 
            for r in range(N):
                for c in range(N):
                    if board[r][c] != '.':
                        place(r, c, int(board[r][c]))
           
            backtrack(0, 0)
    ```