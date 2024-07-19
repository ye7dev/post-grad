# 546. Remove Boxes

Created time: May 26, 2024 4:37 PM
Last edited time: May 27, 2024 7:35 PM

- 문제 이해
    
    box마다 양의 정수가 써 있음 - 같은 색이면 같은 수를 의미 
    
    box가 더 이상 없을 때까지 몇 번을 돌면서 box를 제거할 수 있음 
    
    같은 색깔의 연속된 박스를 선택해서 제거할 수 있음 
    
    이 때 얻게 되는 점수는 제거한 박스의 제곱만큼 
    
    얻을 수 있는 최대 점수를 return 
    
- scratch
    
    이거 옛날에 풀었던 [[**312. Burst Balloons**](https://leetcode.com/problems/burst-balloons/description/)](312%20Burst%20Balloons%204ea4766b2ba44d3489ee8ecaaa8ebd80.md) 이 문제와 비슷
    
    box가 길면 100개 주어지는데 그냥 brute force로 풀어볼까보다. 최소 원소는 1개 
    
    - 예제 follow
    `[1,3,2,2,2,3,4,3,1]`
        - 2의 연속 3개를 없애면 9점 얻고 3343
        - 4를 없애면 1점 얻고 3이 3개가 됨  13331
        - 3의 연속 3개를 없애면 9점 얻고
        - 11 두 개 남고 마져 없애면 4
        
        → 9 +1 + 9 + 4 = 23 
        
    
    다음 같은 원소와의 interval을 기록해볼까 
    
    (no,7), (no, 3), (no,1), (yes,1), (yes, inf), (no, 2), inf, inf, inf 
    
    bottom-up으로 짤 때 k를 임의로 할 순 없으니까 다 계산하는게 맞겠지? 아니야 굳이 그렇게 안해도 될 듯
    
- Trial
    - Bottom-up
        
        ```python
        class Solution:
            def removeBoxes(self, boxes: List[int]) -> int:
                n = len(boxes)
                # dp[i][j][k]: subarray boxes[i:j+1] max point with k continuous box of boxes[i]
                dp = [[[0] * (n+1) for _ in range(n+1)] for _ in range(n+1)]
        
                # base case
                ## invalid range -> already 0 
                ## single box with k same box ahead
                acc = 0
                prev = None
                for i in range(n):
                    for k in range(n+1): # 0~n
                        dp[i][i+1][k] = (k+1) ** 2 
                
                # recursive case
                for i in range(n-1, -1, -1):
                    for j in range(i+2, n+1):
                        for k in range(n-1, -1, -1):
                            pop_now = dp[i][i+1][k] + dp[i+1][j][0]
                            pop_later = 0
                            for mid in range(i, j): # 범위 헷갈림 
                                temp = 0
                                if boxes[i] == boxes[mid]:
                                    temp = dp[i+1][mid][0] + dp[mid][j][k+1]
                                pop_later = max(temp, pop_later)
                            dp[i][j][k] = max(pop_now, pop_later)
                
                return dp[0][n][0]
        
        ```
        
    - Bottom-up II 59/63
        - 시간 초과 에러 난다. top-down이 통과했는데 왜?
        - give up
- solution
    - 기존 정의 및 제약사항
        - state definition
            - T(i, j): boxes[i:j+1] (i, j 모두 inclusive)를 제거할 때 얻을 수 있는 최대 포인트
            - 초기 문제를 다시 정의하면 T(0, n-1)
        - base case
            - T(i, i-1) → boxes[i:i-1+1] → empty set → no boxes, no points
            - T(i, i) → boxes[i:i+1] → single box → 얻을 수 있는 최대 점수는 1
        - recurrence relation
            - boxes[i]를 제거하는 경우의 수
                - 바로 제거해버리면 1점 얻음
                    - 남은 box에 대해 얻고자 하는 최대 점수는 T(i+1, j)
                    
                    → 1 + T(i+1, j)
                    
                - 같은 정수가 있는 다른 박스와 함께 제거하는 경우
                    - 같은 정수가 있는 다른 박스가 neighbor(adjacent)가 될 때까지 기다리기로
                        - 이 박스의 index가 m이라고 하면, boxes[i+1: m]까지의 박스는 제거된 상태여야 함
                        - 제거된 만큼 포인트를 얻기 때문에 여기서 얻은 포인트는 T(i+1, m-1)
                    - 여기서 box는 크게 두 부분으로 나뉨
                        - boxes[i]
                        - boxes[m, j]
                            - 제거하고 난 이후라 i 의 오른쪽에 맞닿아 있음
                            - 바로 T(m, j)로는 할 수 없는 것이, subproblem 정의에 포함되지 않은 추가적인 정보가 있기 때문
                - subproblem 정의에만 의존하지 않고, 외부 정보를 이용하는 dp 문제 유형
                    - [[**312. Burst Balloons**](https://leetcode.com/problems/burst-balloons/description/)](312%20Burst%20Balloons%204ea4766b2ba44d3489ee8ecaaa8ebd80.md) 의 경우, nums[i, j]로부터 얻을 수 있는 maximum coins가 nums[i]의 왼쪽 두 숫자와, nums[j]의 오른쪽 두 숫자에 의해 결정되었음
                        - 점화식
                            
                            ```python
                            dp[0][4] = dp[0][2] + nums[0] * nums[2] * nums[4] + dp[2][4]
                            # dp[0][4]: 1~3 풍선을 터트릴 때 얻을 수 있는 가장 최대 동전 수 
                            # dp[0][2]: 1번 풍선을 먼저 터트릴 때 얻을 수 있는 최대값 
                            # dp[2][4]: 3번 풍선을 먼저 터트릴 때 얻을 수 있는 최대값
                            # 앞에 두 개의 경우를 미리 dp table에서 가져왔다 = 1번, 3번 풍선을 터트린 상태 
                            # -> 0, 2, 4번 풍선만 남아 있다 
                            # -> 이 세 개에서 2번 풍선을 마지막으로 터트릴 때 얻을 수 있는 금액이
                            # nums[0] * nums[2] * nums[4]
                            ```
                            
                            ```python
                            for L in range(2, n):
                                        for i in range(n-L): # 0:n-2 ~ 0
                                            j = i+L # j: 0+2-1=1, 0+n-1=n-1
                                            for k in range(i+1, j):  
                                                dp[i][j] = max(dp[i][j], dp[i][k] + nums[i]*nums[k]*nums[j] + dp[k][j])
                                    
                            ```
                            
                    - 이런 문제 유형의 문제는 well-defined recurrence relation을 갖지 못한다는 것
                        - external information을 흡수해서 새로운 subproblem 정의가 self-contained 되게 만들어라
    - state definition 재정의
        - 외부 정보가 뭐냐
            - subarray boxes[m, j] 입장에서 보면 m 왼쪽으로 같은 색깔의 box가 몇 개 있는지-k-에 대한 정보가 전혀 없음
            - k가 주어졌을 때는 얻을 수 있는 최대 점수가 정해져 있음
            
            → T(i, j) 입장에서는 외부 정보가 k 
            
        - k를 state definition에 다시 반영하면 T(i, j, k)
            - subarray boxes[i,j] (j inclusive)를 제거함으로써 얻을 수 있는 최대 점수
            - 이 때 i의 왼쪽에는 i번째 박스와 같은 색의 박스가 k개 나란히 있음
    - original problem(return value)
        - T(0, n-1, 0)
            - index 0보다 왼쪽에 있는 box는 없기 때문에 k는 0
    - termination condition(base case)
        - T(i, i-1, k)
            - k는 무슨 값이 되던 상관 없고, 범위 상 시작점보다 끝점이 작은 범위에는 박스가 존재할 수 없기 때문에 얻을 수 있는 점수도 0.
        - T(i, i, k)
            - 범위 내의 박스는 한 개이고, 그 박스와 같은 숫자의 박스가 k개이기 때문에 총 k+1개가 같은 숫자이면서 continuous
            - 여기서 얻을 수 있는 최대 점수는 (k+1) ** 2
    - recurrence relation for `T(i, j, k)`
        - 두 가지 경우 중 점수가 더 큰 쪽
        - 이번 박스를 터트리는 경우
            - `(k+1) ** 2 + T(i+1, j, 0)`
            - i까지의 박스를 모두 제거한 상태기 때문에, i+1의 왼쪽에는 박스 자체가 없다 → 같은 정수의 박스도 있을 수 없기 때문에 k=0
        - keep 했다가 나중에 터트리는 경우
            - boxes[i]를 같은 색의 boxes[m]에 갖다가 붙여서 터트리기 위해 기다리는 경우
            - `T(i+1, m-1, 0) + T(m, j k+1)`
                - `T(i+1, m-1, 0)`
                    - i, i+1, …, m-1, m
                    - 여기서 i+1~m-1까지 먼저 터뜨려서 얻는 점수
                    - i+1의 왼쪽에는 i가 있어서 연속된 박스가 없기 때문
                        - m은 i+1일 수도 있다.
                        - 그럼 앞부분은 0이 되고, 뒷부분이 T(i+1, j, k+1)로 바로 들어가는 듯?
                - `T(m, j, k+1)`
                    - i와 같은 k개, i, m 이렇게 되어 있는 상태인데
                    - m이랑 i랑 같은 박스 = i 앞에 있는 k와도 모두 같은 박스라는 의미
                    - 그러면 결국 m 기준으로는 k+1개의 같은 박스를 갖고 있는 것.
                - i와 j 사이에서 i와 같은 정수를 가진 박스가 여러 개 있을 수 있기 때문에
                    - i < m ≤ j 이면서, i와 같은 박스 종류를 만족하는 모든 m에 대해 위의 식을 계산해 봐야 함
                        - m은 최소 i+1이어야 함
        
- AC 코드
    - Top-down
        
        ```python
        class Solution:
            def removeBoxes(self, boxes: List[int]) -> int:
                n = len(boxes)
                memo = {}
                # end를 exclusive로 짜보자
                def recur(start, end, num_continuous):
                    # check memo
                    state = (start, end, num_continuous)
                    if state in memo:
                        return memo[state]
                    # base case
                    ## invalid range
                    if start == end:
                        return 0 
                    ## single box in the scope 
                    if end-start == 1:
                        return (num_continuous + 1) ** 2 
                    # recursive case
                    pop_now = (num_continuous + 1) ** 2 + recur(start+1, end, 0) 
                    pop_later = 0 
                    for mid in range(start+1, end):
                        if boxes[start] == boxes[mid]:
                            temp = recur(start+1, mid, 0) + recur(mid, end, num_continuous+1)
                            pop_later = max(temp, pop_later)
                    
                    # save at memo 
                    memo[state] = max(pop_now, pop_later)
                    return memo[state]
                return recur(0, n, 0)
        
                    
                
        ```