# 912. Sort an Array

Status: done, in progress
Theme: sort
Created time: December 1, 2023 4:02 PM
Last edited time: December 1, 2023 4:32 PM

- ~~이런 게 이제 내가 하기 어려워하는 류의 문제인 것이다 index 게임~~ → 응 아니구요 내장함수 쓰지 말란 거였음. 문제를 잘 읽으셈…
- 아오 드디어 풀었다
    
    ```python
    class Solution:
        def sortArray(self, nums: List[int]) -> List[int]:
            def merge_sort(arr):
                n = len(arr)
                if n == 1: return arr
                mid = n // 2 
                left = merge_sort(arr[:mid])
                right = merge_sort(arr[mid:])
                return merge(left, right)
    
            def merge(left, right):
                new_arr = []
                i, j = 0, 0
                while i < len(left) and j < len(right):
                    if left[i] <= right[j]:
                        new_arr.append(left[i])
                        i += 1
                    else:
                        new_arr.append(right[j])
                        j += 1 
    
                new_arr += left[i:]
                new_arr += right[j:]
                return new_arr
            
            return merge_sort(nums)
    ```