# 1235. Maximum Profit in Job Scheduling

Status: done, in progress, with help
Theme: DP
Created time: January 27, 2024 7:36 PM
Last edited time: January 29, 2024 11:06 PM

- Process
    - interval job scheduling problems
        - to find the maximum number of non-overlapping intervals (in this case, jobs) that can be accommodated in a schedule.
        1. **Sort the Jobs by Finish Time**: First, sort all the jobs (or intervals) by their finish times in ascending order.
        2. **Select the Jobs**: Start with the earliest finishing job. Select it and then remove all other jobs that overlap with it from the consideration set.
            - 종료 시간이 가장 이른 job에서 시작
            - 출발 시간이 진행되고 있는 job의 종료 시간보다 이른 경우의 모든 job 삭제 - overlapping
        3. **Repeat**: Continue this process, each time choosing the next job that finishes the earliest and does not overlap with any of the already selected jobs.
    - (a, b)
        - dp[b] = a, b job에서 얻는 profit + dp[a]
            - 출발 시간이 a, 작업 시간은 b-a
        - dp[b]를 만들 수 있는 조합은 여러 가지
            - dp[b-1] + profit
                - 출발 시간이 b-1, 작업 시간은 1
            - dp[1], profit
                - 출발 시간이 1, 작업 시간은 b-1
    - 구간에 대해서는 어떻게 해야 하나?
- AC 코드
    - Top-down
        - jobs가 startTime order로 sort된 것은 맞으나, startTime 자체가 sort된 게 아닐 수도 있음. 따라서 startTime을 정렬된 순서로 update 해줘야 하고
            - end time 가져올 때도 endTime[position] 하면 정렬된 jobs에서의 원소 순서와 다르므로, jobs에서 가져와야 한다
        - base case는 position == n 일 때 - 왜냐면 jobs[n]은 존재하지 않으니까. 그리고 state definition에서 memo[position]은 max profit of jobs[position:]
            - position 기준으로 다음 index나 더 뒤에 있는 index로 이동하는 건데, position = n이면 더 갈 곳이 없음
        
        ```python
        from bisect import bisect_left
        class Solution:
            def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
                jobs = list(zip(startTime, endTime, profit))
                jobs.sort() # sort by start time
                startTime = [job[0] for job in jobs]
        
                memo = {}
        
                # function
                def recur(position):
                    # base case
                    if position == len(jobs):
                        return 0
                    # check memo
                    if position in memo:
                        return memo[position]
                    # recurrence relation
                    ## skip the current
                    no_job = recur(position+1)
                    ## choose the current
                    next_index = bisect_left(startTime, jobs[position][1])
                    yes_job = jobs[position][2] + recur(next_index)
                    # save memo
                    memo[position] = max(no_job, yes_job)
                    return memo[position]
                
                return recur(0)
        ```
        
    - Bottom-up
        
        ```python
        from bisect import bisect_left
        class Solution:
            def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
                jobs = list(zip(startTime, endTime, profit))
                jobs.sort() # sort by start time 
                startTime = [job[0] for job in jobs]
                n = len(jobs)
                
                dp = [0] * (n+1)
                # base case: dp[n]
        
                for position in range(n-1, -1, -1):
                    no_job = dp[position+1]
                    end_time = jobs[position][1]
                    # max bisect_left : len(given_list) == n
                    next_index = bisect_left(startTime, end_time)
                    yes_job = jobs[position][2] + dp[next_index]
                    dp[position] = max(no_job, yes_job)
                
                return dp[0]
        ```
        
    - priority queue
        - heappop
            - 앞에 올 수 있는 chain을 다 꺼내서 max profit 비교
            - 앞에 올 수 있는 chain 중 최대 이익을 얻을 수 있는 경우만 distillation to max profit
        - heappush
            - 현재 profit 붙여서 제일 큰 이익 얻을 수 있는 경우만 다시 heapq에 추가
        
        ```python
        import heapq
        class Solution:
            def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
                jobs = list(zip(startTime, endTime, profit))
                jobs.sort() # sort by start time 
                startTime = [job[0] for job in jobs]
                n = len(jobs)
                max_profit = 0
                pq = []
        
                for i in range(n):
                    start_time, end_time, profit = jobs[i]
                    while pq and pq[0][0] <= start_time:
                        cur_chain = heapq.heappop(pq) # end_time, so_far_profit
                        max_profit = max(max_profit, cur_chain[1])
                    heapq.heappush(pq, [end_time, max_profit + profit])
                
                while pq:
                    cur_chain = heapq.heappop(pq)
                    max_profit = max(max_profit, cur_chain[1])
                
                return max_profit
        ```
        
- Trial
    - post-editorial: top-down 4 /34
        - bisect left: 들어갈 수 있는 자리 중 가장 왼쪽 자리
            - current end time과 같거나 그보다 큰 start time을 가진 job을 채택할 수 있으므로
            - endtime과 같은 startime은 기준보다 오른쪽에 위치해야 함
            - right, left는 알겠는데, 그럼 bisect_left가 return 하는 자리의 원소는 input parameter value보다 큰가 작은가? - it depends
                - **If `some_value` is in `some_list`**: The value at the index returned by **`bisect_left(some_value)`** would be equal to **`some_value`**.
                - **If `some_value` is not in `some_list`**: The value at the index returned by **`bisect_left(some_value)`** would be the next larger value in **`some_list`**, or it could be a position where **`some_value`** can be inserted without breaking the sort order (like at the end of the list if **`some_value`** is larger than all elements).
            
            ```python
            from bisect import bisect_left
            class Solution:
                def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
                    jobs = list(zip(startTime, endTime, profit))
                    jobs.sort() # sort by start time
            
                    memo = {}
            
                    # function
                    def recur(position):
                        # base case
                        if position == len(jobs):
                            return 0
                        # check memo
                        if position in memo:
                            return memo[position]
                        # recurrence relation
                        ## skip the current
                        no_job = recur(position+1)
                        ## choose the current
                        next_index = bisect_left(startTime, endTime[position])
                        yes_job = jobs[position][2] + recur(next_index)
                        # save memo
                        memo[position] = max(no_job, yes_job)
                        return memo[position]
                    
                    return recur(0)
            ```
            
    - post-editorial: priority queue
        
        ```python
        import heapq
        class Solution:
            def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
                jobs = list(zip(startTime, endTime, profit))
                jobs.sort() # sort by start time 
                startTime = [job[0] for job in jobs]
                n = len(jobs)
                max_profit = 0
                pq = [[0, 0]]
        
                for i in range(n):
                    start_time = jobs[i][0]
                    while pq and pq[0][0] <= start_time:
                        cur_chain = heapq.heappop(pq) # end_time, so_far_profit
                        if cur_chain[1]+jobs[i][2] > max_profit:
                            new_chain = [jobs[i][1], max_profit]
                            heapq.heappush(pq, [jobs[i][1], max_profit])
                
                while pq:
                    cur_chain = heapq.heappop(pq)
                    max_profit = max(max_profit, cur_chain[1])
                
                return max_profit
        ```
        
- Editorial
    - Overview
        - non-confilicting jobs
            - (startB, endB) → (startA, endA)
                - endB ≤ startA
            - (startA, endA) → (startB, endB)
                - endA ≤ startB
        - 각 Job에 대해서는 두 개의 option 존재
            - schedule(채택) it or not
            - job이 총 n개 이므로 2^N개의 조합 존재
        - 최적화 방안
            - index i에서의 job을 채택한다고 하면, 종료시간은 endTime[i]
                
                → endTime[i]보다 시작 시간이 이른 다른 모든 job은 버리게 되는 것 
                
            - 그 다음으로 채택하게 되는 job은 시작시간이 endTime[i]와 같거나 커야 겹치는 구간이 발생하지 않음 - startTime[j] ≥ endTime[i]
        - 두 가지 특징 → DP!
            1. 시간이 상충되는 다른 job이 이미 채택되었다면, 그 job은 채택될 수 없다 
                - 우리의 각 결정이 이전의 결과에 영향을 받는다
            2. 문제에서는 non-conflicting job들을 채택함으로써 이익을 최대화 화 하라고 한다 
    - **Approach 1: Top-Down Dynamic Programming + Binary Search**
        - Intuition
            - 시간 소모가 큰 반복적인 접근
                - start time 0: 가장 처음으로는 어떤 job이든 채택할 수 있다
                - 첫번째 job이 종료되면, 다른 모든 job들을 돌면서 시작 시간이 첫번째 job의 종료 시간과 같거나 그보다 늦은 옵션들을 고려한다 → 두번째 job 선택, 종료 시간 고려 → …
            - 더 효과적인 방법
                - start time에 따라 job sorting → binary search로 다음 non-conflicting job 탐색
                    - 다른 job들의 시작 시간 list에서 현재 job의 endTime이 위치하는 곳을 binary search
            - 각 Job에 대해 두 가지 옵션 존재
                - 이번 job을 채택하고, binary search를 사용해서 next non-conflicting job으로 넘어간다
                - 이번 job을 건너 뛰고, 다음 available job으로 넘어간다
                
                → 둘 중에 greater profit 선택 
                
            - memoization
                - 그림
                    - 중복되는 subproblem 존재 → memoization
                    
                    ![Untitled](Untitled%20142.png)
                    
                - 특정 position에 대해 max_profit을 계산하면, 이 값을 array에 저장 - `jobs[position:]` 으로부터 얻을 수 있는 최대 이익을 의미 (?)
                - 같은 position에 대해 max_profit을 계산해야 하면, 바로 찾아다가 사용
            
        - 알고리즘
            1. 각 job의 startTime, endTime, profit을 jobs에 저장 
            2. jobs를 starting time 기준으로 정렬
            3. 왼쪽 → 오른쪽 방향으로 job을 순회. current job index는 position 
                - 각 job에 대해 아래 두 가지 옵션 비교
                    1. current job skip (얻게 되는 profit 0) → position + 1에 있는 job으로 move on 
                    2. current job을 채택하고 (current job을 위한 profit earn), 다음 non-conflicting job (index: nextIndex)로 이동 
                        - nextIndex는 startTime array에 대해 binary search 적용해서 결정됨
            4. 3의 두 가지 옵션 중 profit이 더 큰 쪽을 memoization 
    - **Approach 3: Sorting + Priority Queue**
        - Intuition
            - 유사 문제 - 다만 우리 문제에서는 길이가 아니라 Profit max로
                - [[**646. Maximum Length of Pair Chain**](https://leetcode.com/problems/maximum-length-of-pair-chain/description/?envType=study-plan-v2&envId=dynamic-programming)](646%20Maximum%20Length%20of%20Pair%20Chain%2015e5932c32624cbd8be56ca5c2bc50fd.md)
                - [[**300. Longest Increasing Subsequence**](https://leetcode.com/problems/longest-increasing-subsequence/description/)](300%20Longest%20Increasing%20Subsequence%20654863aaf88d40e9876210846f683f5d.md)
                - 비슷한 접근법 차용
                    - start time 기준으로 job sort → current job에 가장 이익이 되는 쪽으로 chain of jobs 선택
            - chain 연장
                - 그림
                    
                    ![Untitled](Untitled%20143.png)
                    
                - 첫번째 job은 늘 새로운 chain 시작
                - 그 다음 job은 첫번째 job과 overlapping 하면 별도의 chain 시작하고, 아니면 첫번째 job의 chain에 이어서 붙임
                    - 이번 job이 뒤로 붙을 수 있는 chain 후보가 여러 개인 경우, 그중 most profitable 한 옵션을 선택
                - 처음부터 끝까지 모든 job을 순회한 후, 만들어진 chain 들 중 가장 큰 이익을 내는 chain을 선택
                - 근데 이런 접근법에서의 비효율
                    - current job이 시작하기 전이나 시작할 때 끝나는 most profitable chain을 찾기 위해 앞선 모든 previous job chain을 iterate over 해야 함 → O(N^2)
            - key observations
                1. 각 job에 대해 우리는 current job의 start time 이전 혹은 그때 끝나는 모든 chain을 찾고자 함 
                    
                    → existing chain들을 저장 → end time이 가장 빠른 순으로 효율적으로 접근 
                    
                2. job들은 start time 기준으로 정렬된 상태 → 만약 어떤 chain이 current job과 상충되지 않으면, 그보다 뒤에 나오는 다른 job들과도 상충되지 않음 (오히려 interval이 커지지) 
                    
                    → 끝나버린? chain 자체를 기억할 필요는 없고, 각 chain의 max profit을 기억하면 됨 → end time이 더 이른 chain들을 찾아서 자료 구조에서 지운다 ??? → chain 저장하기에 heap을 쓰는 것이 효율적 
                    
            
        - 알고리즘
            - 왼→오 순서대로 job iteration
                - heap에서 existing chain들을 꺼내서, current job이 붙을 만한 chain이 있는지 확인
                - current job과 상충하지 않는 (current job start time보다 이르게, 혹은 그때 끝나는) chain들에 대해서, 가장 profit이 큰 쪽에 current job을 append(total profit도 update) → 이 새로운 chain을 다시 heap에 push
            - chain이 heap에 저장되는 형태
                - end time, total profit
            - tricky part
                - current job을 붙여서 다시 heap으로 돌아가는 chain도 있지만, 그렇지 않은 경우
                - current job과는 상성이 어긋나도, 미래의 다른 job과는 붙을 수 있을지 모르는 일
                    - 예시
                        
                        Certainly, let's delve into an example that illustrates the scenario where profitable job chains, even though not pushed back into the heap, still influence the calculation of profits for subsequent jobs.
                        
                        ### Example Scenario
                        
                        Consider the following jobs `{start, end, profit}`:
                        
                        - Job A: `{1, 3, 100}`
                        - Job B: `{4, 6, 150}`
                        - Job C: `{2, 5, 200}`
                        
                        Here, Job A and Job B do not overlap, but Job C overlaps with both.
                        
                        ### Processing the Jobs
                        
                        1. **Initial State**:
                            - `maxProfit = 0`, Heap = `[]`.
                        2. **Process Job A**: `{1, 3, 100}`.
                            - Push Job A onto the heap: Heap = `[{3, 100}]`.
                            - `maxProfit` remains `0`.
                        3. **Process Job C**: `{2, 5, 200}`.
                            - Job C overlaps with Job A, so we cannot push it onto the heap directly.
                            - We do not pop Job A because Job C starts before Job A ends.
                            - `maxProfit` remains `0` (No chain completion yet).
                            - **Note**: Here, Job C, despite being highly profitable, is not added to the heap due to overlap.
                        4. **Process Job B**: `{4, 6, 150}`.
                            - Job B starts after Job A ends. Pop Job A from the heap and update `maxProfit = 100`.
                            - Push Job B onto the heap: Heap = `[{6, 250}]` (profit of 250 is `100 (maxProfit from Job A) + 150 (Job B's profit)`).
                        
                        ### Key Observation
                        
                        - After processing Job C (which wasn't pushed onto the heap), `maxProfit` remains `0`. However, Job C's presence affects the decision-making process. It couldn't be combined with Job A or Job B due to the overlap.
                        - When Job B is processed, it forms a new chain with the profit from the completed Job A (reflected in `maxProfit`), even though Job A is no longer in the heap.
                        - The final `maxProfit` value represents the maximum achievable profit, considering the constraints (job overlaps) and the best sequences formed till the end.
                        
                        ### Conclusion
                        
                        In this example, Job C, although not pushed back into the heap due to overlap, still plays a role in the overall scheduling scenario. This demonstrates how `maxProfit` accumulates the value from completed chains and influences future decisions, even for jobs that aren't added back into the heap.
                        
                - max_profit 변수 도입
                    - heap에서 chain을 하나씩 꺼낼때마다, 그 chain의 profit을 current max_profit과 비교
                    - 둘 중 더 큰 쪽으로 update max_profit
                - 모든 job들은 시작 시간 기준으로 sorting 되어 있음 → i번째 job을 위해 chain을 pop 하는 경우, 이 chain은 이번 job 뒤에 나오는 - i+1 이상의 index를 가진- 모든 job과도 결합 가능한 상태
                    
                    → end time을 비교할 필요 없으므로 profit만 비교하면 됨 
                    
                - ith iteration의 경우 maxProfit의 값은 ith job이 append 될 수 있는 job chain 들 중 가장 큰 profit 저장
            1. jobs에 start time, end time, profit 저장 후, start time 기준으로 sort
            2. left → right 순으로 job iteration - current job index: i 
                - priority queue top에 존재하는 job chain이 current job과 상충하지 않는 한 pop 지속
                    - 매 popped chain에 대해 max profit 비교 → 현재 job profit까지 더해서 update
            3. ending time, updated profit 을 짝지어서 heap에 추가 
                - current job이 append된 경우의 가장 profitable chain 의미
            4. 모든 job을 돈 다음, max_profit 변수와 priority queue에 있는 remaining chain의 profit 비교 - max profit 값 return