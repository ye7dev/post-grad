# 446. Arithmetic Slices II - Subsequence

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP
Created time: February 4, 2024 5:26 PM
Last edited time: February 5, 2024 10:44 AM

- Progress
    - 문제 이해
        - arithmetic: 최소 세 개의 원소로 구성. 연속된 두 숫자 사이의 차가 모두 같아야 함
        - 예) [1, 3, 5, 7, 9], [7, 7, 7, 7]
        - subsequence : 원소 순서는 안 바꾸고 그 중에 몇 개를 빼거나 하는 식으로 생성
        - 모든 arithmetic subsequence ‘개수’를 구하라
    - 과정
        - 정렬이 되어 있을까? 아니 예시에 [3, -1, -5, -9]도 있다
        - [2, 4, 6, 8, 10]
            - [8, 10] → 2
                - 원소가 두 개라서 base case일 듯
            - [6, 8, 10] → 3개
            - [4, 8, 10] → 안됨
        - mask로 들고 다녀야 하나?
        - subproblem을 찾자
            - 시작점 끝점으로 해야 할까
        - 다른 원소 돌면서 10에서 4 차이 나는 원소를 찾으면 그 Index의 dp 값에 + 1 하는 식…
        - max-min을 최대 차로 두고 하는 건 원소 범위가 너무 큰데
            - `-2^31 <= nums[i] <= 2^31 - 1`
        - recur(start, end, diff)?
        - 어쨌든 주어진 원소 순서를 바꿀 순 없으니
            - 2 4 6 8 10
            - 4 6 8 10
            - …
            - 8 10
            - 10
            - 여기서 찾아야 겠네
        - 8 10 → 차이 2
        - 6 8 10
        - 사전을 초기 원소로 해서 List comprehension 가능. 어느 하나의 key, value 값 바꿔도 다른 index의 사전에는 변화 없다
            
            ```python
            >>> x = [{} for _ in range(3)]
            >>> x[0]
            {}
            >>> x[0]['apple'] = 'red'
            >>> x
            [{'apple': 'red'}, {}, {}]
            ```
            
- AC 코드
    
    ```python
    from collections import defaultdict 
    class Solution:
        def numberOfArithmeticSlices(self, nums: List[int]) -> int:
            ans = 0
            n = len(nums)
            # key: common difference, value: # of weak arithmetic subsequences 
            dp = [defaultdict(int) for _ in range(n)]
    
            for i in range(n):
                for j in range(i):
                    diff = nums[i] - nums[j]
                    num_arith = dp[j].get(diff, 0)
                    dp[i][diff] += (num_arith + 1)
                    ans += num_arith 
            
            return ans
    ```
    
- Editorial
    - **Approach #2 Dynamic Programming [Accepted]**
        - Intuition
            - parameter 2개 필요
                - first(last) element of the sequence, common difference
        - Algorithm
            - status quo 개념들
                - state definition `dp[i][d]`
                    - 공통의 차가 d이고, 마지막 원소가 array[i]인(?아니면 array[i]까지 고려하는) subsequence의 개수
                - state transition
                    - 현재 존재하는 subsequence에 새로운 원소 array[i] 추가를 고려하는 상황
                    - subsequence의 마지막 원소와 array[i]의 차가 공통의 차 d와 동일하면 추가할 수 있음
                - 재귀식으로 표현하면
                    - `for j < i`
                    - `d = arr[i] - arr[j]`
                    - `dp[i][d] += d[j][d]`
                    - i가 j보다 뒤에 오는 원소임
                - d 값에 따라 다양한 j가 있을 수 있음
                    - i까지의 subsequence 개수는 그 모든 j에 대한 subsequence 개수를 다 합친 것
                    - 왜냐면 subsequence의 길이를 물어본게 아니라 그냥 i를 기존 j까지의 subsequence에 붙이기만 하면 되기 때문에 subsequence 숫자가 늘어나지 않는다
            - 문제
                - 근데 dp[j][d]가 0인 경우는 더해도 0이고, 우리의 dp table cell 초기값은 모두 0일텐데?
                    - no existing subsequences before 상태에서 어떻게 새로운 arithmetic subsequence를 형성?
                - 초기 정의에 따르면 subsequence의 길이는 최소 3이어야 한다고 했음
                    - index가 두 개(i, j)만 주어지는 상황에서 새로운 sequence 생성하기 힘듦. (?)
                    - length 2인 subseq도 취하는 게 어떨까(?)
            - 새로운 개념 정의 - weak arithmetic subsequences
                - 최소 두 개의 원소로 구성되어 있으며, 붙어 있는 아무 두 원소 간의 차가 모두 동일한 subsequence
                - 원소 길이에 대한 제약이 줄어듦
                - 유용한 점
                    1. 모든 pair에 대해서 arr[i], arr[j]는 언제나 weak arithmetic subsequence를 형성한다 
                    2. 하나의 weak arithmetic subsequence에 새로운 원소를 추가하고도 stay arithmetic 하면, (원소가 이제 3개가 되었으므로) weak가 아닌 정식 arithmetic subsequence가 된다 
                        - 당연하지. weak ari~와 그냥 ari~는 subsequence 길이 차이 밖에 없기 때문에
            - 새로운 개념 적용
                - state definition
                    - `dp[i][d]`  : array[i]를 마지막 원소로 하면서 공통인 d인 weak arithmetic subsequence 개수
                - state transition
                    - j < i
                    - `dp[i][d] += (dp[j][d] + 1)`
                    - +1의 의미
                        - weak arithmetic subsequence의 첫번째 특징에 따라
                        - [arr[i], arr[j]] 만으로도 하나의 weak arithmetic subsequence 형성할 수 있기 때문에
                - weak arith_subseq의 개수에서 어떻게 normal arith_subseq 개수 구하지?
                    1. pure weak - 길이가 2인 subseq -의 개수를 직접적으로 세기 (그리고 나서 전체 weak arith_subseq 개수에서 1을 빼는 것 ?)
                        - 원소가 두 개인 pair만 고르면 되니까 nC2 = n(n-1)
                    2. 재귀식에서
                        - `dp[j][d]` 는 현재 존재하는 weak arithmetic subseq의 개수
                        - vs. +1은 arr[i], arr[j]로 새롭게 만들어지는 pure weak arith subseq 개수
                        - weak arith의 두번째 특징에 따르면, weak에 새로운 원소를 하나 추가하면 (원소가 3개 이상이 되기 때문에) normal arith를 만드는 것
                        - 따라서 재귀식 중 앞부분 `dp[j][d]` 은 원소를 하나 추가함으로써 얻게 되는 normal arith 개수를 의미
            - 예시
                
                arr : [1, 1, 2, 3, 4, 5]
                
                - i = 0 → 앞에 원소가 없기 때문에 ans(normal arith subseq 개수)= 0
                - i = 1 → 앞에 원소 1, 현재 원소 1 간의 차이는 0 → 이 원소 두 개로 하나의 weak arith subseq 형성 가능
                    - normal의 개수는 여전히 0
                    - `0 : [1, 1]`
                - i = 2 → 앞서 만들어진 weak arith subseq의 공통 diff가 0이라서 이 뒤에 붙을 수 없음
                    - ans = stay 0
                    - 하지만 weak arith subseq는 만들 수 있다
                        - `1: [1, 2], [1, 2]`
                            - index로 따지면 (0, 2), (1, 2)
                - i = 3 → 3- 2 = 1 →
                    1.  weak arith subseq에 append 해서 normal 만들 수 있다
                        - ans += dp[2][1] (2)
                        - 마지막 원소가 arr[2]에서 끝나면서 공통의 차가 1인 pure weak 두 subseq에 3을 각각 append 함으로써 두 개의 normal arith subseq가 생긴다
                    2. i보다 작은 j는 0, 1, 2 이 세 개에 대해 i, j pair로 새로운 weak arith subseq 만들 수 있다 
                        - `2: [1, 3], [1, 3]`
                            - index로 따지면 (0, 3), (1, 3)
                        - `1: [2, 3]`  (앞서서 만들어진 subseq list에 추가)
                - 이후의 과정
                    
                    ![Untitled](Untitled%20210.png)