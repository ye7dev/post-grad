# 1425. Constrained Subsequence Sum

Status: done, in progress, 🏋️‍♀️
Theme: DP
Created time: February 15, 2024 5:17 PM
Last edited time: February 19, 2024 10:26 AM

- 문제 이해
    - input: integer array `nums`, integer `k`
        - nums의 원소는 음수가 나올 수 있음
    - non-empty subsequence 의 max sum을 구해라
        - subsequence에서 i<j인 두 consecutive integer nums[i], nums[j]에 대해
            - i,j는 subsequence에서의 index가 아니라 원래 array인 `nums` 에서의 index
            - 왜냐면 consecutive 원소들이라 subsequence에서의 index는 차이가 1뿐이다
        - index 차 즉 j-i ≤ k를 만족해야 한다
            - j ≤ i + k
    - subsequence
        - 원래 array에서 순서는 유지하면서, 일부 원소를 제거한 array
    - 예)
        
        ```
        Input: nums = [10,2,-10,5,20], k = 2
        Output: 37
        Explanation: The subsequence is [10, 2, 5, 20].
        ```
        
        - subsequence를 원래 index로 표기하면
            - 0, 1, 3, 4
            - 제일 큰 차인 1,3=2 ≤ k
        
        ```
        Input: nums = [-1,-2,-3], k = 1
        Output: -1
        Explanation: The subsequence must be non-empty, so we choose the largest number.
        ```
        
        - nums가 모두 음수라서, empty subsequence의 합이 제일 크지만, 문제에서 non-empty로 제한
        - edge case로 빼야겠다 → max element < 0 이면 max element return
        
        ```
        Input: nums = [10,-2,-10,-5,20], k = 2
        Output: 23
        Explanation: The subsequence is [10, -2, -5, 20].
        ```
        
        - 양수 음수 섞여 있는 경우
        - subsequence를 index로 재표기 하면
            - 0, 1, 3, 4
            - -5의 경우 건너뛰는게 전체 합에 이롭지만 k index 조건 만족하느라…
                - 10 다음에 -2,-10 둘 중 하나 선택
                - -2에서 -10, -5 둘 중 하나 선택
- AC 코드
    - heap + kadane 변수 하나 사용 버전
        
        ```python
        import heapq
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                n = len(nums)
        				
        				# edge case
                if max(nums) < 0:
                    return max(nums)
                if min(nums) >= 0:
                    return sum(nums)
                
                max_heap = []
                heapq.heappush(max_heap, (-nums[0], 0))
                ans = nums[0]
                for i in range(1, n):
        						'''
        						heap에 있는 원소들은 모두 i보다 index가 작음
        						근데 i와 k 넘게 차이나는 원소들은 빼야
        						- i는 앞으로 계속 커지는데, idx 차는 계속 커짐
        						'''
                    while (i-max_heap[0][1]) > k:
                        heapq.heappop(max_heap)
        						# max heap에 부호 반대로 넣은 것 제자리로 
                    heap_top = max(max_heap[0][0] * (-1), 0)
        						# heap_top이 누적 합이 되는 셈 
                    curr = heap_top + nums[i]
                    ans = max(ans, curr)
        						# 주의!! heap에 들어가는 값은 nums[i]가 아니라 누적 값!! 
                    heapq.heappush(max_heap, (-curr, i))
                return ans
        ```
        
    - heap + dp array 사용 버전
        
        ```python
        import heapq
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                # edge case
                if max(nums) < 0:
                    return max(nums)
                if min(nums) >= 0:
                    return sum(nums)
        
                # dp[i]: max sum of subsequence ending at nums[i] 
                n = len(nums)
                dp = [0] * n
                # base case
                dp[0] = nums[0]
        
                max_heap = [(-nums[0], 0)]
                
                for i in range(1, n):
                    # pop-every time we meet idx out of current window
                    while i - max_heap[0][1] > k:
                        heapq.heappop(max_heap)
                    # max cumsum within the window
                    dp[i] = max(max_heap[0][0]*(-1), 0) + nums[i] # no if condition -> max! 
                    '''
                    dp[i] either
                    a. nums[i]
                    b. cumsum + nums[i]
                    '''
                    heapq.heappush(max_heap, (-dp[i], i))
                
                return max(dp)
        ```
        
    - queue + dp
        
        ```python
        from collections import deque
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                # edge case
                if min(nums) >= 0:
                    return sum(nums)
                if max(nums) < 0:
                    return max(nums)
                
                n = len(nums)
                dp = [0] * n
                queue = deque()
        
                for i in range(n):
                    while queue and i - queue[0][1] > k:
                        queue.popleft()
                    dp[i] = nums[i] + (queue[0][0] if queue else 0)
                    if dp[i] > 0:
                        while queue and queue[-1][0] < dp[i]:
                            queue.pop()
                        queue.append((dp[i], i))
                return max(dp)
        ```
        
    - queue + dp : queue에 idx만 저장 버전
        
        ```python
        from collections import deque
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                # edge case
                if max(nums) < 0:
                    return max(nums)
                if min(nums) >= 0:
                    return sum(nums)
                
                n = len(nums)
                dp = [0] * n
                queue = deque()
        
                for i in range(n):
                    # clear range
                    while queue and queue[0] < i-k:
                        queue.popleft()
                    # get cur_sum
                    if queue and dp[queue[0]] > 0:
                        dp[i] = dp[queue[0]] + nums[i]
                    else:
                        dp[i] = nums[i]
                    # check cur_sum
                    if dp[i] > 0:
                        while queue and dp[queue[-1]] < dp[i]:
                            queue.pop()
                        queue.append(i)
                
                return max(dp)
        ```
        
    - queue + dp + idx만 저장 + editorial
        
        ```python
        from collections import deque
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                # edge case
                if max(nums) < 0:
                    return max(nums)
                if min(nums) >= 0:
                    return sum(nums)
                
                n = len(nums)
                dp = [0] * n
                queue = deque()
        
                for i in range(n):
                    # clear range
                    if queue and queue[0] < i-k:
                        queue.popleft()
                    # get cur_sum
                    dp[i] = (dp[queue[0]] if queue else 0) + nums[i]
                    # drop smaller values
                    while queue and dp[queue[-1]] < dp[i]:
                        queue.pop()
                    # check cur_sum
                    if dp[i] > 0:
                        queue.append(i)
                
                return max(dp)
        ```
        
- Trial
    - Bottom-up → 20/40 TLE
        - 순수 DP로만 구현해서 TLE 난 듯
        
        ```python
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                n = len(nums)
        
                # edge case
                if max(nums) < 0:
                    return max(nums)
                
                dp = [0] * (n+1)
        
                # dp[i]: considering nums[i:] or start at nums[i]?
                ## return dp[0] -> fits the first definition
                dp[n-1] = nums[n-1] if nums[n-1] >= 0 else 0 
        
                # this relation always consider put curr into the subsequence
                for i in range(n-2, -1, -1):
                    curr = nums[i]
                    for j in range(i+1, min(i+k+1, n)):
                        dp[i] = max(dp[i], curr + dp[j])
                
                return max(dp)
        ```
        
    - heap + kadane → 예제 1/3
        
        ```python
        import heapq
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                n = len(nums)
        
                # edge cases
                if max(nums) < 0:
                    return max(nums)
                if min(nums) >= 0:
                    return sum(nums)
                
                max_heap = []
                heapq.heappush(max_heap, (-nums[0], 0))
                ans = nums[0]
                for i in range(1, n):
                    while (i-max_heap[0][1]) > k:
                        heapq.heappop(max_heap)
                    heap_top = heapq.heappop(max_heap)[0] * (-1)
                    if heap_top < 0:
                        heap_top = 0
                    curr = heap_top + nums[i]
                    ans = max(ans, curr)
                    heapq.heappush(max_heap, (-nums[i], i))
                return ans
        ```
        
    - queue + dp → 예제 1/3
        
        ```python
        from collections import deque 
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                # edge case
                if max(nums) < 0:
                    return max(nums)
                if min(nums) >= 0:
                    return sum(nums)
                
                n = len(nums)
                dp = [0] * n
                dp[0] = nums[0]
                queue = deque([(nums[0], 0)])
        
                for i in range(1, n):
                    if dp[i] < 0:
                        continue
                    while queue and i-queue[0][1] > k:
                        queue.popleft()
                    dp[i] = queue[0][0] + nums[i]
                    while queue and dp[i] < queue[-1][0]:
                        queue.pop()
                    queue.append((dp[i], i))
                
                return max(dp)
        ```
        
    - queue + dp → 28/40
        
        ```python
        from collections import deque 
        class Solution:
            def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
                # edge case
                if max(nums) < 0:
                    return max(nums)
                if min(nums) >= 0:
                    return sum(nums)
                
                n = len(nums)
                dp = [0] * n
                dp[0] = nums[0]
                queue = deque([(nums[0], 0)])
        
                for i in range(1, n):
                    while queue and i-queue[0][1] > k:
                        queue.popleft()
                    if queue:
                        dp[i] = queue[0][0] + nums[i]
                    else:
                        dp[i] = nums[i]
                    while queue and dp[i] > queue[-1][0]:
                        queue.pop()
                    if dp[i] > 0:
                        queue.append((dp[i], i))
                
                return max(dp)
        ```
        
- Editorial
    - **Approach 1: Heap/Priority Queue**
        - Intuition
            - 순수 DP까지의 접근
                - 양수로 구성된 array의 경우, 늘 array 전체를 take 해야 → edge case 추가함
                - 음수 원소는 양수 원소들로 이동하기 위한 bridge로 생각
                    - 그림
                        
                        ![Untitled](Untitled%209.png)
                        
                - 언제 해당 음수 원소를 취하는 것이 worth it 한지 알 수 있는가?
                    - 음수를 취함으로 얻는 순이익(net gain)이 양수이면 이 원소를 취하는 것을 고려해야 함
                        - 예) 그림에서 -5를 얻음으로써 첫번째 원소인 16을 취할 수 있기 때문에 net gain은 11
                - 왼쪽에서 오른쪽으로 iteration
                    - each idx i에서 nums[i]를 마지막 원소로 포함하는 subsequence의 maximum possible sum `curr` 을 고려
                    - 주어진 i에 대해 `curr` 구하는 법
                        - last k indices의 원소를 마지막 원소로 갖는 subsequence의 maximum possible sum을 구한다
                            - i-k, i-1 사이의 index j를 돌면서 max dp[j]를 구한다
                        - 여기에 nums[i]를 더한다
                            - dp[i] = nums[i] + max dp[j]
                - 순수 DP로 접근하면 너무 느리다
                    - 각 state dp[i]에 대해 최대 k번의 iteration을 해야 해서
                    
                    → i-k ~ i-1 사이 index j에 대해 max dp[j]를 구할 더 빠른 방법이 필요 
                    
            - max sum → max heap 사용
                - last k indices인 모든 j에 대해 max heap이 dp[j]의 값을 저장
                    
                    → max heap의 top만 확인하면 curr을 구할 수 있음 
                    
                - 주의: 현재 index i로부터 k보다 더 크게 떨어져 있는 원소는 들어가면 안됨
                    - curr을 구하기 전에, i-k~i-1 범위를 벗어나게 되면 heap의 top에서 pop(?)
                    - 이를 확인하기 위해서는 max heap의 entry가 인덱스 관련 정보도 담고 있어야 함
                - heap의 top이 negative인 경우, 취하지 않는 것이 좋다
                    - Kadane’s algorithm과 비슷 ∝ maximum subarray problem
                    - top이 negative인 경우, 이 subsequence의 sum이 0보다 작아질 수 있음을 의미.
                    - current index 보다 왼쪽의 모든 원소가 버려져야 한다 → any bridge would not be worth taking
                    - 그래서 이 부분에서 어떤 index를 subsequence에 포함해서 음수 합을 만드는 대신, 아예 subsequence에 시작도 못하게 한다
        - Algorithm
            1. max heap을 초기화 (nums[0], 0), ans = nums[0]
            2. i를 1부터 n-1까지 돌면서 
                - while i - heapTop_idx > k → heappop
                - curr = heapTop + nums[i]
                    - heapTop < 0 인 경우 0으로 처리
                - ans = max(ans, curr)
                - heappush (curr, i)
            3. return ans 
    - **Approach 3: Monotonic Deque**
        
        239번 문제와 밀접하게 관련
        
        - Intuition
            - last k indices에 대해 dp에서 maximum value를 O(1)으로 최대값을 찾는 방법
                - monotonic data structure
                    - elements가 이미 정렬된 상태
                - last k indices에 대해 dp 값들을 monotonic 자료 구조로 유지할 수 있으면 해당 자료 구조의 첫번째 element가 우리가 찾는 값
                - dp[i]를 넣기 전에 마지막 요소를 체크
                    - 이번에 들어가는 dp[i]가 자료 구조에서 가장 작은 값이어야 함
                        - dp[i] 보다 앞에 오는 값들이 dp[i]보다 작으면, i보다 뒤에 있는 원소들에 대해 이 값들이 maximum value in the last k indices에 들 수가 없음
                    - 마지막 요소가 dp[i]보다 작으면 pop
                        - 자료 구조 뒤에서 제거
                    - 그렇지 않으면 monotonic property가 무너짐
                    - for loop으로 자료 구조를 clean 하게 만드는 과정이 필요
                - dp[i]가 양의 값일 때만 queue에 추가
                - max value를 체크하지 전에, 그게 out of range가 아닌지 확인해야 함
                    - dp[i]가 자료 구조에서 가장 작은 값으로 들어가기 때문에, 이미 자료 구조에 있는 값들은 dp[i]보다 큰 값 → max value를 호출했을 때 i로부터 한참 더 먼, i-k보다 더 작은 index의 값이 있을 수 있음 → invalid → 이런 값은 제거해야 함
                    - 이런 값들은 dp[i]보다 훨씬 오래전에 들어갔을 것이므로 앞에서 제거해야 함
                - 앞과 뒤 양쪽으로 원소를 제거해야 함 → deque 사용
                    - 앞에서 제거: out of range
                        - max value가 out of range인지 확인하려면(?)
                            - i - queue.front() > k 확인
                        - 가장 큰 값을 얻으려면 dp[queue.front()]
                    - 뒤에서 제거: dp[i]보다 작은 값들
                        - dp[queue.back()]
        - Algorithm
            1. deque, dp(길이: len(nums)) 초기화
            2. i에 대해 nums의 indices 를 돌면서
                1. queue의 앞에서 i 기준 k보다 더 오래 전에 들어간 원소들 제거 
                2. dp[i] 계산
                    - dp[i] = dp[queue.front()] + nums[i]
                    - queue가 비어 있으면 가져올 front가 없으므로 0
                3. dp[queue.back()]이 dp[i]보다 작은 한, queue에서 마지막 요소를 pop 한다 
                4. 만약 dp[i] > 0 이면 queue에 i를 추가한다 
            3. dp에서 max element를 return 
- 구현 시 주의 사항
    - 양수 음수 같이 있는 경우의 max heap
        - min heap에다가 원소 부호만 반대로 해서 넣는다
        - 음수 원소의 경우 양수로 들어가기 때문에 min heap 기준으로는 뒤에 가게 될 것
        - 양수 원소의 경우 음수로 들어가기 때문에 min heap 기준으로 앞에 가게 될 것
    - 그냥 List에 원소 넣은 다음에 heappop 할 수 있나? → 된다
        
        ```python
        >>> x = [3]
        >>> heapq.heappop(x)
        3
        ```