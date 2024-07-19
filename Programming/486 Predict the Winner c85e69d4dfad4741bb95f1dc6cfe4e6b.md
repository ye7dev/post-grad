# 486. Predict the Winner

Status: in progress, 🏋️‍♀️
Theme: DP
Created time: November 28, 2023 3:08 PM
Last edited time: November 29, 2023 11:47 AM

- [x]  다시 풀어보기. 특히 DP bottom up index 주의 해서
- 코드
    
    ```python
    class Solution:
        def predictTheWinner(self, nums: List[int]) -> bool:
            n = len(nums)
            dp = [[0] * n for _ in range(n)]
            # base case : diagonals
            for i in range(n):
                dp[i][i] = nums[i]
            # transition for upper diagonals
            for i in range(n-2, -1, -1):
                for j in range(i+1, n):
                    dp[i][j] = max(nums[i]-dp[i+1][j], nums[j]-dp[i][j-1])
            
            return dp[0][n-1] >= 0
    ```
    
- 빈출 미디엄
- 문제 이해
    - p1이 시작 → 번갈아가며 가장자리(0 or -1)에 있는 숫자 가져감 → 선택한 숫자를 자기 점수에 더함 → array에 원소가 더 이상 남아 있지 않으면 게임 종료 → p1이 이기는 게임이거나 동점이면 return True,
- 과정
    
    nums[0]과 nums[-1] 중에 더 큰 걸 ad hoc 하게 고르는 게 능사가 아님-반례: `nums = [1,5,233,7]`
    
    둘 중에 하나를 고르고 나면 나머지 하나는 다음 선수의 edge가 됨 
    
    한번의 선택 시에 두 개의 layer를 생각해야 함 
    
    자기 layer랑 그 안쪽의 layer. 위의 예시에서 보면 1,7 → 1 선택 시에 5,7이 다음 선수에게 가고, 7 선택 시에 1, 233이 다음 선수에게 감. 이 두 개 중에 자기한테 더 유리한 걸 선택 
    
    ```python
    # nums[0] choice -> nums[1] nums[-1]이 다음 선택
    # nums[-1] choice -> nums[0], nums[-2]이 다음 선택
    ```
    
    1시간 풀었고 41/62까지 그냥 iteration으로 맞췄는데 이후는 답을 봐야겠다 
    
    ```python
    class Solution:
        def predictTheWinner(self, nums: List[int]) -> bool:
            n = len(nums)
            p1, p2 = 0, 0 
            play_times = n // 2 
            s, e = 0, n-1
            for t in range(play_times):
                if e-s+1 == 2:
                    p1 += max(nums[s], nums[e])
                    p2 += min(nums[s], nums[e])
                else:
                    if max(nums[s], nums[e-1]) > max(nums[s+1], nums[e]):
                        p1 += nums[s]
                        if nums[s+1] > nums[e]:
                            p2 += nums[s+1]
                            s += 2 
                        else:
                            p2 += nums[e]
                            s += 1
                            e -= 1 
                    else:
                        p1 += nums[e]
                        if nums[s] > nums[e-1]:
                            p2 += nums[s]
                            s += 1
                            e -= 1 
                        else:
                            p2 += nums[e-1]
                            e -= 2 
            if n & 1:
                p1 += nums[s]
            
            if p1 >= p2:
                return True
            else:
                return False
    ```
    
- Editorial-무려 solution이 4가지나 된다.
    - Recursion
        - function `max_diff(left, right)`
            - input: left, right indices
            - 두 선수 사이의 점수 차를 최대로 만들기 위한 함수
        - at each step
            - 현재 선수가 숫자를 하나 선택
            - 함수를 재귀 호출 → 다음 선수가 최적의 수를 선택
            - 두 선수 간의 점수 차이 update
            - 첫번째 선수가 얻을 수 있는 최대 점수 차이를 return
        - negative impact factor
            - 첫번째 선수가 선택할 수 있는 숫자는 nums[left], nums[right]. → `max_diff(left, right)` 는 첫번째 선수의 입장에서 얻을 수 있는 최대 점수 차
            - left가 먼저 선택되었다고 하면 두번째 선수의 선택지는 nums[left+1]부터 nums[right] → `max_diff(left+1, right)` 는 두번째 선수 입장에서 얻을 수 있는 최대 점수 차. ⇒ 우리는 첫번째 선수를 응원하는 입장이고, 두번째 선수의 득점은 첫번째 선수의 실점이기 때문에, 첫번째 선수 입장에서는 마이너스 ⇒ 두번째 선수의 max_diff 값 앞에는 -1을 붙이자
            
            ⇒ 첫번째 선수가 left를 선택하고 나서 얻을 수 있는 최대 점수 차는 `nums[left] - max_diff(left+1, right)`
            
            반대로 right를 선택하고 나서 얻을 수 있는 최대 점수 차는 `nums[right] - max_diff(left, right-1)`
            
            ⇒ 둘 중에 더 큰 걸 골라야 하기 때문에 `max_diff(left, right) = max(nums[left]-max_diff(left+1, right), nums[right]-max_diff(left, right-1))`
            
        - 재귀호출 계속하다가 hit 하고 return 좌르륵 하는 지점
            - left =right : 마지막 순서의 선수가 마지막으로 남은 숫자를 고르는 경우
            - 이 때 그가 만들 수 있는 최대 점수 차이는 `nums[left]`
                - 어차피 원소가 하나라 그냥 nums[left]로 하는 것
        - 위의 가이드에 따라 짠 코드
            
            ```python
            class Solution:
                def predictTheWinner(self, nums: List[int]) -> bool:
                    def max_diff(left, right):
                        if left == right:
                            return nums[left]
                        choose_left = nums[left]-max_diff(left+1, right)
                        choose_right = nums[right]-max_diff(left, right-1)
                        return max(choose_left, choose_right)
                    
                    return max_diff(0, len(nums)-1) >= 0
            ```
            
        
    - DP, Top-down (best)
        - dictionary나 2d array 사용해서 cache 생성-저장하고 기억하기-memo
        - max_diff(left, right)가 이미 memo 에 있으면 계산하지 말고 그대로 가져다가 써라
        - 시간 개빨라짐 recursive 2958 → 35
    - DP, Bottom-up (설명이 잘 이해안감)
        - 더 작은 부분 문제에서 더 큰 부분 문제로 합쳐가기
        - 모든 subproblem들을 2D array에 나타낸다
            - `dp[left][right]` : subarray nums[left~right]를 대상으로 현재 선수가 얻을 수 있는 최대 점수
                
                → 우리가 얻으려는 답: `dp[0][n-1]`
                
        - base case
            - `dp[i][i]` : 범위 안에 있는 숫자가 하나기 때문에 최대 점수는 nums[left]. recursive에서의 base case랑 동일
            - `dp[left][right]`
                - nums[left] 선택 → 내가 얻은 점수 nums[left]
                    - 두번째 선수가 얻는 점수: dp[left+1][right]
                    - 증가하는 점수 차 nums[left] - dp[left+1][right]
                        - a.k.a 내가 실질적으로 얻은 점수
                - nums[right] 선택 → 점수 차는 nums[right]-dp[left][right-1] 만큼 증가
        - 코드
            
            ```python
            class Solution:
                def predictTheWinner(self, nums: List[int]) -> bool:
                    n = len(nums)
                    dp = [[0]*n for _ in range(n)]
                    # base case
                    for i in range(n-1):
                        dp[i][i] = nums[i]
                    
                    for diff in range(1, n): # 1..n-1
                        for left in range(n-diff): # n-2..0
                            right = left + diff 
                            dp[left][right] = max(nums[left]-dp[left+1][right], 
            																			nums[right]-dp[left][right-1])
                    
                            
                    
                    return dp[0][n-1] >= 0
            ```
            
            ```python
             for diff in range(1, n): # 1..n-1
                for left in range(n-diff): # n-2..0
                    right = left + diff 
            ```
            
            | diff | left | right |
            | --- | --- | --- |
            | 1 | 0, 1, …, n-2 | 1, 2, …, n-1 |
            | 2 | 0, 1, …, n-3 | 2, 3, …, n-1 |
            | n-2 | 0, 1 | n-2, n-1 |
            | n-1 | 0 | n-1 |
            - 더 직관적인 indexing
                - left가 n-1에서 시작하면 이미 오른쪽 끝이라 오른쪽에 더 채울 것이 없음
                    - right가 없기 때문에 dp[n-1][n-1]이 경계인데, 이미 채워진 상태.
                
                → left는 n-2에서 시작해서 점점 앞으로 감. 작아짐
                
                - right는 항상 left보다 한 칸 뒤에서 시작, 갈 수 있는 가장 오른쪽 까지
            
            ```python
            for left in range(n-2, -1, -1):
            	for right in range(left+1, n):
            ```
            
            | left | right |
            | --- | --- |
            | n-2 | n-1 |
            | n-3 | n-2, n-1  |
            | 1 | 2, 3, … n-1 |
            | 0 | 1, 2, … n-1 |
            - left = n-2, right = n-1일 때
                
                → max(nums[n-2]-dp[n-1][n-1], nums[n-1]-dp[n-2][n-2])
                
            - left = n-3, right = n-1일 때
                
                → max(nums[n-3]-dp[n-2][n-1], nums[n-1]-dp[n-3][n-2])