# 33. Search in Rotated Sorted Array

Status: done, in progress
Theme: Binary Search
Created time: November 3, 2023 5:17 PM
Last edited time: November 9, 2023 5:14 PM

- 문제 이해
    - target은 k가 아니고, k를 return 필요는 없음
    - 값이 갑자기 감소하는 부분을 찾고, 그 부분을 기준으로 반을 나눠서 target을 각각 탐색하거나
    - 감소하는 부분을 찾고 다시 오름차순으로 만들어서 target을 탐색하거나
- 나의 최선
    - 그래도 예제는 통과했다 장하다
    
    ```python
    class Solution:
        def search(self, nums: List[int], target: int) -> int:
            def bs(arr, start):
                left, right = 0, len(arr)-1
                # base case
                while left <= right:
                    mid = (left + right) // 2
                    if arr[mid] == target:
                        return mid + start
                    if arr[mid] < target:
                        left = mid + 1
                    else:
                        right = mid -1
                return -1 
            
            # base case
            if nums[0] < nums[len(nums)-1]:
                return bs(nums, 0)
    
            left, right = 0, len(nums)-1
            while nums[right] < nums[left]:
                mid = (left + right) // 2
                if nums[mid] == target:
                    return mid
                if nums[right] < nums[mid] < nums[left]:
                    if target > nums[mid]:
                        if target >= nums[left]:     
                            right = mid-1
                        else:
                            left = mid + 1 
                    else:
                        right = mid -1 
                elif nums[left] < nums[mid]:
                    if target > nums[mid]:
                        return -1
                    else:
                        if target >= nums[left]:
                            right = mid -1 
                        else:
                            left = mid + 1
                elif nums[mid] < nums[right]:
                    if target < nums[mid]:
                        right = mid - 1
                    else:
                        if target <= nums[right]:
                            left = mid + 1
                        else:
                            right = mid -1  
                    
            return bs(nums[left:right+1], left)
    ```
    
- 헷갈리는 점-어째서 main branch condition이 nums[left] ≤ nums[mid] 하나
    - rotation point: index of smallest element in the array
    - nums[left] ≤ nums[mid]
        1. rotation 없이 주어진 array가 그대로 오름차순인 경우 
            - target > nums[mid] 인 경우: 일반적인 bs로 right part를 봐야
        2. 우리가 non-rotated part를 보고 있는 경우 ([4, 5, 6, 7, 0, 1, 2])
            - target < nums[left]인 경우: rotated인 right part를 봐야
        
        ⇒ nums[left] ≤ target < nums[mid] 이면 일반적인 bs 
        
        ⇒ 아니면 the other half of the array를 탐색해야 → left = mid +1 
        
    - nums[left] > nums[mid]
        - rotation이 무조건 일어난 상황이고, mid가 rotated subarray의 일부 ([6, 7, 0, 1, 2, 4, 5])
            - target < nums[mid]: rotated 내부에 있을 테니 left part 봐야
            - target > nums[right]: 역시 rotated 내부에 있을테니 left part 봐야
        - 가장 작은 element가 mid나 mid의 왼쪽에 있을 것 = mid부터 right까지는 오름차순으로 정렬된 상태
        
        ⇒ nums[mid] < target ≤ nums[right] 이면 일반적인 bs 
        
        ⇒ 아니면 the other half of the array 탐색 → right = mid-1
        
- 구현 시 주의 사항
    - left = mid인 경우도 있으니 main branch condition에 꼭 등호를 넣어야 한다
- chat 선생님 답안
    - # Determine which side is normally ordered
    - Target이 구간 안에 있는 경우와 아닌 경우 두 개만 신경씀
    - 두 구간이 모두 멀쩡할 경우 앞구간부터 봄
        - Target이 뒷구간에 있더라도 내부 조건문에 의해 low가 mid 뒤로 옮겨지면서 자연스럽게 뒷 구간으로 탐색 범위가 이동
        
        ```python
        def search(nums, target):
            if not nums:
                return -1
        
            low, high = 0, len(nums) - 1
        
            while low <= high:
                mid = (low + high) // 2
                if target == nums[mid]:
                    return mid
        
                # Determine which side is normally ordered
                if nums[low] <= nums[mid]:
                    # The left side is normally ordered
                    if nums[low] <= target < nums[mid]:  # Target is in the left half
                        high = mid - 1
                    else:  # Target is in the right half
                        low = mid + 1 # target이 low보다 작거나 mid보다 큰 경우 중 앞에 것은 어차피 해가 없으므로 신경 안쓰는듯
        
                else:
                    # The right side is normally ordered
                    if nums[mid] < target <= nums[high]:  # Target is in the right half
                        low = mid + 1
                    else:  # Target is in the left half
                        high = mid - 1 # mid보다 target이 작은 경우만 고려? # high보다 큰 경우는?  
        
            return -1  # Target is not found
        
        # Example usage:
        nums = [4,5,6,7,0,1,2]
        target = 6
        print(search(nums, target))  # Output: 2
        ```