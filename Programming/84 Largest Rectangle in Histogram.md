# 84. Largest Rectangle in Histogram

Status: done, in progress, incomplete, 👀1
Theme: DP
Created time: November 14, 2023 10:56 AM
Last edited time: December 7, 2023 4:53 PM

- [ ]  다시 짜보기
- 복습 포인트
    
    <aside>
    ⭐ 복습 포인트 
    - 왼쪽 경계 오른쪽 경계를 구해서 높이랑 곱한다 
    - 각 방향의 경계를 구할 때 dp 즉 이전에 저장해둔 정보가 다시 활용된다 
    - 왼쪽 경계: default -1에서 시작. left[i]: 현재 높이를 왼쪽으로 연장했을 때 어디까지 연장할 수 있는지 
    - 오른쪽 경계: default n에서 시작. right[i]: 현재 높이를 오른쪽으로 연장했을 때 어디까지 연장할 수 있는지 
    - 두 경계에서 사실 저장되는 값은 연장이 가로막히는 첫 지점임 → 넓이 구할 때 한쪽을 좁혀야
      - 오른쪽을 하나 내리거나 왼쪽을 하나 늘리거나
    
    </aside>
    
- Editorial
    - Brute force
        - 설명
            - 어떤 두 개의 막대로 만들 수 있는 직사각형의 높이: 그 사이에 있는 가장 낮은 막대의 높이로 제한됨
            - every possible pair of bars에서 만들어질 수 있는 모든 직사각형을 고려
                - 직사각형의 높이: 두 막대 사이에서 높이가 가장 낮은 막대의 높이
                - 직사각형의 너비: 두 막대 사이의 거리
            - 그림
                
                ![Untitled](Untitled%20135.png)
                
        - 코드 (TLE)
            - min(heights[i:j+1]) 까지 고려하면 O(n^3) 극악의 시간 복잡도
            
            ```python
            class Solution:
                def largestRectangleArea(self, heights: List[int]) -> int:
                    N = len(heights)
                    max_area = 0
                    for i in range(N):
                        for j in range(i, N):
                            l, r = heights[i], heights[j]
                            cur_width = j-i+1
                            cur_height = min(heights[i:j+1])
                            if cur_width * cur_height > max_area:
                                max_area = cur_width * cur_height
                    return max_area
            ```
            
    - Better Brute force
        - 설명
            - 모든 쌍에 대해서 최소 높이 막대를 찾는 대신 → 이전 pair에서의 minimum height를 이용해서 current pair에서의 최소 높이 막대를 탐색 : $min \ height = \ min(min \ height, \ height[j])$
        - 코드 (TLE)
            - 모든 j에 대해 i에서 j까지 다 비교하는 부분이 없어졌기 때문에 O(n^2)로 시간복잡도 하락
            
            ```python
            class Solution:
                def largestRectangleArea(self, heights: List[int]) -> int:
                    N = len(heights)
                    max_area = 0
                    for i in range(N):
                        min_height = float('inf')
                        for j in range(i, N):
                            cur_width = j-i+1
                            min_height = min(min_height, heights[j])
                            max_area = max(cur_width * min_height, max_area)
                    return max_area
            ```
            
    - Divide and Conquer
        - 설명
            - 관찰: 최대 넓이의 사각형은 아래의 상황에 대한 최대이다
                1. 높이가 최소 높이와 같으면서 가로로 가장 넓은 사각형의 면적 
                2. 가장 높이가 낮은 막대를 경계로 삼아 그보다 왼쪽에 형성될 수 있는 가장 큰 직사각형의 면적 (subproblem)
                3. 가장 높이가 낮은 막대를 경계로 삼아 그보다 오른쪽에 형성될 수 있는 가장 큰 직사각형의 면적 (subproblem)
            - 예시
                
                ```python
                [6, 4, 5, 2, 4, 3, 9]
                ```
                
                - 가장 높이가 낮은 막대의 높이: 2
                    1. 의 경우의 사각형 넓이: 2 * 7 = 14
                    2. 의 경우의 사각형 넓이: 4* 3 = 12 
                        - 왼쪽 부분 한정으로 보면 최소 높이 막대는 4
                        - 그래서 2.는 왼쪽 부분으로 보면 1.에 해당하기도 함
                        - 왼쪽 부분 한정에서 2.는 왼쪽의 6 *1 = 6
                        - 왼쪽 부분 한정에서 3.은 오른쪽의 5*1 = 5
                    3. 의 경우의 사각형 넓이: 3*3 = 9 
                        - 오른쪽 부분 한정으로 보면 최소 높이 막대는 3
                        - 그래서 3.은 왼쪽 부분 한정으로 보면 1.에 해당하기도 함
                        - 오른쪽 부분 한정에서 2.는 4*1= 4
                        - 오른쪽 부분 한정에서 3.은 9*1 = 9
                    
                    ⇒ 따라서 1.2.3.의 max는 14
                    
        - 코드 (심지어 예제도 TLE)
            - heights array가 오름차순이나 내림차순으로 정렬되어 있으면 divide and conquer의 이점을 얻지 못하고 worst case in O(n^2)
            - 아니면 O(nlogn)
            - 공간복잡도의 경우 최악의 상황에서 깊이 n의 재귀함수 stack이 생겨나서 O(n)
            
            ```python
            class Solution:
                def largestRectangleArea(self, heights: List[int]) -> int:
                    def divide_conquer(start, end):
                        if start > end: return 0
                        # get 1.case
                        # shortest idx만 얻으면 된다 
                        min_idx = start
                        for i in range(start, end+1):
                            if heights[i] < heights[min_idx]:
                                min_idx = i
                        widest_area = heights[min_idx] * (end-start+1)
                        # get 2.case
                        left_max = divide_conquer(start, min_idx-1)
                        # get 3.case
                        right_max = divide_conquer(min_idx+1, end)
                        return max(widest_area, left_max, right_max)
            
                    return divide_conquer(0, len(heights)-1)
            ```
            
    - 🪇Better Divide and Conquer
        - 설명
            - Segment Tree를 사용해서 최소를 찾으려고 한다.
            - Segment Tree
                - 구간에서의 query(합, 최소, 최대) 등 update가 빈번히 발생하는 array에 대해 효율적으로 답을 꺼내줄 수 있도록 설계된 자료 구조
                    - 세그먼트 트리의 각 노드는 원본 배열의 특정 구간(부분 집합)에 대한 정보를 의미합니다. 이 정보는 주로 구간에 대한 집계 데이터로, 예를 들어 합계, 최소값, 최대값 등이 될 수 있습니다.
                    1. **리프 노드**: 트리의 리프 노드는 원본 배열의 개별 요소를 나타냅니다. 각 리프 노드는 배열의 한 요소에 대응되며, 그 요소의 값을 저장합니다.
                    2. **내부 노드**: 내부 노드는 두 개의 자식 노드의 구간을 합친 것을 나타냅니다. 예를 들어, 내부 노드가 자식 노드들을 통해 [i, j] 및 [j+1, k] 구간을 나타내면, 이 노드는 [i, k] 구간을 대표합니다. 내부 노드는 이 구간에 대한 정보를 저장하며, 이는 보통 자식 노드들의 데이터를 합한 것입니다(예: 구간의 합계, 최소값, 최대값).
                    3. **루트 노드**: 세그먼트 트리의 루트 노드는 원본 배열의 전체 구간을 나타냅니다. 이 노드는 배열의 전체 구간에 대한 정보를 저장합니다.
                    - 그림
                        
                        ![Untitled](Untitled%20136.png)
                        
                - 원본 array를 다양한 구간으로 나누어 각 구간에 대한 정보를 node에 저장
                - 로그 시간 복잡도-구간 query와 업데이트 모두 O(log N)
                - 이진 트리 구조
                - python code
                    - 참고: complete binary tree
                        
                        ![Untitled](Untitled%20137.png)
                        
                    
                    ```python
                    class SegmentTree:
                        def __init__(self, arr):
                            self.n = len(arr)
                            self.tree = [0] * (4 * self.n)
                    				# 전체 list에 대한 tree 생성해라 
                            self.build(arr, 0, 0, self.n - 1) 
                    
                        def build(self, arr, node, start, end):
                            if start == end: # leaf node
                                self.tree[node] = arr[start]
                            else:
                                mid = (start + end) // 2
                                self.build(arr, 2 * node + 1, start, mid)
                                self.build(arr, 2 * node + 2, mid + 1, end)
                                self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
                    
                        def sum_query(self, node, start, end, l, r):
                            if l > end or r < start:
                                return 0
                            if l <= start and end <= r: # start, end 구간이 l,r  구간 안에 있으면
                                return self.tree[node]
                            mid = (start + end) // 2
                            return self.sum_query(2 * node + 1, start, mid, l, r) + \
                                   self.sum_query(2 * node + 2, mid + 1, end, l, r)
                    
                        def query(self, l, r):
                            return self.sum_query(0, 0, self.n - 1, l, r)
                    
                    # 사용 예시
                    arr = [1, 3, 5, 7, 9, 11]
                    st = SegmentTree(arr)
                    print(st.query(1, 3))  # 1번 인덱스부터 3번 인덱스까지의 합
                    ```
                    
        - 요약
            1. 세그먼트 트리 노드 클래스 정의 
            2. mothership 함수
                
                1) heights 가 빈 집합인 경우의 base case 처리
                
                2) segment tree 생성하는 함수 콜 (4. 함수)
                
                3) max area 구하는 함수 콜 (3. 함수)
                
                → 2)의 정보를 가져오는 함수 콜 (5. 함수)
                
            3. max area 구하는 함수 (`divide & conquer`)
                1. base case  (범위 restriction 어기는 경우) 
                    
                    ↳ 나중에 combine 하는 방식이 return된 값에 바로 max 때리는 거라서 무시될 수 있는 -1 return 
                    
                2. 막대 하나의 넓이 구하는 경우 (특정 범위 해당, width가 1이라 넓이가 곧 높이)
                3. a, b에 해당하지 않는 경우 
                    1. segment tree에서 정보 가져오는 함수 콜
                    2. [이 세가지 경우](84%20Largest%20Rectangle%20in%20Histogram%20bab4a72971c243ef839cb80c246fe7a5.md) 에 대한 subproblem solution 구해둔다 (재귀함수 콜, divide & conuqer)
                        
                        ↳ 세 가지 경우 중에 최소 높이 막대를 높이로 삼고, widest 직사각형 넓이 구하는 경우가 있고, 나머지 두 경우도 최소 높이 막대를 기준으로 왼쪽, 오른쪽 구간을 좁혀서 재귀 콜하는 것 → 최소 높이 막대가 주어진 구간에서 어디 위치해있는지 정보가 필수 → 이 정보를 segment tree node에 저장해두었다가 가져오는 것 → segment tree node에서 구간내 최소 높이 막대 위치를 가져오는 함수가 필요 
                        
                    3. max값 취해서 combine 
            4. segment tree 생성 함수  (`divide & conquer`)
                1. base case 1 (범위 restriction 어기는 경우) 
                    
                    ↳ 나중에 combine 하는 방식:  return 된 클래스 인스턴스의 인스턴스 변수에 min. return 자체는 값이 아니라 클래스 인스턴스 → base case에 해당하는 경우 None 나오게끔 해서 combine 할 때 걸러내는 줄 알았는데 코드를 따져보면 없어도 되는 부분인 것 같다 ;;
                    
                2. base case 2 (특정 범위 해당)
                    
                    ↳ 여기서 재귀콜을 한번 더해야 base case 1으로 넘어가는데, 그러지 않기 때문에 a.는 사실상 없어도 되는 듯 
                    
                    인스턴스 변수에 값을 지정한 뒤 node return 
                    
                3. divde & conquer
                    
                    ↳ 구간 범위 좁혀서 재귀 함수 콜. 경계는 모두 inclusive인 점 주의 
                    
                    ↳ subproblem의 solution (node)들을 현재 node의 인스턴스 변수에 배치함으로써 노드 간의 관계를 형성, 나아가 트리를 만들게 된다 
                    
                4. combine
                    
                    ↳ c.에서 return 되는 subproblems의 solution인 노드들의 인스턴스 변수 값을 가지고 Min 때림 → 그게 이번 node의 인스턴스 변수 값이 됨 
                    
            5. 주어진 구간 내의 최소 높이 막대의 index return 하는 함수  (`divide & conquer`)
                1. base case (범위 restriction 어기는 경우)
                    
                    ↳ query 함수가 재귀적으로 호출되는 경우는 요청 구간이 현재 노드가 커버하는 구간보다 더 좁은 경우 → 그래서 쪼개서 요청 구간에 정확히 해당하는 구간에서의 최소값을 구하는 것이 목표. 쪼갰을 때 요청 구간에 포함되지 않는 구간은 combine 단계에서 무시되어야 함. 
                    
                    ↳ 나중에 combine을 min으로 때리기 때문에 a) 무시될 수 있는 값(예를 들어 float(’inf’))를 return 하도록 하거나 b) combine 전에 이 경우에 해당하는 값만 필터링 할 수 있도록 설정 
                    
                    ↳ editorial 에서는 b)를 선택해서 음수를 return 하도록 하고, 추가 if condition 설정함 
                    
                    1. ~~요청된 구간이 이미 input node에 의해 커버되는 구간인 경우~~ 요청된 구간이 input node에 의해 커버되는 구간을 넘을 경우 → 단순히 값 retrieval 하면 된다. input node의 인스턴스 변수 값 return 
                2. 주어진 구간이 input node가 커버하는 구간안에 속해 있어서 더 정교한 solution이 필요할 때 
                    1. divide and conquer
                        
                        ↳ 요청 구간은 유지, node 간의 관계 이용해서 tree에서 더 좁은 부분만 커버하는 다른 node로 이동 → 각 subproblem solution return
                        
                    2.  각 subproblem solution 중에 요청 구간에 포함되지 않는 부분이 있는지 확인, 둘 중에 하나라도 invalid 하면 바로 나머지 하나가 바로 final solution 
                    3. 둘 다 valid 하면 인덱스에 위치한 원소의 크기 비교해서 더 작은 쪽을 최종 solution으로 return (다른 함수에서 넓이 구할 때 특정 구간의 최소 높이 막대가 위치한 인덱스)
        - 코드
            - 시간 복잡도: O(n log n)
                - chat gpt 부연 설명
                    1. 구**성 시간 복잡도**: 세그먼트 트리를 처음 구성할 때의 시간 복잡도는 O(n)입니다. 여기서 n은 배열의 원소 수입니다. 세그먼트 트리는 각 노드가 특정 범위를 대표하는 트리 구조로, 전체 배열을 커버하는 트리를 구성하는 데 n개의 원소를 모두 고려해야 합니다.
                    2. **쿼리 시간 복잡도**: 세그먼트 트리를 사용해 특정 구간에 대한 쿼리를 수행할 때의 시간 복잡도는 O(log⁡n)입니다. 이는 트리의 높이가 log⁡n이기 때문입니다. 구간 쿼리는 트리를 위에서 아래로 내려가면서 특정 범위를 찾는 과정이므로, 트리의 각 레벨을 거쳐가는데 log⁡n의 시간이 소요됩니다.
            
            ```python
            class SegTreeNode:
                def __init__(self, start, end):
                    self.start = start # 해당 노드가 정보를 담고 있는 구간의 시작점
                    self.end = end # 구간 종료 지점
                    self.min = None # 해당 구간에서의 최소 높이를 갖는 index
                    # 노드 간의 관계를 지정해서 tree를 형성하는 부분
            				self.left = None # 왼쪽 자식 노드 toggle 3에서 본 shortest 기준 왼쪽 부분 한정
                    self.right = None # 오른쪽 자식 노드
            
            class Solution:
                def largestRectangleArea(self, heights):
                    if len(heights) == 0:
                        return 0
            				# tree 생성
                    root = self.buildSegmentTree(heights, 0, len(heights) - 1)
            				# max area 구하는 함수 콜
                    return self.calculateMax(heights, root, 0, len(heights) - 1)
            
                def calculateMax(self, heights, root, start, end):
            				# base case
                    if start > end:
                        return -1
                    if start == end: # 이 경우 자기 혼자의 막대이고, width가 1이라 height가 곧 넓이 
                        return heights[start] # leaf node. 구간이 아닌 개별 요소의 값
            				
            				# segment tree에서 정보 들고 옴 
                    minIndex = self.query(root, heights, start, end)
            				# divide 
                    leftMax = self.calculateMax(heights, root, start, minIndex - 1)
                    rightMax = self.calculateMax(heights, root, minIndex + 1, end)
                    minMax = heights[minIndex] * (end - start + 1)
                    # combine 
            				return max(max(leftMax, rightMax), minMax)
            
                def buildSegmentTree(self, heights, start, end):
                    if start > end:
                        return None
                    root = SegTreeNode(start, end)# 빈 node를 하나 만들고
                    if start == end:
                        root.min = start # leaf node의 경우 minIndex는 자기 자신 
                        return root
                    else:
                        middle = (start + end) // 2
            						# 여기에 root.left나 root.right가 None인지 확인 안해도 되나? 
                        root.left = self.buildSegmentTree(heights, start, middle)
                        root.right = self.buildSegmentTree(heights, middle + 1, end)
                        root.min = (root.left.min if heights[root.left.min] < heights[root.right.min] 
                                    else root.right.min)
                        return root
            
                def query(self, root, heights, start, end):
            				# base case
                    if not root or end < root.start or start > root.end:
                        return -1
            				# 최소값을 가져오도록 요청된 구간이 이미 input node(root)가 커버하는 구간인 경우
                    if start <= root.start and end >= root.end:
            						# 그대로 node에 저장된 정보를 가져오기만 한다 
                        return root.min
            				
            				# 현재 node root가 커버하는 구간이 더 넓어서 요청된 구간에 포함되지 않는 부분까지 커버하고 있을 때 
            				# divide and get subproblem solutions
            				## 이 subproblem의 해는 결국에 어느 지점에서의 base case거나 node에 저장된 값을 가져오는 값 둘 중 하나
                    leftMin = self.query(root.left, heights, start, end)
                    rightMin = self.query(root.right, heights, start, end)
                    # base case 값으로 return 된 경우 처리 
            				if leftMin == -1:
                        return rightMin
                    if rightMin == -1:
                        return leftMin
            				# subproblem의 index를 가져와서 해당 높이 비교(combine)
                    return leftMin if heights[leftMin] < heights[rightMin] else rightMin
            
            # 사용 예시
            sol = Solution()
            heights = [2, 1, 5, 6, 2, 3]
            print(sol.largestRectangleArea(heights))
            ```
            
    - Using stack
        - 설명
            - 진짜 핵심 요약 설명
                1. stack에 -1만 넣고 초기화한다 
                2. 각 인덱스를 돌면서 max_area를 update 하거나 stack에 인덱스를 추가한다
                    1. stack에 인덱스를 추가하는 경우 
                        - 현재까지 stack의 최대 높이(stack[-1])를 이번 인덱스의 높이 heights[i]가 감당할 수 있다는 뜻 = 현재까지 stack의 높이를 오른쪽으로 더 뻗을 수 있다 = heights[i]가 stack 안에서 최대 높이보다 크다
                        - 이런 식으로 진행하다보면 stack에 쌓이는 index 순서는 높이 오름차순이 된다 = 더 높이가 높은 index가 오른쪽에 있는 경우 stack 맨 위에 놓이게 된다
                            - 다른 말로 하면, stack에 아직 남아 있는 index 들은 오른쪽에 더 높이가 낮은 막대를 만나기 전 상태
                    2. max_area update 하는 경우 
                        - 현재까지 stack의 최대 높이(stack[-1])를 이번 index의 높이 (heights[i])가 감당할 수 없다 → 현재 최대 높이를 높이로 삼는 직사각형의 넓이를 구해버린다 → stack에는 기존 top보다 높이가 낮은 위치의 Index가 새로운 top이 된다 → 이 top의 높이가 이번 인덱스의 높이보다 낮으면 그제야 이번 인덱스의 높이를 추가한다
                        - 직사각형 넓이 구하기
                            - 당연히 높이는 방금 pop 한 ex-top의 index의 높이. heights[stack.pop()]
                            - 너비
                                - 오른쪽 경계: 현재 index 바로 앞 (방금 pop 한 인덱스의 높이로 연장할 수 있는 가장 오른쪽 경계) = i-1 (inclusive)
                                    - 왜 그런지 그림
                                        
                                        ![Untitled](Untitled%20138.png)
                                        
                                        - heights[4] = 2. 2는 5보다도 작고 6보다도 작다.
                                        - 먼저 6에 해당하는 인덱스인 3이 top이라서 pop 할 건데, 6은 자기 위치에서 시작해서 2바로 전 그니까 역시 자기 자신에서 끝난다
                                        - 그 다음 top인 5도 2보다 작으니까 pop할 건데, 5는 자기 위치에서 시작해서 2 바로 전 그니까 6 자리까지 연장 가능하다
                                - 왼쪽 경계: 현재 높이보다 작으면서 가장 오른쪽에 있는 막대의 index = new stack top (exclusive)
                                
                                ⇒ `(i-1) - stack[-1]`
                                
                3. 인덱스를 다 돌고 났는데도 stack에 -1 말고 다른 원소가 남아 있을 때
                    - 남은 index에 해당하는 높이를 오른쪽 맨 끝까지 (inclusive N-1) 연장할 수 있는 애들만 남은 상태임
                    - 여긴 무조건 2-b와 같은 동작만 반복해서 stack에 -1만 남긴다
                        - 다만 너비 구할 때 오른쪽 경계가 오른쪽 맨 끝 그러니까 N-1로 대체된다는 점이 다름
            - 그림 보고 내가 다시 쓰는 설명
                - stack[top-1]은 stack[top]의 높이를 연장시킬 수 없는 첫 지점이다. stack[top-1]의 Index는 exclusive라는 의미
                1. -1을 stack에 넣어서 end 지점을 표시, max_area 초기값은 0
                2. stack[top]보다 이번 heights[i] 값이 더 큰(클?) 동안 stack에 계속 push
                    - stack에 쌓인 값들은 오름차순
                3. stack[top]이 더 큰 동안 pop 하고 넓이 구하고, max_area 업뎃 
                    - 넓이 구하기: pop 한 원소에 해당하는 높이 * (현재 넣으려고 했던 원소의 index i - pop 하고 난 뒤 stack의 top 원소 index - 1)
                        - pop 한번 할 때마다 높이, 너비 다 바뀐다
                        - 내 생각에는 현재 넣으려고 하는 index i보다 바로 한칸 앞인 i-1 자리에서의 넓이를 구하기 위함이고, 마지막 -1이 앞으로 가야 말이 되는 것 같다
                            
                            → 너비: (i-1) - stack[top-1]
                            
                            - 그림
                                
                                ![Untitled](Untitled%20139.png)
                                
                    - 드디어 stack top이 -1이거나 그 index에 해당하는 값이 heights[i]보다 작아지면 그제서야 push
                        - stack 안에서는 오름차순이니까
                4. 마지막 원소에 도달하면 push 하자마자 pop 하고 넓이 구하기
                    - 여기서는 남은 원소를 -1 나올 때까지 다 pop 하는데, 넓이 구하는 공식이 조금 바뀐다
                    - 마지막 원소까지 왔을 때 stack에 남아 있는 애들을 하나씩 pop 하면서 사각형 넓이를 구하는데, 이 때 너비 기준점은 마지막 index (length -1)이다
                        - 높이: pop 한 원소 위치에 해당하는 높이
                        - 너비: 제일 마지막 index - 다음 stack top index
                            - 예) 7 자리의 높이 3은 4 자리까지 연장 가능. 3 자리의 높이 2는 더 낮아서 그 뒤로는 연장 불가 → 7-다음 top에 해당하는 index = 7-3 = 4
                            - 예) 3 자리의 높이 2는 오른쪽으로는 마지막 인덱스까지, 왼쪽으로는 다음 top -1까지 연장 가능 → 7-다음 top에 해당하는 index (-1) = 7+1 = 8
            - 원래 설명
                - -1을 stack에 넣어서 end 지점을 표시
                - push
                    - 두 개의 연속하는 숫자가 내림차순으로 나올 때까지 ($heights[i-1] > heights[i]$)
                    - 가장 왼쪽에 있는 막대에서 시작해서 현재 막대의 Index를 stack에 계속 push
                - pop
                    - pop된 원소 자리의 높이가 현재 막대의 높이보다 작거나 같을 때까지 ($heights[stack[j]] \leq heights[i]$) stack에서 계속 pop
                    - pop 할 때마다 직사각형의 넓이를 구해본다
                        - 높이 : 방금 pop된 원소($stack[top]$)
                        - 너비: $stack[top-1]-1$과 현재 index i 사이의 차
                        - 넓이: $(i-stack[top-1]-1) \times heights[stack[top]]$
                - array에 끝에 도달하면 stack에서 모든 원소를 pop
                    - pop 할 때마다 아래의 공식을 사용해서 넓이를 찾는다
                        
                        $(len(heights)-stack[top-1]-1) \times heights[stack[top]]$ 
                        
            - 헷갈리는 마지막 부분 설명
                - chat 센세
                    
                    히스토그램의 최대 직사각형 문제에서, 배열의 모든 원소를 처리한 후 스택에 남아 있는 원소들은 해당 원소들의 오른쪽에 더 낮은 막대가 없는 막대들을 의미합니다. 이들은 히스토그램의 오른쪽 끝까지 확장될 수 있는 직사각형의 높이를 나타냅니다.
                    
                    히스토그램의 각 막대를 스택에 넣는 과정은, 해당 막대가 현재까지의 최대 높이를 유지할 수 있는지 확인하는 과정입니다. 스택에서 막대를 제거하는 것은 그 막대보다 더 낮은 높이의 막대를 만났을 때 발생합니다. 이는 해당 막대를 기준으로 한 최대 직사각형의 오른쪽 경계를 찾았음을 의미합니다.
                    
                    그러나 배열의 끝까지 처리한 후에도 스택에 막대가 남아 있다면, 이들은 오른쪽에 더 낮은 막대를 만나지 않았음을 의미합니다. 이 경우:
                    
                    - 이 막대들은 히스토그램의 오른쪽 끝까지 확장될 수 있는 직사각형을 형성합니다.
                    - 이들의 높이는 각각 **`heights[stack[top]]`**이며, 너비는 해당 막대의 인덱스부터 히스토그램의 끝까지의 거리가 됩니다.
                    
                    따라서, 마지막으로 스택에 남은 각 막대에 대해 최대 직사각형의 면적을 계산해야 합니다. 이 계산은 히스토그램의 전체 범위에서 가능한 최대 면적을 정확히 찾기 위해 필요합니다.
                    
        - 코드
            - 내가 짜본 코드~
                
                ```python
                class Solution:
                    def largestRectangleArea(self, heights: List[int]) -> int:
                        stack = [-1] # ascending stack! 
                        N = len(heights)
                        max_area = 0
                        for i in range(N):
                          ~~if~~ stack[-1] == -1 or heights[i] >= stack[-1]:
                            stack.append(heights[i])
                          else:
                            while heights[i] < stack[-1]:
                              cur_idx = stack.pop() # same as i-1?
                              #cur_height = height[cur_idx]
                              #boundary = stack[-1]
                              #cur_width = (i-1) - boundary
                              if i == N-1:
                                max_area = max(max_area, ((n-1)-stack[-1]) * heights[cur_idx])
                              else:
                                max_area = max(max_area, ((i-1)-stack[-1]) * heights[cur_idx])
                            stack.append(heights[i])
                        return max_area
                ```
                
            - Editorial 코드
                
                ```python
                class Solution:
                    def largestRectangleArea(self, heights: List[int]) -> int:
                        stack = [-1] # ascending stack! 
                        N = len(heights)
                        max_area = 0
                        for i in range(N):
                          # 넓이 update
                          while stack[-1] != -1 and heights[i] < heights[stack[-1]]:
                            cur_height = heights[stack.pop()]
                            cur_width = (i - 1) - stack[-1]
                            max_area = max(max_area, cur_width * cur_height)
                          # 현재까지의 stack 안의 최대 높이로 오른쪽에 연장 가능하기 때문에 stack에 append
                          stack.append(i)
                
                        # for loop 다 돌고도 stack에 원소가 남아 있으면
                        while stack[-1] != -1:
                          cur_height = heights[stack.pop()]
                          cur_width = (N - 1) - stack[-1]
                          max_area = max(max_area, cur_width * cur_height)
                
                        return max_area
                ```
                
    
- [x]  전체 코드 쫙 한번 더 짜보기
- [[**85. Maximal Rectangle**](https://leetcode.com/problems/maximal-rectangle/description/)](85%20Maximal%20Rectangle%2090bc1c0de658492db51c8ad17f9fe389.md) 랑 비슷한 문제인 것 같은데, 이 문제에서는 row가 하나이고, matrix 값이 1일때를 기준으로 transition case가 나뉘지 않는다
    - 그리고 85번에서는 일단 0이 한번 나오면 더 이상 사각형이 만들어질 수 없었는데
    - 이 문제에서는 이전보다 높이가 낮아도 사각형을 만들 수 있다
- 비슷하게 하고 이전 height랑 차이로 분기하도록 했는데 64/98개까지 맞음 ㅎㅎ
    - 왼쪽은 자기랑 같은 높이일 수 있으면서 (더 커도 상관 없음) 가장 왼쪽에 있는 Index
    - 오른쪽은 자기랑 같은 높이일 수 있으면서 (더 커도 상관없음) 가장 오른쪽에 있는 index + 1
        - 왜냐면 right-left 했을 때 + 1을 해야 변의 길이를 제대로 얻을 수 있기 때문
- cur_left, cur_right 사용하는 걸로 해도(사실 update가 어떻게 정확히 이루어지는 지 기억이 긴가민가하지만) 64개까지만 맞음
- 오른쪽이 문제다
    - 현재 내 위치의 높이보다 같거나 크면서 가장 오른쪽에 있는 위치를 기록해가야 하는데…
    - 그러면서 내 위치에서 연속해서 거기까지 갈 수 있어야 함. 중간에 나보다 더 낮은 높이를 만나면 안됨
    - 오른쪽 tracking
        
        ```python
        for i in range(n-2, -1, -1): 
        	p = i+1
        	while p < n and height[p] >= height[i]:
        		p = right[p] 
        	right[i] = p 
        ```
        
        ```python
        right = [8, 8, 8, 4, 8, 6, 8 ,8] # i=4까지만 update 한 것임 
        ```
        
    - 예를 들어 [4, 2, 0, 3, 2, 4, 3, 4], N=8에서
        - i = 6에서 시작, p=7
            - height[p] = 4 ≥ height[i] = 3 → p = right[p] = n = 8
            - p = n → while loop break → right[6] = 8
        - i = 5, p = 6
            - height[p] = 3 < height[i] = 4 → while loop break
            - right[5] = 6
        - i = 4, p = 5
            - height[p] = 4 > height[i] = 2 → p = right[5] = 6
            - height[p] = height[6] = 3 > height[i] = 2 → p = right[6] = 8
            - p = n → while loop break → right[4] = 8
        - i = 3, p = 4
            - height[p] = 2 < height[i] = 3 → while loop break
            - right[3] = 4
    - 정리하면…
        - 오른쪽 tracking은 오른쪽→왼쪽으로
        - 가장 오른쪽은 그보다 더 오른쪽이 없으니, 그리고 나중에 right-left를 고려해서 현재 위치 +1 = n
        - n-2번째 column부터 시작
        - 자기 기준으로 자기보다 바로 뒤에 있는 column과 우선 비교
            - 만약 뒤보다 내가 더 높으면, 더 뒤는 볼 필요도 없고, 내가 가장 오른쪽 칼럼이니까 i+1 = p
            - 내 높이를 어디까지 연장할 수 있는지 Pointer p를 미루고 미루다가 마지막 n-1+1=n까지 닿으면 그냥 그걸 rightmost 경계로 넣어준다
            - 만약 뒤에 있는 column이 더 높으면, 그 뒤에 있는 column로 더 높은지 봐야 함
                - 우선 우리가 미리 확보한 정보: i+1번째 column과 연속으로 같은 높이를 연장해나갔을 때 가장 오른쪽에 있는 column 정보 = right[i+1]
                - pointer p를 right[i+1]로 이동, 그 위치에 해당하는 높이 height[right[i+1]] == height[p]로 이동 → 다시 현재 우리 높이와 비교
                - 그래도 우리보다 더 높으면 또 그 뒤에 있는 column과 비교해야 함. 이 때 다시 과거에 기억해둔 정보-즉 right[i+1]의 높이를 오른쪽으로 쭉 연장했을 때 닿을 수 있는 끝, 가장 오른쪽에 있는 column = right[height[right[i+1]]] = right[p]-으로 또 pointer 이동해서 비교
- 왼쪽 tracking도 수정해야 한다
    
    예) [3,6,5,7,4,8,1,0] → 1(height[6]) 의 입장에서 1을 연장할 수 있는 왼쪽 끝은 0번째 index인데 바로 직전만 비교하는 코드로는 0에 도달할 수 없다 → 오른쪽 tracking처럼 pointer p 도입해야 함 
    
    - [x]  왼쪽 tracking java code python으로 옮기기
        
        ```python
        for i in range(1, n):
        	p = i-1
        	while p >= 0 and height[p] >= height[i]:
        		p = left[p]
        	left[i] = p 
        ```
        
        - i = 0인 경우는 왼쪽보다 더 왼쪽이 없기 때문에 초기값을 0에서 시작하면 문제 없음
        - 왼쪽 tracking에서 p는 더 왼쪽으로 왼쪽으로 갈 것이기 때문에 0보다 작아지면 while loop 멈춰야 함 - 0일 때는 while loop 유지됨
        - height[p] ≥ height[i]: i의 높이로 왼쪽으로 더 p까지 연장 가능. 더 왼쪽으로 갈 수 있는지 여부를 보려면, p = left[p]로 p의 높이로 가장 왼쪽까지 갈 수 있는 곳에 도달한 뒤, 다시 그곳의 높이 height[p]를 가져다가 height[i]와 비교
        - while loop break: p가 왼쪽으로 가다가 0보다 더 작아지거나, height[i]를 왼쪽으로 연장할 수 없는 경우
    - [x]  위의 예시로 해보기
        - 왼쪽
            
            
            | p | i | height[p] | height[i] | break | left[p] | left[i] |
            | --- | --- | --- | --- | --- | --- | --- |
            | 0 | 1 | 3 | 6 | Yes |  | 0 |
            | 1 | 2 | 6 | 5 | No | 0 |  |
            | 0 | 2 | 3 | 5 | Yes |  | 0 |
            | 2 | 3 | 5 | 7 | Yes |  | 2 |
            | 3 | 4 | 7 | 4 | No | 2 |  |
            | 2 | 4 | 5 | 4 | No | 0 |  |
            | 0 | 4 | 3 | 4 | Yes |  | 0 |
            | 4 | 5 | 4 | 8 | Yes |  | 4 |
            | 5 | 6 | 8 | 1 | No | 4 |  |
            | 4 | 6 | 4 | 1 | No | 0 |  |
            | 0 | 6 | 3 | 1 | No | -1 |  |
            | -1 | 6 |  |  | Yes |  | -1 |
            | 6 | 7 | 1 | 0 | No | -1 |  |
            | -1 | 7 |  |  | Yes |  | -1 |
        - 오른쪽
            
            ```python
            for i in range(n-2, -1, -1): 
            	p = i+1
            	while p < n and height[p] >= height[i]:
            		p = right[p] 
            	right[i] = p 
            ```
            
            | p | i | height[p] | height[i] | break | right[p] | right[i] |
            | --- | --- | --- | --- | --- | --- | --- |
            | 7 | 6 | 0 | 1 | Yes |  | 7 |
            | 6 | 5 | 1 | 8 | Yes |  | 6 |
            | 5 | 4 | 8 | 4 | No | 6 |  |
            | 6 | 4 | 1 | 4 | Yes |  | 6 |
            | 4 | 3 | 4 | 7 | Yes |  | 4 |
            | 3 | 2 | 7 | 5 | No | 4 |  |
            | 4 | 2 | 4 | 5 | Yes |  | 4 |
            | 2 | 1 | 5 | 6 | Yes |  | 2 |
            | 1 | 0 | 6 | 3 | No | 2 |  |
            | 2 | 0 | 5 | 3 | No | 6 |  |
            | 6 | 0 | 1 | 3 | Yes |  | 6 |
    - [x]  영역 구할 때 left[i]-1 필요한지 확인하기
        - 잘못 썼다 주어진 식은 right-left-1인데 이렇게 해야 하는 이유는 우리의 left가 직관적으로 계산했을 때 대비 1칸씩 더 작다. 범위가 하나 늘어난 셈이기 때문에 left의 하방을 하나 올려줘야 한다
        - right-(left+1)의 의미에서 right-left-1이 필요하다
        
- 근데 while loop 순회하면 공간은 적게 쓰고 시간은 많이 쓴다
    - [ ]  dietpepsi의 시간 적게 쓰는 solution 확인(stack)
- [[Recursion II](https://leetcode.com/explore/learn/card/recursion-ii/) ](Recursion%20II%20295b3c8068a5427a847db92fc8561127.md) conclusion에서 다시 복습
    - 재귀를 쓰라는 것
        - 근데 historgram이라 for loop이랑 별로 차이가 없는 듯?
    - divide & conquer 같은데 왜냐면 답이 하나로 정해져있으니까?
    - 모르겠다