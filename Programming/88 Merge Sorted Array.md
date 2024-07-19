# 88. Merge Sorted Array

Status: done, in progress
Theme: Divide & Conquer
Created time: December 1, 2023 1:54 PM
Last edited time: December 1, 2023 3:13 PM

- [ ]  생각날때마다 다시 풀어보기
    - [ ]  1번
- easy
- 통과한 코드
    - 샵숑키들 누가 sort를 쓰게 하남
    
    ```python
    class Solution:
        def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
            """
            Do not return anything, modify nums1 in-place instead.
            """
            nums1[m:] = nums2[:]
            nums1.sort()
    ```
    
- decent 코드
    
    ```python
    class Solution:
        def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
            """
            Do not return anything, modify nums1 in-place instead.
            """
            p1 = m-1
            p2 = n-1
            
            # current position: p 
            for p in range(n+m-1, -1, -1):
                if p2 < 0: break 
                if p1 >= 0 and nums1[p1] > nums2[p2]:
                    nums1[p] = nums1[p1]
                    p1 -= 1 
                else: # no more nums1 or nums2[p2] >= nums1[p1]
                    nums1[p] = nums2[p2]
                    p2 -= 1
    ```