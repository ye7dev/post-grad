# 85. Maximal Rectangle

Status: done, in progress, incomplete
Theme: DP
Created time: November 13, 2023 11:58 AM
Last edited time: November 14, 2023 10:58 AM

- 11/10 시험과 거의 쌍둥이 문제
- 바로 해설 가즈아 그냥 외우자 ㅋㅋㅋㅋ
- [x]  코딩해서 한번 더 풀어보기
- 우선 따라 적어보는 해설
    - 첫번째 row부터 하나씩 진행
        - 각 row마다 모든 col에 대해서 계산
    - maximal rectangle area at i, j
        - [right(i,j)-left(i,j)] * height(i,j)
        - 각 항은 이전 row와 현재 row의 정보 이용
    - state
        - height(i, j)
            - 0~i번째 row까지 j column에서 연속적으로 나온 1의 개수 (세로로)
        - left(i,j)
            - 1) current cell (i,j)를 포함하면서 2) height(i, j)를 만족하는(그만큼의 height를 갖고 있는) 3) 가장 왼쪽의 column 위치
        - right(i, j)
            - 1) current cell (i,j)를 포함하면서 2) height(i, j)를 만족하는(그만큼의 height를 갖고 있는) 3) 가장 오른쪽의 column 위치
    - transition
        - cur_left, cur_right = 0, n으로 각 row마다 초기화
        - height(i,j)
            - 각 column을 돌면서 matrix의 i,j cell이 0이면 바로 0
            - 아니면 이전 row의 height 값에 +1 (현재 cell에도 1이 있기 때문에 누적)
        - left(i, j)
            - 각 column을 돌면서 matrix에서 이번 cell값이 0이면 해당 column의 left를(left[j]) 0으로 만듦 (초기화) & cur_left는 다음 column으로 (j+1)
                - cur_left: 같은 row에서 앞쪽에 cell 값이 0인  column이 몇 개가 있었는지 알려줌
            - matrix에서 이번 cell값이 1이면 cur_left와 기존 left[j] 중 더 큰 쪽(더 오른쪽)을 선택
        - right(i, j)
            - 오른쪽에서 왼쪽으로 계산
            - matrix에서 이번 cell 값이 0이면 해당 column의 right를 n으로 만듦(초기화) & cur_right를 현재 column으로 (right[j] = j)
- 솔직히 뭔말인지 몰라서 우선 따라서 해보자
    
    ```python
    # 3 * 7 matrix 
    0 0 0 1 0 0 0 
    0 0 1 1 1 0 0 
    0 1 1 1 1 1 0
    
    # 누적으로 사용할 거라 한 행 당 사용할 메모리만 초기화 
    left = [0] * 7 
    right = [n] * 7
    height = [0] * 7
    
    # 0th row 
    cur_left, cur_right = 0, 7
    max_area = -1
    # height
    '''
    0 0 0 1 0 0 0
    '''
    for j in range(n):
    	if matrix[i][j] == 0: 
    		height[j] = 0
    	else:
    		height[j] += 1 
    # left 
    '''
    left[j]:  0 0 0 3 0 0 0
    cur_left: 1 2 3 3 4 5 6
    '''
    for j in range(n):
    	if matrix[i][j] == 0:
    		left[j] = 0 # max 하면 cur_left가 선택됨 
    		cur_left = j+1 
    	else:
    		left[j] = max(left[j], cur_left)
    # right
    '''
    right[j]:  7 7 7 4 7 7 7  
    cur_right: 6 5 4 4 2 1 0
    '''
    for j in range(n-1, -1, -1):
    	if matrix[i][j] == 0:
    		right[j] = n # min 하면 cur_right가 선택됨 
    		cur_right = j
    	else:
    		right[j] = min(right[j], cur_right)
    # area
    '''
    0 0 0 1 0 0 0 
    ''' 
    for j in range(n):
    	max_area = max(max_area, height[j] * (right[j]-left[j]) 
    
    ```
    
    - 나머지 rows
        
        ```python
        1st row : 0 0 0 1 0 0 0  
        	 left : 0 0 0 3 0 0 0
        	right : 7 7 7 4 7 7 7 
         height : 0 0 0 1 0 0 0
        	 area : 0 0 0 1 0 0 0
        ------------------------
        cur_left, cur_right = 0, 7
        2nd row : 0 0 1 1 1 0 0 
         height : 0 0 1 2 1 0 0
        	 left : 0 0 2 3 2 0 0 
        ~~curleft : 1 2 2 2 2 6 7~~
        	right : 7 7 5 4 5 7 7
        ~~curright: 6 5 5 5 5 1 0~~
        	 area : 0 0 3 2 3 0 0 
        ------------------------
        3rd row : 0 1 1 1 1 1 0 
         height : 0 1 2 3 2 1 0 
        	 left : 0 1 2 3 2 1 0
        ~~curleft : 1 1 1 1 1 1 7~~
        	right : 7 6 5 4 5 6 7
        ~~curright: 6 6 6 6 6 6 0~~
        	 area : 0 5 6 3 6 5 0
        ```
        
- 복습하면서 다시 깨달은 점
    
    `left[j] = max(left[j], cur_left)`
    
    - max(이전 row 정보, 현재 row 정보)
        - 이전 row 정보: 이전 row의 j column과 같은 높이를 가진 가장 왼쪽 column index
        - 현재 row 정보: 현재 row에서 j보다 앞에 있는 column 중 matrix 값이 0인 가장 마지막 column +1
        - [ ]  그러나 왜 이 둘을 비교하는지는 모르겠다
    - cur_left: 지금 내 cell이 1이라면 consecutive 1의 시작점. 내 cell이 0일 때 j+1로 설정하고 넘어가는 이유는 다음 potential 1을 맞이하기 위한 준비
    - 코드 짜다가 틀린 점
        - matrix size가 n by n이 아니라 m by n
        - matrix cell value가 int가 아니라 string
- chat 센세가 알려주는 각 변수의 역할
    - [ ]  다시 한번 읽어보기
    
    In the given code snippet, which is a C++ function intended to solve the problem of finding the largest rectangle containing all ones in a 2D binary matrix, the variables `cur_left` and `cur_right` play a crucial role in dynamically tracking the boundaries of such rectangles at each row.
    
    Here's what each variable represents:
    
    - `cur_left`: This variable tracks the leftmost boundary where a continuous sequence of 1s starts in the current row being processed. It gets reset to `0` at the start of each new row.
    - `cur_right`: Similarly, this variable tracks the rightmost boundary where a continuous sequence of 1s ends in the current row being processed. It is initialized to `n`, which is the width of the matrix.
    
    When the code processes a new row in the matrix (the `i` loop), it updates the `height`, `left`, and `right` arrays for each column (the `j` loops).
    
    - The `height[j]` records the number of consecutive 1s up to the current row (like a histogram).
    - The `left[j]` keeps track of the leftmost index where the sequence of 1s begins, considering all rows up to the current one.
    - The `right[j]` keeps track of the rightmost index where the sequence of 1s ends.
    
    The comparison `left[j] = max(left[j], cur_left)` is performed to update the `left[j]` value for each column. When processing a particular cell:
    
    - If the cell contains a `1`, it means that the current sequence of 1s extends at least from `cur_left` to this column. Since `left[j]` may have been set in a previous row, the `max` function ensures that `left[j]` is updated to the furthest left boundary observed for this column so far.
    - If the cell contains a `0`, it means the current sequence of 1s is interrupted, and so `cur_left` is updated to `j+1`, the index right after this cell, for the next potential sequence of 1s.
    
    As for `cur_right`, it is updated in a similar but opposite manner when iterating from right to left. If a `1` is encountered, `right[j]` is updated to be the minimum of its current value or `cur_right`, ensuring it records the closest interruption from the right.
    
    Finally, after updating `left`, `right`, and `height` for each column, the area of the rectangle that ends at each column is calculated with `(right[j] - left[j]) * height[j]`, and the maximum area encountered is stored in `maxA`. The function returns this maximum area after processing all rows.