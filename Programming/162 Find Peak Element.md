# 162. Find Peak Element

Status: done, in progress
Theme: Binary Search
Created time: November 3, 2023 3:31 PM
Last edited time: November 3, 2023 5:17 PM

- 문제 이해
    - You may imagine that `nums[-1] = nums[n] = -∞`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.
        - `-∞` 1, 2, 3, 1 `-∞` 라는 뜻. 그러니까 제일 왼쪽에 있는 원소는 자기 오른쪽 보다만 크면 peak이고, 제일 오른쪽에 있는 원소는 자기 왼쪽 보다만 크면 peak라는 뜻
    - peak가 2개 이상인 경우 둘 중에 하나만 return 하면 됨
    - `nums[i] != nums[i + 1]` for all valid `i`
        - 원소 위치마다 값이 다름
- 나의 30분
    - binary search의 근본 행동은 조건에 맞지 않는 절반을 버린다는 것
    - merge sort 처럼 두 개씩 남을 때까지 쪼개서 둘 중에 큰 쪽을 남기는데…
        - 어디까지 올라와야 하는지
        - 그리고 merge 함수에서는 쪼개진 Input을 받을 때마다 index가 0으로 항상 초기화됨. 문제에서처럼 원래 arr에서의 index는 어떻게 구해야 할지 모르겠음
- 남의 아이디어
    - mid를 기준으로 세 가지 경우가 가능
        
        ![Untitled](Untitled%2058.png)
        
        1. peak가 mid의 왼쪽에 있는 경우 
            - nums[mid-1] > nums[mid]
            - 정답이 왼쪽에 있으니 mid의 오른쪽 값은 모두 버린다
            - mid의 왼쪽 side 재탐색
        2. mid가 peak인 경우
            - 그대로 mid를 return
        3. peak가 mid의 오른쪽에 있는 경우
            - nums[mid] < nums[mid+1]
            - 정답이 오른쪽에 있으니 mid의 왼쪽 값은 모두 버린다
            - mid의 오른쪽 side 재탐색
    - base case
        - nums에 원소 하나만 있는 경우 → 0 return
        - 제일 가장 자리 원소들이 peak인 경우 → 조건 하나씩만 만족하면 됨
- 남의 아이디어 → 내가 짠 코드
    
    ```python
    class Solution:
        def findPeakElement(self, nums: List[int]) -> int:
            # base case
            if len(nums) == 1 or nums[0] > nums[1]: return 0 
            if nums[len(nums)-1] > nums[len(nums)-2]: return len(nums)-1
    
            # middle 
            left, right = 1, len(nums)-2
            while left <= right:
                mid = (left + right) // 2
                if nums[mid-1] < nums[mid] and nums[mid] > nums[mid+1]:
                    return mid 
                elif nums[mid-1] > nums[mid]:
                    right = mid -1 
                elif nums[mid+1] > nums[mid]:
                    left = mid + 1
    ```