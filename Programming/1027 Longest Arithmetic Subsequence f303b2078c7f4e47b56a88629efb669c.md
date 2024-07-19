# 1027. Longest Arithmetic Subsequence

Status: done, in progress
Theme: DP, Longest Increasing Subsequence
Created time: January 18, 2024 4:45 PM
Last edited time: January 19, 2024 11:29 AM

- Trial
    - 연속인 두 숫자 사이의 차를 구해서 count 하는 단순한 방법 - 예제 다 틀림 ㅋ
        
        ```python
        class Solution:
            def longestArithSeqLength(self, nums: List[int]) -> int:
                n = len(nums)
                diff_count = {}
                for i in range(1, n):
                    cur_diff = nums[i]-nums[i-1]
                    if cur_diff not in diff_count:
                        diff_count[cur_diff] = 0
                    diff_count[cur_diff] += 1
                
                return max(diff_count.values())
        ```
        
    - 현재 숫자랑 그 앞에 있는 모든 숫자 사이의 차를 구해서 count 한 뒤 자기 자신 1 더해서 답을 구해봤으나… 6/65
        
        ```python
        class Solution:
            def longestArithSeqLength(self, nums: List[int]) -> int:
                n = len(nums)
                diff_count = {}
        
                for i in range(1, n):
                    for j in range(i):
                        if nums[i] - nums[j] in diff_count:
                            diff_count[nums[i] - nums[j]] += 1
                        else:
                            diff_count[nums[i] - nums[j]] = 1
                
                return max(diff_count.values()) + 1
        ```
        
    - 위에다가 첫번째 숫자를 맞이하면 1을 더하는 방식으로 변형을 해봤으나 8/65
        
        ```python
        class Solution:
            def longestArithSeqLength(self, nums: List[int]) -> int:
                n = len(nums)
                diff_count = {}
        
                for i in range(1, n):
                    for j in range(i):
                        if nums[i] - nums[j] in diff_count:
                            diff_count[nums[i] - nums[j]] += 1
                        else:
                            diff_count[nums[i] - nums[j]] = 1
                        if j == 0:
                            diff_count[nums[i]-nums[j]] += 1 
                
                return max(diff_count.values())
        ```
        
    - while loop도 꺼내봤으나 예제 2개만 맞춤
        
        ```python
        class Solution:
            def longestArithSeqLength(self, nums: List[int]) -> int:
                n = len(nums)
                max_count = 0
                for i in range(n-1, 0, -1): # n-1 ~ 1
                    a = nums[i]
                    j = i-1 # n-2 ~ 0
                    b = nums[j] 
                    cur_diff = a - b
                    count = 2
                    while True:
                        a = b
                        j -= 1 
                        if j < 0:
                            break 
                        b = nums[j]
                        if a - b == cur_diff:
                            count += 1 
                    max_count = max(count, max_count)
                return max_count
        ```
        
- AC 코드
    - post-editorial bottom-up
        - 점화식이 좀 헷갈렸는데, 만약 이전에 그런 차를 만드는 pair가 없었으면 이번 (left, right) pair가 첫번째 이므로 2를 더해야 하고, 있었으면 right만 그 seq에 더해지면 되니까 dp[left][diff]+1을 따랐다
        - max를 매 left마다 해줘야 하는 이유는 right에서 끝나는 LAS가 어느 left에서 시작할지 모르니까 다 돌면서 그 중에 최대값을 저장하기 위해서
        
        ```python
        from collections import defaultdict
        class Solution:
            def longestArithSeqLength(self, nums: List[int]) -> int:
                n = len(nums)
        
                # array
                # dp[right][diff] - length of LAS 
                ## ending at nums[right] with common diff as 'diff' 
                dp = [defaultdict(int) for _ in range(n)]
        
                # base case: left = 0 -> dp[left][diff] = 0
                ## automatically covered by defaultdict(int)
                max_len = 2 
                for right in range(1, n):
                    for left in range(right):
                        diff = nums[right] - nums[left]
                        if dp[left][diff] == 0:
                            dp[right][diff] = max(dp[right][diff], 2)
                        else:
                            dp[right][diff] = max(dp[right][diff], dp[left][diff]+1)
                        max_len = max(max_len, dp[right[diff]])
                    
                return max_len
        ```
        
    - editorial bottom-up
        - list of dictionary가 아니라 dictionary 하나를 사용했고, 대신 key를 tuple로 가져감
        - right가 0부터 시작해도 left가 알아서 valid 범위에서 시작하니 따로 index 조정 없이 넣어줬고
        - dictionary method `dp.get` 사용
            - key에 해당하는 값이 있으면 그 값을 가져와서 1을 더한 값이 dp[(right, diff)] 값이 되고
            - 만약 없으면 get에서 default value로 준 1을 return 하기 때문에 거기에 1을 더해서 2를 만든다
        - 내 방식에 비해 빠른가?
            - 그렇다 근데 주로 빠른 이유가 다른게 아니고 max_len 때문인듯. 마지막에 사전 값만 가져와서 max 한번 때리는게 더 빠른 듯
        
        ```python
        class Solution:
            def longestArithSeqLength(self, nums: List[int]) -> int:
                dp = {}
                
                for right in range(len(nums)):
                    for left in range(0, right):
                        dp[(right, nums[right] - nums[left])] = dp.get((left, nums[right] - nums[left]), 1) + 1   
                
                return max(dp.values())
        ```
        
    - final bottom-up (⚡️)
        
        ```python
        from collections import defaultdict
        class Solution:
            def longestArithSeqLength(self, nums: List[int]) -> int:
                n = len(nums)
        
                # array
                # dp[right][diff] - length of LAS 
                ## ending at nums[right] with common diff as 'diff' 
                dp = {}
        
                # base case: left = 0 -> dp[left][diff] = 0
                ## automatically covered by defaultdict(int)
                for right in range(1, n):
                    for left in range(right):
                        diff = nums[right] - nums[left]
                        dp[(right, diff)] = dp.get((left, diff), 1) + 1
                        
                max_len = max(dp.values())
                    
                return max_len
        ```
        
- Editorial
    - Intuition
        - Brute-force approach (O(n^3), TLE)
            - 모든 arithmetic sequence는 길이 2 이상
            - nums를 nested iteration으로 돌면서 arithmetic sequence의 첫 두 element를 구성하는 nums[left], nums[right]를 찾는다
            - 각 indice pair (left, right)에 대해 diff를 구한 뒤 이걸 common difference로 삼고, right의 오른쪽 부분을 순회하면서 following elements(?)가 있는지 본다
                - 예) nums[right]와 diff를 가지고 제3의 element인 nums[right] + diff가 nums[right]의 오른쪽에 존재하는지
        - nums[left], nums[right]를 sequence의 starting two element로 두는 대신, last two elements라고 생각
            
            ![Untitled](Untitled%20221.png)
            
        - array의 각 원소에서 끝나는 가능한 모든 arithmetic sequence와 common diff, length를 keep track
        - left에서 끝나는 array들(?)을 이미 알고, 그것들의 common difference, length를 이미 알고 있다고 가정하면, 이것들 중 nums[right]-nums[left] = `diff` 를 common difference로 삼는 arithmetic sequence를 연장하면 됨. 그리고 길이도 이미 아니까 거기에 +1 하면 되고
            
            ![Untitled](Untitled%20222.png)
            
            - 문제에서 최장 길이만 요구하고 있기 때문에 sequence 자체를 저장할 필요는 없다. diff랑 length만 저장하면 될일
            
            ![Untitled](Untitled%20223.png)
            
        - state definition
            - `dp[right][diff]` : index `right` 에 위치한 원소를 마지막 원소로 갖는 가장 긴 arithmetic sequence의 길이. 이 때 이 sequence의 common diff는 `diff`
        - transition equation
            - `dp[right][diff]` = `dp[left][diff]`
                - 주의: right는 index이고, diff는 값의 차이
                - left는 nums[right]-nums[left] = diff인 원소의 index. 당연히 right > left
        - original question
            - maximum value in dp
    - Algorithm
        1. dp init
            - 초기값, 사이즈에 대한 정보는 왜 없냐!
        2. iterate over the last index `right` 
            - right는 0에서 시작. base case 겠지? no valid left → move one
            - right가 한 칸 오른쪽의 새로운 값을 갖게 되면(1 증가하면) left는 0으로 돌아감
            - left < right인 모든 left를 돌면서
                - common difference 계산 (nums[right]-nums[left])
                - if there exists such a subsequence
                    - dp[right][diff] = dp[left][diff]+1
                - 아니면 dp[right][diff]를 2로 초기화해라
        3. dp에서 max value를 return 
- 헷갈려서 찍어본 코드 - defaultdict, dict in list
    
    ```python
    >>> n =3
    >>> dp = [{} for _ in range(n)]
    >>> dp
    [{}, {}, {}]
    >>> dp[0]
    {}
    >>> from collections import defaultdict
    >>> x = defaultdict(int)
    >>> x[0]
    0
    >>> dp = [defaultdict(int) for _ in range(n)]
    >>> dp[0]
    defaultdict(<class 'int'>, {})
    >>> dp[0][4]
    0
    >>>
    ```