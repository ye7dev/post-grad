# 35. Search Insert Position

Status: done, in progress
Theme: Binary Search
Created time: November 2, 2023 4:45 PM
Last edited time: November 2, 2023 4:55 PM

- matching index가 없을 때는 should-be index를 return 해야 하는데 왜 이게 while loop 빠져나와서 left가 되어야 하는지?
    - chat 센세도 명확한 답을 안줌. 그냥 left가 should be index라는 것을 외우는 게 빠르겠다
    - 참고로 **`right`** represents the index of the last element checked in the binary search
- 코드

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)-1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                right = mid -1 
            else:
                left = mid + 1 
        return left
```