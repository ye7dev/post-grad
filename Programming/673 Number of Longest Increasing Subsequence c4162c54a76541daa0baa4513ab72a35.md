# 673. Number of Longest Increasing Subsequence

Status: done, in progress, with help
Theme: Longest Increasing Subsequence
Created time: January 17, 2024 3:52 PM
Last edited time: January 18, 2024 2:47 PM

- Process
    - 또 헷갈리는 점
        - subsequence는 contiguous 한가?
            
            → not necessarily `nums = [1,3,5,4,7]` 의 LIS는 [1, 3, 5, 7]
            
        - kadane’s algorithm은 subsequence를 위한 것인가?
            
            → no. maximum sum subarray를 위한 것. subarray는 contiguous
            
    - 각 index 자리가 마지막일 때의 LIS 길이 자체는 구할 수 있음. 근데 최장 길이가 몇 개가 되느냐는 어떻게 구하지…
    - dp에서 LIS 길이를 구한 다음, count는 앞에서부터 쫙 돌면서 길이가 같은 LIS가 몇 개인지 세야 할 듯 → 그렇게 하면 안나온다
        - 7에서 dp[-1]은 4인데, 그 앞에 애들의 LIS 길이는 모두 그보다 작다
    - double for loop을 쓴다
- AC 코드
    - Bottom-up
        
        ```jsx
        class Solution:
            def findNumberOfLIS(self, nums: List[int]) -> int:
                n = len(nums)
                # base case: every element is IS of length 1 
                dp = [1] * n 
                count = [1] * n
        
                for i in range(1, n):
                    for j in range(i):
                        # update dp value
                        if nums[j] < nums[i]:
                            # new LIS emergence
                            if dp[i] < dp[j] + 1: 
                                dp[i] = max(dp[i], dp[j]+1)
                                count[i] = 0 # reset for the new count
                            # title defense
                            if dp[i] == dp[j] + 1:
                                count[i] += count[j]
                
                # get all indices having 
                ## increasing subsequences ending at the arr[i]
                ## whose LIS is the maximum of dp array 
                max_len = max(dp)
                count_sum = 0
                for i in range(n):
                    if dp[i] == max_len:
                        count_sum += count[i]
                return count_sum
        ```
        
    - Top-down (🐌)
        - 값을 return 하는게 필요하도록 만듦 - 재귀식 보면 recur(j) 값을 가져다 쓰게
        
        ```python
        class Solution:
            def findNumberOfLIS(self, nums: List[int]) -> int:
                n = len(nums)
                length = [-1] * n
                length[0] = 1
                count = [-1] * n
                count[0] = 1
        
                # function 
                def recur(cur_idx):
                    # base case: first index
                    if cur_idx == 0:
                        return 1 
                    
                    # check memoized
                    if length[cur_idx] != -1:
                        return length[cur_idx]
                    
                    # recurrence relation
                    max_len = 1
                    cur_count = 1
                    for j in range(cur_idx):
                        if nums[j] < nums[cur_idx]:
                            if max_len < recur(j) + 1:
                                max_len = recur(j) + 1
                                cur_count = 0
                            if max_len == recur(j) + 1:
                                cur_count += count[j]
                    
                    # save result 
                    length[cur_idx] = max_len
                    count[cur_idx] = cur_count
        
                    return length[cur_idx]
        
                for i in range(1, n):
                    recur(i)
        
                count_sum = 0
                for i in range(n):
                    if length[i] == max(length):
                        count_sum += count[i]
                
                return count_sum
        ```
        
    - Top-down : return 하는 값 안 받아도 되게끔
        - 어차피 바깥에 for loop을 통해 값이 작은 i부터 recur를 한번씩 다 돌기 때문에 무조건 자기 보다 작은 index 값에 해당하는 memo는 채워져 있는게 보장됨
        - 그래서 재귀식에서 재귀함수를 호출하지 않고 memo를 호출해서 사용하는 게 가능
        
        ```python
        class Solution:
            def findNumberOfLIS(self, nums: List[int]) -> int:
                n = len(nums)
                length = [-1] * n
                length[0] = 1
                count = [-1] * n
                count[0] = 1
        
                # function 
                def recur(cur_idx):
                    # base case: first index
                    if cur_idx == 0:
                        return 1 
                    
                    # check memoized
                    if length[cur_idx] != -1:
                        return 
                    
                    # recurrence relation
                    max_len = 1
                    cur_count = 1
                    for j in range(cur_idx):
                        if nums[j] < nums[cur_idx]:
                            if max_len < length[j] + 1:
                                max_len = length[j] + 1
                                cur_count = 0
                            if max_len == length[j] + 1:
                                cur_count += count[j]
                    
                    # save result 
                    length[cur_idx] = max_len
                    count[cur_idx] = cur_count
        
                for i in range(1, n):
                    recur(i)
        
                count_sum = 0
                for i in range(n):
                    if length[i] == max(length):
                        count_sum += count[i]
                
                return count_sum
        ```
        
- Trial
    - 그냥 LIS 구하기
        - 이 식 자체는 내가 포함되던 안되던 내 자리에서 끊을 때 가장 긴 LIS의 길이
        - 직전 인덱스만 확인하는 이 답은 틀린 코드~
        
        ```jsx
        class Solution:
            def findNumberOfLIS(self, nums: List[int]) -> int:
                n = len(nums)
                dp = [1] * n
                count = {i:[] for i in range(n)}
                # base case: every element is IS of length 1 
                for i in range(1, n):
                    if nums[i-1] < nums[i]:
                        dp[i] += dp[i-1]
                    else:
                        dp[i] = max(dp[i-1], dp[i])
        
                return dp[-1]
        ```
        
    - 예제만 통과
        
        ```jsx
        class Solution:
            def findNumberOfLIS(self, nums: List[int]) -> int:
                n = len(nums)
                dp = [1] * n
                # base case: every element is IS of length 1 
                for i in range(1, n):
                    max_len = 0
                    max_count = 0
                    for j in range(i-1, -1, -1):
                        if nums[j] < nums[i]:
                            max_len = max(dp[j], max_len)
                            if dp[j] == max_len:
                                max_count += 1 
                    dp[i] += max_len
        
                if max_count == 0:
                    return n
                return max_count
        ```
        
    - post-editorial
        
        ```jsx
        class Solution:
            def findNumberOfLIS(self, nums: List[int]) -> int:
                n = len(nums)
                # base case: every element is IS of length 1 
                dp = [1] * n 
                count = [1] * n
        
                for i in range(1, n):
                    for j in range(i):
                        # update dp value
                        if nums[j] < nums[i]:
                            # new LIS emergence
                            if dp[i] < dp[j] + 1: 
                                dp[i] = max(dp[i], dp[j]+1)
                                count[i] = 0 # prepare for the new count
                            # title defense
                            if dp[i] == dp[j] + 1:
                                count[i] += count[j]
                
                # get index of Longest over all the position
                max_val = 0
                max_idx = -1
                for i, value in enumerate(dp):
                    if max_val < value:
                        max_idx = i 
        
                return count[max_idx]
        ```
        
- Editorial
    - Bottom-up
        - array 2개 사용
            - `dp` LIS 길이 저장
                - dp[i]: index i에서 끝나는 length of LIS
                    - 정의를 잘못 알고 있었음. index i까지 considering 해서 해당 위치 원소가 포함 안되어도 so far longest를 저장하는 게 아님
                    - 무조건 자기 자신을 포함하는 subsequence의 길이를 의미
                        
                        Yes, that's correct. In the context of the Longest Increasing Subsequence (LIS) problem, **`dp[i]`** includes **`arr[i]`** itself. It represents the length of the longest increasing subsequence that ends with the **`i`**-th element, **`arr[i]`**. This means the subsequence counted in **`dp[i]`** must include **`arr[i]`** as the last element.
                        
            - `count` index i에서 끝나는 LIS의 개수 저장
                - count[i] 초기값도 dp와 마찬가지로 1. 자기 자신으로 시작하고 끝나는 LIS 1개가 존재하기 때문에
        - 바로 앞까지의 index를 돌면서 (`j in range(i)`)
            - j에 위치한 숫자가 i에 위치한 숫자보다 작을 경우
                - j에서 끝나는 subsequence에다가 nums[i]를 하나 더해서 만들어지는 새로운 subsequence가 만들어짐 → 기존 LIS 길이랑 새로 만들어진 IS 길이 비교해서 LIS at the index update
                    - `dp[i] = max(dp[i], dp[j]+1)`
                - 기본 원칙은 dp[i]가 dp[j]+1과 같다면 count[i]에 count[j]를 더한다 인데
                    - dp[i]가 이전 업데이트에서 이미 dp[j]+1의 길이를 갖고 있던 상태라면
                        - 그냥 count[i] += count[j]만 하면 된다
                    - 이번 업데이트에서 dp[i] = dp[j]+1로 되는 상황이라면-dp[j]+1이 LIS임
                        - 기존에 더 짧은 길이의 LIS를 count 하던 것을 버리고, 새로 count[j]를 더해줘야 한다
        - 마지막에 무슨 값을 return 해야 하는가
            - 가장 긴 LIS가 몇 개 있는지
                1. 가장 긴 LIS의 길이를 구한다
                2. 그 길이를 갖는 dp에서의 인덱스를 모두 구한다 
                3. count에서 해당 인덱스에 위치한 값을 모두 더 한다 
            - 다시 정리
                - dp[i]: arr[i]에서 끝나는 increasing subsequence 중 가장 길이가 긴 것의 길이를 저장
                - count[i]: arr[i]로 끝나는 increasing subsequence 중 max_length를 가진 IS의 개수가 몇 개인지
            
- 원래 LIS 구하는 식도 앞의 인덱스를 다 도는 과정을 포함한다
    
    ```jsx
    class Solution:
        def lengthOfLIS(self, nums: List[int]) -> int:
            dp = [1] * len(nums)
            # dp[i]: LIS from up to nums[:i+1]
            # base case
            ## each letter is its own LIS of length 1
            ## dp[0] -> nums[0:1] -> single num -> 1
    
            for i in range(len(nums)):
                cur_num = nums[i]
                for j in range(i):
                    if nums[j] < cur_num:
                        dp[i] = max(dp[i], 1 + dp[j])
            
            return max(dp)
    ```