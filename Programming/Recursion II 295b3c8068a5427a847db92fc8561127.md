# Recursion II

Status: algorithm
Theme: recursive
Created time: December 1, 2023 11:10 AM
Last edited time: December 6, 2023 3:11 PM

# Divide and Conquer

- Introduction
    - 그 문제를 직접 해결할 수 있을 때까지 문제를 한번에 두 개씩 혹은 그 이상으로 작게 쪼갬 → 모든 subproblem 결과를 합쳐서 return
    - 문제를 쪼갠다 = 더 작은 argument를 넣어서 재귀콜
- Merge Sort $O(NlogN)$
    - merge sort fm 코드
        
        ```python
        def merge_sort(nums):
            # conquer
            if len(nums) <= 1:
                return nums
        		# divide
            pivot = int(len(nums) / 2)
            left_list = merge_sort(nums[0:pivot])
            right_list = merge_sort(nums[pivot:])
        		# combine
            return merge(left_list, right_list)
        
        def merge(left_list, right_list):
        		# combine 
            left_cursor = right_cursor = 0
            ret = []
            while left_cursor < len(left_list) and right_cursor < len(right_list):
                if left_list[left_cursor] < right_list[right_cursor]:
                    ret.append(left_list[left_cursor])
                    left_cursor += 1
                else:
                    ret.append(right_list[right_cursor])
                    right_cursor += 1
            ret.extend(right_list[right_cursor:])
            
            return ret
        ```
        
    - top-down
        
        (divide) 주어진 unsorted list를 여러 개의 부분 list로 나눈다 
        
        (conquer) 각 sublist를 정렬한다 - 재귀적으로 
        
        ↳ 재귀로 sublist 범위를 좁혀 들어가다가 base case 도달 
        
        ↳ base case: 원소가 없거나 하나만 있는 list (아래 그림에서 파란색 사각형)
        
        (combine) 정렬된 sublist를 합쳐서 새로운 sorted list로 만든다 
        
        ↳ O(N)으로 수행되는 task 
        
        - 이미지
            
            ![Untitled](Untitled%2025.png)
            
    - bottom-up
        - 솔직히 뭐가 다른지 모르겠음. 어쨌든 모든 list를 원소가 하나 남을 때까지 쪼갠다 → 하나 남은 원소는 이미 정렬된 상태 → 한번에 두 sublist 씩 합쳐서 최종적으로 하나의 list만 남긴다
        - 그림
            
            ![Untitled](Untitled%2026.png)
            
    - complexity
        - 각 원소를 하나의 sublist로 만드는 데 O(N) 필요
        - 위의 그림에서 보면 recursion tree 높이가 `log N`
            - 각 tree 높이에서 N개의 원소 비교해야 하니까
        
        ⇒ O(NlogN) 
        
- Template
    
    ```python
    def divide_and_conquer( S ):
        # (1). Divide the problem into a set of subproblems.
        [S1, S2, ... Sn] = divide(S)
    
        # (2). Solve the subproblem recursively,
        #   obtain the results of subproblems as [R1, R2... Rn].
        rets = [divide_and_conquer(Si) for Si in [S1, S2, ... Sn]]
        [R1, R2,... Rn] = rets
    
        # (3). combine the results from the subproblems.
        #   and return the combined result.
        return combine([R1, R2,... Rn])
    ```
    
    - Search 2D matrix code
        
        ```python
        class Solution:
            def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
                m, n = len(matrix), len(matrix[0])
                def check_submatrix(up, down, left, right):
                    # conquer
                    if up > down or left > right: return False 
                    smallest, largest = matrix[up][left], matrix[down][right]
                    if target < smallest or target > largest: return False
                    # divide
                    mid = left + (right-left) // 2 
                    row = up
                    while row <= down and matrix[row][mid] <= target:
                        if matrix[row][mid] == target:
                            return True 
                        row += 1 
                    # combine
                    if check_submatrix(up, row-1, mid+1, right) or check_submatrix(row, down, left, mid-1):
                        return True 
                    return False
                return check_submatrix(0, m-1, 0, n-1)
        ```
        
- Quick Sort $O(NlogN)$
    - template에 맞춘 설명
        - D**ividing the problem**
            - `partitioning`
                - pivot 선택 - 이걸 경계로 두 개의 sublist를 쪼갬
                    - 선택 전략 다양하지만 보통은 가장 첫번째 원소나 랜덤으로 선택
                - sublist 하나는 pivot 보다 값이 작은 모든 value를 포함
                - 다른 하나는 pivot과 같거나 그보다 큰 모든 value를 포함
        - S**olving the subproblems (conquer)**
            - 재귀적으로 두 개의 sublist를 sort
            - base case
                - input list가 비어 있거나 하나의 원소만 포함하는 경우 그대로 return
        - C**ombining the results of subproblems**
            - partitioning process가 끝나면 한쪽의 sublist가 포함하는 모든 원소들이 다른 쪽이 포함하는 모든 원소보다 작거나 같다는 것을 알 수 있음
            - sort된 두 개의 sublist를 단순히 붙이기만 해도 최종 sorted list를 얻을 수 있음
    - FM code
        
        ```python
        class Solution:
            def sortColors(self, nums: List[int]) -> None:
                n = len(nums)
                def quickSort(low, high):
                    if low < high:
                        p = partition(low, high)
                     
                        quickSort(low, p-1)
                        quickSort(p+1, high)
        
                def partition(low, high):
                    pivot = nums[high]
                    i = low 
                    for j in range(low, high):
                        if nums[j] < pivot:            
                            nums[i], nums[j] = nums[j], nums[i]
                            i += 1 
                                     
                    nums[i], nums[high] = nums[high], nums[i]
                    return i 
                
                return quickSort(0, n-1)
        ```
        
- Master Theorem (🏋️‍♀️)
    - 다양한(그러나 한정된) 재귀 알고리즘의 시간 복잡도 계산에 사용되는 방법
    
    ```python
    def dac(n):
    	if n < k: # k: some constant
    		Solve 'n' directly without recursion
    	else:
    			[1]. problem 'n'을 서로 같은 사이즈들의 subproblems 'b'개로 나눈다
    						-> 각 subproblem의 크기는 'n/b'
    			[2]. subproblem에 대해 함수 'dac()'를 재귀적으로 "a"번 호출
    			[3]. subproblem으로부터 얻은 결과를 합친다 
    ```
    
    - 위의 recursion 알고리즘에 대한 시간 복잡도를 $T(n)$이라고 하면,
        
        $$
        T(n) = a \cdot T(\scriptsize{n\over b}\small) + f(n)
        $$
        
        ↳ f(n): 문제를 n개의 subproblem으로 쪼갰다가 거기서 얻은 결과를 합치는 데 드는 시간 복잡도 
        
        ↳ $O(n^d), d\geq0$ 로 표현 가능 
        
        ↳ 우리는 문제를 b개로 나누기 때문에 $O(b^d)$
        
    - Master Theorem
        - a, b, d 간의 관계에 따라 아래의 세 가지가 될 수 있음
        - $a > b^d$ → $T(n) = O(n^{log_{b}a})$
            - 함수 호출한 횟수가 쪼갰다가 합치는 시간복잡도?보다 큰 경우 (conquer > divide)
            - 왼쪽 부등식에 log b를 취하면 $log_b{a} > d$
            - 더 큰 수에 비례하기 때문에 $T(n) = O(n^{log_{b}a})$
                - [ ]  왜 지수의 밑이 n인지는 모르겠음
        - $a = b^d$ → $T(n) = O(n^{log_{b}a}*log \ n)$
        - $a < b^d$ → $T(n) = O(n^d)$
            - $log_{b} \ a < d$
    - 예시
        - binary tree traversal → DFS
            - b: 2 ← problem divided into halves
            - a: 2 ← both subproblems needed to be solved
            - f(n) = O(1) → d = 0
                - DFS에서 문제를 쪼개는데 드는 노력은 constant-왜냐면 input 자체가 이미 collections of subproblems(children subtrees)
                    - left, right로 이미 가지치기 되어 있으니까 따라 가기만 하면 되어서
                - 각 recursion call에서 결과를 합치는데 드는 노력도 상수
                    - 왜냐면 maximum depth라고 하면 비교 한번만 하면 되니까
            
            ⇒ d = 0 < log_b_a = 1 → $T(n) = O(n^{log_ba}) = O(n^1) = O(n)$
            
            - 실제로 DFS 재귀 알고리즘의 시간 복잡도는 O(n)-왜냐면 tree의 각 node를 하나씩 방문하면 되니까
        - binary search
            - b: 2 (problem divided into halves)
            - a: 1 (only one of the subproblems needed to be solved)
                - 만약에 target이 mid보다 작다고 하면, right를 mid-1로 옮기면서 mid부터 원래 right까지는 모두 탐색 범위에서 제외되기 때문
            - f(n) = O(1) → d= 0
                - 주어진 input은 이미 정렬된 상태 → index만으로 원하는 범위로 좁힐 수 있음 → 문제를 쪼개는 노력은 상수
                - 문제를 합칠 필요가 사실상 없고 같은 값이 탐색 범위 안에 있으면 index만 return 하면 됨
            
            ⇒ a = 1  = b^d = 2^0 = 1  → $O(n^{log_{b}a}*log \ n)$ = $O(n^{log_21} * log \ n) = O(n^0*logn) = O(log \ n)$
            
            - 실제로 binary search 알고리즘의 시간 복잡도는 o(log n)
        - merge sort의 경우도 a == b^d의 case에 속함
        - quickselect 알고리즘
            - 정렬되지 않은 list에서 k번째로 큰/작은 원소를 찾는 알고리즘
            - 어떤 pivot을 정하고 그걸 기준으로 partition 해서 문제를 더 좁은 범위로 만듦
            - pivot이 input array의 median인 경우
                - b = 2 ← pivot 기준으로 더 큰 원소들, 더 작은 원소들끼리 모임
                - a = 1 ← 두 paritition 중에 하나만 보면 됨
                - d = 1 ← paritition 할 때마다 각 원소를 한번씩 pivot과 비교하면 되므로 $O(n)$
                
                ⇒ a = 1 vs. b^d = 2^1 = 2 → $T(n) = O(n^d) = O(n)$
                
    - 한계
        - subproblem들의 크기가 같을 때만 적용 가능
            - 피보나치 수열과 같은 재귀 알고리즘에는 적용하기 어려움
                - F(n) = F(n-1) + F(n-2). 두 subproblem의 크기가 서로 다름
            - 이런 경우는 Akra-Bazzi theorem을 사용하면 된다고 함

# Backtracking

- Introduction
    
    ![Untitled](Untitled%2027.png)
    
    - 점진적으로 solution에 대한 candidate들을 만들어나가는 과정에
    - 어떤 candidate이 조건을 만족하지 않는 것(invalid)으로 밝혀지면 바로 버려버리는 (backtrack) 방법
    - 주로 제약 만족 문제(CSP)들에 대한 solution인 경우가 많음
        - CSP 참고
            1. **변수(Variables)**: 값을 할당받아야 하는 요소들입니다. 예를 들어, 색칠 문제에서는 지도의 각 지역이 변수가 될 수 있습니다.
            2. **도메인(Domains)**: 각 변수에 할당될 수 있는 가능한 값들의 집합입니다. 예를 들어, 색칠 문제에서는 사용할 수 있는 색상의 집합이 됩니다.
            3. **제약 조건(Constraints)**: 변수들 간의 관계를 정의하는 규칙이나 제한입니다. 이들은 변수들이 취할 수 있는 값들을 제한합니다. 예를 들어, 색칠 문제에서 인접한 지역은 다른 색으로 칠해져야 한다는 것이 제약 조건이 될 수 있습니다.
    - tree traversal에 대한 비유
        - root node에서 시작 → leaf node에 위치한 solution을 찾아나섬
        - 각 intermediate node는 잠재적으로 final valid solution으로 이끌어주는 partial candidate solution으로 볼 수 있음
        - 각 node에서 우리는 final solution으로 한 step 더 움직임 = 현재 node의 child node들을 iterate
        - 어떤 특정한 current node가 valid solution으로 도달할 수 없다는 게 밝혀지자마자, current node를 버리고 바로 그의 parent node로 돌아가서 다른 가능성을 살펴본다
    - 필요없는 탐색을 줄여주기 때문에 brute-force search보다 더 빠르다
- 예시
    - 각 가지의 끝이 단어인 tree에서 주어진 단어가 tree에 포함되어 있는지 알아보기
        
        ![Untitled](Untitled%2028.png)
        
        - As we come across such node we **back-track**. That is go back to the previous node and take the next step.
            
            ![Untitled](Untitled%2029.png)
            
        - pruning the recursion tree
    - N-Queen puzzle
        - NxN 체스판에서 어떤 두 queen들끼리도 서로를 공격하지 못하도록 N개의 queen을 두는 문제
            - 어떤 queen이 공격할 수 있는 대상은 같은 row, 같은 col, 같은 대각선, 같은 anti-대각선에 있는 모든 말 (현재 cell을 중심으로 큰 x자 그려야)
        - N queen을 놓을 수 있는 방법의 개수를 세기 위해…
            1. 각 row를 돈다-마지막 row에 도달하면 모든 가능한 solution을 탐색한 것
            2. 특정 row에서 각 column을 돈다-특정 cell에 queen을 하나 놓을 수 있는지 가능성을 explore 
            3. (row, col)에 queen을 하나 놓았다면, 이 cell이 다른 queen의 공격 범위에 있거나 다른 queen이 이미 차지한 자리가 아닌지 확인할 필요가 있음 → `def is_not_under_attack(row, col)`
            4. check pass이면 proceed. 새로 놓인 queen의 공격 범위도 체크해야 → `def place_queen(row, col)`
            5. 이전 결정을 버리고  `def remove_queen(row, col)` → 다른 candidate를 찾아서 이동
                - 어디로 이동? 다음 row로
        - 수도 코드
            - 보드의 칼럼, row 개수도, 놓아야 할 퀸의 개수도 모두 n
            
            ```python
            def backtrack_nqueen(row = 0, count = 0):
                for col in range(n):
                    # iterate through columns at the curent row.
                    if is_not_under_attack(row, col):
                        # explore this partial candidate solution, and mark the attacking zone
                        place_queen(row, col)
                        if row + 1 == n:
                            # we reach the bottom, i.e. we find a solution!
                            count += 1
                        else: # row가 아직 맨 끝에 도달 안했으면 현 상태 그대로 유지하면서 전진
                            # we move on to the next row
                            count = backtrack_nqueen(row + 1, count)
                        # backtrack, i.e. remove the queen and remove the attacking zone.
                        remove_queen(row, col)
                return count
            ```
            
- Template
    - pseudo code
        
        ```python
        def backtrack(candidate):
            if find_solution(candidate):
                output(candidate)
                return
            
            # iterate all possible candidates.
            for next_candidate in list_of_candidates:
                if is_valid(next_candidate):
                    # try this partial candidate solution
                    place(next_candidate)
                    # given the candidate, explore further.
                    backtrack(next_candidate)
                    # backtrack
                    remove(next_candidate)
        ```
        
    - 적용 예시: Robot Room Cleaner
        - 문제: 주어진 matrix의 각 cell의 value는 장애물인지 아닌지를 나타낸다. 한 번에 한 칸씩 4방향으로 움직일 수 있는 로봇 청소기가 주어질 때 방을 청소해라
        - 로봇 청소기의 각 step은 재귀 함수로 나타낼 수 있다
            - 로봇이 장애물이나 이미 청소된 cell을 만날 경우 현상태에서 변화없이 더 전진
            - 한번에 한 칸씩 방문되면서 결국에는 matrix traverse 완성
        - 각 step에서 로봇 청소기는 4가지 방향으로 갈 수 있지만, 못 가는 경우도 있음 - 다음 cell이 invalid 한 경우
            - 장애물이거나 이미 청소된 곳이거나 → 이런 곳으로는 더 이상 전진하지 않도록 pruning the search space
        - 로봇이 어느 방향으로 전진한다면(valid 한 cell이라서), 마킹이 필요하다 (place)
        - 현 상태를 유지하면서 전진하다가 다 돌아오면 그때는 다시 이전의 결정을 revert 한다 (remove) = 이전 cell로 돌아와서 방향을 복원(?)
    - 적용 예시: Sudoku Solver
        1. input: 일부분 숫자로 채워진 matrix → output: 스도쿠 게임 제약사항을 만족하는 숫자들로 빈 cell을 채우기 
        each step(cell 숫자로 채우기)을 recursive function으로 구현
        2. 각 step에서 후보 숫자는 1~9. 제약 사항 반영해서 valid한 candidate 걸러냄 
        3. valid candidate 하나씩 돌면서 cell을 채워봄 (place). 쭉 가다가 끝까지 도달하고 나면 return 하고 backtrack-reverting the decision (remove)
        4. 재귀 형태로 현 상태 유지하면서 전진 - 하다가 적절한 후보가 더 이상 없거나 빈 cell을 valid candidate으로 다 채웠거나 하면 끝남 
        

# Unfold Recursion

- Introduction
    - recursion → non-recursion (iterative)
    - recursion 한계
        - stack over flow, duplicate calculation, 가독성 떨어짐
    - 대안
        - stack, queue와 같은 자료 구조 이용
            - 왜 이런 것들을 써야 하냐? system call stack의 역할을 대신
                - recursive call을 불러야 하는 상황이 오면, 그렇게 하는 대신 parameter를 update 해서 걔네를 자료 구조에 넣어준다
                - 참고: system call stack 의 역할
                    1. **함수 호출 기록**: 현재 함수의 호출 정보가 스택에 저장됩니다. 이 정보에는 함수의 매개변수, 지역 변수, 반환 주소 등이 포함됩니다.
                    2. **상태 유지**: 재귀 함수가 자신을 다시 호출하면, 이전 호출의 상태는 스택에 그대로 남아 있으며, 새로운 호출의 상태가 스택의 상단에 추가됩니다.
                    3. **반환 및 스택 해제**: 재귀 함수가 반환 조건에 도달하면, 가장 최근의 함수 호출이 스택에서 제거되고 제어가 이전 함수 호출로 돌아갑니다. 이 과정이 반복되면서 스택이 점차 비워집니다.
                    4. **스택 오버플로우 방지**: 재귀의 깊이가 너무 깊어지면 스택 오버플로우(stack overflow)가 발생할 수 있습니다. 이는 스택 메모리가 가득 차서 더 이상의 함수 호출을 저장할 수 없는 상태를 의미합니다.
        - 우리가 생성한 자료 구조에 대해 loop 생성
            - 연쇄적으로 재귀 함수 호출하는 게 loop 안에서 iteration 하는 것으로 대체
    - 예시: 두 binary tree가 동일한지 체크하는 함수
        - recursive
            
            ```python
            class Solution:
                def isSameTree(self, p, q):
                    """
                    :type p: TreeNode
                    :type q: TreeNode
                    :rtype: bool
                    """    
                    # p and q are both None
                    if not p and not q:
                        return True
                    # one of p and q is None
                    if not q or not p:
                        return False
                    if p.val != q.val:
                        return False
            				# 같은 방향끼리 넣어줌 
                    return self.isSameTree(p.right, q.right) and \
                           self.isSameTree(p.left, q.left)
            ```
            
        - iterative
            
            ```python
            from collections import deque
            class Solution:
                def isSameTree(self, p, q):
                    """
                    :type p: TreeNode
                    :type q: TreeNode
                    :rtype: bool
                    """    
                    def check(p, q):
                        # if both are None
                        if not p and not q:
                            return True
                        # one of p and q is None
                        if not q or not p:
                            return False
                        if p.val != q.val:
                            return False
                        return True
                    
                    deq = deque([(p, q),])
                    while deq:
                        p, q = deq.popleft()
            						# 이번 거 통과 못하면 
                        if not check(p, q):
                            return False   
            						# 통과했고 둘 다 None이 아니면 dq에 추가       
                        if p:
                            deq.append((p.left, q.left))
                            deq.append((p.right, q.right))
                    return True
            ```
            

# Conclusion

- divide and conquer
    
    문제를 바로 풀 수 있을 때까지 여러 개로 쪼갠 다음, 각 쪼개진 문제들을 정복하고, 거기서 얻은 부분 정답들을 모아서 최종 정답을 낸다 
    
- backtracking
    
    후보들을 둘러보면서 점진적인 정답들을 여러개 키우다가, 그 중 하나가 절대 최종 정답이 안될 것으로 밝혀지면 바로 버리고, 그 전단계로 돌아가서 다른 후보를 살펴본다 
    
- dc VS bt
    1. divide and conquer는 최종 solution이 하나인 경우가 왕왕 있음↔ backtracking은 최종 solution이 몇 개인지 알려져 있지 않음 
        
        예) merge sort: sorted list의 형태는 한가지 (dq) vs. N-queen: 정답이 될 수 있는 방법이 여러 개 (bt)
        
    2. divide and conquer 문제의 각 step은 최종 solution을 생성하기 위해 필수적인 것들 ↔ backtracking의 중간 step들 다수는 invalid로 밝혀지는 것처럼 최종 solution을 탐색하는 시도지 필수 불가결 하지 않음
        
        예) merge sort: divide, conquer, combine 셋이 다 합해서 최종 sorted list로 이름 ↔ N-queen에서는 여기 놓아봤다가 안되면 취소하고 그런 시행착오가 많음 
        
    3. divide and conquer 알고리즘에서는 하나의 분명하고 이미 정의된 path가 존재 ↔ backtracking 에서는 솔루션에 이르는 명확한 path가 미리 정의되어 있지 않음
        
        예) top-down merge sort : 먼저 제귀적으로 문제를 두 개의 부분 문제로 나누고, 이 부분문제들의 답을 합친다 vs. N-queen: 어디에 queen들을 배치해야 하는지 미리 알고 있다면 N step으로 충분하겠지만, backtracking알고리즘 적용하면 여러 후보들을 다 거침 → 최종 solution에 이르기 까지 사전에 몇 개의 step을 거쳐야 하는지 알 수 없음