# 75. Sort Colors

Status: done, in progress, with help, 👀1
Theme: sort
Created time: December 4, 2023 11:55 AM
Last edited time: December 5, 2023 12:46 PM

- [ ]  다시 짜보기
- [x]  다시 짜보기
- QuickSort 연습 문제
- 처음에 내가 짠 코드
    
    ```python
    class Solution:
        def sortColors(self, nums: List[int]) -> None:
            def quickSort(arr):
                if len(arr) == 0 or len(arr) == 1:
                    return arr 
                pivot = arr[0]
                smaller, larger = [], []
                for n in arr:
                    if n < pivot:
                        smaller.append(n)
                    else:
                        larger.append(n)
                return quickSort(smaller) + quickSort(larger)
            
            return quickSort(nums)
    ```
    
    → maximum recursion depth error 
    
    - 무엇을 잘못하였나
        - sublist 생성 시에 별도의 list를 따로 생성하지 않고 index로 움직였어야 함
        - pivot 자체는 양쪽 sublist 어느 쪽에도 포함되지 않음
- Editorial 코드
    
    ```python
    class Solution:
        def sortColors(self, nums: List[int]) -> None:
            n = len(nums)
            def quickSort(low, high):
                if low < high:
                    p = partition(low, high)
                    # partition이 끝나고 나면 pivot을 중심으로 
                    # 작은 값과 큰 값이 divide 된 상태 
    
                    # p는 중심을 지키고 그 앞과 뒤를 conquer
                    quickSort(low, p-1)
                    quickSort(p+1, high)
    
            def partition(low, high):
                pivot = nums[high]
                i = low 
                for j in range(low, high):
                    if nums[j] < pivot:
                        # 작다고 확실히 밝혀진 원소를 더 앞으로 보냄 
                        nums[i], nums[j] = nums[j], nums[i]
                        # 기존 i 자리에는 확실히 더 작은 원소가 들어갔으므로
                        # 또 확실히 작은 원소가 나타났을 때 들어오게 되는 자리는
                        # 바로 다음 자리. i+1 
                        i += 1 
                # i-1까지는 모두 pivot보다 작은 원소라는 게 확실
                # i번째로 작은 원소는 무조건 pivot
                # 맨 오른쪽에 있던 pivot을 중간(적절한 자리)로 옮긴다 
                nums[i], nums[high] = nums[high], nums[i]
                # pivot의 위치를 return 
                return i 
            
            return quickSort(0, n-1)
    ```
    
- 다시 풀 때 막혔던 점
    - RecursionError: maximum recursion depth exceeded in comparison
        - recursive function에서 base case를 제대로 설정하지 않은 경우에 주로 발생
        - low가 high보다 크거나 같으면 return 하는 것이 base case
            
            → 더 깔끔한 코드로는 if low < high로 조건문 통과할 때만 실행하도록 하는 것
            
    - partition에서 return 하는 대상은 pivot 자체가 아니라 pivot이 위치한 인덱스, i임