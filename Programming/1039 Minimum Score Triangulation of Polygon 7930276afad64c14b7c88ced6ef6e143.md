# 1039. Minimum Score Triangulation of Polygon

Created time: June 20, 2024 5:28 PM
Last edited time: June 21, 2024 3:13 PM

- 문제 이해
    - n개의 면을 가진 다각형. 각 꼭지점에는 정수값이 할당되어 있음
    - 주어진 array values는 꼭지점을 시계 방향으로 돌면서 값을 가져온 것
    - n개의 변을 가진 다각형은  n - 2 개의 삼각형으로 분할될 수 있다
        - 예) 오각형은 3개의 삼각형, 사각형은 2개의 삼각형으로 분할 가능
    - 각 삼각형에 대해, 해당 삼각형의 값은 세 꼭지점 값의 곱
    - 삼각분할의 총 점수는 n-2개 삼각형 값의 합
    - 가장 작은 총 점수를 구하라
- scratch
    - length=3의 sliding window인가 했는데
        - [3, 7, 4, 5]에서 [3, 7, 4]가 한 세트, [7, 4, 5]가 한 세트
    - 꼭 그렇지만도 않음 -  `1,3,1,4,1,5`
    - 그냥 삼각형으로 아무 세 원소 뽑고, 나머지는…?
- solution
    - domain knowledge
        - 다각형 내에서 하나의 삼각형은 두 개의 하위 다각형을 만든다
        - 다각형의 각 edge는 정확히 하나의 삼각형의 일부여야 한다
            - 교차해서 삼각형을 만들 수는 없으니
    - 어제 본 Video에서…
        - matrix multiplication 유형의 dp 문제라고 했음.
        - 다각형의 각 변 edge는 array 상에서 나란히 있는 두 vertex
        - 교차하지 않는 삼각형은 어떻게 보장하는지 모르겠음
            - 삼각형 하나를 만들면서 영역이 아예 갈라진다고(?) 보면 된다
            
            ![Untitled](Untitled%2078.png)
            
- AC 코드
    - recursive + memo
        
        ```python
        class Solution:
            def minScoreTriangulation(self, values: List[int]) -> int:
                n = len(values)
                memo = {}
        
                def recur(i, j):
                    # check memo
                    state = (i, j)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i+1 == j:
                        return 0 
                    # recursive case
                    min_score = float('inf')
                    cur_score = values[i] * values[j]
                    for k in range(i+1, j):
                        next_score = recur(i, k) + recur(k, j)
                        min_score = min(min_score, cur_score * values[k] + next_score)
                    # save memo
                    memo[state] = min_score
                    return memo[state]
                return recur(0, n-1) 
        ```
        
    - bottom-up (⚡️)
        
        ```python
        class Solution:
            def minScoreTriangulation(self, values: List[int]) -> int:
                n = len(values)
                dp = [[float('inf')] * n for _ in range(n)]
        
                # base case
                for i in range(n): # n-1
                    for j in range(i, min(n, i+2)):
                        dp[i][j] = 0 
                
                # iterative case
                for length in range(3, n+1):
                    for start in range(n+1-length):
                        # start + length - 1 < n -> stat < n+1-length
                        end = start + length -1 
                        cur_score = values[start] * values[end]
                        for k in range(start+1, end):
                            dp[start][end] = min(dp[start][end], cur_score * values[k] + dp[start][k] + dp[k][end])
                            
                return dp[0][n-1]
        ```