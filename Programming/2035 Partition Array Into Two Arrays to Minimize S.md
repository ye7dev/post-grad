# 2035. Partition Array Into Two Arrays to Minimize Sum Difference

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP
Created time: February 2, 2024 9:57 AM
Last edited time: February 2, 2024 5:23 PM

- Process
    - 2진법 써서 들고 다녀야 할 것 같음
        - (1 << 5) - 1 : n자리 1  11111
        - (1 << 4) = 10000
    - mask에서 구하는 연산을 base case에 가져다 둬도 될까? 뭔가 재귀적 접근법에 안 맞는 기분인데
        
        ```python
        for i in range(n-1, -1, -1):
          if (1 << i) & mask: 
              sub_a += nums[i]
          else:
              sub_b += nums[i]
        ```
        
    - total에서 n//2개를 고르는 상황이라고 생각하자
    - [ ]  subset sum  대신 마스크를 들고 다니는 게 나을 듯
- AC 코드
    - Meet in middle
        
        ```python
        class Solution:
            def minimumDifference(self, nums: List[int]) -> int:
                # util func1
                def get_subset_sum(arr, size):
                    sums = set()
                    def recur(i, remain, cur_sum):
                        # base case
                        if remain == 0:
                            sums.add(cur_sum)
                            return 
                        if i == n:
                            return 
                        # recurrence
                        recur(i+1, remain, cur_sum)
                        recur(i+1, remain-1, cur_sum + arr[i])
        
                    recur(0, size, 0)              
                    
                    return list(sums)
        
                n = len(nums) // 2 
                total_sum = sum(nums)
                half_sum = total_sum // 2 # not necessarily integer
        
                # arbitrary split
                left = nums[:n]
                right = nums[n:]
        
                # get all possible subset sum
                left_subset_sums, right_subset_sums = {0:[0]}, {0:[0]}
                for size in range(n+1):
                    left_subset_sums[size] = get_subset_sum(left, size)
                    right_subset_sums[size] = get_subset_sum(right, size)
                    right_subset_sums[size].sort()
                
                # iterate over a and binary search b 
                min_diff = float('inf')
                for size in range(n+1): # zero necessaire?
                    left_size, right_size = size, n-size
                    for sum_left in left_subset_sums[left_size]:
                        target = half_sum - sum_left
                        cand_idx = bisect_left(right_subset_sums[right_size], target)
                        # get closest b 
                        if cand_idx == len(right_subset_sums[right_size]):
                            cand_idx -= 1
                        elif 0 < cand_idx < len(right_subset_sums[right_size]):
                            cand1 = abs(target - right_subset_sums[right_size][cand_idx])
                            cand2 = abs(target - right_subset_sums[right_size][cand_idx-1])
                            if cand2 < cand1:
                                cand_idx -= 1 
                        # get ans for current left, right
                        sum_right = right_subset_sums[right_size][cand_idx]
                        temp_ans = abs(total_sum - 2 * (sum_left + sum_right))
                        min_diff = min(min_diff, temp_ans)
                return min_diff
        ```
        
    - clean-up final version (⚡️)
        
        ```python
        from itertools import combinations
        from bisect import bisect_left 
        
        class Solution:
            def minimumDifference(self, nums: List[int]) -> int:
                # util func1
                def get_subset_sum(arr, size):
                    subsets = combinations(arr, size)
                    subset_sums = list(set([sum(subset) for subset in subsets]))
                    subset_sums.sort()
                    return subset_sums 
                
                # util func2
                def get_closest(arr, target):
                    cand_idx = bisect_left(arr, target)
                    if cand_idx == len(arr):
                        return cand_idx - 1 
                    if cand_idx == 0:
                        return cand_idx
                    cand1 = abs(target - arr[cand_idx])
                    cand2 = abs(target - arr[cand_idx-1])
                    return cand_idx -1 if cand2 < cand1 else cand_idx
                    
                n = len(nums) // 2 
                total_sum = sum(nums)
                half_sum = total_sum // 2 # not necessarily integer
        
                # arbitrary split
                left = nums[:n]
                right = nums[n:]
        
                # get all possible subset sum
                left_subset_sums, right_subset_sums = {0:[0]}, {0:[0]}
                for size in range(n+1):
                    left_subset_sums[size] = get_subset_sum(left, size)
                    right_subset_sums[size] = get_subset_sum(right, size)
                
                # iterate over a and binary search b 
                min_diff = float('inf')
                for size in range(n+1): # zero necessaire
                    left_size, right_size = size, n-size
                    for sum_left in left_subset_sums[left_size]:
                        # get closest b 
                        target = half_sum - sum_left
                        cand_idx = get_closest(right_subset_sums[right_size], target)
                        # get ans for current left, right
                        sum_right = right_subset_sums[right_size][cand_idx]
                        temp_ans = abs(total_sum - 2 * (sum_left + sum_right))
                        min_diff = min(min_diff, temp_ans)
                return min_diff
        ```
        
- Trial
    - brute force → 예제 1/3
        - [-36, 36] 같은 경우 커버 안됨
        
        ```python
        nums.sort()
        n = len(nums)
        a, b = 0, 0
        for i in range(n//2):
            if i & 1:
                b += (nums[i] + nums[n-i-1])
            else:
                a += (nums[i] + nums[n-i-1])
        return abs(a-b)
        ```
        
    - top-down like… → 예제 2/3
        
        ```python
        class Solution:
            def minimumDifference(self, nums: List[int]) -> int:
                n = len(nums)
                memo = {}
                starting_mask = (1 << n) - 1 
                # function
                def recur(i, mask):
                    # check memo
                    if (i, mask) in memo:
                        return memo[(i, mask)]
        
                    # base case?
                    if i == n:
                        sub_a, sub_b = 0, 0
                        for i in range(n-1, -1, -1):
                            if (1 << i) & mask: 
                                sub_a += nums[i]
                            else:
                                sub_b += nums[i]
                        return abs(sub_a - sub_b)
                    
                    # recurrence relation
                    take_curr = recur(i+1, mask^(1<<i))
                    skip_curr = recur(i+1, mask)
                    
                    memo[(i, mask)] = min(take_curr, skip_curr)
                    return memo[(i, mask)]
        
                return recur(0, starting_mask)
        ```
        
    - top-down like → 예제 2/3
        - 원소를 공평하게 하나씩 보내는 걸 어떻게 해야 하는지 모르겠음
        
        ```python
        class Solution:
            def minimumDifference(self, nums: List[int]) -> int:
                n = len(nums)
                memo = {}
                # function
                def recur(i, sum_a, sum_b):
                    # check memo
                    state = (i, sum_a, sum_b) 
                    if state in memo:
                        return memo[state]
        
                    # base case?
                    if i == n:
                        return abs(sum_a - sum_b)
                    # recurrence relation
                    take_curr = recur(i+1, sum_a + nums[i], sum_b)
                    skip_curr = recur(i+1, sum_a, sum_b + nums[i])
                    
                    memo[state] = min(take_curr, skip_curr)
                    return memo[state]
        
                return recur(0, 0, 0)
        ```
        
    - top-down → 134/201 (memory error)
        - 접근법은 맞는데 parameter를 줄여야 할 듯
        
        ```python
        class Solution:
            def minimumDifference(self, nums: List[int]) -> int:
                n = len(nums)
                memo = {}
                total_sum = sum(nums)
                # function
                def recur(i, remain, sub_sum):
                    # check memo
                    state = (i, remain, sub_sum)
                    if state in memo:
                        return memo[state]
        
                    # base case
                    if remain == 0:
                        other_sub = total_sum - sub_sum
                        return abs(other_sub - sub_sum)
                    if i == n:
                        return float('inf')
                        
        
                    # recurrence 
                    take_curr = recur(i+1, remain-1, sub_sum + nums[i])
                    skip_curr = recur(i+1, remain, sub_sum)
        
                    memo[state] = min(take_curr, skip_curr)
                    return memo[state]
        
                
                return recur(0, n//2, 0)
        ```
        
    - top-down 2 params → 예제 2/4
        
        ```python
        class Solution:
            def minimumDifference(self, nums: List[int]) -> int:
                n = len(nums)
                memo = {}
                total_sum = sum(nums)
                # function
                def recur(i, remain):
                    # check memo
                    state = (i, remain)
                    if state in memo:
                        return memo[state]
        
                    # base case
                    if remain == 0:
                        return 0
                    if i == n:
                        return float('inf')
                        
        
                    # recurrence 
                    take_sum = nums[i] + recur(i+1, remain-1)
                    take_curr = abs((total_sum - take_sum) - take_sum)
        
                    skip_sum = recur(i+1, remain)
                    skip_curr = abs((total_sum - skip_sum) - skip_sum)
        
                    memo[state] = min(take_curr, skip_curr)
                    return memo[state]
        
                
                return recur(0, n//2)
        ```
        
    - top-down : bit mask → 134/201 (memory error)
        
        ```python
        class Solution:
            def minimumDifference(self, nums: List[int]) -> int:
                n = len(nums)
                starting_mask = (1 << n) - 1 
                total_sum = sum(nums)
                memo = {}
                # function
                def recur(i, remain, mask):
                    # check memo
                    state = (i, remain, mask)
                    if state in memo:
                        return memo[state]
                    
                    # base case
                    if remain == 0:
                        sub_sum = 0
                        for i in range(n):
                            if mask & (1 << i):
                                sub_sum += nums[i]
                        return abs((total_sum - sub_sum) - sub_sum)
                    if i == n:
                        return float('inf')
                    
                    # recurrence relation
                    skip_curr = recur(i+1, remain, mask)
                    new_mask = mask ^ (1 << i) # both 1 -> return 0
                    take_curr = recur(i+1, remain-1, new_mask)
                    memo[state] = min(skip_curr, take_curr)
                    return memo[state]
                return recur(0, n//2, starting_mask)
        ```
        
    - meet in middle → 147 / 201 (TLE)
- Editorial
    - unofficial top-down
        - input array가 양수로 구성된 경우만 가능 (?)
            1. total_sum을 구해서 0부터 이 값까지의 array 생성
            2. array를 반으로 나눠서(input array인지 total_sum range array인지) first half의 값? 아님 abs 값?을 최소화한다
                - minimize(abs(sum_a - sum_b))
                    - total_sum = sum_a + sum_b
                    - sum_b = total_sum - sum_A
                    
                    ⇒ minimize(abs(sum_a - total_sum + sum_a))
                    
                    = `minimize(abs(total_sum - 2 * sum_a))` 
                    
                - 따라서 first half인
            - 왜 양수에서만 가능한가?
                - total_sum → 1의 range가 음수가 될 수 있음
                - negative range나 0에서 2D matrix 만들 수 없음
        - Meet in the middle approach
            1. input array를 두 부분으로 나눈다 
                - 길이가 2 * n이라고 명시되어 있으니, 각 array 길이는 n일 것
            2. 두 array 에서의 모든 subset sum을 찾는다
                - left, right array 각각의 subset sum을 계산할 때, 그 sum에 사용된 element 개수도 고려해야 한다
            3. 주어진 값들에 대한 sum을 2D matrix나 hash map에 저장 
                - 예) input array: [3,9,7,3]
                    - array를 반으로 나눈다 →  left = [3,9] , right = [7,3]
                    - sum for left [0: 0, 1: 3, 9, 2: 12]
                        - key: 사용된 숫자 개수 (subset size), value: subset sum
                    - sum for right [0: 0, 1: 3, 7, 2: 10]
            4. left part에서 subset을 하나 꺼내고, right part에서 subset을 또 하나 꺼낸다 - 이 때 두 subset의 크기의 합이 n//2 이어야 함 
                - left subset sum이 a, right subset sum이 b라고 할 때
                - left, right part에서 꺼낸 각 subset을 합치면 총 n//2의 크기가 되고, 합은 a+b
                - 남은 절반의 원소들을 합친 값은 total_sum - (a+b)
            5. 두 subset sum abs diff를 최소화한다 
                - 우리가 구해야 하는 답은 abs((total_sum - (a+b)) - (a+b))
                    
                    = abs(total_sum - 2 * (a+b))
                    
                - a를 iterate 하면서 right part?에 대해 binary search를 수행한다
                    - a+b 값이 total_sum의 절반에 가깝게 되어야 함
                    - 차가 제일 작은 경우는 total_sum = 2 * (a+b) → (a+b) = total_sum // 2
                    - 우선 right part의 모든 subset sum이 정렬된 상태어야 함
                        - 같은 원소 개수에 대해 subset sum 값이 하나면 상관 없겠지만, 1: [3, 7] 처럼 있는 경우, 둘 중에 뭐를 사용해야 하는가
                - 왜 binary search 를 쓰냐?
                    - 예를 들어 total_sum // 2 = 11일 때 a가 7이면 이면 b가 4여야 함. binary search를 사용하면 4와 가장 가까운 값을 linear search 보다 빠르게 찾아주기 때문에
                    - bisect_left 쓰면 target value가 들어갈 수 있는 첫 자리를 return 한다
                        - [1, 2, 3, 5] 에서 target value가 4이면 bisect_left 값은 3
                        - [1, 2, 3, 4, 5]에서 target value가 4이면 bisect_left 값은 여전히 3
                    - bisect_left 결과 해석
                        - array에 찾는 값이 이미 있는 경우
                            - return index는 그 값이 처음으로 위치한 곳의 index
                        - array에 찾는 값이 없는 경우
                            - return index는 그 값보다 바로 하나 큰 값
                        
                        → 따라서 bisect_left 결과랑, 그보다 하나 바로 작은 index에 위치한 값 두 개를 살펴보면 closest가 반드시 존재한다 
                        
                        - 이 때 bisect_left 결과가 0이면 그냥 0 값이 가장 가까운 것