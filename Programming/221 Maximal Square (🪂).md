# 221. Maximal Square (🪂)

Status: done, in progress, with help, 💎
Theme: DP
Created time: January 5, 2024 3:42 PM
Last edited time: January 6, 2024 10:03 AM

- Editorial
    - Brute Force
        - Algorithm
            1. early exit: if input matrix is None return 0
            2. iterate over all the cell 
                1. check if the current cell is 1 → if not continue 
                2. offset of next row/col to explore from the current position (start from 1)
                    
                    ↳ 정사각형을 넓힐 때 탐색 범위는 뒤집어진 니은자 모양으로 추가됨 
                    
                    ↳ 중점은 우하향 대각선을 그리며 이동. (0, 0) → (n, n)
                    
                    ↳ 탐색 범위는 (n,0)~(n,n-1) for the bottom row & (0, n)~(n-1, n) for the rightmost column 
                    
                3. set flag as True 
                    
                    ↳ 탐색 범위에서 0이 하나라도 나오는 순간 False가 되면서 
                    
        - TLE but correct solution
            
            ```python
            class Solution:
                def maximalSquare(self, matrix: List[List[str]]) -> int:
                    num_rows, num_cols = len(matrix), len(matrix[0])
                    
                    # edge case
                    if num_rows == 1 and num_cols == 1:
                        return 1 if matrix[0][0] == '1' else 0
            
                    max_side_length = 0
            
                    for i in range(num_rows):
                        for j in range(num_cols):
                            # check current cell 
                            if matrix[i][j] != '1': 
                                continue 
                            # current cell = top-left cell in the current square
                            valid_square = True                 
                            side_length = 1                
                            # check boundary validity 
                            while valid_square and i + side_length < num_rows and j + side_length < num_cols:               
                                # check bottom-right cell validity 
                                bottom = i + side_length
                                rightmost = j + side_length 
                                # check bottom row validity 
                                for c in range(j, rightmost+1):
                                    if matrix[bottom][c] != '1': 
                                        valid_square = False
                                        break 
                                # check rightmost column validity
                                for r in range(i, bottom+1):
                                    if matrix[r][rightmost] != '1':
                                        valid_square = False
                                        break 
            
                                # prize en finale!
                                if valid_square:       
                                    side_length += 1 
                            
                            # aggregate the result from the current cell
                            max_side_length = max(max_side_length, side_length) 
            
                    return max_side_length ** 2
            ```
            
        - 복잡도 분석
            - 시간: O((mn)^2)
                - top-left cell 후보 개수 double for loop → m*n
                - 각 top-left cell에서 사각형 길이가 1, 2, …, k로 늘어갈 때 additional bottom row & right col 체크
                    - 사각형 길이가 k 일 때 2k개의 cell을 체크하는 셈
                    - 사각형 길이는 1, 2, …, k → k(k+1)/2 * 2 = k^2 + k
                    - 가장 고차항만 남기면 k^2
                    - 이 때 k는 min(m, n) 이기 때문에, 하나의 top-left cell에 대해 검사해야 하는 cell의 개수는 min(m, n)^2
                
                ⇒ cell 개수 * 하나의 cell 당 검사해야 하는 일의 상한 = O(m*n*min(m, n)^2)
                
                - min(m, n)^2 < m*n 일테니 단순화해서 O((mn)^2))라고 한 듯
            - 공간 복잡도: O(1). 추가로 필요한 공간 없음
    - **Dynamic Programming**
        - Algorithm
            - dp matrix 초기화
                - size: input matrix와 동일. m * n
                - 초기 cell value: 0
            - state definition
                - `dp[i,j]` : bottom-right corner 가 matrix[i][j]인 사각형 중 가장 크기가 큰 사각형의 side length
            - recurrence relation
                - dp[i, j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1
            - 그림 예시
                
                ![Untitled](Untitled%20201.png)
                
                - dp[2][3] = ?
                    - dp[1][3] = 2 의 의미
                        - original matrix[1][3]까지 고려했을 때, 가능한 가장 큰 정사각형 한변의 길이는 2 라는 의미
                    - dp[1][2], dp[2][2]도 2 인 상태
                    - 한 변의 길이가 3인 정사각형을 얻을 수 있는지 여부는 original matrix[2][3]에 달려 있음 → 해당 cell 값도 1임 → dp[2][3]에 3이 들어갈 수 있음
                - dp[3][4] = ?
                    - dp[2][3], dp[3][3] 모두 값이 3 = 각 cell을 bottom-right로 하는 정사각형은 최대 3 by 3까지 가능
                    - 그러나 dp[2][4] = 1 → dp[3][4]에서는 matrix[3][4]를 bottom right로 할 때 최대 길이가 2인 사각형 밖에 만들지 못함. (bottom right cell 자체가 길이 1인 사각형 + 바로 한 칸 위인 matrix[2][4]까지만 1이 보장되어 있기 때문에 = 2)
                    - 따라서 dp[3][4] = 2
        - 복잡도 분석
            - 시간 복잡도: O(m*n). 각 bottom-right cell에서 해야 하는 일이 상수 O(1)
            - 공간 복잡도: O(m*n). dp matrix size는 original matrix size와 동일
    - **Better Dynamic Programming**
        - 공간복잡도 더 줄이기 (O(mn) → O(n)). 결국 필요한 건
            
            ![Untitled](Untitled%20202.png)
            
            - dp를 num_cols 크기로 초기화
            - 현재 구하려는 값: dp[j] (matrix 기준으로는 i,j 이지만 i는 무시)
                - matrix[i][j]가 0이면 그대로 0.
                - matrix[i][j]가 1이면,
                    - dp[j] = min(dp[j-1], prev, dp[j]) + 1
                    - dp[j-1]에는 같은 row, previous column의 최대값 저장
                        - 같은 i 값에서 inner for loop을 돌면서 채워지는 값들
                    - dp[j]에는 같은 col, previous row의 최대값 저장
                        - 이번에 dp[j] 업데이트 하기 전 상태는 matrix[i-1][j] cell이 bottom right cell일 때 계산한 값
                        - outer for loop 값은 달라지고, inner for loop에서는 같은 차례
                    - prev에는 inner for loop 하나 전에서 temp→prev로 바뀐 값을 갖고 있음
                        - temp는 dp[j] 업데이트 하기 전 값 즉, outer for loop 하나 전에서 구한 값을 저장해 두었음
                        - 따라서 inner for loop도 하나 전, outer for loop도 하나 전의 값을 갖고 있는 셈
- Trial
    - Editorial 보고 짰는데 왜 예제도 통과 못하지
        
        ```python
        class Solution:
            def maximalSquare(self, matrix: List[List[str]]) -> int:
                num_rows, num_cols = len(matrix), len(matrix[0])
                dp = [[0] * num_cols for _ in range(num_rows)]
        
                # base case
                ## edge cell as bottom-right cell -> max side length is always 1 
                for i in range(num_rows):
                    dp[i][0] = int(matrix[i][0])
                for j in range(num_cols):
                    dp[0][j] = int(matrix[0][j])
                
                # recurrence relation 
                for i in range(1, num_rows):
                    for j in range(1, num_cols):
                        if matrix[i][j] != '1':
                            continue
                        dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1
                
                return dp[-1][-1]
        ```
        
- 놓쳤던 점
    - return 값은 dp[-1][-1]이 아니다 - dp matrix에서 가장 큰 값의 제곱(넓이)
        - 근데 다 계산하고 마지막에 한번 더 돌면서 최대값 구하려면 번거로우니
        - 각 cell 값을 구할 때마다 최대값을 미리 미리 update 해둔다
- AC 코드 (⚡️)
    
    ```python
    class Solution:
        def maximalSquare(self, matrix: List[List[str]]) -> int:
            num_rows, num_cols = len(matrix), len(matrix[0])
            dp = [[0] * num_cols for _ in range(num_rows)]
            max_side_length = 0
            # base case
            ## edge cell as bottom-right cell -> max side length is always 1 
            for i in range(num_rows):
                dp[i][0] = int(matrix[i][0])
                max_side_length = max(max_side_length, dp[i][0])
            for j in range(num_cols):
                dp[0][j] = int(matrix[0][j])
                max_side_length = max(max_side_length, dp[0][j])
            
            # recurrence relation 
            for i in range(1, num_rows):
                for j in range(1, num_cols):
                    if matrix[i][j] != '1':
                        continue
                    dp[i][j] = min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1]) + 1
                    max_side_length = max(max_side_length, dp[i][j])
    
            
            return max_side_length ** 2
    ```
    
- AC 코드 (공간 복잡도 개선, ⚡️)
    
    ```python
    class Solution:
        def maximalSquare(self, matrix: List[List[str]]) -> int:
            num_rows, num_cols = len(matrix), len(matrix[0])
            dp = [0] * num_cols 
            max_side_length, prev = 0, 0
    
            # recurrence relation 
            for i in range(num_rows):
                prev = 0 # reset prev for each new row 
                for j in range(num_cols):
                    temp = dp[j] # save the result from the previous row 
                    
                    if matrix[i][j] == '1':      
                        # base case 
                        if i == 0 or j == 0:
                            dp[j] = 1
                        # recurrence relation
                        else:
                            # use of old prev
                            dp[j] = min(dp[j-1], prev, dp[j]) + 1
                        max_side_length = max(max_side_length, dp[j])
                    else:
                        dp[j] = 0 
    
                    prev = temp # updated prev
            
            return max_side_length ** 2
    ```