# 153. Find Minimum in Rotated Sorted Array

Status: in progress
Theme: Binary Search
Created time: November 9, 2023 6:39 PM
Last edited time: November 12, 2023 3:45 PM

- test case by case로 코드를 끼워맞추는 습관을 고쳐야 할 필요가 있음
- rotated의 의미: 맨 마지막에 있던 원소가 앞으로 가고, 나머지 원소들이 뒤로 한칸씩 밀린다
- 내가 짜서 통과한 코드
    
    ```python
    class Solution:
        def findMin(self, nums: List[int]) -> int:
            if len(nums) == 1:
                return nums[0]
            left, right = 0, len(nums)-1
            while left <= right:
                mid = (left + right) // 2
                if left == right: return nums[left]
                elif nums[left] > nums[right]: 
                    # mid vs. right
                    if left == mid: return nums[right]
                    elif nums[mid] < nums[right]: 
                        right = mid 
                    else:
                        left = mid + 1 
                else: # mid vs. left
                    if left == mid: return nums[left]
                    elif nums[left] < nums[mid]:
                        right = mid -1 
                    else:
                        right = mid
    ```
    
- 너무 훌륭한 남의 답안
    
    ```python
    class Solution:
        def findMin(self, nums: List[int]) -> int:
            left, right = 0, len(nums)-1
            while left < right:
                mid = (left + right) // 2
                if nums[mid] > nums[right]:
                    left = mid + 1 
                else:
                    right = mid 
            return nums[left]
    ```
    
- unique elements, sorted → rotated 까지된 상태에서 시작하기 때문에
    - mid값과 right 값만 비교해도 모든 경우의 수를 커버할 수 있음
    - mid ≤ right → mid와 right 사이에 더 작은 값이 나올 가능성은 없다. right를 mid로 당겨온다
        - 둘의 값이 같은 경우도 right를 mid-1이 아닌 mid로 옮겨오기 때문에 문제 없다
    - mid > right → 뒤쪽에 있어야 할 원소들이 앞쪽으로 갔다는 것. 앞쪽에 있는 작은 값들은 뒤에 있다는 것이기 때문에 left를 mid + 1로 미뤄서 더 작은 원소들이 있는 쪽으로 범위를 옮긴다
- 중요한 것은 while left < right에서 등호가 없다는 것. 왜지?
    - left = right가 되면 while break 하고 return 하게끔
    - while left ≤ right를 조건으로 걸면 left > right가 되어야 끝