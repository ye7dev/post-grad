# 321. Create Maximum Number (re)

Status: done, in progress, revisited
Theme: DP
Created time: November 22, 2023 5:15 PM
Last edited time: November 22, 2023 10:21 PM

multidimensional hard

잘해쪙! 🪇

- 과정
    
    [[**321. Create Maximum Number**](https://leetcode.com/problems/create-maximum-number/description/?envType=list&envId=pri9k1mv)](321%20Create%20Maximum%20Number%207b4e7a310c6540a2a84af35be213cb72.md) 풀어봤던 문젠데 기억이 잘 안난다;;
    
    k가 크면 어쨌든 이번 리스트 원소를 다 쓰고, 그리고 나서도 다른 list원소를 가져다 써야 하고
    
    k가 작으면 이번 list 원소가 충분히 크지 않다 싶으면 제끼고 다음 걸 고려하는 사치를 부려도 됨 
    
    stack을 사용했던 기억이 난다 
    
    그리고 한번 전진한 이상 다시 앞으로 가는 일은 없다 
    
    merge를 활용했던 기억이 난다. 기억 났다. 크기가 다를 때는 더 큰 쪽을 넣으면 되고, 같을 때가 문제인데, 처음으로 다른게 나올때까지 앞으로 돌아가야 했던…?
    
    p = i-1 아닌가 trapping water 같은 문제였나…
    
    아 기억났다 각 list의 maximum number를 모든 숫자를 사용해서 만든 다음, merge를 한다. k만큼
    
    sub문제가 두 개였던 것으로 기억 
    
    더 기억이 난다 i, k-i개의 max number를 각각 만들어서 merge 그리고 전체 for loop에 대해서 원소 가장 큰것들이 앞에 나오면 그게 정답 장하다 내머리
    
    ---
    
    i를 nums1, k-i를 nums2에 부여할 거고, (max_number_list를 만들라고), len(nums1) = m, len(nums2) = n이라고 하면
    
    → i ≤ m. k-i ≤ n → k-n ≤ i ≤ m
    
    i가 m을 넘지 않으면 되는거지. 꼭 i가 m에서 시작할 이유가 없음 
    
- 코드
    
    복기 잘해서 결국 풀었지만 merge에서 좀 시행착오 있었음
    
    ```python
    class Solution:
        def maxNumber(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
            def make_max_number(n, arr):
                stack = []
                for i in range(len(arr)):
                    num_not_checked = len(arr)-i-1 # 바로 아래 while 문에서 비교 예정이라 i 자신은 제외
                    while stack and stack[-1] < arr[i] and num_not_checked >= n-len(stack):
                        stack.pop()
                    if len(stack) < n:
                        stack.append(arr[i])
                return stack 
    
            def merge_two_nums(arr1, arr2):
                n1, n2 = len(arr1), len(arr2)
                i, j = 0, 0
                res = []
                while i < n1 and j < n2:
                    if arr1[i] < arr2[j]:
                        res.append(arr2[j])
                        j += 1 
                    elif arr1[i] > arr2[j]:
                        res.append(arr1[i])
                        i += 1 
                    else:
                        new_i, new_j = i, j
                        while new_i < n1 and new_j < n2 and arr1[new_i] == arr2[new_j]:
                            new_i += 1
                            new_j += 1 
                        if new_i == n1: 
                            res.append(arr2[j])
                            j += 1
                        elif new_j == n2:
                            res.append(arr1[i])
                            i += 1
                        elif arr1[new_i] < arr2[new_j]:
                            res.append(arr2[j])
                            j += 1
                        elif arr1[new_i] > arr2[new_j]:
                            res.append(arr1[i])
                            i += 1 
                             
                if i < n1:
                    res += arr1[i:]
                if j < n2:
                    res += arr2[j:]
                return res 
    
            m, n = len(nums1), len(nums2)
            res = [-1] * k
            for i in range(max(0, k-n), m+1): # i가 0이면 
                first = make_max_number(i, nums1)
                second = make_max_number(k-i, nums2)
                temp = merge_two_nums(first, second)
                idx = 0
                while idx < k:
                    if res[idx] < temp[idx]:
                        res = temp
                        break 
                    elif res[idx] > temp[idx]:
                        break 
                    else:
                        idx += 1 
            return res
    ```