# 240. Search a 2D Matrix II

Status: done, in progress
Theme: Divide & Conquer
Created time: December 2, 2023 11:14 AM
Last edited time: December 4, 2023 11:37 AM

- [x]  divide & conquer 처음부터 다시 짜보기
- 코드
    
    ```python
    class Solution:
        def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
            def binary_search(arr, target):
                left, right = 0, len(arr)-1
                while left <= right:
                    mid = (left + right) // 2
                    if arr[mid] == target: 
                        return mid
                    elif arr[mid] < target:
                        left = mid + 1 
                    else:
                        right = mid - 1 
                return right
    
            m, n = len(matrix), len(matrix[0])
    
            heads = []
            for i in range(m):
                heads.append(matrix[i][0])
            
            right_row = binary_search(heads, target)
            if matrix[right_row][0] == target:
                return True 
            else:
                for i in range(right_row+1):
                    if matrix[i][-1] < target:
                        continue 
                    right_col = binary_search(matrix[i], target)
                    if matrix[i][right_col] == target:
                        return True
                return False
    ```
    
- divide & conquer 코드
    
    ```python
    class Solution:
        def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
            m, n = len(matrix), len(matrix[0])
            
            def check_submatrix(coordinates):
                up, down, left, right = coordinates
                # base case 
                if left > right or up > down: return False 
                smallest = matrix[up][left]
                if target < smallest: return False
                largest = matrix[down][right]
                if target > largest: return False 
    
                # get marker
                mid = left + (right-left) // 2 
                row = up
                while row <= down and matrix[row][mid] <= target:
                    if matrix[row][mid] == target:
                        return True
                    row += 1
                
                # recursive call
                top_right = [up, row-1, mid+1, right]
                bottom_left = [row, down, left, mid-1]
    
                return check_submatrix(top_right) or check_submatrix(bottom_left)
                
            
            start_coor = [0, m-1, 0, n-1]
            return check_submatrix(start_coor)
    ```
    
- Divide & Conquer 사용한 Editorial
    - matrix를 4개의 submatrices로 분할 → 두 개는 target을 포함하고 있을 수 있고, 나머지 두 개는 절대 포함할리가 없는 상태 (?)
    - base case
        1. submatrix의 area가 0인 경우. 원소가 아예 없는 경우를 의미하는 듯?  → return False
        2. target이 submatrix의 가장 작은 값보다 작거나 가장 큰 값보다 큰 경우 → return False 
    - recursive
        - index `row`에 대해 다음을 만족하는 mid column을 구함
            
            `matrix[row-1][mid] < target < matrix[row][mid]`
            
            - [ ]  모든 row에 대해 mid를 다 구하나?
        - 이 index? 를 기준으로 matrix를 4분면으로 나눌 수 있음
            - 이 중에서 좌상단, 우하단에 있는 submatrix 들은 target을 포함하고 있을 수 없음 → search space에서 제외
                - [x]  왜?
                    - 좌상단: row는 row-1보다 작고, col은 mid보다 작음 → 무조건 target보다 작음. 왜냐면 좌상단의 제일 큰 값은 오른쪽 맨 아래에 위치해 있는데, 이 index가 [row-1][mid]일 것이기 때문
                    - 우하단: row는 row보다 크고, col은 mid보다 큼 → 무조건 target보다 큼. 왜냐면 우하단의 제일 작은 값은 맨 왼쪽 맨 위쪽에 위치해있는데, 이 index가 [row][mid]일 것이기 때문
            - 우상단, 좌하단에 있는 submatrix들 대상으로 다시 재귀
- Editorial 보고 짠 코드
    - mine1
        
        ```python
        class Solution:
            def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
                m, n = len(matrix), len(matrix[0])
                def seek_index(submat):
                    sub_m, sub_n = len(submat), len(submat[0])
                    i = 0
                    while i < sub_m and matrix[i][0] < target:
                        i += 1 
                    if matrix[i][0] == target:
                        return i, 0
                    for row in range(1, i):
                        for j in range(sub_n):
                            if submat[row-1][j] < target < submat[row][j]:
                                return row, j 
        
                def check_submatrix(submat):
                    if len(submat) == 0: return False
                    if submat[0][0] > target: return False
                    if submat[-1][-1] < target: return False
        
                    that_row, that_col = seek_index(submat)
                    if submat[that_row][that_col] == target: return True 
        
                    bottom_left = []
                    for i in range(that_row, m):
                        row = []
                        for j in range(that_col):
                            row.append(submat[i][j])
                        bottom_left.append(row)
                    
                    if check_submatrix(bottom_left): return True 
        
                    top_right = []
                    for i in range(that_row):
                        row = []
                        for j in range(that_col, n):
                            row.append(submat[i][j])
                        top_right.append(row)
                    
                    if check_submatrix(top_right): return True 
        
                    return False
                
                return check_submatrix(matrix)
        ```
        
    - 생각하지 못한 점
        - matrix를 다 들고 다닐 필요가 없고, 네 귀퉁이의 index만 들고 다니면 된다
        - mid는 그냥 left와 right의 중간, row는 for loop 돌면서 조건 만족하는 경우 탐색
            - 이 때 row는 0부터 m 사이는 아니고, up과 down 사이 이면서
            - matrix[row][mid] ≤ target 일 때만 row+1
            - 모든 row에 대해 matrix[row][mid]가 target과 일치하지는 않는지 체크
            - row가 down보다 커지거나, matrix[row][mid]> target일 때 while loop break
                
                → matrix[row-1][mid] 까지는 < target, matrix[row][mid] > target
                
    - 위를 반영한 mine2-그러나 또 틀림
        
        ```python
        class Solution:
            def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
                m, n = len(matrix), len(matrix[0])
                
                def check_submatrix(coordinates):
                    up, down, left, right = coordinates
                    # base case 
                    if left > right or up > down: return False 
                    smallest = matrix[up][left]
                    if target < smallest: return False
                    largest = matrix[down][right]
                    if target > largest: return False 
        
                    # get marker
                    mid = left + (right-left) // 2 
                    for row in range(up, down+1):
                        if matrix[row][mid] == target:
                            return True 
                        if matrix[row][mid] > target:
                            break 
                    
                    top_right = [up, up+row-1, left, left+mid-1]
                    bottom_left = [row, down, mid, right]
        
                    return check_submatrix(top_right) or check_submatrix(bottom_left)
                
                start_coor = [0, m-1, 0, n-1]
                return check_submatrix(start_coor)
        ```
        
    - 또 생각하지 못한 점
        - 경계 marker는 어디에 포함되나? → 경계 마커를 들고 다음 재귀에 들어간다는 건 matrix[row][mid]에서 target을 얻지 못했다는 뜻 → (row, mid) marker는 범위에서 제외한다
        - 경계 marker를 찾는 while loop을 for loop으로 변환 시도했으나 성공적으로 변환하지 못함
            
            ```python
            for row in range(up, down+1):
                if matrix[row][mid] == target:
                    return True 
                if matrix[row][mid] > target:
                    break
            
            top_right = [up, row, mid+1, right]
            bottom_left = [row+1, down, left, mid-1]
            ```
            
            vs. 원래 while loop 
            
            ```python
            row = up
            while row <= down and matrix[row][mid] <= target:
                if matrix[row][mid] == target:
                    return True
                row += 1
            # matrix[row-1][mid] < target < matrix[row][mid]
            top_right = [up, row-1, mid+1, right]
            bottom_left = [row, down, left, mid-1]
            ```
            
            - 두 개가 왜 다른지 헷갈려서 직접 해보기
                - matrix = [[-1,3]], target: 3→ 둘 다 True / for loop 변형의 경우
                    - while loop
                        
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 0 | 1 | 0 | 0 | -1 |
                        |  |  |  |  |  | 1 | 3 |
                        
                        bottom_left = [1, 0, 0, -1] → base case → False
                        
                        top_right = [0, 0, 1, 1] 
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 1 | 1 | 1 | 0 | 3 |
                        
                        → return True 
                        
                    - for loop
                        
                        ```python
                        for row in range(up, down+1):
                            if matrix[row][mid] == target:
                                return True 
                            if matrix[row][mid] > target:
                                break
                        
                        top_right = [up, row, mid+1, right]
                        bottom_left = [row+1, down, left, mid-1]
                        ```
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 0 | 1 | 0 | 0 | -1 |
                        
                        bottom_right = [1, 0, 0, -1] → base case → False
                        
                        top_left = [0, 0, 1, 1] 
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 1 | 1 | 1 | 0 | 3 |
                        
                        → return True 
                        
                    - for loop 변형
                        
                        ```python
                        for row in range(up, down+1):
                            if matrix[row][mid] == target:
                                return True 
                            if matrix[row][mid] > target:
                                break
                        
                        top_right = [up, row-1, mid+1, right]
                        bottom_left = [row, down, left, mid-1]
                        ```
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 0 | 1 | 0 | 0 | -1 |
                        
                        top_right = [0, -1, 1, 1] → base case → False  
                        
                        bottom_left = [0, 0, 0, -1] → base case → False
                        
                        ⇒ wrong
                        
                - matrix = [[1,3,5]], target: 1 → for loop에서 target보다 더 큰 값이 있는 범위로 이상하게 좁혀서 탐색하는 바람에 false return. wrong.
                    
                    
                    | up | down | left | right | mid | row | matrix[row][mid] |
                    | --- | --- | --- | --- | --- | --- | --- |
                    |  |  |  |  |  |  |  |
                    |  |  |  |  |  |  |  |
                    - while loop
                        
                        ```python
                        row = up
                        while row <= down and matrix[row][mid] <= target:
                            if matrix[row][mid] == target:
                                return True
                            row += 1
                        
                        top_right = [up, row-1, mid+1, right]
                        bottom_left = [row, down, left, mid-1]
                        ```
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 0 | 2 | 1 | 0 | 3 |
                        
                        → matrix[row][mid] > target 으로 while loop exit (row는 up)
                        
                        top_right = [0, -1, 2, 2] → base case → return False 
                        
                        bottom_left = [0, 0, 0, 0] 
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
                        
                        → return True 
                        
                    - for loop
                        
                        ```python
                        for row in range(up, down+1):
                            if matrix[row][mid] == target:
                                return True 
                            if matrix[row][mid] > target:
                                break
                        
                        top_right = [up, row, mid+1, right]
                        bottom_left = [row+1, down, left, mid-1]
                        ```
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 0 | 2 | 1 | 0 | 3 |
                        
                        → for loop exit
                        
                        bottom_left = [1, 0, 0, 0] → base case → return False 
                        
                        top_right = [0, 0, 2, 2]
                        
                        | up | down | left | right | mid | row | matrix[row][mid] |
                        | --- | --- | --- | --- | --- | --- | --- |
                        | 0 | 0 | 2 | 2 | 2 | 0 | 5 |
                        
                        → for loop exit 
                        
                        top_right = [0, 0, 3, 2] → base case → return False 
                        
                        bottom_left = [1, 0, 2, 1] → base case → return False
                        
                        ⇒ wrong! 
                        

![Untitled](Untitled%20211.png)