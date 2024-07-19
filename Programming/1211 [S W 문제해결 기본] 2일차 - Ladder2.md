# 1211. [S/W 문제해결 기본] 2일차 - Ladder2

Created time: May 3, 2024 3:58 PM
Last edited time: May 3, 2024 5:26 PM

- 문제 이해
    - input이 통째로 주어졌던 것 같은데 맞나?
        
        0~99, 100~199, 200~299 … 900~999, … 9900~9999
        
        → i * 100 ~ (i * 100)+100
        
        아니였다 열마다 주어짐 ;; 
        
    - 힘이 조금 빠지므로 화장실 다녀와서 마져~!!!
    - 키위 실컷 먹고 돌아옴 힘내서 하자!!
- AC 코드
    
    ```python
    import sys
    sys.stdin = open("temp_input/input.txt", "r")
    
    def explore(r, c):
        num_moves = 0
        while r < N-1:
            prev_col = c
            num_moves += 1
            while c-1 >= 0 and matrix[r][c-1] == 1:
                c -= 1
                num_moves += 1
            # direction change
            if prev_col != c:
                r += 1
                continue
            while c+1 < N and matrix[r][c+1] == 1:
                c += 1
                num_moves += 1
            r += 1
        num_moves += 1
        return num_moves
    
    def get_best_start():
        shortest_move = float('inf')
        best_start = -1
        for c in range(N):
            if matrix[0][c] == 1:
                temp = explore(0, c)
                #print(c, temp)
                if temp <= shortest_move:
                    best_start = max(c, best_start)
                    shortest_move = temp
        return best_start
    
    N = 100
    for t in range(1, 11):
        _ = input()  # tc
        matrix = []
        for _ in range(N):
            row = list(map(int, input().split()))
            matrix.append(row)
        ans = get_best_start()
        print(f'#{t} {ans}')
    ```