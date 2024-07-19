# 1130. Minimum Cost Tree From Leaf Values

Created time: June 11, 2024 1:27 PM
Last edited time: June 12, 2024 10:19 PM

- scratch
    - root 노드 값은 정해져있음
    - 6 → *2, *4
        
        2 → *4 
        
        12, 24, 8 
        
    - inorder : 왼→ 현→ 오
        
        6, 12, 2, 24, 4
        
        6, 24, 2, 8, 4 
        
    - recursive로 짠다고 하면…
        
        inorder는 보통 
        
        inorder(left)
        
        current node job
        
        inorder(right)
        
        이런 식으로 진행 
        
    - 자식이 2명이거나 없거나니까
        
        ![Untitled](Untitled%2073.png)
        
        - 6,2를 자식으로 하는 노드가 있고, 4는 부모노드가 바로 루트 노드. root가 아닌 non-leaf가 없는 것
        - 어쨌든 root는 무조건 들어가니까 제일 앞, 뒤 곱한 값이 더해지고
    - a b c d라고 하면
        - a, b가 하나의 노드의 자식
        - c, d가 하나의 노드의 자식
        - a, bc, d로 할 수 있나?
            - 할 수 있다
            - a랑 bc의 부모가 한 노드로 묶이고, d가 root에 바로 연결
            - 아님 a가 root에 바로 연결, bc가 한 노드로 묶이고 그 노드가 d랑 다시 한 노드로 묶여서 그 노드가 root에 연결
            - root
            - parent    d
            - a    son
            
                        b   c
            
            - non-leaf node
                - son = b * c
                - parent = a * max(b, c)
                - root = max(a, b, c) * d
    - 묶기 문제네 결국
        - a, b, c, d
        - 묶기1
            - a, b*c, d → b*c 값을 답으로 더하면서, max(b, c) 중 하나를 남긴다
            - a, b, d → a*b 값을 답에 더하면서 max(a, b) 중 하나를 남긴다
            - a, d → a*d 값을 답에 더하면서 끝낸다
        - 묶기2
            - a, b, c, d→ a*b 값을 답으로 더하면서 max(a,b) 중 하나를 남긴다
            - a, c, d → c*d 값을 답으로 더하면서 max(b, c) 중 하나를 남긴다
            - a, c → a*c 값을 답으로 더하면서 끝낸다
        - a 입장에서는 b랑 묶어서 하나의 답을 남기던가, 아니면 a는 그대로 남겨 두던가 두 가지 선택이 있음
        - a recur(b, c) d
        - recur(a, b) recur(c, d)
    - `2 <= arr.length <= 40`
- Trial
    - recursive
        
        ```python
        class Solution:
            def mctFromLeafValues(self, arr: List[int]) -> int:
                def recur(subarr, cumsum):
                    # base case
                    if len(subarr) == 1:
                        return subarr[0], cumsum
                    if len(subarr) == 2:
                        return max(subarr), cumsum + subarr[0]*subarr[1]
                    # recursive case
                    skip_last, skip_sum = recur(subarr[1:], cumsum)
                    skip = skip_sum + (subarr[0] * skip_last)
                    take_last, take = recur(subarr[2:], cumsum + subarr[0]*subarr[1])
                    return max(subarr), min(skip, take)
                
                return recur(arr, 0)[1]
        ```
        
    - greedy (15/103)
        
        ```python
        class Solution:
            def mctFromLeafValues(self, arr: List[int]) -> int:
                cost = 0
                while len(arr) > 1:
                    min_val = min(arr)
                    min_idx = arr.index(min_val)
                    if min_idx == 0:
                        left_smallest = float('inf')
                    else:
                        left_smallest = min(arr[:min_idx])
                    if min_idx == len(arr)-1:
                        right_smallest = float('inf')
                    else:     
                        right_smallest = min(arr[min_idx+1:])
                    min_neighbor = min(left_smallest, right_smallest)
                    cost += min_val * min_neighbor
                    arr = arr[:min_idx] + arr[min_idx+1:]
                return cost
                    
                
        ```
        
    - monotonic stack(41/103)
        
        ```python
        class Solution:
            def mctFromLeafValues(self, arr: List[int]) -> int:
                cost = 0
                def get_next_larger_element(nums):
                    res = [-1] * len(nums)
                    stack = []
        
                    for i, num in enumerate(nums):
                        while stack and nums[stack[-1]] < num:
                            idx = stack.pop()
                            res[idx] = num # nums[idx]'s next smaller is num 
                        stack.append(i)
                    return res
        
                # get next smaller element in order
                in_order_res= get_next_larger_element(arr)
                # get next smaller element in reverse order
                reverse_res = get_next_larger_element(arr[::-1])[::-1]
        
                for i in range(len(arr)):
                    right_larger = float('inf') if in_order_res[i] == -1 else in_order_res[i]
                    left_larger = float('inf') if reverse_res[i] == -1 else reverse_res[i]
                    next_smaller = min(right_larger, left_larger)
                    if next_smaller == float('inf'):
                        continue
                    cost += arr[i] * next_smaller
        
                return cost
        ```
        
- AC 코드
    - greedy, O(N**2)
        
        ```python
        class Solution:
            def mctFromLeafValues(self, arr: List[int]) -> int:
                cost = 0
                while len(arr) > 1:
                    min_val = min(arr)
                    min_idx = arr.index(min_val)
                    if min_idx == 0: # no left
                        min_neighbor = arr[min_idx+1]
                    elif min_idx == len(arr)-1: # no right
                        min_neighbor = arr[min_idx-1]
                    else:
                        min_neighbor = min(arr[min_idx-1], arr[min_idx+1])
                    cost += min_val * min_neighbor
                    arr = arr[:min_idx] + arr[min_idx+1:]
                return cost
        ```
        
    - Monotonic stack, O(N)
        
        ```python
        class Solution:
        	    def mctFromLeafValues(self, arr: List[int]) -> int:
                stack = [float('inf')]
                res = 0
                for num in arr:
                    while stack and stack[-1] <= num:
                        cur = stack.pop()
                        # cur의 first bigger element on the right side가 num
                        # cur의 first bigger element on the left side가 stack[-1]
                        res += cur * min(stack[-1], num)
                    
                    # stack[-1]은 num의 first bigger element on the left side
                    stack.append(num)
                
                # 더 이상 right side로는 더 큰 원소가 없음
                # first bigger element on the left side만 존재
                # monotonic decreasing stack
                # stack[0]은 늘 float('inf')이기 때문에 len(stack) <= 2면
                # 사실상 원소가 하나 남거나 없는 거라 종료하는 게 맞음 
                while len(stack) > 2:
                    res += stack.pop() * stack[-1]
                return res
        ```
        
- Solution
    - lee215
        - dp 방식
            - 구간 [i, j](j도 포함인가봄)에 대한 cost 찾기
            - leftsubtree와 rightsubtree로 쪼개기
                - `dp[i, j] = dp[i, k] + dp[k+1, j], max(A[i, k]) * max(A[k+1, j])`
        - 사실은 dp 문제가 아님. brute force with memo
            - dp solution으로 풀려면 필요 없는 tree들을 많이 만들어야 해서 비효율 (정확히 저번 시험 때 내가 한 것…)
        - tree에서 하나의 노드를 만들기 위해서는 숫자 a와 b를 비교해야 함
            - 더 작은 숫자는 더 이상 사용될 일이 없으므로 제거. 큰 숫자만 남는다
        - 문제 재정의
            - 주어진 array에 대해 array a와 b에서 두 개의 neighbor를 선택해라
            - 이 중 더 작은 것을 제거하는 비용은 a*b일 때, 원소가 하나만 남을 때까지 다른 모든 원소를 없애는 최소 비용은 얼마인가?
        - 더 작은 원소가 늘 a라고 하면 a의 제거 비용은 a*?
            - 여기서 a에 곱해지는 ?는 a보다 큰 수 이면서 작을 수록 비용이 작게 나올 것
            - ?의 후보는 왼쪽에서 a보다 처음으로 큰 숫자, 오른쪽에서 처음으로 큰 숫자
                - [ ]  왜 처음으로 만나는 큰 숫자여야 하는가?
            - 결국 a를 제거하는 비용은 a * min(left, right)
    - [ASaltyFish](https://leetcode.com/u/ASaltyFish/)
        - inorder traversl에서는 pivot이 존재
            - 어떤 구간을 왼쪽 subtree와 오른쪽 subtree로 나누는 pivot
            - 각 subtree에 대해 min sum을 알고 있으면, parent tree의 결과를 만드는 데 사용할 수 있다
                
                ```sql
                for k from i to j
                    res(i, j) = min(res(i, k) + res(k + 1, j) + max(arr[i] ... arr[k]) * max(arr[k + 1] ... arr[j]))
                ```
                
                - parent tree의 결과는 왼쪽 오른쪽 subtree의 root 즉 non-leaf node의 합을 모두 포함하고 있어야 함. 왜냐면 sum of values of each non-leaf node
        - 가장 중요한 관찰: non-leaf node 하나를 만들 때, 그 노드의 왼쪽 subtree에서 가장 큰 leaf value와 오른쪽 subtree에서 가장 큰 leaf value를 곱한다는 것
        - 값이 큰 leaf node들은 root와 가까울 수록 유리
            - 그렇지 않으면 non-leaf node를 만들 때마다 사용돼서 총 비용을 증가시킬 것
        - array에서 가장 작은 값을 찾고, ~~그 이웃 중에 가장 작은 값~~ 양쪽 이웃 중에 더 작은 값을 찾아서 하나의 non-leaf node 만들고 난 뒤, 가장 작은 값을 array에서 삭제
        - monotonic stack
            
            ```python
            class Solution:
            	    def mctFromLeafValues(self, arr: List[int]) -> int:
                    stack = [float('inf')]
                    res = 0
                    for num in arr:
                        while stack and stack[-1] <= num:
                            cur = stack.pop()
                            # cur의 first bigger element on the right side가 num
                            # cur의 first bigger element on the left side가 stack[-1]
                            res += cur * min(stack[-1], num)
                        
                        # stack[-1]은 num의 first bigger element on the left side
                        stack.append(num)
                    
                    # 더 이상 right side로는 더 큰 원소가 없음
                    # first bigger element on the left side만 존재
                    # monotonic decreasing stack
                    # stack[0]은 늘 float('inf')이기 때문에 len(stack) <= 2면
                    # 사실상 원소가 하나 남거나 없는 거라 종료하는 게 맞음 
                    while len(stack) > 2:
                        res += stack.pop() * stack[-1]
                    return res
            ```
            
            - stack = […, next_top, old_top]
                - old_top > num 이면 그대로 num 추가.
                    - new_top은 num이 되고, stack = […, next_top, first left bigger(old_top), num]이 됨. remaining array에서 num보다 큰 첫번째 원소 즉, first right bigger(new_top)을 만날 때까지 기다리게 됨
                - old_top ≤ num 이면 old_top을 제거할 기회가 온 것!
                    - next_top은 old_top 보다 무조건 크다
                        - 왜냐면 old_top이 stack에 추가되려면 당시 top이었던 next_top보다 작은 숫자여야만 하니까
                        - monotonic decreasing stack이 되겠구만
                    - old_top의 입장에서 보면
                        - stack[-1]: 왼쪽 방향으로 가장 가까우면서 처음으로 값이 더 큰 원소
                        - num: 오른쪽 방향으로 가장 가까우면서 처음으로 값이 더 큰 원소
                    - 둘 중 더 작은 쪽이랑 곱해져서 비용에 더해져야 함
            - 요약
                - while stack and stack[-1] <= num
                    - 이 조건으로 num을 first bigger on the right side로 삼는 원소들을 모두 처리
                - stack에는 더 이상 num보다 작은 원소가 없게 된다
                    - num 넣기 직전 stack top은 num의 first bigger on the left임
                - stack에 num을 넣어주기
                    - num이 first bigger on the right 을 만날 수 있도록 대기 모드에 넣어둠
                    - num을 first bigger on the left로 삼는 원소들이 stack에 들어오는 것을 기다림
                - 이모티콘
                    
                    stack = [☁️3 2 1]🌈 
                    
                    - 1 ≤ 🌈
                        - pop → 1
                        - stack top: 2 = 1의 first bigger on the left side
                        - num = 1의 first bigger on the right side
                        
                        → cost += min(2, 🌈) * 1 
                        
                    - 2와 3에 대해서도 같이 하고 나면 stack = [☁️]🌈
                    - ☁️ > 🌈
                        - ☁️는 🌈의 first bigger on the left side
                    - stack에 🌈 추가 → stack = [☁️🌈]
                    - 다음 원소로 ☀️가 들어 왔다고 하면
                        - 🌈 ≤ ☀️ → ☀️는 🌈의 first bigger on the right side
                        - 🌈 양옆 기준으로 모두 bigger element가 들어왔기 때문에 🌈를 제거하고 비용 추가한 뒤 넘어간다
- 솔루션 최종 정리
    - 더 작은 원소가 늘 a라고 하면 a의 제거 비용은 a*?
        - 여기서 a에 곱해지는 ?는 a보다 큰 수 이면서 값이 작을 수록 비용이 작게 나올 것
    - full binary tree(자식이 0/2개만 존재)에서 inorder traversal을 한 뒤 leaf node만 남긴 array
        - 인접한 두 원소끼리 형제 관계. left → parent → right니까
        - 하나만 남으면 root에 바로 연결된 leaf node
        - 예) [6, 2, 4]
            - 6,2가 하나의 부모를 둔 형제 관계이고, 4가 root의 childless 자식이거나
            - 2, 4가 하나의 부모를 둔 형제 관계이고, 6이 root의 childless 자식이거나
    - array에서 가장 작은 값을 찾고, 양쪽 이웃 중에 더 작은 값을 찾아서 하나의 non-leaf node 만들고 난 뒤, 가장 작은 값을 array에서 삭제
        - 하나 더 윗 level의 할아버지 노드를 구할 때도 아버지 노드로 들어오고 나면 가장 큰 leaf node 값은 이웃 중에 하나지 가장 작은 값이 아니기 때문에 필요 없어서
    - greedy에서 반복되는 연산: 전 단계에서 최소 값을 삭제하고, 다시 이번 단계에서 최소 값을 찾는 것
    - 시간을 더 줄일 수 있는 관찰 요소
        - 최소값을 삭제해나가면서 어떤 원소가 남아 있는 array의 최소 값이라고 하면
        - 그 원소의 왼쪽, 오른쪽 이웃은 원래 input으로 들어온 array에서도 원소의 first bigger element on the left, first bigger element on the right임
        - 예) ☁️⛄️⛄️⛄️🌈⛄️⛄️☀️
            - 원래 array에서 눈사람은 모두 무지개보다 작은 값의 원소
            - 최소값을 삭제해나가기 때문에 무지개가 최소값이 되었을 시점에 눈사람은 이미 모두 사라졌을 것임
            - 무지개가 최소값이 되었을 시점의 array 상태: ☁️🌈☀️
                - 구름은 원래 array에서 무지개보다 왼쪽에 있는 first bigger element
                - 해도 원래 array에서 무지개보다 오른쪽에 있는 first bigger element