# 750. Number Of Corner Rectangles

Status: in progress, incomplete
Theme: DP
Created time: November 28, 2023 1:08 PM
Last edited time: November 29, 2023 11:51 AM

- [x]  복기해서 풀어보기
- 프리미엄 문제
- 문제 이해
    
    축이랑 평행하면서 네 모서리의 1로 만들어질 수 있는 사각형의 개수 
    
    정사각형이 아니라 직사각형
    
    1이 있는 같은 칼럼 같은 행
    
    Also, all four `1`'s used must be distinct. → 한 칸짜리 1은 혼자서 사각형이 될 수 있지만 이건 count 대상은 아니라는 뜻 같음.
    
    이런 것도 안됨 
    
    ![Untitled](Untitled%20149.png)
    
- 남의 코드
    
    ```python
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(n)] # num_col x num_col
    ans = 0
    for i in range(m):
    		for j in range(n):
    				if grid[i][j] == 1: # 좌상 꼭짓점
    						for k in range(j+1, n):
    								if grid[i][k] == 1: # 같은 row, 더 오른쪽 col # 우상 꼭짓점 
    										ans += dp[j][k] # 처음에는 0
    										dp[j][k] += 1
    return ans 
    ```