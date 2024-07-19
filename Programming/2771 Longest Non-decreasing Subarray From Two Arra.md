# 2771. Longest Non-decreasing Subarray From Two Arrays

Status: in progress, incomplete, 👀1
Theme: DP
Created time: February 1, 2024 3:43 PM
Last edited time: February 1, 2024 4:59 PM

- Progress
    - 문제 이해
        - nums1, nums2 모두 길이 n의 integer array
        - nums3 array도 길이 n이 되도록 만들어야 하는데, nums3[i]는 nums1[i]나 nums2[i]에서 하나 가져와야 함
        - 이 선택을 최적으로 해서 nums3 안에서 non-decreasing(증가하거나 값을 유지하는) subarray(원소가 연속으로 있어야 함)의 길이를 최대로 만들어야 함
        - nums1, 2, 3 length는 모두 10^5 → log N의 solution이 필요하다…
    - 과정
        - 만들 수 있는 방법의 가지수가 아니라 최대 길이만 구하면 됨
        - 지금 몇 번째 원소인지, 마지막 원소 값이 뭐였는지
            - 지금 몇 번째 원소인지 알아야 다음 원소를 알 수 있고
            - 마지막 원소 값을 알아야 거기서 다시 후보를 좁힐 수 있음
        - 근데 decreasing 원소가 나타난다고 해서 안 붙일 수는 없음. 무조건 nums3의 길이를 n으로 맞추긴 해야 함
        - dp[n][i]
            - numsi 집합에서 마지막으로 원소를 추가해서 길이 n의 nums3를 만들었을 때 최대 non-decreasing subarray
            - 빈 sequence는 longest ~ 정의에 맞지 않아서 0
        - 두번째 parameter를 뭐로 써야 할지 모르겠음
            - 여기서도 nums3를 들고 다닐 필요 없고
            - 그리고 i, arr 만으로는 unique state를 만들 수 없음
                - 왜냐면 i-1까지 결과가 여러 갠데 각각에 이어지는 i, arr를 모두 담을 수 있나?
                - 근데 모두 담을 필요 없지. 최장 길이만 저장하면 되니까
        - base case
            - 원소가 하나일 때는 무조건 1
        - 근데 last num을 들고 다니면 10^9까지도 자리가 필요하지 않을까?
        - 1234 → 네번째 자리에 는 이미 와있다고 생각하고
        - 세번째 자리에 올 수 있는 애는 nums1[2], nums2[2] 중 4보다 작거나 같은 애
            - 3, 2 둘 다 됨
        - dp[i][last_num]
            - 고려하는 범위가 nums[i:]일 때 last_num일 때 조건 만족하는 array 최대 길이
- Trial
    - Top-down
        
        ```python
        class Solution:
            def maxNonDecreasingLength(self, nums1: List[int], nums2: List[int]) -> int:
                n = len(nums1)
                memo = {}
        
                # function
                def recur(i, last_num):
                    # check memo
                    state = (i, last_num)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i == n:
                        return 0
                    # recurrence relation
                    if nums1[i] <= last_num:
                        choose_a = 1 + recur(i+1, nums1[i])
                    else:
                        choose_a = recur(i+1, nums1[i])
                    if nums2[i] <= last_num:
                        choose_b = 1 + recur(i+1, nums2[i])
                    else:
                        choose_b = recur(i+1, nums2[i])
                    memo[state] = max(choose_a, choose_b)
                    return memo[state]
                
                return recur(0, 0)
        ```
        
    - Top-down 1024/2973
        - 부등호 방향 잘못 되어서 바꿔줌
        
        ```python
        class Solution:
            def maxNonDecreasingLength(self, nums1: List[int], nums2: List[int]) -> int:
                n = len(nums1)
                memo = {}
        
                # function
                def recur(i, last_num):
                    # check memo
                    state = (i, last_num)
                    if state in memo:
                        return memo[state]
                    # base case
                    if i == n:
                        return 0
                    # recurrence relation
                    if nums1[i] <= last_num:
                        choose_a = 1 + recur(i+1, nums1[i])
                    else:
                        choose_a = recur(i+1, nums1[i])
                    if nums2[i] <= last_num:
                        choose_b = 1 + recur(i+1, nums2[i])
                    else:
                        choose_b = recur(i+1, nums2[i])
                    memo[state] = max(choose_a, choose_b)
                    return memo[state]
                
                return recur(0, 0)
        ```
        
- AC 코드
    - 두 array 모두에서 decreasing 원소를 얻게 되는 경우의 수 고려했어야 - 그럼 그 decreasing 원소부터 다시 longest ~ 세어 나가야 하기 때문에 prev를 0으로 유지
    
    ```python
    class Solution:
        def maxNonDecreasingLength(self, nums1: List[int], nums2: List[int]) -> int:
            n = len(nums1)
            memo = {}
    
            # function
            def recur(i, last_num):
                # check memo
                state = (i, last_num)
                if state in memo:
                    return memo[state]
                # base case
                if i == n:
                    return 0
                # recurrence relation
                new_start = 0
                if last_num == 0:
                    new_start = recur(i+1, 0)
    
                choose_a, choose_b = 0, 0
                if nums1[i] >= last_num:
                    choose_a = 1 + recur(i+1, nums1[i])
                if nums2[i] >= last_num:
                    choose_b = 1 + recur(i+1, nums2[i])
                    
                memo[state] = max(choose_a, choose_b, new_start)
                return memo[state]
            
            return recur(0, 0)
    ```