# 221. Maximal Square

Status: done, in progress
Theme: DP
Created time: November 13, 2023 11:14 AM
Last edited time: November 13, 2023 11:59 AM

- 11/10 시험과 밀접한 문제로 보인다
    
    주어진 사각형에서 중복되지 않은 원소들을 갖고 있는 가장 큰 사각형의 크기를 구하라 
    
- 코드
    
    ```python
    class Solution:
        def maximalSquare(self, matrix: List[List[str]]) -> int:
            m, n = len(matrix), len(matrix[0])
            dp = [[0]*(n+1) for _ in range(m+1)]
            max_side = 0 
            for i in range(m):
                for j in range(n):
                    if int(matrix[i][j]) == 1:
                        dp[i+1][j+1] = min(dp[i][j], dp[i+1][j], dp[i][j+1]) + 1 
                        if dp[i+1][j+1] > max_side:
                            max_side = dp[i+1][j+1]
            print(dp)
            return max_side * max_side
    ```
    
- 바로 해설로 넘어감
- 이 문제는 정사각형을 다룬다
- 새로운 값 계산
    
    1) matrix에서의 값이 1이면 탐색 시작 (i, j)
    
    - 우리가 dp table에서 채우려는 위치는 (i+1, j+1) 왜냐면 dp matrix의 크기는 (m+1 * n+1)
    
    2) 1)이 정사각형에서 bottom-right cell라고 생각
    
    3) surrounding elements: (i-1, j-1), (i, j-1), (i-1, j)
    
    - 만약 i-1 <0 or j-1<0이면? ⇒ 이럴 때를 위해 dp matrix는 padding (m+1 by n+1)
    
    4) 3)의 min 값을 구한다 
    
    - min이 0이면 셋 중에 하나는 0이라서 정사각형 만들기 실패
    - min이 1이면 셋 다 1이라서 정사각형 만들기 성공
    
    5) 4) +1 (matrix에서 i,j cell 값)
    
    - 주변이 어떠하든 자기 자신은 1이기 때문에 최소 1x1의 사각형을 만들 수 있음
    
    ![Untitled](Untitled%2076.png)
    
- transition & end
    - base case: dp table 초기화를 0으로 해서 따로 코드는 없지만 top left → bottom left 진행 방향의 다른 문제들이 그렇듯이 첫번째 row, 첫번째 column 모두 0
    - end: matrix에서 가장 큰 값 by 큰 값
    - 사각형 크기를 더 넓게 잡는 것을 고려하지 않고, 그냥 (0, 0)부터 (m,n)까지 똑같은 과정 반복
    
    ![Untitled](Untitled%2077.png)
    
- dp table 초기화가 조금 알쏭달쏭. 첫번째 row, column은 둔다고 하는데, 두번째 row, column은 matrix랑 동일하게 맞춰줘야 시작이 되는 것 아닌가? → base case가 문제가 아니라 table indexing이 문제였음
    - 점화식에서 dp table은 padding이 되어 있어서 i+1, j+1 로 indexing
    - 근데 평소 처럼 i-1, j-1 을 가져다쓰니 총 2칸 차이가 나버리고, 원래 생각했던 대로 이전 계산 결과를 가져다 쓰는 게 아니게 됨
    - base 케이스는 따로 생성하지 않고, 점화식을 i-1 → i, j-1 → j로 수정했더니 해결
    - 점화식 내에서 min 값을 구하는 이웃은 matrix가 아니라 dp table 기준