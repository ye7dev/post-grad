# 321. Create Maximum Number

Status: in progress, 👀1
Theme: DP
Created time: November 15, 2023 4:29 PM
Last edited time: November 16, 2023 3:26 PM

- sum이 큰쪽으로 움직이는 거랑 비슷하지 않을까?
    - 오름차순은 아니다 그냥 원래 순서를 거역하지 않으면서 제일 큰 k개를 모으는 것
- 다들 어렵다고 혀를 내두르는 문제…근데 해설봐도 잘 모르겠다 우선 해설을 옮겨보자
    - 진짜 핵어렵다
- 무지성 [해설](https://web.archive.org/web/20160120093629/http://algobox.org/create-maximum-number/) 번역
    - 두 가지의 sub 문제로 해결할 수 있음
        1. 한 array의 maximum number(?)를 생성 
        2. 모든 숫자(?)를 사용해서 두 array의 maximum number(?)를 생성 
    - (algo1) 길이 n의 array가 주어질 때, length k의 maximum number를 생성
        - Greedy + stack
        - 빈 stack을 초기화
        - 주어진 array nums를 돌면서
            - stack의 맨 마지막 요소(top)가 nums[i]보다 작으면 계속 pop해 나가다가
                - stack에 더 이상 숫자가 남아 있지 않거나
                - stack에 남은 숫자의 개수가 k보다 작으면 stop
                
                → 코딩으로 구현할 때는 검은 네모 두 개가 while loop 조건으로 먼저 오고, 상위 흰색 동그라미가 while loop 하위로 구현됨. 바꿔서 구현할 수도 있음 
                
                ```python
                while stack and len(stack) >= k: # 두 가지 조건 한꺼번에 넣어도 되지 않나? 
                	if nums[i] > stack[-1]:
                			stack.pop() 
                
                # 아니면
                while nums[i] > stack[-1]:
                	stack.pop()
                	if len(stack) < k: break 
                ```
                
            - stack size가 k보다 작으면 push nums[i]
        - 마지막에 return stack
        - java code python으로 번역
            
            ```python
            def maxArray(nums, k)
            	n = len(nums)
            	stack = []
            	for i in range(n):
            		while stack and (n-i+len(stack)) > k and stack[-1] < nums[i]:
            			stack.pop() 
            		if len(stack) < k: 
            			stack.append(nums[i])
            	return stack 
            ```
            
        - 예시
            
            nums = [9, 1, 2, 5, 8, 3], k = 3 (n=6)
            
            | i | len(stack) | nums[i] | n-i+len(stack) | stack[-1] | push | pop | stack |
            | --- | --- | --- | --- | --- | --- | --- | --- |
            | 0 | 0 | 9 | 6-0+0=6 |  | yes |  | [9] |
            | 1 | 1 | 1 | 6-1+1=6 | 9 | yes |  | [9, 1] |
            | 2 | 2 | 2 | 6-2+2=6 | 1 |  | yes | [9] |
            |  | 1 |  |  |  | yes |  | [9, 2] |
            | 3 | 2 | 5 | 6-3+2=5 | 2 |  | yes | [9] |
            |  | 1 |  |  |  | yes |  | [9, 5] |
            | 4 | 2 | 8 | 6-4+2=4 | 5 |  | yes | [9] |
            |  | 1 |  |  |  | yes |  | [9, 8] |
            | 5 | 2 | 3 | 6-5+2=3 |  |  |  |  |
            |  | 2 |  |  |  | yes |  | [9, 8, 3] |
            |  |  |  |  |  |  |  |  |
            
        - n-i+len(stack) > k의 의미
            - len(stack): 이미 채운 숫자
            - n-i
                - 예) n=6, i =5 → n-i = 1 : 이번 index 숫자 하나 남은 거
                - 예) n=6, i =4 → n-i = 2 : 이번 index에 해당하는 숫자 하나랑(nums[4]) + 아직 for문 안 돌은 숫자 (nums[5]) 총 2개
            - n-i+len(stack)
                - 아직 stack top이랑 비교 안한 탐색 전 숫자 개수 + 이미 stack에 포함된 숫자 개수 > 채워야 하는 숫자 개수
        - 정리하면 stack pop 하는 경우는 세 가지 조건을 모두 충족해야 함
            1. stack에 원소가 있는 경우
            2. 탐색 전 숫자 개수 + 이미 stack에 들어 있는 숫자 개수가 채워야 하는 숫자 보다 큰 경우 
            3. stack top이 이번에 탐색하는 숫자보다 작을 경우 
    - (algo2) 각각 길이가 m, n인 array 두 개가 주어질 때, k= m+n개인 길이의 maximum number를 생성
        - 321번은 k ≤ m+n인데 비해, 이 상황에서는 주어진 모든 숫자를 사용
        - 해야 하는 판단은 총 k번 - 각 상황에서 maximum number array(stack or whatever)에 이번에 들어갈 요소가 두 array 중 어디서 오는 건지 판단하면 됨 → 당연히 두 원소 중 더 큰 걸 집어넣으면 되는데(요고는 merge sort랑 비슷하기도), 문제는 같은 경우는 어떻게?
        - 두 원소가 같은 경우, 각자 속한 array에서 그 다음으로 오는 숫자의 값을 비교
            - 예를 들어 matt = [6, 7, …], johnny = [6, 0, …] 일 때, 이번에 넣을 6은 matt에게서 가져와야. matt에서 6 다음에는 7이 오지만, johnny에서는 다음에 0이 옴
            - 만약 뒤의 원소도 같은 경우는 다음으로 다른 숫자가 나올 때까지 각자의 뒤를 계속 이어서 봄
                - [6, 5, 4, 3, 7] vs. [6, 5, 4, 3, 9] 중 어디에서 6을 가져와야 하는지 보려면 5, 4, 3 같은 숫자는 계속 제끼고, 7 ≠ 9 까지 도달. 그리고 9가 더 크기 때문에 두번째 array에서 6을 가져오기로 한다
        - java code translation
            
            ```python
            def merge(nums1, nums2, k):
            	res = []
            	i, j = 0, 0
            	for _ in range(k): # or while len(res) < k
            		if get_front(nums1, i, nums2, j):
            			res.append(nums1[i])
            			i += 1 
            		else:
            			res.append(nums2[j])
            			j += 1 
            	return res  
            
            def get_front(nums1, i, nums2, j):
            	while i < len(nums1) and j < len(nums2) and nums[i] == nums2[j]:
            		i += 1 
            		j += 1
            	if j == len(nums2): # nums1도 끝났더라도 둘다 끝났을 때는 nums1에서 가져감 
            		return True 
            	if i < len(nums1) and nums1[i] > nums2[j]:
            		return True
            	# nums1만 먼저 끝났거나 둘 다 안 끝났는데 nums2 숫자가 더 크거나 
            	return False 
            ```
            
    - 두 solution을 합해서 이 문제를 풀어보면
        - guide
            1. 채워야 하는 숫자 k개를 두 개의 subpart로 나눈다- i, k-i
                - 각 subpart를 algo1을 이용해서 생성
                - part (i): 한 array에서 길이 i만큼의 maximum number를 생성
                - part (k-i): 다른 array에서 길이 i-k 만큼의 maximum number 생성
            2. algo2를 이용해서 part (i)와 part(k-i)를 합친다
            3. 우리가 갖고 있는 결과(?)와 비교해서 더 큰 걸 최종 답으로 return(?) 
        - java code 번역
            
            ```python
            def maxNumber(nums1, nums2, k):
            	m, n = len(nums1), len(nums2)
            	res = [] 
            	for i in range(max(0, k-n), min(k, m)+1):
            		tmp1 = maxArray(nums1, i) 
            		tmp2 = maxArray(nums2, k-i)
            		cand = merge(tmp1, tmp2, k) 
            		# 처음으로 두 array의 원소 값이 서로 다른 지점에서 cand의 값이 더 크면 
            		if get_front(cand, 0, res, 0): 
            			res = cand 
            	return res 
            ```
            
            - `max(0, k-n), min(k, m)+1` 이건 또 뭐람?
                - nums1에서는 i개의 숫자를 가져와야 하고
                    - i ≤ len(nums1) → 0≤ i ≤ m
                - num2에서는 k-i개의 숫자를 가져와야 한다
                    - k-i ≤ len(nums2) →  k ≤ i+n → k - n ≤ i
                - 두 조건을 모두 결합하면 k-n ≤ i ≤ m
            - 한 번 해봐야 한다
                
                `nums1 = [3,4,6,5], nums2 = [9,1,2,5,8,3], k = 5`
                
                m = 4, n = 6
                
                max(0, k-n) → max(0, -1) = 0
                
                min(k, m) + 1 → min(5, 4) + 1 =5
                
                - nums1: `[3,4,6,5]`
                
                | k | i | n-i+len(stack) | stack |
                | --- | --- | --- | --- |
                | 0 |  |  | [] |
                | 1 |  |  | [6] |
                | 2 |  |  | [6, 5] |
                | 3 |  |  | [4, 6, 5] |
                | 4 |  | 4-4 = 0 | [3, 4, 6, 5] |
                - nums2: `[9,1,2,5,8,3]`
                
                | k-i | i | n-i+len(stack) | stack |
                | --- | --- | --- | --- |
                | 5 | 3 | 6-3+2=5 | [9, 2, 5, 8, 3] |
                | 4 | 4 | 6-4+2=4 | [9, 5, 8, 3] |
                | 3 | 5 | 6-5+2=3 | [9, 8, 3] |
                | 2 | 5 | 6-5+2=3 | [9, 8] |
                | 1 | 1 | 6-1+1=6 | [9] |
                - merge
                
                | i | tmp1 | tmp2 | cand | get_cand | res |
                | --- | --- | --- | --- | --- | --- |
                | 0 | [] | [9, 2, 5, 8, 3] | [9, 2, 5, 8, 3] | True | [9, 2, 5, 8, 3] |
                | 1 | [6] | [9, 5, 8, 3] | [9, 6, 5, 8, 3] | True | [9, 6, 5, 8, 3] |
                | 2 | [6, 5] | [9, 8, 3] | [9, 8, 6, 5, 3] | True | [9, 8, 6, 5, 3] |
                | 3 | [4, 6, 5] | [9, 8] | [9, 8, 4, 6, 5] | False | [9, 8, 6, 5, 3] |
                | 4 | [3, 4, 6, 5] | [9] | [9, 3, 4, 6, 5] | False | [9, 8, 6, 5, 3] |
- [x]  해설 더 간결하게 요약
    - 모든 가능한 i에 대해 아래의 동작 반복
        1.  두 array 각각에서 i, k-i 개의 maximum number를 만듦 
            - i의 범위 설정 유의
            - array1의 길이가 m, array2의 길이가 n이라고 할 때
            - i는 m을 넘을 수 없고, k-i는 n을 넘을 수 없음
                - i < m, k-i <n → k-n < i < m
                - 그러는 한편, 0≤ i <k
                - 두 범위를 합치면 max(0, k-n) ≤ i < min(k, m)
                - range로 표기하면 i in range(max(0, k-n), min(k,m)+1)
        2. 각각의 maximum number를 앞에서부터 비교해서 더 큰 숫자가 나오는 대로 cand list에 붙여간다
        3. 이전 iteration에서 만든 res와 cand 중 더 큰 원소가 어디서 더 빨리 나오는지에 따라 res를 업데이트 하거나 말거나 한다 
- [ ]  코드 복기해서 문제 풀기