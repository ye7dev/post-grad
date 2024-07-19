# 34. Find First and Last Position of Element in Sorted Array

Status: in progress
Theme: Binary Search
Created time: November 9, 2023 5:14 PM
Last edited time: November 9, 2023 6:38 PM

- 문제 이해
    
    중복된 값이 있는 array. non-decreasing order
    
- 나의 최선
    
    ```python
    class Solution:
        def searchRange(self, nums: List[int], target: int) -> List[int]:
            if len(nums) == 0: return [-1, -1]
    
            res = [len(nums), -1]
    
            def bs(arr, start):
                left, right = 0, len(arr)-1
                if nums[left] == nums[right] == target:
                    if res[0] > start:
                        res[0] = start
                    elif res[1] < start:
                        res[1] = start
                    return 
    
                while left <= right:
                    mid = (left + right) // 2
                    if nums[mid] == target:
                        bs(arr[left:mid], start+left)
                        bs(arr[mid:right+1], start+mid)
                    elif nums[mid] > target:
                        right = mid-1 
                    else:
                        left = mid +1 
    
            bs(nums, 0)     
             
            if res == [len(nums), -1]:
                return [-1, -1]
            else:
                return res
    ```
    
- chat 스승님 답안
    - 그냥 leftmost, rightmost 찾는다…
    - leftmost 찾는 코드는 nums[mid] == target일 때도 right=mid-1로 당겨오고, 마지막에 left return 하는 것. while loop condition은 똑같이 while left ≤ right
    - rightmost 찾는 코드는 nums[mid] == target일 때도 left = mid + 1로 미루고, 마지막에 right return 하는 것. while loop condition은 똑같이 while left ≤ right
    - 주의: 마지막에 leftmost, rightmost 함수에서 return된 두 값이 leftmost<rightmost인지 비교해야 함
        - ~most 찾는 함수에서 둘 다 값이 없더라도 결국 무슨 값을 return 하긴 함
        - leftmost code: If the target is not found, it will return the index where the target could be inserted (which will be the index of the smallest element greater than the target).
            - left가 right 뒤에 와있는 상태인데(while loop exit), 여기서 left를 return 하면, target보다 더 큰 원소 중에 가장 작은 것의 index를 return
        - rightmost code: If the target is not found, it will return the index of the largest element less than the target.
            - left가 right 뒤에 와있는 상태인데 right를 return 하니까, target보다 작은 값 중에 가장 큰 원소의 index를 return