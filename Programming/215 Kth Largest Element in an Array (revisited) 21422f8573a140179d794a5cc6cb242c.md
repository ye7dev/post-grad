# 215. Kth Largest Element in an Array (revisited)

Status: in progress
Theme: sort
Created time: March 7, 2024 1:34 PM
Last edited time: March 8, 2024 10:23 PM

- [Elements of Programming Interviews](Elements%20of%20Programming%20Interviews%202bc669b6f47c41169d7363539f55c00b.md) 문제 복습용 (sorting 사용 → TLE at the last)
    
    divide & conquer + randomization + binary search 
    
    interval: pivot 뽑는 index 허용 구간 
    
    partition sort: pivot을 중심으로 그보다 작은 원소, 그보다 큰 원소 크게 두 그룹으로 나눔
    
    ↳ pivot의 위치도 정렬 과정에서 바뀌고, 최종 return 값은 pivot의 index 
    
    input array에는 중복 없음 
    
    내림차순 정렬에서 가장 큰 원소(idx 0): 첫번째로 큰 원소, 가장 작은 원소(idx n-1): n번째로 큰 원소
    
    → kth largest element: 내림차순 정렬에서 index k-1에 위치
    
    내림차순 정렬에서 idx 0은 그보다 큰 원소가 0개, idx n-1은 그보다 큰 원소가 n-1개 
    
    → index k-1: 내림차순 정렬 기준으로 그보다 큰 값이 앞에 k-1개 있다는 뜻 
    
    따라서 partition sort 후 pivot의 새로운 위치가 k-1이면 우리가 구하고자 하는 k번째로 큰 값임 
    
    - binary search 에서 new_pivot_idx가 k-1보다 작은 경우
        
        → pivot보다 큰 값이 충분히 많지 않다는 뜻. pivot을 더 작게 만들어야 함 
        
        → 현재 pivot보다 작은 값들은 new_pivot_idx 기준으로 오른쪽에 존재 
        
        → left idx를 오른쪽으로 밀어야 함 
        
    - 반대 경우
        
        → pivot 값이 너무 작아서 그보다 큰 값이 앞에 너무 많다는 뜻
        
        → pivot 값을 키워야 함. 현재 Pivot보다 큰 값들은 모두 new_pivot_idx 보다 왼쪽에 있음
        
        → right index를 당겨서 pivot_index가 새롭게 뽑힐 위치를 왼쪽으로 당겨와야 함 
        
    - 모르겠는 점
        - partition sort에서 언제 swap해야 하는지
    - 코드
        
        ```python
        import random
        class Solution:
            def findKthLargest(self, nums: List[int], k: int) -> int:
                # partition sort 
                def partition_sort(left, right, pivot_idx):
                    new_pivot_idx = left
                    pivot_value = nums[pivot_idx]
                    nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
                    for i in range(left, right):
                        if nums[i] > pivot_value: # 큰 값이 더 앞으로 가야 함 
                            nums[i], nums[new_pivot_idx] = nums[new_pivot_idx], nums[i]
                            new_pivot_idx += 1 
                    nums[right], nums[new_pivot_idx] = nums[new_pivot_idx], nums[right]
                    return new_pivot_idx
        
                left, right = 0, len(nums)-1
                while left <= right:
                    pivot_idx = random.randint(left, right)
                    new_pivot_idx = partition_sort(left, right, pivot_idx)
                    if new_pivot_idx == k-1:
                        return nums[new_pivot_idx]
                    elif new_pivot_idx < k-1: 
                        left = new_pivot_idx + 1 
                    else: 
                        right = new_pivot_idx -1 
                
        
                
        ```
        
- [x]  heap 써서 sorting 없이 풀어보기