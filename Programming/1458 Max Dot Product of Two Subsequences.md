# 1458. Max Dot Product of Two Subsequences

Status: in progress
Theme: DP
Created time: February 1, 2024 4:59 PM
Last edited time: February 1, 2024 5:58 PM

- Progress
    - 문제 이해
        
        nums1, nums2 array 2개가 주어질 때, 각각에서 subsequence(contiguous 할 필요 없고 일부 원소 지운 subset, 다만 순서는 유지)를 뽑아 dot product를 구할 때, 최대 값을 구하라 
        
    - 과정
        - substring 일치시키는 문제처럼 교차해서 곱하기는 안될 듯
        - dp[i][j]
            - nums1[i:] 와 nums2[j:] 원소에서 구할 수 있는 max dot product
            - base case
                - 원소가 하나만 있을 때 아닐까
                - 근데 반대편을 뭐랑 곱했는지가
- Trial
    - Bottom-up → 42/69
        
        ```python
        class Solution:
            def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
                m, n = len(nums1), len(nums2)
                dp = [[-float('inf')] * n for _ in range(m)]
        
                # base case
                for j in range(n):
                    dp[m-1][j] = max(dp[m-1][j], nums1[m-1] * nums2[j])
                for i in range(m):
                    dp[i][n-1] = max(dp[i][n-1], nums1[i] * nums2[n-1])
                
                # recurrence relation
                for i in range(m-2, -1, -1):
                    for j in range(n-2, -1, -1):
                        cur_prod = nums1[i] * nums2[j]
                        dp[i][j] = max(dp[i+1][j], dp[i][j+1], cur_prod + dp[i+1][j+1])
                return dp[0][0]
        ```
        
    - Bottom-up → 50/69
        
        ```python
        class Solution:
            def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:        
                m, n = len(nums1), len(nums2)
                dp = [[-float('inf')] * (n+1) for _ in range(m+1)]
        
                # base case
                for j in range(n):
                    dp[m-1][j] = max(dp[m-1][j], nums1[m-1] * nums2[j])
                for i in range(m):
                    dp[i][n-1] = max(dp[i][n-1], nums1[i] * nums2[n-1])
                
                # recurrence relation
                for i in range(m-2, -1, -1):
                    for j in range(n-2, -1, -1):
                        cur_prod = nums1[i] * nums2[j]
                        dp[i][j] = max(dp[i+1][j], dp[i][j+1], cur_prod + dp[i+1][j+1], dp[i+1][j+1], cur_prod)
                return dp[0][0]
        ```
        
- Editorial
    - **Approach 1: Top-Down Dynamic Programming**
        - Intuition
            - `dp(i, j)`
                - suffix of nums1 starting at index i  → nums1[i:]
                - suffix of nums2 starting at index j → nums2[j:]
                - 두 subarray에서 원소를 뽑는 것을 고려할 때 얻을 수 있는 max dot product
            - base case
                - i == m `OR` j == n → 둘 중 하나라도 array가 exhausted → return 0
            - recurrence relation
                - each state 당 세 가지 option 존재
                    1. nums[i] * nums[j]를 합에 더한다 → nums[i] * nums[j] + dp[i+1][j+1]
                        - 이것 때문이라도 dp를 (m+1) * (n+1)로 잡아야 한다
                        - dp가 m * n 이면 nums[m-1] * nums[j-1] + dp[m][n]인 경우는 고려할 수가 없다.
                        - 마지막 원소들도 곱해서 기회를 줘야~~!!
                    2. nums2에서 현재 원소를 skip 한다 → dp[i][j+1]
                    3. nums1에서 현재 원소를 skip → dp[i+1][j]
                - 세 개 중 max가 현재 state의 답
            - missing case
                - 문제에서 non-empty sequence라고 되어 있음
                    - 음수로 결과가 나오더라도 최소 한번의 operation 결과를 들고 있어야 함
                - 두 array 중 하나는 다 양수고 하나는 다 음수인 경우
                    - 예)
                        
                        `nums1 = [-1, -4, -7]`
                        
                        `nums2 = [6, 2, 52]`
                        
                        → 조합을 어떻게 가져가던 음수가 나옴 → 위의 식만 가지고 계산하면 다 skip 해버리고 base case 도달해서 0을 return 할 것 
                        
                    - 이런 경우에는 재귀 함수 들어가기 전에 그냥 그나마 큰 음수 결과를 return 하도록 해야 함
- AC 코드
    - Bottom-up(⚡️)
        - 고려해야 하는 option이 상당히 많음 (5개)
            - 현재 곱에 지난 결과를 더한 것
            - 현재 곱만 가져가는 경우 (지난 결과가 음수인 경우)
            - 지난 결과만 가져가는 경우 (현재 곱이 음수인 경우)
            - index i, j 중 둘 중 하나 skip 하는 경우
        
        ```python
        class Solution:
            def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:        
                m, n = len(nums1), len(nums2)
                dp = [[-float('inf')] * (n+1) for _ in range(m+1)]
        
                # recurrence relation
                for i in range(m-1, -1, -1):
                    for j in range(n-1, -1, -1):
                        cur_prod = nums1[i] * nums2[j]
                        dp[i][j] = max(dp[i+1][j], dp[i][j+1], cur_prod + dp[i+1][j+1], dp[i+1][j+1], cur_prod)
                return dp[0][0]
        ```
        
    - Top-down
        
        ```python
        class Solution:
            def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
                # edge case - all negative & all possible
                if max(nums1) < 0 and min(nums2) > 0: # nums1: all negative
                    return max(nums1) * min(nums2)
                if max(nums2) < 0 and min(nums1) > 0: # nums2: all negative 
                    return max(nums2) * min(nums1)
                
                m, n = len(nums1), len(nums2)
                memo = {}
                # function
                def recur(i, j):
                    # check memo
                    if (i, j) in memo:
                        return memo[(i, j)]
                    # base case
                    if i == m or j == n:
                        return 0
                    # recurrence relation
                    left_skip = recur(i+1, j)
                    right_skip = recur(i, j+1)
                    no_skip = (nums1[i] * nums2[j]) + recur(i+1, j+1)
                    memo[(i, j)] = max(left_skip, right_skip, no_skip)
                    return memo[(i, j)]
                return recur(0, 0)
        ```
        
    - Editorial Bottom-up (⚡️)
        - 초기값을 0으로 설정. -float(’inf’)로 커버하는 경우에는 edge case가 없는 대신 option이 5개
        - 여기서는 edge case가 있고, state 당 option이 3개
        
        ```python
        class Solution:
            def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
                # edge case - all negative & all possible
                if max(nums1) < 0 and min(nums2) > 0: # nums1: all negative
                    return max(nums1) * min(nums2)
                if max(nums2) < 0 and min(nums1) > 0: # nums2: all negative 
                    return max(nums2) * min(nums1)
                
                m, n = len(nums1), len(nums2)
                dp = [[0] * (n+1) for _ in range(m+1)]
                
                for i in range(m-1, -1, -1):
                    for j in range(n-1, -1, -1):
                        left_skip = dp[i+1][j]
                        right_skip = dp[i][j+1]
                        no_skip = (nums1[i] * nums2[j]) + dp[i+1][j+1]
                        dp[i][j] = max(left_skip, right_skip, no_skip)
                return dp[0][0]
        ```
        
- [ ]  sum-up