# 799. Champagne Tower

Status: done, in progress, with help
Theme: DP
Created time: February 3, 2024 12:08 PM
Last edited time: February 4, 2024 5:26 PM

- Progress
    - 문제 이해
        - 그림
            
            ![Untitled](Untitled%20226.png)
            
        - 첫번째 row는 잔 1개, 두번째는 잔 2개 … 100번째 row까지 있음
        - 가장 꼭대기의 첫번째 잔에 샴페인을 부을 때, 꽉 차서 넘치는 양은 그 잔의 바로 왼쪽과 오른쪽으로 흘러들어가게 됨. 얘네도 꽉 차면 각 잔의 또 바로 왼쪽 오른쪽으로 넘쳐 들어가고…만약 맨 아래 100번째 row에 있는 잔에도 꽉 차고 나면 넘친 샴페인은 바닥으로 흐르게 됨
        - 두 잔의 샴페인을 부으면 첫번째 row의 잔이 꽉 차고, 남은 한 잔의 양은 두번째 row의 양 잔에 절반씩을 채우게 됨
        - 세 컵을 부으면 세 잔 모두 차고, 네 컵을 부으면 위의 세 컵 다 차고, 남은 한 잔의 양이 네 컵에 나누어 들어가게 됨 → ~~세번째 row의 잔마다 1/4컵의 샴페인이 채워진 상태~~
            
            → 문제 잘못 이해함. the third row has the middle glass half full, and the two outside glasses are a quarter full, as pictured below.
            
        - non-negative integer cups of champagne이 부어질 때(input: poured), i번째 row의 j번째 glass가 얼마나 차 있게 되는지 return 하라
    - 과정
        - i th row에는 i+1개의 잔이 있음
        - 각 잔은 row, row 안에서의 위치 = col 총 2개의 좌표로 식별됨
        - i th row 까지의 잔의 전체 개수는
            - 1 + 2 +. .. + (i+1) = (i+1) * (i+2) // 2
            - 예) i = 3 → 4 * 3 // 2 = 6 = 1 + 2 + 3
        - i+1 th row는 ith row보다 i+1개 만큼 glass가 많다
            - 예) i+1 = 3 → 2nd row는 3개, 3rd row는 4개 → 4개가 더해짐
        - 부어지는 양 최대는 10**9
            - 잔의 최대 개수는 (99+1) * (99+2) // 2 = 101 * 50 = 5050
        - 반례
            - 25 poured, (6, 1)
            - 1 + … + 5 = 5 * 6 / 2 = 15
            - 10/6
            - 근데 위에서부터 생각해보면
            - 같은 row라도 col index에 따라 받게 되는 양이 달라짐.
            
            | row |  |
            | --- | --- |
            |        1 | 1 |
            |       1 1  | 1 1 |
            |      1 1 1 | 1 2 1 |
            |     1 1 1 1 | 1 2 2 1 |
            |    1 1 1 1 1  | 1 2 2 2 1 |
            |   1 1 1 1 1 1   |  |
            |  1 1 1 1 1 1 1  |  |
            
            1 + 1 + 1  = 3 → 4-3 = 1 → 1/ 4
            
- AC 코드
    - current ans[r][c] : 윗 열에서 넘쳐서 흘러온 양
    - 흘러온 양이 0보다 크면
        - 현재 잔을 채우고 남은 양을 배분해서 또 아래로 넘쳐 흐르도록 한다
        - 현재 잔을 채운다
    - r이 마지막 row 하나 전까지 들어가기 때문에, nested for loop이 끝나고 나면 ans[r][c]는 윗 열에서 넘쳐 흘러온 양을 갖고 있는 상태
        - 만약 윗 열에서 넘쳐 흘러온 양이 음수였으면 r+1에 대한 작업을 안했을 것이므로 0으로 남아 있고
        - 넘쳐 흘러온 양이 양수 였으면 ans[r+1]에 더해줬을 것
    - 마지막 열 ans[r][c]는 1보다 클 수 도 있는 상태라서 1로 clipping 해주면서 return
    - 같은 cell에 들어 있는 state가 다시 두 가지 의미를 갖게 됨
        - overflow → 연산 → 진짜 잔에 채운 양
    - row range(query_row+1) 이니까 0…query_row-1, query_row
        - 그래야 ans[query_row]로 indexing 가능
    - overflow를 계산하기 위해서는 ans[r][c]가 온전히 자기 자신의 잔에 담긴 양일 수 없다
    
    ```python
    class Solution:
        def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
            if poured == 0:
                return 0 
            # row idx : 0 -> 99, glass_num : 1 -> 100
            ans = [[0] * (i+1) for i in range(query_row+1)] 
            # base case
            ans[0][0] = poured
            # recurrence relation
            for r in range(query_row): # r = 0 
                for c in range(r+1): # c = 0
                    overflow = (ans[r][c]-1) / 2
                    if overflow > 0:
                        ans[r+1][c] += overflow
                        ans[r+1][c+1] += overflow
                        ans[r][c] = 1
            
            return min(ans[query_row][query_glass], 1)
    ```
    
    ```python
    class Solution:
        def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
            # row: 0 -> 99, glass: 1 -> 100
            ans = [[0] * (row+1) for row in range(query_row+1)]
            
            # base case
            ans[0][0] = poured # start with overflow 
    
            for r in range(query_row): # 1 -> 98
                for c in range(r+1): # 0, 1, ... r
                    # get overflow for the next row (in total()
                    overflow = ans[r][c] - 1
                    # flow each half to the next row
                    if overflow > 0:
                        ans[r+1][c] += overflow / 2
                        ans[r+1][c+1] += overflow /2 
                        # fill up the current glass
                        ans[r][c] = 1
                    # overflow < 0 -> ans[r][c] - 1 < 0 -> ans[r][c] < 1 -> no overflow
            
            # target cell status: got the half of the overflow from the previous row 
            # if half > 0 -> partially or fully filled / half < 0 -> target cell stays zero 
            return min(ans[query_row][query_glass], 1)
    ```
    
- Trial
    - row 단위 나머지 분배 → 132/312
        - 4 unit이 들어올 때 (2, 1) 잔에 채워진 양
            - 0, 1, 2 → 1, 2, 3
        - prev_row_glass = (2-1+1) * (2-1+2) // 2 = 3
            - 바로 앞 열까지 3잔
        - prev_row_glass + (query_row + 1)
            - 지금까지의 열을 모두 포함할 때의 잔 개수
        - cur_share
            - 1 2 … 2 1
            - 2개만 1이고 나머지는 2 → 1 2 1
            - 남은 양은 1 → 1/4, 1/2, 1/4
        
        ```python
        class Solution:
            def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
                # edge case
                if poured == 0:
                    return 0
                total_glass = 100 * 101 // 2 # 1 + 2 + ... + 100
                if poured >= total_glass:
                    return 1 
                prev_row_glass = (query_row-1+1) * (query_row-1+2) // 2
                if prev_row_glass >= poured:
                    return 0 
                cur_row_glass = (query_row+1) * (query_row+2) // 2
                if cur_row_glass <= poured:
                    return 1 
                return (poured - prev_row_glass) / (query_row+1)
        ```
        
    - simulation
        
        ```python
        class Solution:
            def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
                if poured == 0:
                    return 0 
                # row idx : 0 -> 99, glass_num : 1 -> 100
                ans = [[0] * (i+1) for i in range(100)] 
                # base case
                ans[0][0] = poured
                # recurrence relation
                for r in range(99): # r = 0 
                    for c in range(r+1): # c = 0
                        ans[r+1][c] += (ans[r][c]-1) / 2
                        ans[r+1][c+1] += (ans[r][c]-1) / 2 
                
                return max(ans[query_row][query_glass], 0)
        ```
        
- Editorial
    - Intuition
        - glass에 얼마의 샴페인이 담기는지 추적하지 말고, glass를 지나쳐 흐르는(flow through) 양을 추적한다
            - 예) poured = 10 일 때, top glass의 flow through는 10, 두번째 row의 각 glass의 flow through는 (10 - 1) / 2 = 4.5
    - 알고리듬
        - 어떤 glass가 X의 flow through를 갖는다면, 왼쪽과 오른쪽에 flow through 하게 될 양은 Q = (X-1) / 2
        - 100 rows of glasses에 대해 simulate
        - (r, c) 위치에 있는 잔을 채우고 남는 양은 (r+1, c), (r+1, c+1)의 glass로 가게 될 것