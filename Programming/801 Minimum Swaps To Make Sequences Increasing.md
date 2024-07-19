# 801. Minimum Swaps To Make Sequences Increasing

Created time: May 19, 2024 9:42 PM
Last edited time: May 19, 2024 10:49 PM

- 문제 이해
    - 한번의 operation에서 같은 위치에 있는 두 원소를 맞교환할 수 있음
    - nums1, nums2가 모두 증가하는 원소로만 구성되도록 하기 위해서는 몇 번을 교환해야 하는지
- scratch
    
    1 3 5 5 → 마지막 원소가 strictly increasing 하지 않는다는 의미 
    
    1 2 3 7은 가능
    
    0 3 5 8 9
    
    2 2   6 9
    
    array 길이가 10**5인 걸로 봐서 binary search를 써야 할 것 같음 
    
    전혀 감이 오지 않는다 
    
    0 7 8 10 10 11 12 13 19 19 
    
    4 4 5 7 11 14 15 16 17 20 
    
    0 7 8 7 10 11 12 13 17 19
    
    4 4 5 10 11 14 15 16 17 20 
    
    4 7 8 7 10 11 12 13 17 19
    
    0 4 5 10 11 14 15 16 17 20 
    
    4 7 8 7 10 11 12 13 17 19
    
    0 4 5 10 11 14 15 16 17 20 
    
- Editorial
    - swap[n]: n번째 요소가 교환된 상태에서 A와 B 배열을 증가하는 순서로 만들기 위한 최소 교환 횟수
    - not_swap[n]: n번째 요소가 교환되지 않은 상태에서 A와 B 배열을 증가하는 순서로 만들기 위한 최소 교환 횟수
    - `A[i - 1] < A[i] && B[i - 1] < B[i]`
        - 선택1: i-1, i 둘 다 swap 하지 않음
            
            → not_swap[i] = not_swap[i-1]
            
        - 선택2: i-1, i 모두 스왑
            - 이런 경우도 있을 수 있기 때문에
                - A = [1,3,4,9,6], B = [1,2,3,5,10] ==> Here, 9 > 4 && 5 > 3 but we need to swap 9 and 5 to help achieve the result. And in many other cases to minimize the swaps.
            
            → swap[i] = swap[i-1] + 1 
            
    - `A[i-1] < B[i] && B[i-1] < A[i]`
        - 선택1: i-1번 원소끼리 swap, i에서는 swap 안함
            
            → not_swap[i] = min(swap[i-1], not_swap[i])
            
        - 선택2: i번 원소끼리 swap, i-1에서는 안함
            
            → swap[i] = min(not_swap[i-1] + 1, swap[i])
            
        - 왜 여기서 min이 필요하지? 그냥 등호로 넣으면 안되나?
    
- Trial
    - 예제1개
        
        ```python
        class Solution:
            def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
                n = len(nums1)
                swap = [n] * n
                not_swap = [n] * n 
        
                # base case
                # 원소 하나만 있어서는 모두 valid case
                swap[0] = 1 
                not_swap[0] = 0
        
                # recurrence relation
                for i in range(1, n):
                    if nums1[i-1] < nums1[i] and nums2[i-1] < nums2[i]:
                        not_swap[i] = not_swap[i-1] # no swap both 
                        swap[i] = swap[i-1] + 1 # swap both 
                    if nums1[i-1] < nums2[i] and nums2[i-1] < nums1[i]:
                        not_swap[i] = min(swap[i-1], not_swap[i]) # swap i-1th only 
                        swap[i] = min(not_swap[i-1] + 1, swap[i]) # swap i th only 
                print(swap)
                print(not_swap)
                return min(swap[-1], not_swap[-1])
        
        ```
        
- AC 코드
    
    ```python
    class Solution:
        def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
            n = len(nums1)
            swap = [n] * n
            not_swap = [n] * n 
    
            # base case
            # 원소 하나만 있어서는 모두 valid case
            swap[0] = 1 
            not_swap[0] = 0
    
            # recurrence relation
            for i in range(1, n):
                if nums1[i-1] < nums1[i] and nums2[i-1] < nums2[i]:
                    not_swap[i] = not_swap[i-1] # no swap both 
                    swap[i] = swap[i-1] + 1 # swap both 
                if nums1[i-1] < nums2[i] and nums2[i-1] < nums1[i]:
                    not_swap[i] = min(swap[i-1], not_swap[i]) # swap i-1th only 
                    swap[i] = min(not_swap[i-1] + 1, swap[i]) # swap i th only 
            return min(swap[-1], not_swap[-1])
    
    ```
    
    - if랑 elif가 아니라 하나의 index에 대해 둘다 if다
        - 두 조건을 모두 만족하는 경우가 있기 때문
        - 그래서 두번째 조건에서는 min(기존값) 부분이 추가되는 것
    - dp array 초기화 할 때 cell value는 float(’inf’)로 하면 안된다
        - 왜냐면 원소 수 이상을 바꿀 수는 없으니까?
        - 근데 의문은 남는다. 바꾸다보면 원소 수 이상으로 바꾸게 되는 경우는 없으려나?
            - The test cases are generated so that the given input always makes it possible.
            - 없다 왜냐면 같은 array에서 앞뒤로 바뀌는 경우는 없기 때문
            - 위아래로 바꾼 걸 또 바꾸면 원래 자리로 돌아올 뿐.