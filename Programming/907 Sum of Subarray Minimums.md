# 907. Sum of Subarray Minimums

Status: in progress, 🏋️‍♀️
Theme: DP
Created time: February 9, 2024 10:08 PM
Last edited time: February 13, 2024 12:07 PM

- Progress
    - 문제 이해
        
        arr이 integer array일 때, every contiguous subarray of `arr` 의 최소값의 합을 구하라 
        
    - 과정
        
        `arr = [3,1,2,4]`
        
        3, 31 (1), 312(1), 3124(1) 
        
        이전 state에서 최소값이 유지되면 그 수를 한번 더 더해주는 거고, 새로 추가되는 원소 값이 작으면 그 값을 더해주는 거고 
        
        4(4)
        
        24 (2)
        
        124 (1)
        
        3124 (1) 
        
        2(2)
        
        12(1)
        
        312(1)
        
        1(1)
        
        31(1)
        
        3(3)
        
- Trial
    - Top-down
        
        ```python
        class Solution:
            def sumSubarrayMins(self, arr: List[int]) -> int:
                mod = 10 ** 9 + 7 
                n = len(arr)
                memo = {}
        
                # function
                def recur(start, end, min_value):
                    # check memo
                    state = (start, end, min_value)
                    if state in memo:
                        return memo[state]
                    # base case
                    if end == n:
                        return 0 
                    # recurrence occurence
                    cur_value = arr[end]
                    if cur_value < min_value:
                        memo[state] = (cur_value + recur(start, end+1, cur_value)) % mod
                    else:
                        memo[state] = (min_value + recur(start, end+1, min_value)) % mod
                    return memo[state]
                
                for i in range(n):
                    recur(i, i, 10 ** 5)
                return sum(memo.values()) % mod
        ```
        
    - Top-down → 82/88 (Memory Exceed Error)
    - Bottom-up → 77/88 (Memory Exceed Error)
        
        ```python
        class Solution:
            def sumSubarrayMins(self, arr: List[int]) -> int:
                mod = 10 ** 9 + 7 
                n = len(arr)
                dp = [[0]* n for _ in range(n)]
                # dp[i][j] : sum of min subarray considering arr[i:j+1]
                # base case 
                for i in range(n):
                    dp[i][i] = arr[i] # arr[i:i+1]
                
                for i in range(n):
                    for j in range(i+1, n):
                        dp[i][j] = (dp[i][j] + min(arr[j], dp[i][j-1])) % mod
                
                ans = 0 
                for i in range(n):
                    ans = (ans + sum(dp[i])) % mod
                
                return ans
        ```
        
    - Bottom-up → 77/88(TLE)
        
        ```python
        class Solution:
            def sumSubarrayMins(self, arr: List[int]) -> int:
                mod = 10 ** 9 + 7 
                n = len(arr)
                dp = [0]* n 
                # dp[i] : sum of min subarray of arr[i:]
                # base case 
                for i in range(n):
                    dp[i] = arr[i] # arr[i:i+1]
                
                for i in range(n):
                    cur_min = dp[i]
                    for j in range(i+1, n):
                        if cur_min > arr[j]:
                            cur_min = arr[j]
                        dp[i] = (dp[i] + cur_min) % mod
                
                return sum(dp) % mod
        ```
        
    - Monotonous stack
        - while loop condition에서 index와 값을 혼동하지 말 것
        
        ```python
        class Solution:
            def sumSubarrayMins(self, arr: List[int]) -> int:
                mod = 10 ** 9 + 7
                stack = []
                n = len(arr)
                ans = 0
        
                for i in range(n):
                    while stack and stack[-1] >= arr[i]:
                        mid = stack.pop()
                        left_boundary = stack[-1] if stack else -1 
                        right_boundary = i 
                        contribution = arr[mid] * (mid-left_boundary) * (right_boundary-mid)
                        ans = (ans + contribution) % mod 
                    stack.append(i)
        
                while stack:
                    mid = stack.pop()
                    left_boundary = stack[-1] if stack else -1 
                    right_boundary = n
                    contribution = arr[mid] * (mid-left_boundary) * (right_boundary-mid)
                    ans = (ans + contribution) % mod 
        
                return ans
        ```
        
- Editorial
    - Overview
        - 세 단계 과정
            1. 주어진 array의 모든 subarray를 고려한다
            2. 각 subarray의 minimum을 구한다 
            3. 2에서 구한 모든 minimum을 더한다 
        - 첫번째 approach
            - 각 array element의 정답 contribution
            - monotonic stack 사용
        - 두번째 approach
            - monotonic stack + dp
    - **Approach 1: Monotonic Stack - Contribution of Each Element**
        - Intuition
            - 주어진 array에서 all possible subarray range
                - two nested for loop - 하나는 start, 하나는 end
                - 하나의 범위에 대해서 minimum을 계산할 수 있음
                - running total of all minimums
            - 여기서 대부분의 시간은 모든 subarray를 생성하는데 사용됨 - O(n^2)
        - **Improving on brute force**
            - 범위 대신에 각 element에 주목
                
                → 그 element가 minimum으로 존재하는 모든 범위를 밝힘 
                
                → 모든 minimum sum에 각 element의 contribution을 결정 
                
            - 각 element가 smallest로 존재하는 범위를 이미 알고 있다고 가정
                - 특정 element가 주어진 범위에서 가장 작은 값이면, 그 범위의 subarray 중 해당 element를 포함하는 것의 개수를 결정할 수 있다
                - 해당 원소가 주어진 범위에서 가장 작은 값이기 때문에, 주어진 범위에서 생성하는 subarray-그 원소가 포함된-의 최소값은 늘 해당 원소
                
                → 해당 원소 값 * subarray 개수 = final summation에서 해당 element의 기여도 
                
            - 주어진 범위에서 특정 원소를 포함하는 subarray 개수를 얻는 법
                - 예) array: [0,3,4,5,2,3,4,1,4]
                    - 2를 최소값으로 하는 subarray의 개수를 찾아야
                        - 주어진 array에서 [3, 4, 5, 2, 3, 4] (range[1, 6]) 범위에 대해서 2가 최소 값
                        - 따라서 해당 범위에서 2를 포함하는 모든 subarray는 최소값을 2로 가질 것
                        
                        → 주어진 범위([1, 6])에서 2를 포함하는 subarray의 개수를 찾아라 
                        
                    - 2가 위치한 index 혹은 그보다 앞에서 시작하거나, 2가 위치한 index 혹은 그보다 더 뒤에서 끝나는 모든 subarray를 세야
                        - range [1, 6]을 세 부분으로 쪼갠다 - 2의 위치보다 앞, 2, 2보다 뒤
                        
                        ![Untitled](Untitled%2030.png)
                        
                        - 왼쪽 4가지 option * 오른쪽 3가지 option = 12가지 option
                        - 왼쪽 네 가지 option은 minimum idx - left_boundary = 4-0 = 4
                        - 오른쪽 세, le가지 option은 right_boundary - minimum_idx = 7 - 4 = 3
                    
                    → summation of miminums에 2가 기여하는 정도는 2 * 12 = 24
                    
            - 각 element가 최소 값으로 존재하는 range는 어떻게 얻는가?
                - nearest element on the left, less than itself(element) → idx: i
                - closest element on the right, less than itself(element) → idx : i
                
                → [i+1, j-1] indices가 우리가 찾는 range 
                
                - 예) array: [0,3,4,5,2,3,4,1,4]
                    - 2의 index는 4
                    - 왼쪽에서 2보다 작으면서 가장 가까운 원소: 0 → 0의 index는 0
                    - 오른쪽에서 2보다 작으면서 가장 가까운 원소: 1 → 1의 index는 7
                    
                    → 우리가 찾는 - 2가 최소 원소로 존재할 수 있는 - range는 [0+1, 7-1] → [1, 6]
                    
            - Monotonic increasing stack → i, j 값 정하기
                - 개요
                    - linear time complexity로 previous smaller element, next smaller element 찾는데 사용
                    - 대표적인 문제로는 [[**84. Largest Rectangle in Histogram**](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)](84%20Largest%20Rectangle%20in%20Histogram%20bab4a72971c243ef839cb80c246fe7a5.md)
                - monotonically increasing array
                    - two indices i, j에 대해 i >j, arr[i] ≥ arr[j]가 늘 참일때
                        - strictly increasing의 경우 arr[i] > arr[j]가 늘 참이지만, monotonically increasing의 경우 ≥ 등호가 하나 더 붙는다
                    - 만약 next, previous larger element를 원하면, monotonically decreasing stack을 사용할 수 있다
                - monotonically increasing stack building
                    - array element를 돌면서 stack에 push - 단 increasing property가 유지되어야만 함
                        - stack top에 있는 item이 iteration에서 current에 해당하는 item보다 크거나 같으면, top을 먼저 pop 하고 → current push
                            - 기존 top은 다시 push 하나? → 아니
                    - incoming element와 같거나 그보다 큰 값의 item들은 모두 pop된다 → incoming element는 stack에서 막 자리를 뜨는 item의 next smaller element
                        
                        → popped item마다 next smaller item을 알게 된다 (?)
                        
                    - stack이 비어있지 않으면, 새로운 stack top은 previous smaller item을 포함하게 될 것
                        - 새로운 item이 stack에 추가되면, 그와 같거나 그보다 큰 원소들은 이미 stack에서 제거되고 난 뒤
                        - 따라서 stack은 previous element가 previous smaller element라는 것을 보장한다 (?)
                    - stack이 모두 비게 되면, outgoing item(?)이 여지껏 본 중에 제일 작은 원소라는 것을 의미
                        - previous smaller item의 index는 -1이 되고, range 상으로는 -1 + 1 = 0이 start가 된다
                    - process가 완료되고 나면, stack은 increasing order로 연속된 item을 포함하게 된다
                        - 얘네는 자기 뒤로 더 작은 원소를 갖고 있지 않아서 stack에 남겨진 애들
                        - 얘네의 previous smaller은 stack 안에서 바로 뒤에 위치한 애들
            - 예시: arr = [8, 6, 3, 5, 4, 9, 2]
                - stack이 빈채로 시작
                - 8이 들어감
                - 6이 들어올 차례인데, 8이 더 커서 stack에서 Pop됨
                    
                    → 6은 8의 next smaller item 
                    
                - stack이 비어 있기 때문에 8의 입장에서 previous smaller은 존재하지 않음 → -1
                - 6을 stack에 추가
                - 3이 6보다 작기 때문에, 6을 stack에서 remove
                    - 3은 6의 next smaller
                - stack이 비었기 때문에 6은 previous smaller 없음
                - 3을 stack에 넣는다
                - 5는 3보다 크기 때문에 그 위에 쌓는다
                - 4는 5보다 작기 때문에 5를 stack에서 제거한다
                    - 5의 next smaller item은 4
                    - 5의 previous smaller item은 3
                - 4는 3보다 크기 때문에 stack에 push
                - 9는 4보다 크기 때문에 stack에 push
                - 2는 9보다 작기 때문에 9를 stack에서 pop
                    - 9의 next smaller item은 2
                    - 9의 previous smaller item은 4
                - 2는 4보다 작기 때문에 4를 stack에서 pop
                    - 4의 next smaller item은 2
                    - 4의 previous smaller item은 3
                - 2는 3보다 작기 때문에 3을 stack에서 pop
                    - 3의 next smaller item은 2
                    - 3까지 빠지고 나면 stack이 비어 있기 때문에, 3의 previous smaller item은 없음. -1
                - 빈 stack에 2 추가
                - 모든 iteration이 끝나면, stack에 남아 있는 모든 원소가 pop된다
                - stack이 비어 있기 때문에 2는 previous smaller이 없다 - 물론 next smaller item도 없다
            - **Edge Case - Duplicate Elements**
                - 하나의 element의 contribution을 두번 세어서는 안된다
                    - 예) [2, 2, 2]
                        - range를 찾기 위해 boundary를 찾을 때, current element 기준으로 그보다 왼쪽에서 strictly less인 element를 찾는다 (previous smaller element)
                        - 오른쪽 boundary를 찾을 때는, current element보다 작거나 ‘같은’ next 원소를 찾는다 (next smaller element)
                    - 예) [3, 1, 5, 2, 6, 2, 8, 2, 1]
                        - 2는 3, 5, 7 index 자리에 세 번 등장
                        - 두번째 2(idx = 5)에 대한 range를 계산할 때,
                            - index 7에 위치한 세번째 2를 next smaller element로 삼는다
                            - previous smaller element는 2보다 반드시 작아야 하므로 index 1에 위치한 1
                        - 세번째 2(idx=7)에 대한 range 계산
                            - next smaller item은 idx=8에 위치한 1
                            - previous smaller item은 strictly 2보다 작아야 하므로 idx=1에 위치한 1
                            - 
                            
        - 알고리듬
            - 주의: stack에 저장되는 것은 element 값 자체가 아니라 indices
            1. 필요한 자료구조, 변수 선언
                - stack: monotonically increasing stack
                - ans: minimum들의 합
            2. stack processing
                - range(0, n)에 속한 idx 돌면서
                    1. stack이 비어 있지 않으면 아래의 조건을 만족할 때까지 pop
                        1. stack top ≤ arr[i]
                            - stack top > arr[i] 이면 무조건 pop. 이 때 pop된 구 top의 next smaller은 arr[i]이 된다.
                        2. i가 n에 도달 (?)
                        - 중복 element가 있는 경우 next smaller item에 대해서는 equal element를 함께 고려하지만 vs. previous smaller item에 대해서는 strictly smaller item만 고려
                        - pop된 각 요소-mid-에 대해, 그 요소가 최소 값으로 존재할 수 이있는 범위를 구할 수 있다
                            - mid를 pop하게 만든 요소가 next smaller item이고 (j: right boundary)
                            - mid를 pop 하고도 stack에 원소(top)가 남아 있으면 그 원소가 mid의 previous smaller item (i: left boundary)
                            - stack에 원소가 남아 있지 않으면 mid의 previous smaller item은 -1 (i)
                            - [i+1, j-1]이 mid가 최소값으로 존재할 수 있는 범위긴 하지만, 기여도 계산 시에는 boundary를 사용한다
                            
                            ⇒ mid의 ans에 대한 기여도는 arr[mid] * (j-mid) * (mid-i)
                            
                        - i == n이면 모든 원소를 stack에 한번씩 push 했다는 뜻. 이 때 쯤이면 일부 원소는 pop되기도 했을 것. 마지막까지도 stack에 남은 원소들은 더 이상 next smaller item을 갖지 못함을 의미
                            - 이들에 대한 next smaller index는 n(len(arr))
                        - ans에 특정 mid로부터의 contribution을 더한다
                    2. 현재 원소보다 큰 원소들은 모두 제거되었기 때문에 현재 원소의 index를 stack에 잘 넣는다 
            3. running total ans에 modular 연산 적용해서 최종 return 한다
            - 예시 : arr = [3, 4, 4, 5, 4, 1]
                - stack이 비어 있기 때문에 3의 index인 0 추가
                - 4는 3보다 크기 때문에 4의 index인 1을 0 위에 쌓는다
                - 두번째 4의 경우 4 = stack top(4)이기 때문에 top을 제거한다
                - 제거된 top - 첫번째 4, idx=1-의 contribution을 계산한다
                    - arr[mid] = 4
                    - previousSmallerIdx = stack에 남아 있는 0
                    - nextSmallerIdx = 첫번째 4를 pop하게 만든 두번째 4, idx = 2
                    
                    ⇒ contribution = 4 * (1-0) * (2-1) = 4 
                    
                
    - **Approach 2: Monotonic Stack + Dynamic Programming**
        - Intuition
            - approach1: 모든 요소를 돌면서 그에 대한 range를 구했음 → approach2: 이전 계산 결과 활용
            - overlapping subproblem 어떻게 찾지? → 더 작은 subarray들을 이용해서 더 큰 subarray들에 대한 solution을 찾을 수 있는가?
            - `dp` array
                - given array arr과 같은 길이
                - state definition
                    - dp[i]: index i에서 끝나는 모든 subarray들의 minimum sum
                - state transition
                    - i>j 일 때 dp[i]와 dp[j]의 관계
                        - i에서 끝나는 subarray 개수가 j에서 끝나는 subarray 개수보다 많음 (i > j)
                        - dp[j]의 결과를 가지고 dp[i]를 찾자
                    - 예) arr = [8, 6, 3, 5, 4, 9, 2]
                        - element 3(idx=2)에서 끝나는 모든 subarray를 고려
                            - [8, 6, 3], [6, 3], [3]
                            - 이 세 subarray들의 minimum들은 모두 3
                            
                            → dp[2] = 3 + 3 + 3 = 9 
                            
                        - element 5 (idx=3)에서 끝나는 모든 subarray를 고려
                            - [8, 6, 3, 5], [6, 3, 5], [3, 5] (idx=2에서의 subarray들에 5를 붙인 결과), [5]
                            - current element 5 > 3 → 이전 subarray들에 5를 붙여도 minimum 값은 3으로 유지
                            - [5]에서만 minimum 값이 5가 됨
                            
                            → dp[3] = dp[2] + 5 = 9 + 5 = 14
                            
                        - element 4(idx=4)에서 끝나는 모든 subarray 고려
                            - [8, 6, 3, 5, 4], [6, 3, 5, 4], [3, 5, 4], [5, 4] (idx =3 에서의 subarray들에 4를 붙인 결과), [4]
                            - current element 4 > previous element 5 → [5, 4], [4]의 minimum은 4
                            - 나머지 3개의 subarray minimum은 3 (index=2)
                            
                            → dp[4] = arr[4] * 2 + dp[2] = 4 * 2 + 9 = 17
                            
                        - pattern emerging from this
                            - arr에서 아무 element i를 선택 (i = 4)
                                - i에서 왼쪽으로 진행할 때마다 arr[i]보다 작거나 같은 첫번째(i와 가장 가까운) index를 찾음
                                    - i = 4 → 0으로 가면서 arr[i]보다 작거나 같은 첫번째 index j : 2 (element 3)
                                - arr[i]를 minimum으로 하는 i-j 개의 subarray를 찾음
                                    - i-j = 4-2 = 2개의 array에 대해서는 arr[j]가 아니라 arr[i]가 minimum
                                        - arr[j] < arr[i]이지만, arr[j+1:i+1] 범위에 대해서는 arr[j]가 포함되지 않고, 그보다 같거나 바로 큰 arr[i]가 minimum
                                        - 해당 범위의 subarray 개수
                                            - arr[j+1:i+1], arr[j+2:i+1], …, arr[i:i+1]
                                            - start index로 따지면 j+1, j+2, …, j+(i-j) → j를 빼면 1, 2, …, (i-j) → 총 (i-j)개
                                        
                                        → (i-j) * arr[i] 
                                        
                                - 나머지에 대해서는 dp[j]가 값을 갖고 있음
                                    - dp[j] = dp[2]
                    - 재귀식
                        - dp[i] = dp[j] + (i-j) * arr[i]
                            - arr[i+1] > arr[i]  일 때 dp[i+1] = dp[i] + arr[i+1]
                            - i+1 > i 이면 j = i-1일 때와 같음 → dp[i] = dp[i-1] + 1 * arr[i] = dp[i-1] + arr[i]
                - base case
                    - i = 0이라서 j가 나올 수 없으면 j = -1, dp[j] = 0으로
                        - dp[0] = dp[j] + (0-(-1)) * arr[0] = 0 + arr[0] = arr[0]
            - 여기서도 i 기준 0에서 i-1에서 j를 찾아야 하기 때문에 finding previous smaller items in linear time이 관건 → monotonic stack 사용해서 매 i에 대해 j를 찾는다
                - 동시에 dp array도 population
            - 최종 답은 summation of all the elements in the dp array
                - dp[i]: index i에서 끝나는 모든 subarray들의 minimum sum
                - 모든 end index에 대해 sum of mininum을 구해야 하기 때문에
- AC 코드
    - monotonous stack + contribution
        
        ```python
        class Solution:
            def sumSubarrayMins(self, arr: List[int]) -> int:
                mod = 10 ** 9 + 7
                stack = []
                n = len(arr)
                ans = 0
        
                for i in range(n):
                    while stack and arr[stack[-1]] >= arr[i]:
                        mid = stack.pop()
                        left_boundary = stack[-1] if stack else -1 
                        right_boundary = i 
                        contribution = arr[mid] * (mid-left_boundary) * (right_boundary-mid)
                        ans = (ans + contribution) % mod 
                    stack.append(i)
        
                while stack:
                    mid = stack.pop()
                    left_boundary = stack[-1] if stack else -1 
                    right_boundary = n
                    contribution = arr[mid] * (mid-left_boundary) * (right_boundary-mid)
                    ans = (ans + contribution) % mod 
        
                return ans
        ```
        
    - monotonous stack + dp (⚡️)
        
        ```python
        class Solution:
            def sumSubarrayMins(self, arr: List[int]) -> int:
                mod = 10 ** 9 + 7
                n = len(arr)
                # array 
                dp = [0] * n 
                # base case: j = -1, dp[j]= -1 
                # monotonous stack saving indices!! 
                stack = []
        
                
                for i in range(n):
                    # previous smaller element
                    while stack and arr[stack[-1]] > arr[i]:
                        stack.pop() # stackTop > arr[i]
                    j = stack[-1] if stack else -1 
                    # dp[-1] = dp[n-1] = 0 (not filled yet)
                    dp[i] = (dp[i] + (dp[j] + (i-j) * arr[i])) % mod
                    stack.append(i)
                
                return sum(dp) % mod
        ```