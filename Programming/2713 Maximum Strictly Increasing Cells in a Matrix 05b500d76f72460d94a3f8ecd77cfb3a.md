# 2713. Maximum Strictly Increasing Cells in a Matrix

Status: in progress
Theme: DP
Created time: November 24, 2023 12:54 PM
Last edited time: November 25, 2023 12:35 PM

- 과정
    
    matrix에 hard에 빈출이면 삼성에서도 좋아할 문제다
    
    근데 문제만 이해하고 우선 샤워하러 가자 
    
    cell 값이 가장 작은 데서부터 시작하는 게 좋을 듯 
    
    모든 cell을 다 돌면서 개수를 세야 할 것 같은데 여기서 dp를 어떻게 활용해야 할지 모르겠다 
    
    샤워하러 가자 
    
    확실한 건 최대값 cell에서 이동을 종료한다는 것 
    
- 힌트
    - cell 값을 정렬해서 오름차순으로 늘려가면서 이전 maximum path를 저장해라
    - 최소 값에서 갈 수 있는 값이 두 개일 경우 둘 중에 어느걸 가지고 가야 하는지가 문제임
- 남의 풀이
    
    key를 value, value를 좌표로 해서 sorted(dict) 하는게 더 코드가 간편 
    
    table을 dp와 res 두 가지 사용 
    
    - dp[i][j] : i, j 좌표까지 왔을 때 그동안 지나온 cell의 최대 개수
        - 이전 단계에서 i,j와 같은 row거나 같은 column이어야 다음 step에서 dp[i][j]에 올 수 있다
        - max(같은 row에 있는 cell 중 지나온 cell의 최대 개수, 같은 col에 있는 cell 중 지나온 cell의 최대 가수) + 1 (current cell)
    - res[i] : row i에서 max_step을 가진 cell의 step 수
    - res[m+j] : column j에 있는 max_step을 가진 cell의 step 수
        - m은 모든 row의 개수
    
    ```python
    for a in sorted(A):
                for i, j in A[a]:  
                  dp[i][j] = max(res[i], res[~j]) + 1  
                for i, j in A[a]: 
                   res[~j] = max(res[~j], dp[i][j]) 
                   res[i] = max(res[i], dp[i][j])    
      return max(res)
    ```