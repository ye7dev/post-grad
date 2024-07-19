# 629. K Inverse Pairs Array

Status: done, in progress, incomplete, no idea 🤷‍♀️, 🏋️‍♀️
Theme: DP
Created time: February 7, 2024 10:59 PM
Last edited time: February 13, 2024 8:51 PM

- Progress
    - 문제 이해
        - integer array nums
        - inverse pair : [i, j]
            - 0 ≤ i < j < len(nums)
            - nums[i] > nums[j]
            - index 상으로는 i가 더 작지만, 값은 nums[i]가 더 크다
        - n, k가 주어질 때
            - 숫자 1~n으로 이루어진 서로 다른 array의 숫자를 개수를 구하라
                - 근데 그 array에는 정확히 k개의 Inverse pair가 있어야 함
            - modulo 연산 적용
        - 값이 오름차순으로 증가하면 inverse pair가 0개
            - 1, 2/ 2, 3/ 1, 3 모두 오른쪽 값이 더 크다
    - 과정
        - [1, 3, 2] 우선 나올 수 있는 pair가
            - 1, 3/ 1, 2/ 3, 2
                - 3, 2만 Inverse pair
            - 맨 앞에 있는 index는 len(nums)-1개의 pair를 갖고…
                
                → ith idx: nums[i+1:]의 원소와 짝을 이룰 수 있으므로 len(nums)-(i+1)개의 pair 형성 가능 
                
            - ith idx 기준으로
                - nums[i-1]에 자기보다 큰 원소가 없으면 Inverse pair가 0개
                - nums[i-2]에 자기보다 큰 원소가 없고, nums[i-1]만 자기보다 크면 Inverse pair가 1개
                    - nums[i-1] > nums[i]
                    - nums[:i-1] < nums[i]
                - nums[i-3]에 자기보다 큰 원소가 없고, nums[i-2]> nums[i-1] > nums[i] 이면 Inverse pair가 총 3개
                    - nums[i-2] > nums[i]
                    - nums[i-2] > nums[i-1]
                    - nums[i-1> nums[i-1]
            - ith idx 기준으로
                - nums[i-1]의 모든 원소가 자기보다 작은 범위의 오름차순, nums[i+1]의 모든 원소가 자기보다 큰 범위의 오름차순이면 inverse pair가 0
                - nums[i-2]의 모든 원소가 자기보다 작은 범위의 오름차순, nums[i+1]의 모든 원소가 자기보다 큰 범위의 오름차순이면, nums[i-2] < nums[i-1] > nums[i] < nums[i+1]
            - n이 모두 내림차순 정렬이면 inverse pair는 max 개수
                - for i in range(n):
                    - for j in range(i+1, n):
                - n(n-1)/ 2
            - n이 모두 오름차순 정렬이면 inverse pair는 min 개수: 0
            - n = 2
                - num_inverse: 1 (2, 1)
                - num_order: 1 (1, 2)
            - n = 3
                - 3이 붙을 수 있는 위치는
                    - 맨 앞
                        - 맨 앞 + inverse pair: 내림차순 정렬이라서 max, 3 (3, 2, 1)
                        - 맨 앞 + order pair: 2 (3, 1, 2)
                    - 맨 뒤
                        - inverse pair + 맨 뒤: 그대로 1개 유지. (2, 1, 3)
                        - order pair + 맨 뒤 : 오름차순 정렬이라서 0. (1, 2, 3)
                    - 중간
                        - inverse pair 중간: (2, 3, 1) → 2개
                        - order pair 중간: (1, 3, 2) → 1개
                    - 다 합하면
                        - 3 + 2 + 1 + 0 + 2 + 1 = 9
            - n = 4
            - 
                
                
    - 재도전
        - 재귀식이 총 2개 있는 것과 다름 없었음
        - [1, 2, …, n]
            - default state, ascending order라서 inverse pair 없음
            - 여기서 2를 앞으로 보내면
                - [2, 1, …, n]
                - [1, … n]까지는 ascending order라서 inverse pair 없음
                - [2, 1] 1개 존재
                    - 2를 왼쪽으로 1칸 이동했기 때문
            - 여기서 4를 앞으로 보내면
                - [4, 1, 2, 3, 5, …, n]
                - [5, …, n]까지는 ascending order라서 inverse pair 없음
                - [4, 1, 2, 3]에서는 3개 나옴
                    - 4를 왼쪽으로 3칸 이동했기 때문에
            - [1, 2, 3, 4] → [2, 1, 4, 3]
                - inverse pair: [2, 1], [4, 3] 2개
                    - 4를 왼쪽으로 1칸, 2를 왼쪽으로 1칸 총 2칸 이동했기 때문에
            - 근데 그냥 숫자 하나를 옮기는 경우를 생각해보면
                - 숫자 i를 옮긴다고 할 때 i를 왼쪽으로
    
- Trial
    - Top-down → 12/81
        
        ```python
        class Solution:
            def kInversePairs(self, n: int, k: int) -> int:
                memo = {}
                # function
                def recur(i, j):
                    # check memo
                    if (i, j) in memo:
                        return memo[(i, j)]
                    # base case 
                    if i == 0: # no pair out of zero elements
                        return 0 
                    if j == 0: # sorted in ascending order -> no inverse pair
                        return 1 
                    # recurrence relation
                    ans = 0 
                    for new_j in range(min(j, i-1)+1): # 0 <= j <= min(n-1, k)
                        ans += recur(i-1, new_j)
                    memo[(i, j)] = ans
                    return memo[(i, j)]
                
                return recur(n, k)
        ```
        
    - Top-down → TLE (35/81)
        
        ```python
        class Solution:
            def kInversePairs(self, n: int, k: int) -> int:
                mod = 10 ** 9 + 7
                memo = {}
                # function
                def recur(i, j):
                    # check memo
                    if (i, j) in memo:
                        return memo[(i, j)]
                    # base case 
                    if i == 0: # no pair out of zero elements
                        return 0 
                    if j == 0: # sorted in ascending order -> no inverse pair
                        return 1 
                    # recurrence relation
                    ans = 0 
                    for new_j in range(min(j, i-1)+1): # 0 <= j <= min(n-1, k)
                        ans += recur(i-1, j-new_j) % mod
                    memo[(i, j)] = ans % mod
                    return memo[(i, j)]
                
                return recur(n, k)
        ```
        
    - Bottom-up → TLE
        
        ```python
        class Solution:
            def kInversePairs(self, n: int, k: int) -> int:
                mod = 10 ** 9 + 7
        
                dp = [[0] * (k+1) for _ in range(n+1)]
        
                ''' 
                base case 1 - auto covered
                for j in range(k+1):
                    dp[0][j] = 0
                '''
        
                # base case 2 - ascending sorting -> no inverse pairs
                for i in range(n+1):
                    dp[i][0] = 1
                
                # recurrence relation
                for i in range(1, n+1):
                    for j in range(1, k+1):
                        for new_num in range(min(j, i-1)+1):
                            dp[i][j] = (dp[i][j] + dp[i-1][j-new_num]) % mod
        
                return dp[n][k]
        ```
        
    - (post-edit) Bottom-up → 예제 1
        
        ```python
        class Solution:
            def kInversePairs(self, n: int, k: int) -> int:
                mod = 10 ** 9 + 7
                # array
                dp = [[0] * (k+1) for _ in range(n+1)]
                # base case
                for i in range(1, n+1):
                    dp[i][0] = 1 # ascending order
        
                for i in range(1, n+1):
                    for j in range(1, k+1):
                        dp[i][j] = (dp[i][j-1] + dp[i-1][j]) % mod
                        if j - i >= 0:
                            dp[i][j] = (dp[i][j] - dp[i-1][j-i]) % mod
                
                return dp[n][k]
        ```
        
- Editorial
    - Brute Force
        - 1부터 n까지 모든 permutation 구한 다음, 각 조합에서 inverse pair 개수 세고, 거기서 k개인 조합이 몇 개인지 센다
        - n개의 원소가 있을 때 n!개의 permutations 생성 가능
        - 하나의 permutation에서 inverse pair 개수는 merge sort algorithm 변형해서 셀 수 있다고 함?(그래서 시간 복잡도가 O(nlogn)
            - merge step - 두 sorted halves가 하나의 single sorted array로 합쳐지는 과정
            - merge 단계에서 right half 쪽의 element가 left half 쪽의 element 보다 더 앞에 오게 되면 left half에 남아 있는 모든 element와 inverse pair를 형성하게 됨
        - 예) left half = [2, 5], right half = [1, 3]
            - 2랑 1이랑 비교 → 1이 먼저 옴
            - 1은 right half로 부터 왔고, 2보다 작으므로 left half의 모든 원소보다 작은 값
            - 근데 index 자체는 left half의 모든 원소가 1보다 작다
            - 따라서 1과 모든 left half 원소는 inverse pair를 만들 수 있다
    - **Approach 2: Using Recursion with Memoization**
        - 임의의 array b with some n (1~n 사이의 숫자가 array element)→ 새로운 원소 n+1를 array b의 p steps from the right 의 자리에 넣으면 → 기존 array b가 가지고 있던 inverse pair 개수(x라고 하자)에 p개의 inverse pair가 추가되는 셈 → x + p = k 일 때 우리가 원하는 답을 얻을 수 있음
            - non-zero k에 대해 arrangement를 생성하기 위해서는, a_0에서 x개의 원소를 왼쪽으로 옮겨야
                - n =4, k = 0의 경우에 만족하는 array a_0은 [1, 2, 3, 4]
                - 이 때 각 shift s_1, …, s_x이 일 때, 이 shift들(?)의 합이 k가 되어야 함
                - 예) [1, 2, 4, 3] → inverse pair 개수는 1
                    - shifting 4 by one position towards the left
                - 예) [2, 4, 1, 3]
                    - a_0 → 2를 왼쪽으로 한칸 shift → 4를 왼쪽으로 두 칸 shift
                        - [1, 2, 3, 4] → [2, 1, 3, 4] → [2, 4, 1, 3]
                    - total number of displacement(개별 숫자들이 왼쪽으로 이동한 횟수) : 3 = # of inverse pairs in the new array
            - 오름차순 정렬에서 시작해서, 개별 숫자들이 왼쪽으로 이동한 횟수의 합 == k가 되어야 한다는 법칙
                - 어떤 숫자가 왼쪽으로 y번 이동하고 나면, 이 숫자보다 작은 y개의 숫자들이 어떤 숫자의 오른쪽에 위치하게 됨 → shift 한 숫자와, y개 숫자들은 모두 inverse pair 형성 가능 → 전체 y개의 inverse pairs
                    - 4가 왼쪽으로 1번 이동하고 나면, 이 숫자보다 작은 1개의 숫자(3)이 4의 오른쪽에 위치하게 됨 → (4, 3)은 inverse pair 형성
            - 예) a_3 = [2, 4, 1, 3], k=3의 경우
                - n=5인 array를 고려하기 위해 a_3에 새로운 숫자 5를 더하고 싶으면, 5를 a_3의 맨 마지막에 붙인다 → [2, 4, 1, 3, 5]
                - 가장 큰 숫자가 마지막에 붙었기 때문에, 새로운 숫자 5는 새로운 inverse pair를 만들지 못한다. 여전히 a_3이던 상태와 마찬가지로 inverse pair 숫자는 3으로 유지
                - a_3의 모든 숫자는 5보다 작다 → 5를 y steps from the right에 추가하면, 5보다 작은 y개의 숫자가 5의 오른쪽에 위치하게 된다
                    - 예) 5를 맨 오른쪽 끝인 index = 4 → index = 2로 2칸 왼쪽으로 이동시키면, 5보다 작은 숫자 2개(1, 3)이 5의 오른쪽에 위치하고, 따라서 2개의 inverse pair를 새로 만들 수 있다 [2, 4, 5, 1, 3]
                    
                    ⇒ 5를 y steps from the right에 추가하면 기존 a_3의 inverse pair 개수 3 + 새로 만들어진 y개로 늘어나게 된다 
                    
            - n개 element로 k개의 inverse pair를 만들 수 있는 arrangement의 개수를 세는 것은 어렵지 않다
                - 이를 확장해서 count_k를 정의해보면
                    - 주어진 element 범위가 1~n-1(총 n-1개)이고, 이 array의 여러 arrangements(permutations 말하는 거겠지?) 중
                    - inverse pair의 개수가 0, 1, 2, …,k를 만족하는 조합의 개수를
                    - count_0, count_1, …, count_k라고 하자
                - 기존 n-1개의 element로 k개의 inverse pair를 만들던 모든 arrangement 맨 뒤에 새로운 숫자 n (max)를 붙이기만 하면 된다
                    - 제일 큰 숫자가 마지막에 붙으면 새로 만들어지는 inverse pair는 없다
                - 기존 n-1개의 element로 k-1개의 inverse pair를 만들던 모든 arrangement에서 출발해서, 새로운 숫자 n을 1 steps from the right 자리에 넣으면
                    - n보다 작은 하나의 숫자가 n의 오른쪽에 있게 되고, 따라서 새로운 inverse pair가 하나 더 생긴다
                    - 그럼 k-1+1 = k개의 inverse pair를 만족
                - … 기존 n-1개의 element로 k-i개의 inverse pair를 만들던 모든 arrangement에서 출발해서, 새로운 숫자 n을 i steps from the right 자리에 넣으면
                    - n보다 작은 i개의 숫자가 n의 오른쪽에 위치하기 때문에, 새로운 inverse pair를 i개 더 만들 수 있고
                    - 총 inverse pair 개수는 k-i + i = k로 조건을 만족한다
                - 그림 (n= 5, k = 4)
                    
                    ![Untitled](Untitled%20212.png)
                    
                - 정리하면 n개의 숫자로 k개의 inverse pair를 만드는 arrangement의 개수는
                    - count_0 + count_1 + … + count_k
        - state definition
            - count(i, j): i개의 elements로 j inverse pair를 만드는 arrangements의 개수
        - base case
            - i = 0 → count(0, k) : 0
            - j = 0 → count(n, 0) : 1 (오름차순 정렬)
        - state transition
            - count(n, k) += count(n-1, k-i)
                - 이 때 k-i는 음수가 될 수 없음 → k-i ≥0 → i ≤ k
                - i의 또 다른 상한선은 n-1
                    - n번째 숫자를 추가하면서 추가로 i개의 inverse pair를 만들기 위해서는, n을 i steps from the right의 자리에 넣어야 함
                    - n을 제일 왼쪽으로 보낸다고 해도, n의 오른쪽에 올 수 있는 숫자의 최대 개수는 n-1개 → 추가할 수 있는 최대 inverse pair 개수도 n-1
                        
                        → i ≤ n-1 
                        
                
                ⇒ 따라서 0 ≤ i ≤ min(k, n-1)
                
        
    - **Approach 4: Dynamic Programming with Cumulative Sum**
        - 재귀식에 따르면, 현재 dp cell을 채우기 위해 이전 row의 일부분으로 돌아가야 함
            
            ```python
            for new_num in range(min(j, i-1)+1):
            		dp[i][j] = (dp[i][j] + dp[i-1][j-new_num]) % mod
            ```
            
        - traversing back 대신에 현재 element까지의 cumulative sum을 구하는 접근법
            
            ```python
            dp[i][j] = count(i, j) + (dp[i][k] for k in range(j))
            ```
            
            - count(i, j) : i개의 element로 j개의 inverse pair를 만드는 arrangement의 개수
            - 따라서 각 cell의 값은 ← dp[i][j]
                - 자기 자신의 결과에다가 ← count(i, j)
                - 같은 row에 있는 ← dp[i]
                - 모든 이전 element의 sum을 포함하게 된다 ← sum(dp[i][0] +… + dp[i][j-1])
            - 각 cell의 값이 cumulative sum을 의미하기 때문에, count(i, j)의 값을 얻기 위해 traversing 할 필요가 없다
                - dp[i-1][j-i+1] + dp[i-1][j-i+2] + … + dp[i-1][j-1] + dp[i-1][j]의 합을 얻기 위해서는 dp[i-1][j] - dp[i-1][j-i]를 쓰면 된다
                - dp[i-1][j] = dp[i-1][0] + … + dp[i-1][j-i] + dp[i-1][j-i+1] + … + dp[i-1][j-1] + dp[i-1][j]
                - dp[i-1][j-i] = dp[i-1][0] + … + dp[i-1][j-i-1] + dp[i-1][j-i]
                
                ---
                
                = dp[i-1][j] - dp[i-1][j-1] = dp[i-1][j-i+1] + … + dp[i-1][j-1] + dp[i-1][j] 
                
        - 이전 재귀식에서 min(*j*,*i*−1) 조건은 어떻게 반영되는가? (???)
            
            ```python
            for new_num in range(min(j, i-1)+1):
            		dp[i][j] = (dp[i][j] + dp[i-1][j-new_num]) % mod
            ```
            
            - new_num = 0 → dp[i-1][j]
            - new_num = 1 → dp[i-1][j-1]
            - … new_num = j → dp[i-1][0]
            
            = 다 더하면 dp[i-1][j] + … + dp[i-1][0] 
            
            ---
            
            - … new_num = i-1 → dp[i-1][j-i+1]
            
            = 다 더하면 dp[i-1][j] + … + dp[i-1][j-i+1]
            
            ↳ cumulative sum을 담는 버전에서  dp[i-1][j] - dp[i-1][j-1]의 내용물과 동일 
            
            ↳ j, j-1, …, j-i+1 에 -j+i 하면 i, i-1, …, 1 → 총 i개의 element
            
            - 이해 안가는 원문
                
                ![Untitled](Untitled%20213.png)
                
        - 새로운 재귀식에서 보면
            
            ```python
            dp[i][j] = count(i, j) + (dp[i][k] for k in range(j))
            ```
            
            - min(j, i-1) = i-1인 경우
                - j개의 새로운 inverse pair를 추가하기 위해서는, i를 새로운 숫자로 jth position에 넣을 때 가능 ( j steps from the right 이야기 하는 건가?)
                    - j의 최대값은 i-1. 왜냐면 새로운 숫자가 i일 때, i보다 작은 숫자는 i-1, …, 1 총 i-1개
                    - 따라서 dp[i-1][j-(i-1)], dp[i-1][j-(i-2)], … dp[i-1][j]까지의 값이 필요 → 이 값은 dp[i-1][j] - dp[i-1][j-i]를 통해 구할 수 있음
                        - 단 이때 j-i ≥ 0 ???
                        - min(j, i-1) = i-1 → j > i-1
            - min(j, i-1) = j인 경우
                - dp[i-1][j] + … + dp[i-1][0]
        - 최종적으로 구해야 하는 답은 count(n, k)라서 dp[n][k] - dp[n][k-1]로 구할 수 있음
        - 
- CumSum 관련 추가 정리
    - dp[3][3]은 1, 2, 3을 가지고 inverse pair를 최대 3개 갖는 경우의 수
        - inverse pair를 0개, 1개, 2개, 3개 갖는 경우의 수가 모두 누적된 상태
    - 우리는 dp[i][j-1] + val로 이 값을 구하려고 하는데
        - dp[3][2]는 1, 2, 3를 가지고 inverse pair를 최대 2개 갖는 경우의 수
        - val로 넘어 와서 j-i = 3-3 = 0
            - dp[i-1][j] - dp[i-1][j-i]
            - dp[i-1][j] = dp[2][2]
                - 1, 2를 가지고 inverse pair를 최대 2개 갖는 경우의 수
                - 근데 1, 2로는 inverse pair를 0, 1개 밖에 만들 수 없음
            - dp[i-1][j-i] = dp[2][0]
                - 1, 2를 가지고 inverse pair를 0개 만드는 경우의 수 = 1
                - 이 경우에는 3을 가지고 온다고 해도 inverse pair를 정확히 3개 만들 수 없음
                    - [1, 2] → [3, 1,2]는 2개, [1, 2, 3]은 0개
            - 위에서 아래를 빼면 1, 2를 가지고 inverse pair를 1개 만드는 경우의 수만 남게 됨
                - 이 경우에야만 3을 추가해서 inverse pair를 정확히 3개로 만드는 전단계가 될 수 있기 때문에
                - [2, 1] → [3, 2, 1]은 3개 가능. [2, 1, 3]은 1개 가능
                    - [2, 1,3]은 dp[3][2]에 포함되어 있으니 중복 count가 아닌가?
- AC 코드
    
    ```python
    class Solution:
        def kInversePairs(self, n: int, k: int) -> int:
            mod = 10 ** 9 + 7
            # array
            dp = [[0] * (k+1) for _ in range(n+1)]
            # base case
            for i in range(n+1): # alert: i = 0 can make zero pairs too!!
                dp[i][0] = 1 # ascending order
    
            for i in range(1, n+1):
                for j in range(1, k+1):
                    dp[i][j] = (dp[i][j-1] + dp[i-1][j]) % mod
                    if j - i >= 0:
                        dp[i][j] = (dp[i][j] + mod - dp[i-1][j-i]) % mod
            
            return dp[n][k]
    ```