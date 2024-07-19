# 119. Pascal's Triangle II

Status: done, in progress
Theme: DP
Created time: November 29, 2023 12:39 PM
Last edited time: November 29, 2023 3:17 PM

- 몸풀기 easy
- dp로 어떻게 푸는 지는 모르겠고 그냥 for loop으로 풀자
- 코드
    
    ```python
    class Solution:
        def getRow(self, rowIndex: int) -> List[int]:
            if rowIndex == 0:
                return [1] 
            if rowIndex == 1:
                return [1, 1]
    
            last_row = [1, 1]
            for i in range(2, rowIndex+1):
                temp = [1]
                for j in range(i-1): # 0..i-1 & 1..i 
                    temp.append(last_row[j]+last_row[j+1])
                temp.append(1)
                last_row = temp 
            return last_row
    ```
    
    - 그래서 DP로 풀면 어떻게…?
        - brute force recursion
            - `get_num(row_idx, col_idx)`
                - row_idx 행의 col_idx 번째 숫자를 return
                - 각 숫자는 바로 위에 있는 두 숫자의 합이라는 관계를 점화식으로 나타내면
                    
                    ```python
                    get_num(row_idx, col_idx) = get_num(row_idx-1, col_idx-1) + get_num(row_idx-1, col_idx) 
                    ```
                    
                - base case(recursion deep down → hit the base)
                    - first row는 그냥 1
                    - 모든 row의 맨 앞과 맨 끝 원소는 1 → 식으로 나타내면 `get_num(k, 0) = 1`, `get_num(k, k) = 1`
                - code
                    
                    ```python
                    def get_num(row, col):
                    	# base case 
                    	if row == 0: return 1 # first row 
                    	if col == 0: return 1 # first col 
                    	if row == col: return 1 # last col 
                    
                    	# transition
                    	return get_num(row-1, col-1) + get_num(row-1, col)
                    ```
                    
                    ```python
                    def get_row(row):
                    	ans = []
                    	for col in range(row+1): # col: 0..row
                    		ans.append(get_num(row, col))
                    	return ans 
                    ```
                    
        - DP-prev에 이전 결과(전 row)를 저장했다가 꺼내서 쓰니까 기억해서 풀기
            
            ```python
            class Solution:
                def getRow(self, rowIndex):
                    prev = [1]
                    for i in range(1, rowIndex + 1):
                        curr = [1] * (i + 1)
                        for j in range(1, i):
                            curr[j] = prev[j - 1] + prev[j]
            
                        prev = curr
            
                    return prev
            ```
            
            - 예) rowIndex = 4
                
                
                | i | curr | j | prev | curr[j] |
                | --- | --- | --- | --- | --- |
                | 1 | [1, 1]  | - | [1, 1] |  |
                | 2 | [1, 1, 1] | 1 |  | prev[0]+prev[1] =2  |
                |  |  |  | [1, 2, 1] |  |
                | 3 | [1, 1, 1, 1] | 1 |  | 3  |
                |  | [1, 3, 1, 1] | 2 |  | prev[1]+prev[2] = 3  |
                |  | [1, 3, 3, 1] |  | [1, 3, 3, 1] |  |
                | 4 | [1, 1, 1, 1, 1] | 1 |  | 4 |
                |  | [1, 4, 1, 1, 1] | 2 |  | 6 |
                |  | [1, 4, 6, 1, 1] | 3 |  | 4 |
                |  | [1, 4, 6, 4, 1] |  | [1, 4, 6, 4, 1] |  |