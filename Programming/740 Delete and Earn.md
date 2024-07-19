# 740. Delete and Earn

- 문제 이해
    - len(nums) 최소 값은 1. 원소가 1개면 그거 터트리고 그 점수 그대로 얻으면 됨
    - 원소가 2개인 경우
        - 두 원소가 같으면 다 점수로 환원
        - 서로 다른 경우
            - 차가 1인 경우
                - 둘 중에 큰 쪽만 점수로 환원되고 나머지는 효용 없이 사라짐
            - 아닌 경우
                - 두 숫자 모두 점수로 환원
    - 내 상태를 나타낼 수 있는 변수는 무엇일까?
        - nums[i]를 삭제했을 때 얻을 수 있는 최대 점수?
            - 근데 이건 현재 원소가 몇 개 남았고 등등에 영향을 받는 걸
- Explore 힌트
    
    1) 전처리 - nums 오름차순으로 정렬하고, 각 값마다 몇 개씩 있는지 count
    
    2) state - dp[i] = i부터 nums array 끝까지 (nums[i:]) 사이에서 얻을 수 있는 최대 점수 
    
    3) recurrence relation - index i에서 두 가지 옵션이 있음
    
    - nums[i]와 같은 숫자를 모두 취하고, skip all nums[i] + 1
    - nums[i]를 취하지 않고 nums[i] + 1의 첫번째 등장 위치로 이동
    
    → 둘 중에 더 높은 점수를 내는 쪽을 선택
    
    +++ 첫번째 옵션이 두번째보다 항상 더 나은 경우는 언제인가? 
    
    4) base case - i = len(nums) 인 경우 더 이상 얻을 수 있는 점수가 없으므로 0
    
- Trial
    - 힌트를 코드로 옮겨서 예제는 통과
        
        ```python
        class Solution:
            def deleteAndEarn(self, nums: List[int]) -> int:
                # preprocessing
                nums.sort()
                count = collections.Counter(nums)
                
                # array
                dp = [0] * (len(nums) + 1)
        
                # recurrence relation
                for i in range(len(nums)-1, -1, -1):
                    cur_num = nums[i]
                    cur_gain = cur_num * count[cur_num]
        
                    first_occurrence = -1
                    skip_position = -1
                    
                    if cur_num + 1 in count:
                        first_occurrence = sum(count[n] for n in range(cur_num+1))
                        skip_position = first_occurrence + count[cur_num+1]
                    dp[i] = max(cur_gain + dp[skip_position], dp[first_occurrence])
                
                return dp[0]
        ```
        
- AC 코드
    - approach 1 보고 코드 짜기 - AC!
        - base case는 recursive 함수 밖에? 안에?
            - 0, 1이 자주 불려질 것을 고려하면 그냥 memo에 넣어놓고
            - memo에 있는 값이면 바로 가져오는 걸 재귀 함수의 base case로 두면 코드가 깔끔한듯
        
        ```python
        class Solution:
            def deleteAndEarn(self, nums: List[int]) -> int:
                # preprocessing
                count = collections.Counter(nums)
                
                # hashmap
                memo = {}
                
                # base case
                memo[0] = 0
                if 1 in count:
                    memo[1] = 1 * count[1]
                else:
                    memo[1] = 0
        
                def max_points(num):
                    if num in memo:
                        return memo[num]
                    
                    if num not in count:
                        gain = 0
                    else:
                        gain = num * count[num]
        
                    memo[num] = max(gain + max_points(num-2), max_points(num-1))
                    return memo[num]
                
                return max_points(max(nums))
        ```
        
    - bottom-up
        
        ```python
        class Solution:
            def deleteAndEarn(self, nums: List[int]) -> int:
                nums.sort()
                count = collections.Counter(nums)
        
                # array
                dp = [0] * (max(nums)+1)
        
                # base case
                if 1 in count:
                    dp[1] = 1 * count[1]
                
                # recurrence relation
                for i in range(2, max(nums)+1):
                    if i not in count:
                        gain = 0
                    else:
                        gain = i * count[i]
                    dp[i] = max(dp[i-2]+gain, dp[i-1])
                
                return dp[-1]
        ```
        
- Editorial
    - Overview
        - 문제에 힌트가 - 주어진 `nums` 안에서 element의 순서가 전혀 상관없다는 것을 알면 최적화 가능
        - nums에서 x가 여러 번 나올 때, 하나씩 취하는 것보다 한꺼번에 모든 x에 대해 점수를 계산하는 게 효율적.
            
            ↳ x가 일단 한번이라도 나오면 x-1, x+1 값들은 모두 제거되기 때문에. 이후 나오는 x는 점수를 늘리기만 할 뿐. 그러니 같은 값들에 대해 한꺼번에 계산하는 게 편함 
            
        - nums array에서 중복 요소끼리 모으자: counter hashmap → 우리가 관심 있는 건 각 숫자가 몇 점을 가져다 줄 수 있는지니까, dictionary value를 단순 count에서 점수로 변환 (key를 곱하면 됨)
    - **Approach 1: Top-Down Dynamic Programming**
        - Intuition
            - 이 문제가 DP로 풀어야 함을 암시하는 부분
                1. 무언가의 최대 값을 구하라고 함
                2. 어떤 숫자를 취할지에 대한 decision이 필요하고, 이게 future decision에 영향을 미침 (예-5들을 취하면, 4나 6들은 버려야 함)
            - nums → dict (key: 취하려는 숫자, value: 그 숫자로 얻을 수 있는 총점)
                - future impacts of current decisions → 그리디로는 매 단계에서의 결정이 모두 옳다는 것을 보장할 수 없음. 현재 가장 큰 점수를 얻는 쪽으로 행동해도, 미래 단계에서 더 높은 점수를 얻을 수 있는 상황을 가로 막는 결과를 낳을 수도 있음
            - DP formulation
                1. **hash table `maxPoints`**
                    - maxPoints[num]: nums array에서 0과 num 사이값을 갖는 element들을 모두 고려했을 때 얻을 수 있는 최대 점수
                2. **recurrence relation-a way to move between states**
                    - nums에 한 번 이상 등장하는 임의의 숫자 x에 있다고 가정
                        
                        → maxPoints[x]를 구하는 법?
                        
                    - x에 대해서 내릴 수 있는 결정은 두 가지
                        - x를 취한다
                            - gain: x * count[x]
                            - x 말고 고려할 수 있는 숫자 중 가장 큰 숫자: x-2
                                - 0과 x-2 사이에서 숫자들 사이에서 얻을 수 있는 가장 큰 점수
                            
                            → `gain + maxPoints(x-2)`
                            
                        - x를 버린다
                            - gain: 0
                            - x 말고 고려할 수 있는 숫자 중 가장 큰 숫자: x-1
                            
                            → `maxPoints(x-1)`
                            
                    
                    ⇒ 점화식: `maxPoints(x) = max(gain + maxPoints(x-2), maxPoints(x-1))`
                    
                3. **base case** 
                    - maxPoints(0) = 0 (nums[i] 최소 값은 1)
                    - maxPoints(1) = 1 * count(1)
                    
                    → recursive는 i=2~max(nums)
                    
                4. memoization
        - 알고리즘
            - 큰 흐름은 같고, defaultdict(int) 사용하면 나오는 모든 숫자에 자동으로 0을 부여하니까 편할 듯
        - Complexity Analysis
            - N: len(nums), k: max(nums)
            - 시간 복잡도: O(N+k)
                - nums 한 번 쫙 훑으면서 count → O(N)
                - max_point 함수를 max(nums) 호출
                    - base case인 0, 1 도달하기까지 max(num)에서 하나씩 줄여가면서 함수 콜 계속
                    - 다만 한번 계산한 결과는 캐싱하기 때문에 각 subproblem의 시간복잡도는 O(1) → O(1) * k = O(k)
                
                ⇒ 둘을 더하면 O(N+k)
                
            - 공간 복잡도: O(N+k)
                - hash table `count` → O(len(set(nums)) = unique element 개수
                    - 최악의 경우 nums의 모든 element가 unique → O(N)
                - max_point 함수 재귀 콜 스택
                    - max(nums) = k에서 시작해서 base case 0이나 1 도달할 때까지 stack에 쌓아두다가, hit 하면 returning values → O(k)
                - memo
                    - 2부터 max(nums)=k 까지 모든 Key에 대한 값을 저장 → O(k)
                
                ⇒ O(N) + O(k) + O(k) = O(N + 2*k) = O(N+k)
                
    - **Approach 2: Bottom-Up Dynamic Programming**
        - Intuition
            - top-down approach: max(nums) → base case로 argument 값이 점점 작아짐
            
            ↔ bottom-up approach: base case → max(nums)로 iteration i 값이 점점 커짐