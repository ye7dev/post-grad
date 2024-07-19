# Dynamic Programming

Status: algorithm, done
Theme: DP
Created time: January 2, 2024 11:37 PM
Last edited time: January 12, 2024 8:32 PM

# Intro to DP

## What is DP?

- systemically-step by step-, 효율적으로 가능한 모든 솔루션을 탐색하는 것
- 아래와 같은 특징을 가진 문제들이 주로 해당
    1. overlapping subproblem으로 쪼갤 수 있다 
        - 원래 문제를 작은 버전으로 만들어서 여러번 재사용됨
    2. optimal substructure를 가진다 
- 피보나치 수열의 경우
    - 0, 1, …, 그 다음 숫자는 previous two numbers의 합
    - F(n): n번째 피보나치 숫자 = F(n-1) + F(n-2)
        - F(n-1), F(n-2)는 각각 subproblems
        - F(n-1) + F(n-2) 이렇게 더해서 다음번 피보나치 수가 나온다는 것은 optimal substructure
            - 부분 문제의 해를 가지고 원래 문제의 해를 구할 수 있다
        - overlapping
            - F(4)의 해는 F(5)를 구하는 데도 쓰이고, F(6)을 구하는데도 쓰인다
- 다른 문제들과의 비교
    - 그리디: optimal substructure O, **overlapping subproblems X**
    - 분할정복: subproblem으로 쪼개기 O, overlapping subproblems X
        - divide & conquer랑 DP랑 자주 헷갈린다고 함
        - 분할정복은 병렬화가 가능
            - 분할정복에서 subproblem들은 서로 서로 독립적이기 때문에
- DP 장점
    - 복잡한 문제를 풀 수 있을 만한 문제로 쪼갬
    - overlapping subproblems들에 대해 불필요한 계산 반복 피할 수 있음
    - 부분 문제의 결과를 가지고 원래의 복잡한 문제를 해결하는 데 사용
    - brute force 솔루션이랑 비교하면 시간 복잡도 개선
        - 피보나치의 경우 브루트 포스로 하면 exponential(O(2^n) 처럼 input data가 하나 더 들어올 때마다 문제 해결에 걸리는 시간이 두 배 걸리는 경우. 지수로 시간이 증가함을 의미)
        - DP로 풀면 linear time complexity-부분 문제의 해를 저장해뒀다가 다시 사용하기 때문에

## **Top-down and Bottom-up**

### **Bottom-up (Tabulation)**

- base case에서 시작해서 iteration
- 피보나치의 경우
    - base case: F(0) = 0, F(1) = 1
    - 얘네를 가지고 F(2)를 구하고, F(1)이랑 F(2)를 가지고 다시 F(3)을 구하고… → F(n)
    - 수도 코드
        
        ```python
        F = array of length (n + 1)
        F[0] = 0
        F[1] = 1
        for i from 2 to n:
            F[i] = F[i - 1] + F[i - 2]
        ```
        

### **Top-down (Memoization)**

- recursion으로 구현해서 memoization으로 효율 업
- 피보나치의 경우
    - F(n)을 구하고 싶으면 F(n-1), F(n-2)부터 찾는다
    - recursive pattern으로 argument를 줄여나가다가 base case hit - F(0) = 0, F(1) = 1
- memoization이 없으면 엄청난 횟수의 불필요하고 반복되는 계산을 해야 한다는 점
    - 이 recursion tree에서 F(2)는 세번이나 계산되어야
        
        ![Untitled](Untitled%2079.png)
        
    - memoizing a result
        - function call(특정 argument 값에서의)의 결과를 hashmap이나 array에 저장하는 것을 의미
        - 그래서 동일한 function call이 발생했을 때, memoized 결과를 return 하기만 하면 됨
    - memoization 전과 후 비교
        
        ![Untitled](Untitled%2080.png)
        
        ![Untitled](Untitled%2081.png)
        
- 피보나치 수도 코드
    
    ```python
    memo = hashmap
    Function F(integer i):
        if i is 0 or 1: 
            return i
        if i doesn't exist in memo:
            memo[i] = F(i - 1) + F(i - 2)
        return memo[i]
    ```
    

### **Which is better?**

- bottom-up
    - 런타임이 보통 더 빠름. iteration은 recursion에서처럼 overhead가 없기 때문
    - logical ordering of solving subproblems 필요
- top-down
    - 코드 짜기 더 쉬움
    - subproblem 순서가 상관 없기 때문에

## When to Use DP

- 알아보기 쉬운 DP 문제의 특성
    1. **무언가의 optimum value를 구하는 문제 (min, max)**
        - 예시
            - What is the minimum cost of doing...
            - What is the maximum profit from...
            - How many ways are there to do...
            - What is the longest possible...
            - Is it possible to reach a certain point...
    2. **미래의 결정이 앞선 결정에 의존한다** 
        - 어느 단계에서의 결정이 이후 단계에서 할 수 있는 것들에 영향을 미침
        - 어떤 한 요소를 사용하면 다른 요소의 사용이 불가해진다던ㄷ가…
    - 대표적인 예시: House Robber
        - 붙어 있는 집들 끼리는 보안 시스템을 공유해서, 같은 날에 붙어 있는 두 집을 털면 경찰에 발각된다는 제약
        - 각 집에서 털 수 있는 금액이 array로 주어질 때, 경찰에 들키지 않고 오늘 도둑질 할 수 있는 최대 금액을 구하여라
        
        → 첫번째 집과 두번째 집 중 어디를 터느냐가 다음 번 결정에 영향을 미침 
        
    - 예시2: Longest Increasing Subsequence
        - 숫자 array가 주어질 때, strictly increasing subsequence 중 가장 긴 것의 길이를 구해야
        - [1, 2, 6, 3, 5]가 있을 때 6을 선택하면[1, 2, 6], 6을 안 선택하면 [1, 2, 3, 5] - 지금의 선택이 미래의 선택지에 영향을 미침
- 두번째 특징-미래의 결정이 앞선 결정에 의존한다-에 부합하는 지 헷갈린다면
    - 두번째 특징이 없다고 가정하고, 그리디 알고리즘이 작동하지 않는 다는 것을 증명할 counterexample을 떠올려라
    - 앞선 결정이 미래의 결정에 영향을 미치면 DP 적용 가능

# Strategic Approach to DP

## Framework for DP Problems

- 예시 문제-Climbing Stairs
    
    꼭대기까지 가는 데 n개의 계단을 올라야 한다. 한 번에 1개 혹은 2개를 오를 수 있을 때, 꼭대기까지 도달하는 서로 다른 방법은 모두 몇 개? 
    
- state
    - a set of variables that can sufficiently describe a scenario
        - state variables
    - 예시 문제에서의 state: 우리가 지금 몇 번째 계단에 서 있는지
        - 예) i = 6 → 6번째 계단에 올라 있는 상태
        - 각 unique value i는 하나의 unique state를 표현

### The Framework

- 아래 세 가지 요소를 합쳐야 하나의 DP 문제를 풀 수 있따
1. **모든 주어진 상태에 대해, 문제에 대한 답을 계산하는 함수 또는 답을 저장하고 있는 자료 구조**
    - 예시 문제에서의 1번 요소: 함수 `dp`
        - dp(i): i번째 계단까지 오르는 서로 다른 방법의 개수를 return 하는 함수
    - 함수의 설계
        - 문제에서의 요구 사항: 꼭대기까지 오르는 서로 다른 방법의 개수 → 함수는 어떤 특정 계단까지 오르는 서로 다른 방법을 represent
            - 원래 문제와 같아 보이지만, Generalized for a given state
    - 보통 top-down은 재귀 함수 + hashmap으로, bottom-up은 nested for loops + array로 구현
        - 이 함수나 array를 설계할 때는, argument로 전달할 state variable을 뭘로 할 것인지 결정해야 함
2. **서로 다른 상태 사이를 오고갈 recurrent relation** (재귀식) 
    - 재귀식
        - 서로 다른 상태를 연관짓는 등식? 방정식? equation
        - 한 번에 1개 혹은 2개 계단만 오를 수 있음 → 30번째 계단을 오른다 = 28번째 혹은 29번째 계단에서 출발해야 함
            
            ⇒ 30번째 계단을 오르는 방법의 개수 = 28번째 계단을 오르는 방법의 수(에서 두 칸 한 번에 오르면 되니까) + 29번째 계단을 오르는 방법의 수(에서 한 칸 한번만 오르면 되니까) 
            
            ⇒ dp(i) = dp(i-1) + dp(i-2) (finonacci in disguise)
            
3. **recurrence relation이 무한대로 이어지지 않게 해주는 Base case**
    - dp(i) = dp(i-1) + dp(i-2) 그냥 놔두면 음의 무한대까지 계속 갈 것 → 실제로 어떤 값으로 return 되게끔 base case가 필요
    - DP 없이 바로 답을 찾을 수 있는 상태들은 어떤 것인가?
    - 예시 문제에서의 3번 요소
        - 첫번째 계단을 오르는 방법의 수 (dp(1)) = 1
        - 두번째 계단을 오르는 방법의 수 (dp(2)) = 2개를 한꺼번에 + 1개씩 두번에 걸쳐 = 2

### Example Implementations

- top-down using 3 components
    - memoization을 사용하지 않았기 때문에 O(2^n) TC를 가짐
    
    ```python
    class Solution:
        def climbStairs(self, n: int) -> int:
            def dp(i): 
                """A function that returns the answer to the problem for a given state."""
                # Base cases: when i is less than 3 there are i ways to reach the ith stair.
                if i <= 2: 
                    return i
                
                # If i is not a base case, then use the recurrence relation.
                return dp(i - 1) + dp(i - 2)
            
            return dp(n)
    ```
    
- top down + memoization
    - O(n) TC
    
    ```python
    class Solution:
        def climbStairs(self, n: int) -> int:
            def dp(i):
                if i <= 2: 
                    return i
                if i not in memo:
                    # Instead of just returning dp(i - 1) + dp(i - 2), calculate it once and then
                    # store the result inside a hashmap to refer to in the future.
                    memo[i] = dp(i - 1) + dp(i - 2)
                
                return memo[i]
            
            memo = {}
            return dp(n)
    ```
    
- bottom-up
    
    ```python
    class Solution:
        def climbStairs(self, n: int) -> int:
            if n == 1:
                return 1
                
            # An array that represents the answer to the problem for a given state
            dp = [0] * (n + 1)
            dp[1] = 1 # Base cases
            dp[2] = 2 # Base cases
            
            for i in range(3, n + 1):
                dp[i] = dp[i - 1] + dp[i - 2] # Recurrence relation
    
            return dp[n]
    ```
    

## Example 198. House Robber

- 전형적인 DP 문제 특성에 부합
    - maximum of 하루 안에 훔칠 수 있는 돈
    - 현재의 결정이 다음 번 결정에서 취할 수 있는 option에 영향
- **주어진 state에 문제에 대한 답을 주는 function or array**
    - state variable
        - 이 변수(들)로 하나의 시나리오를 서술하는데 충분해야 함
        - 일렬로 나열된 집들이 있고, 내가 도둑
            - 내가 저 집 들 중 하나에 있다면, 내 상황을 설명할 수 있는 유일한 변수는 하나의 정수 - 현재 위치한 집이 일렬에서 몇 번째 위치하는지 (an index of the house array)
        - 만약 이 상황에서 최대 K개의 집만 털 수 있다는 제약이 추가되면, 현재까지 훔친 집의 개수 k가 추가로 필수적인 state variable이 될 것
    - dp[i] or dp(i)
        - array, bottom-up→ dp[i]: i번째 집까지 고려(up to and including)했을 때 훔칠 수 있는 최대 금액을 represent
        - function, top-down → dp(i): i번째 집까지 고려(up to and including)했을 때 훔칠 수 있는 최대 금액을 return
        - 둘 다 nums[:i+1](i inclusive) 상황에서 문제에 대한 답을 줌
        
        ⇒ 원래 문제에 대한 답은 dp[len(nums)-1] or dp(len(nums)-1)
        
- **A recurrence relation to transition between states**
    - general state를 생각 - i번째 집에 있는 상태 & 문제 서술에서 정보 모으기 → 다른 state들이 현재 상태와 연결될 수 있는지 생각
    - 우리가 어떤 집에 있을 때, 두 가지 선택권이 주어짐
        - 이 집을 털던가 / 안 털던가
        - 이 집을 안 털기로 하면 → 현재 얻을 수 있는 돈은 없음
            - 얼마가 되었던 이전 집에서 가지고 있던 금액 그대로가 현재 우리가 이 집에서 갖게 될 금액 = dp(i-1)
        - 이 집을 털기로 하면 → nums[i]의 금액을 얻음
            - 근데 이렇게 되려면, 바로 직전 집은 털지 않았어야 가능
            - 우리가 i번째 집에 도착했을 당시 갖고 있었던 금액 = 이전 집에서 도둑질하지 않은 상태로 갖고 있던 금액 = 두 집 이전에 우리가 갖고 있었던 금액 = dp(i-2)
            - + i번째 집에서 턴 금액 = dp(i-2) + nums[i]
        - 이 두 가지 옵션 중에 더 큰 이윤을 남기는 쪽을 선택
            - dp(i) = max(dp(i-1), dp(i-2) + nums[i])
- **Base cases**
    - recurrence relation에게 멈출 때를 알려줌
    - 주로 문제 설명에서 실마리를 찾을 수 있거나 논리적 사고로 발견
    - 우리 문제의 경우
        - 집이 하나만 있을 경우, 그 집을 털거나 안털거나 중 max 금액은 집을 터는 경우에 얻을 수 있음 (dp(0) = nums[0])
        - 집이 두 개면 둘 다 연속으로 털 수 없으니 둘 중에 더 큰 쪽 집을 털어야 앋을 수 있음 (dp(1) = max(nums[0], nums[1])
- Top-down Implementation
    
    ```python
    # function 
    def rob(nums):
    		def dp(i):
    			# base case
    			if i == 0: 
    					return nums[0]
    			if i == 1: 
    					return max(nums[0], nums[1])
    	
    			# recurrence relation
    			if i not in memo:			
    					memo[i] = max(rob(i-1), rob(i-2) + nums[i])
    
    			return memo[i]
    			
    	
    		memo = {} # hashmap
    		return dp(len(nums)-1)		
    ```
    
- Bottom-up Implementation
    - top-down이나 bottom-up이나 두 경우 모두 시간/공간 복잡도는 O(n)
    
    ```python
    def rob(nums):
    		if len(nums) == 1:
    				return nums[0]
    		
    		# array
    		dp = [0] * len(nums)
    		
    		# base case 
    		dp[0] = nums[0]
    		dp[1] = max(nums[0], nums[1])
    
    		# recurrence relations
    		for i in range(2, len(nums)):
    				dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    
    		return dp[len(nums)-1]			
    ```
    

## **Multidimensional DP**

- dimension of DP algorithm
    - the number of state variables used to define each state
- state variable 관련 주의해야 할 점
    - index along input
        - 주어진 input이 array 거나 string인 경우
        - 몇 번째 input까지 고려했을 때의 답인지를 나타냄
            - 예) input: nums = [0, 1, 2, 3, 4, 5, 6] → dp(4):  [0, 1, 2, 3, 4] (nums[:4+1]) 까지의 input에서 문제에 대한 답 가져다줌
    - second index along input
        - 두 개의 index state variable - i, j라고 해보자
        - index i에서 시작해서 index j에서 끝나는 input - input[i:j+1] 을 고려했을 때 문제에 대한 답을 나타내기 위해 사용할 수도
            - 예) dp(1, 3) → nums[1:4] = [1, 2, 3]을 고려했을 때 문제에 대한 답
    - 명시적인 수 제약
        - 예) 최대 k번의 거래가 허용될 때, 최대 k개의 장애물을 부수도록 허용될 때 등
    - 하나의 주어진 상황에서 statuses(?)를 서술하는 변수들
        - 예) 현재 key를 갖고 있으면 true, 아니면 False
        - 예2) 현재 k개의 소포를 갖고 있으면
    - 방문 여부, 사용 여부를 나타내기 위해 사용되는 tuple, bitmask와 같은 데이터
        - 예) ith bit가 i번째 도시의 방문 여부를 나태는 bit mask
        - array와 같은 mutable 자료 구조는 사용될 수 없다 - 숫자나 string과 같은 immutable 자료 구조만 hashed, memoized 도리 수 있다.

## Top-down to Bottom-up

- top-down이 구현하기는 더 쉽지만 보통 면접에서는 bottom-up 답이 나오길 기대하고, 실행 시간도 bottom-up이 더 빠르기 때문
- Top-down을 bottom-up으로 전환하기
    1. top-down으로 구현 완료 
    2. dp array initialize 
        - state variable에 따라 array size 결정
            - 예) input이 nums array와 허용된 최대 액션의 개수인 k인 경우 → dp array size는 len(nums) * k
        - 초기값은 문제에서 요구하는 것의 반대로 설정
            - 예) 문제에서 최대값을 물으면, cell 값은 negative infinity로 설정 ↔ 최소값을 물으면, cell 값은 inifinity
    3. base case 설정 
        - top-down function에서와 동일한 것으로 사용
            - 함수의 base case → bottom-up에서는 dp의 가장 작은 index 들의 cell 값으로 들어감
    
    5. state variable을 도는 for loop 작성
    
    - state variable이 여러 개면 nested for loop
    - iteration은 base case부터 시작
    1. 이제 dp는 모든 가능한 state에 대해 우리가 해결해야 하는 동일한 문제에 대한 답을 갖고 있게 됨 → original problem의 답을 return
        - return dp(…) → return dp[…]
- House robber의 예시
    
    ```python
    def rob(houses):
    		# avoid index out of bounds error
    		if len(houses) == 1:
    				return houses[0] 
    			
    		# array
    		dp = [0] * len(houses)
    		
    		# base cases
    		dp[0] = houses[0]
    		dp[1] = max(houses[0], houses[1])
    
    		# for loop
    		for i in range(2, len(houses)):
    				# recurrence relation 
    				dp[i] = max(dp[i-2]+houses[i], dp[i-1])
    		
    		return dp[-1]
    
    			
    ```
    

## **Example 1770. Maximum Score from Performing Multiplication Operations**

### a function or array (⭐️⭐️⭐️)

- 어떤 state variable을 pass 할 것인가?
- 무엇을 답으로 return 할 것인가?
- 각 operation마다 알아야 하는 세 가지 정보
    - 이번에 사용할 multiplier가 몇 번째인가? (=지금까지 몇 번의 operation을 마쳤는가?)
    - nums에서 가용 원소 중 가장 왼쪽 원소의 인덱스
    - nums에서 가용 원소 중 가장 오른쪽 원소의 인덱스
    
    ⇒ 세 가지 state variable을 사용해야 하는가? 
    
    - 두 개의 정보를 사용해서 나머지 하나에 대한 equation을 만들 수 있다
    - 우선 operation 횟수에 대해서는 `i` 사용 (= 왼쪽이든 오른쪽이든 가장 자리에서 원소를 취한 횟수)
    - 지금까지 leftside에서 몇 개의 원소를 취했는지 알 수 있으면 (`left`)
    
    → right = n - 1 - (`i` - `left`)
    

### A recurrence relation to transition between states

- 각 state에서 하나의 operation을 수행해야 하고, 한 번의 operation 시에 제일 왼쪽과 오른쪽 (`nums[left]` or `nums[right]`) 중 어느 쪽으로부터 점수를 얻고 원소를 제거할 것인지 결정해야
- 개념적으로는 위와 같고, 구현 단계로 내려 오면
    - 점수를 얻고 숫자를 제거하는 행위 = state variable i와 left를 증가시키는 것 → 그래야 다음 두 개의 left, right 숫자를 가리킬 수 있기 때문에
        - 숫자를 제거하면서 i를 증가시킴
        - left는 왼쪽에서 제거한 경우에만 증가
- 좌냐 우냐 선택
    - 왼쪽을 선택하면 multipliers[i] * nums[left]만큼의 점수를 얻는다 → 그럼 그 다음 operation에서 i와 left 모두 1씩 증가
        
        ⇒ mult * nums[left] + dp(i+1, left+1)
        
    - 오른쪽을 선택하면 multipliers[i] * nums[n-1-(i-left)] 만큼의 점수를 얻는다 → 그럼 그 다음 operation에서 i만 1 증가
        
        ⇒ mult * nums[n-1-(i-left)] + dp(i+1, left)
        
    - 둘 중 max를 선택하면 dp(i, left)의 값이 나옴

### Base cases

- i == m → 더 이상 operation을 할 수 없음 → return 0

### Top-down AC 코드

```python
class Solution:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        n, m = len(nums), len(multipliers)
        memo = {}
				
				# function 
        def recur(i, left):
            # base case
            if i == m:
                return 0 
            if (i, left) in memo: # tuple
                return memo[(i, left)]
            
            # recurrence relation
            mult = multipliers[i]
            right = n - 1 - (i - left)
            choose_left = mult * nums[left] + recur(i+1, left+1)
            choose_right = mult * nums[right] + recur(i+1, left)
            memo[(i, left)] = max(choose_left, choose_right)

            return memo[(i, left)]
        
        return recur(0, 0)
```

- lru_cache decorator 쓰면 훨씬 빠르긴 하다
    
    ```python
    from functools import lru_cache
    
    @lru_cache(2000)
    def recur(argument):
    		pass
    ```
    

### Bottom-up Implementation

- dp[i][left] : i번의 operation이 수행됐고, 그 중 왼쪽 원소를 left번 선택했을 때 얻을 수 있는 최대 점수
- m에서 시작해서 i를 줄이면서 iterate
    - 왜냐면 base case는 i=m으로 top-down과 동일하기 때문
- dp array에 대해 추가로 row를 하나 더 만들어줘야
    - outer loop의 first iteration 시에 out of bounds 에러 피하기 위해(?)
- dp array size: (m+1) * (m+1)
    - base case는 i=m이니까

### Bottom-up AC 코드 (⚡️)

- 헷갈렸던 점
    - dp array size
        - n은 등장하지 않는다-i의 최대값은 m
        - **left의 최대값은 i**
        - 이 때 row, col 개수를 m+1 해야 하는 이유
            - top-down에서도 base case는 i=m 즉, m+1번째 operation인 경우를 나타냈다
            - base case를 다룰 추가적인 열과 행이 필요
    - base case
        - m+1번째 operation인 경우 = i가 m인 경우 → last row being zero
        - left의 최대값은 i 이므로, left도 m까지 갈 수 있고, 이 경우도 모두 0이 나와야 함 → last column being zero
        - 근데 dp matrix 초기값을 0으로 뒀기 때문에 따로 코드에는 명시 하지 않음

```python
class Solution:
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        n, m = len(nums), len(multipliers)
        
        # array 
        dp = [[0] * (m + 1) for _ in range(m + 1)] # row: 0~m, col: 0~m
        # col 개수는 좀 적게 만들어도 되지 않나? 왼쪽을 n-1까지 다 갈 일이 있나? 
        # -> 맞다. 왼쪽 오른쪽 합쳐서 최대 i개가 되어야 하니까, 왼쪽의 max도 i가 된다 
        
        # base case
        # i = m+1 -> 0 
        # left = m+1 -> 0
        
        for i in range(m-1, -1, -1):
            for left in range(i, -1, -1):
                mult = multipliers[i]
                right = n - 1 - (i-left)
                choose_left = mult * nums[left] + dp[i+1][left+1]  
                choose_right = mult * nums[right] + dp[i+1][left]
                dp[i][left] = max(choose_left, choose_right)
        
        return dp[0][0]
```

## **Time and Space Complexity**

- DP에서는 반복되는 계산이 없다 - tabulation이던 memoization이던 -
    
    → state 하나당 한 번의 계산만 수행 
    
    - 특히 이 한 번의 계산도 대부분 재귀식을 통해 계산해서 O(1)
    
    ⇒ DP 알고리즘의 시간 복잡도는 정확히 possible states 개수에 따라 결정됨 
    
- 나타날 수 있는 state의 개수는 몇 개인가?
    - state variable의 개수 * 각 state variable이 취할 수 있는 값의 개수
    - 예- i, k, holding 세 가지 변수가 존재
        - i: input array nums의 index
        - k: maximum actions we can do - input으로 주어지는 제약
        - holding: boolean
        
        ⇒ len(nums) * k * 2 = O(N * K)
        
- 공간복잡도 역시 미리 계산한 결과를 모두 저장하기 때문에 계산이 이루어지는 개수에 비례
    - 계산이 이루어지는 개수 = state의 개수 = TC랑 같다

# Common Patterns in DP

## **Iteration in the recurrence relation**

- 지금까지 본 문제들에서의 recurrence relation
    - static equation - 절대 변하지 않지
    - 예- Min Cost Climbing Stairs의 경우 점화식
        - dp(i) = min(dp(i-1) + cost[i-1], dp(i-2) + cost[i-2])
        - 한번에 오를 수 있는 계단은 1개 혹은 2개
- 만약 한 번에 오를 수 있는 계단의 개수가 k개로 늘어난다면?
    
    → recurrence relation도 dynamic 해진다 
    
    ```python
    for j in range(i-k, i): # i-k ~ i-1
    		dp(i) = min(dp(j) + cost(j))
    ```
    
- 고정된 개수의 option으로부터 선택지를 고려하는 대신, for loop을 하나 더 넣어서 dynamic number of option을 고려하고 그 중 best를 뽑으면 되는 것

## **Example 1335. Minimum Difficulty of a Job Schedule (⭐️⭐️⭐️)**

- 문제 이해
    - input: a list of jobs, d days
    - job들 간에는 위계가 있음-어떤 job을 하기 위한 선행조건으로 다른 job이 있는 등…
        - i번째 job을 수행하기 위해서는 그보다 앞선 index의 일을 모두 한 상태여야 한다 = 오름차순으로 일을 해야 한다
    - 하루에 최소 하나의 task를 수행해야 함
    - 하나의 job schedule을 수행하는 difficulty(품)
        - 총 d개의 날들의 difficulties의 합
        - 하루의 difficulty는 무엇으로 대표?
            - 그 날 수행한 job 들중 가장 큰 difficulty
    - output: 위의 제약사항을 고려해서 짠 job schedule의 minimum difficulty
        - 만약 schedule을 찾을 수 없으면 -1을 return
- DP 문제의 특징에 부합하는가? yes
    - minimum of something을 구하라
    - 주어진 날에 몇 개의 job을 수행하느냐가 훗날에 할 수 있는 job들에 영향을 미침
- **A function that answers the problem for a given state**
    - state variables
        - d개의 날이 끝날 때에는 주어진 순서대로 모든 job을 완료한 상태여야 함
            - 결정해야 하는 사항: 각 날에 몇 개의 job을 수행할 것인지
        
        ⇒ state variable `i`: 그 날에 수행된 첫번째 job의 index 
        
        ⇒ state variable `day` : 현재 몇 번째 날인지 표시 
        
    - function
        - `dp(i, day)` : day 번째 날에 i번째 job을 시작하는 job schedule의 최소 어려움
            
            → original problem은 dp(0, 1)이 됨 
            
            - job index는 0부터 시작하고, d의 최소값은 1이라서
            - 첫번째 날에 첫번째 작업을 시작하는 상태
        - 예시
            - 그림
                
                ![Untitled](Untitled%2082.png)
                
            - input: [6, 5, 4, 3, 2, 1], d = 2
            - dp(3, 2) : i = 3  job(0-indexed라서 사실은 4번째) 을 day 2에 시작할 때의 최소 품
                - day 1에 6, 5, 4는 모두 수행된 상태(?)
                - 그리고 남은 일이 3, 2, 1 이라 highlighted
                - d는 우리가 일을 마쳐야 하는 날, 즉 일을 할 수 있는 마지막 날을 의미 → 우리는 day 2에 남은 일 3, 2, 1을 모두 마쳐야 한다. → day 2를 대표하는 difficulty는 셋 중 가장 값이 큰 3
- **A recurrence relation to transition between states**
    - 하나의 state: day 번째 날에 i 번째 job을 수행해야 함
        
        → 그리고 나서 몇 개의 job을 추가로 더 선택 가능 
        
    - 몇 개의 job을 추가로 더 수행할 수 있을까?
        - 문제에서는 최소 하루에 하나의 일을 해야 한다고 함
        - 전체 날 수 `d` - 현재 날짜 `day` 만큼의 일이 남아 있어야 함
            - 남은 날 수가 d-day이기 때문에, 똑같은 수만큼의 일이 남아 있어야 하루에 최소 하나의 일 수행 가능
        
        → n = len(jobDifficulty) = 전체 job의 개수라고 할 때, 주어진 상태 (i, day)에서 할 수 있는 일은 
        
        - i 번째에서 시작해서 n - (d-day) 전까지
        - n - (d-day) = 전체 일의 개수 - 남겨야 하는 일의 개수 = 오늘까지 해도 되는 일의 개수
    - 주어진 날에 대해 가능한 모든 옵션을 시도해봐야
        - 일의 idx가 n - (d-day) 넘지 않는 선에서 그날에 한 개의 일만 할 수도 있고, 두 개도 할 수 있고, …
        - 이 중 가장 좋은 선택은 최대 difficulty가 가장 작게 나오는 편인듯?
    - 스케줄링 제약
        1. 주어진 하루에 몇 개의 일을 수행하던 그 날의 대표 difficulty 값은 그날 수행한 일 중 가장 높은 difficulty를 가진 일의 difficulty를 따라감 
        2. job들 간에는 수행되어야 하는 선후관계가 있음 
        - 만약 그날 할 수 있는 일의 범위를 모두 돌면서 해본다면 `hardest` 변수를 두고, 그날 한 가장 어려운 일의 difficulty 정보를 저장
        - 예- 어떤 날(dp(i, day))에 j번째 job까지(inclusive) 수행 가능한 상태라고 하면
            - i(input parameter) ≤ j < n - (d- day)
            
            → 다음 날인 day + 1 번째 날에는 j+1 th 일부터 시작한다는 의미 
            
            ⇒ total difficulty 는 hardest + dp(j+1, day + 1)
            
    - Scariest Recurrence relation
        - 구하려는 값: dp(i, day)
        - iterate over dynamic number of options
            - 1 ~ n - (d-day) - 1개 (?)
            - j : day 번째 날에 수행하는 마지막 일의 index
                - choose to do jobs up to the jth job(inclusive)
                - j의 범위: i ≤ j < n - (d - day)
            - hardest : max (jobDifficulty[k]) ( i ≤ k ≤ j)
                - k: day 번째 날에 수행되는 일들의 index
        
        ⇒ dp(i, day) = min(hardest + dp(j+1, day+1)) for all i ≤ j < n - (d - day), where hardest = max(jobDifficulty[k]) for all i ≤ k ≤ j 
        
        🧙‍♂️ 우리가 현재 날에 몇 개의 일을 하기로 선택하든, 하나의 job schedule을 대표하는 difficulty는 `오늘의 difficulty` + `the next state` (= 다음 날에 아직 수행되지 않은 첫번째 일부터 수행하는 상황)
        
    - 위의 무서운 식을 말로 풀어보면
        - 모든 날에 우리는 가능한 모든 옵션을 탐방한다
            - 옵션: 하루에 할 수 있는 일의 개수들
            
            → 한 개, 두 개, … 가능한(미래 날들에 최소 한 개씩 할 수 있는 만큼은 남겨둬야 하기 때문에) 최대 개수까지 
            
        - hardest 는 그날 수행한 일 중 가장 어려운 일의 difficulty = 그 날 전체를 대표하는 difficulty
            - 이 hardest를 next state(다음 날에 다음 일을 시작하는 상황)에 더해준다
        - 허락된 모든 일의 개수에 대해 hardest를 계산하고, next state에 더해주면서 그날까지(up to day th day)에 얻을 수 있는 difficulty를 모두 살펴봄 → 그 중 minimum을 선택
    - 슬라이드쇼로 나타내면
        
        ![Untitled](Untitled%2083.png)
        
        ![Untitled](Untitled%2084.png)
        
        ![Untitled](Untitled%2085.png)
        
- **Base cases**
    - d 일 안에 모든 job을 끝내야 함 = 마지막 날 (d th day)에 남은 모든 일을 완료해야 함 → 그럼 마지막날의 difficulty는 남은 일 중 가장 어려운 일의 difficulty = max(jobDifficulty[i:])
    - array `hardestJobRemaining` 을 미리 계산해둠
        - hardestJobRemaining[i] = 현재 parameter로 들어온 i부터 남은 일들 중 가장 어려운 일의 difficulty (max(jobDifficulty[i:])
        - 이러면 base case를 상수 시간으로 다룰 수 있게 됨(?)
            - 날짜는 d로 고정이지만, i는 달라질 수 있기 때문에(?)
    - edge case - early exit
        - 주어진 날 수보다 일의 개수가 적으면, 하루에 최소 한 개의 일을 수행해야 한다는 제약을 만족할 수 없음 → return -1

## Example 139. Word Break

- 평소처럼 maximum 혹은 minimum이 아님-숫자가 아님
    
    → 우선 greedy로 풀 수 있다고 가정하고 반례가 있는지 살펴본다 
    
    - 예- s =”abcdef”, wordDict=["abcde", "ef", "abc", "a", "d"]
        - greedy algorithm: longest substring available 선택
            
            : abcde 선택 → f만 남아서 False return
            
        - 맞는 답: True
            - abc, d, ef 선택하면 단어를 남김없이 쪼갤 수 있음
        - greedy algorithm에서 longest를 shortest로 바꿔도 틀린 답인 건 매한가지
    
    ⇒ 반례를 찾았기 때문에 DP로 넘어가자
    
- Bottom-up first (⭐️⭐️)
    1. array - 하나의 state에 대해 정답을 제공 
        - state variable i : input string s에서 현재 위치한 index 표현
            - wordDict에 있는 단어는 횟수 제한없이 쓸 수 있기 때문에 state variable 필요 없음
                - 만약 k번으로 사용횟수가 제한되면 추가로 state variable 사용해야 함
        - dp[i]: string[:i+1](i inclusive?)까지의 substring에 대해 wordDict로 남김없이 쪼개지면 True
            - original problem을 dp로 표현하면 dp[:i+1] = dp[:n]이 되어야 하니까 dp[n-1]을 구해야 함 (n = len(s))
            - 초기값은 모두 False
    2. recurrence relation - transition between states
        - dp[i] = True임을 어떻게 결정?
            
            1) wordDict에 들어 있는 단어 중 index i에서 끝나는 단어가 최소 하나는 있어야 함 (새로 붙이는 단어 관련)
            
            - index로 표기하면… w_len = len(w)일 때, s[x:i+1] = w여야 한다는 것이고, i+1-x = w_len이어야 함
                - 예) s=’abcd’ → s[1:4] = ‘bcd’. 3 = 4-1
                - x = i+1-w_len
            
            2) 붙이기 전까지의 부분 string이 wordDict로 formable 해야 (새로 붙이는 단어 바로 앞까지, 기존 부분 관련)
            
            - 우리는 단어를 붙여가면서 s를 만들려고 함 - 1)의 기준을 만족하는 단어가 있고, 그것을 solution 사용하려고 하면, 다른 substring의 ‘뒤’에다가 그 단어를 붙이게 될 것
            - state i가 주어졌을 때 새로운 단어는 i+1-w_len 자리에 붙게 됨 → 그렇다면 그 바로 앞인 `i-w_len` 까지의 substring은 wordDict로 formable 한 것인가?
        
        ⇒ 1)과 2)가 모두 True여야 dp[i]는 True가 될 수 있다 
        
        ```python
        for w in wordDict:
        	if s[i+1-w_len:i+1] != w:
        			continue 
        	if not dp[i-w_len]:
        			continue
        	# if both are True
        	dp[i] = True 
        	if dp[i]: break 
        ```
        
    3. base case 
        - wordDict에서 처음으로 사용되는 단어는 index 0에서 시작 → dp[-1]이 2)에 부합하는지 check해야 하는데 out of bounds → i == w_len-1 이면 2)를 만족하는 것으로 하고 넘어간다(?)
        - 예를 들어 substring 전체가 한 단어이면, 기존 부분은 “”가 되는데, “”는 무조건 True가 될 수 있도록 해야 하는데
            - dp[0]: string[:0+1 = 1]까지가 True인지 → letter 1개임. ‘’가 아니라

[139. Word Break (🪂)](139%20Word%20Break%20(%F0%9F%AA%82)%209c3bb3f9d0944d399cd88e46c48983eb.md) 

## State Transition by Inaction

- Doing nothing
    - 같은 값을 가진 두 개의 서로 다른 state를 가리킴
    - 같은 값의 새로운 state에 도착하는 경우
        - 이전 state에서 아무것도 하지 않음으로서
    - 물론 decision making process가 있긴 함
        - 단지 maximize or minimize a score 하기 위해서는 최선의 선택이 아무것도 하지 않는 것인 경우에 해당할 뿐
    - 실제로 재귀식은 이런 식이다 - dp(i, j) = max(dp(i-1, j), …).
- Doing nothing의 현신: input array에서 다음 element로 옮기는 것
    - 이건 문제에서의 제약사항 때문에 발생하는 decision making process의 일부
- 예) House robber
    - 각 집을 털거나 털지 않거나 두 가지 옵션이 있는데, 어떤 경우에는 지금 이 집을 털지 않는 게 max 노획금으로 이어짐
        - 이 경우 dp[i] 값은 dp[i-1]과 동일

## **Example 188. Best Time to Buy and Sell Stock IV**

- **A function that answers the problem for a given state.**
    - 각 state/decision에 어떤 정보가 필요한가?
        - i: 오늘이 몇 번째 날인지 (day index)
            - 그래야 현재 주식 가격(prices[i])을 알아볼 수 있으니까
            - 범위: 0~len(prices)-1
        - trx_remaining: 몇 번의 거래를 더할 수 있는지 (k)
            - 하나의 주식을 판매할 때마다 k에서 1씩 감소한다
        - holding: 갖고 있는 주식이 있는지(1) 없는지(0)
            - 문제에서의 제약: 동시에 여러 거래를 수행하는 것은 안됨. 하나의 주식을 사기 위해서는 갖고 있는 게 없거나 갖고 있던 하나를 반드시 팔아야 함
            - 그럼 우리의 state는 두 개로 좁혀짐 → 주식을 갖고 있거나(갖고 있으면 무조건 한 개만 가능), 팔았거나
            - holding = 0 → 주식을 구매할 수 있는 옵션을 갖고 있는 상태
            - holding = 1 → 무조건 판매해야 함
    
    ⇒ `dp(i, trx_remain, holding)` 
    
    - 주식 보유 상태가 holding인
    - i번째 날에 시작해서
    - trx_remain 만큼의 거래를 더 할 수 있을 때
    - 얻을 수 있는 최대의 이익
    - original problem을 함수로 표현하면 dp(0, k, 0)
- **A recurrence relation to transition between states (⭐️⭐️⭐️)**
    - holding state variable 상태에 따라 판단이 달라짐
        - holding = 1
            - 할 수 있는 행위: 팔거나 팔지 않거나
                - 판다
                    - 현재: prices[i] 만큼의 이익을 얻게 되고
                    - 미래: dp(i+1, k-1, 0)
                    
                    → prices[i] + dp(i+1, k-1, 0)
                    
                - 안 판다
                    - doing nothing - i index만 옮긴다
                    
                    → dp(i+1, k, 1)
                    
        - holding = 0
            - 할 수 있는 행위: 사거나 사지 않거나
                - 산다
                    - 현재: prices[i] 만큼의 비용을 지불
                    - 미래: dp(i+1, k, 1)
                        - 판매하지 않았기 때문에 하나의 trx를 두 요소 중 반쪽만 완료한 상태라서 k 값에는 변화 없다
                            - 주식을 구매했을 때 하나의 trx가 완료되도록 짜는 방법도 있다고 함
                    
                    → -prices[i] + dp(i+1, k, 1)
                    
                - 안 산다
                    - doing nothing - i index만 옮긴다
                    
                    → dp(i+1, k, 0)
                    
            
        
        ⇒ 각 4가지(근데 사실은 3가지 왜냐면-doing nothing은 하나의 식으로 두 경우 모두 표현 가능하기 때문에. 마지막 holding 변수를 원래 holding으로 넣어주기만 하면) 상황 중 max profit을 가져다주는 상황을 선택 
        
        ⇒ 약식으로 표현하면 
        
        ```python
        if holding:
        	dp(i, trx_remain, holding) = max(doingNothing, sellStock)
        else:
        	dp(i, trx_remain, holding) = max(doingNothing, buyStock)
        ```
        
    - 이미지
        
        ![Untitled](Untitled%2086.png)
        
- **Base cases**
    - 거래 기회가 다 소진된 경우 (trx_remain = 0)
        - 얻을 수 있는 이익은 0
    - 주어진 날짜가 다 소진된 경우 (i = len(prices))
        - 거래를 할 수 없으니 이 때도 0

# Common Patterns Continued

## State Reduction

- 예) [1770 in Strategic Approach to DP](Dynamic%20Programming%207dcf39589230406d98662b9562c792f0.md)
    - i, left, right 세 가지 state variable을 들고 문제를 풀 수도 있지만, right는 i와 left를 가지고 구할 수 있었다
    - 그래서 3개 → 2개로 state variable 개수를 줄임
    - 이렇게 하면 계산해야 하는 state 개수가 줄어서 효율적(전체 state 개수는 state variable 조합(곱)으로 표현되기 때문에)
- 시간 공간 복잡도를 모두 줄이는 경우도 있고, 공간만 줄이게 되는 경우도 있다
    - 시간 공간 복잡도를 모두 줄이는 경우는 TD, BU 구현에서 모두 적용할 수 있지만
    - 공간만 줄이는 경우는 주로 BU 구현에서 이루어짐
- 재귀식에서 제한된 숫자의 state(이전 계산 결과)를 사용할 때 공간 복잡도를 줄일 수 있음
    - 왜냐면 이전에 계산한 모든 결과를 들고 있지 않아도 되니까
- state reduction이 직접적으로 이루어지는 부분은 재귀식
    - 예) House robber
        - 하나의 state variable만 사용 - i(몇 번째 집인지)
        - 추가로 하나의 state variable을 더 사용할 수도 있음 - prev(이전 집을 털었는지 안 털었는지)
        - 코드를 보면 사실 근데 max 부분에 두 개 있던 식을 하나로 합친 거라고 밖에 안 보임(?)
            
            ```python
            class Solution:
                def rob(self, nums: List[int]) -> int:
                    @cache
                    def dp(i, prev):
                        if i < 0:
                            return 0
                        ans = dp(i - 1, False)
                        if not prev:
                            ans = max(ans, dp(i - 1, True) + nums[i])
                            
                        return ans
                    
                    return dp(len(nums) - 1, False)
            ```
            
- general advice는 없고 state variable 간의 관계를 등식으로 나타낼 수 있는지 주목해서 보기
    - 만약 등식으로 나타낼 수 있으면 등호 왼쪽과 오른쪽 중 하나의 state variable은 줄일 수 있다는 의미
    - 어떤 문제가 iteration을 필요로 하지 않으면, 보통 가능한 state reduction의 형태가 어떤 식으로든 존재하기 마련(?)
    - DP 알고리즘으로 계산된 값들이 몇 번만 쓰이고 다시는 안스이면, 변수로 array를 대체할 수 있는 가능성이 있는지 보기
        - 어떤 previous state들이 재귀식에서 사용되는지 보는 것이 시작
- 공간 복잡도를 개선할 수 있는 또 하나의 시나리오
    - 재귀식이 하나의 차원을 따라 static(iteration이 없음)한 경우
    - 예) 피보나치 : *F*(*i*)=*F*(*i*−1)+*F*(*i*−2) ← static
        - i번째 피보나치 수를 구하기 위해서는 앞의 두 숫자만 신경쓰면 됨
        
        → bottom-up 구현을 한다면 n번째 피보나치 숫자를 찾기 위해 base case에서 시작해서 쭉 올라가지만, 실제로 중간에 있는 모든 숫자에 대한 값을 array에 저장할 필요가 없다는 것을 의미. 3칸만 있으면 될듯?
        
        - F(100)을 구한다고 하면 F(2)에서 F(99)까지 계산해야 함
        - 그러나 실제 F(100)을 구하는 시점에서 필요한 정보는 F(98)과 F(99) 뿐. 나머지 90+ 개의 피보나치 수는 실제로 필요하지 않기 때문에 공간 낭비
            
            ![Untitled](Untitled%2087.png)
            
        - 코드
            - array도 필요 없고 그냥 변수 2개만 있으면 됨
            - 이러면 공간 복잡도가 O(n) → O(1) 급감. 시간은 복잡도는 변화 없음
            
            ```python
            class Solution:
                def fib(self, n: int) -> int:
            				# base case 
                    if n <= 1: return n
                    one_back = 1 # F(n-1)
                    two_back = 0 # F(n-2)
            
                    for i in range(2, n + 1):
                        temp = one_back
            						# next turn fib(i+1)에서 one back은 fib(i)
                        one_back += two_back # F(n-1) + F(n-2)
                        # next turn fib(i+1)에서 two back은 fib(n-1)
            						two_back = temp # F(n-1)
            
                    return one_back # F(n-1) + F(n-2)
            ```
            

## Counting DP

- optimum 말고 distinct ways 개수를 묻는 문제들
    - 예) [Climbing Stairs](Dynamic%20Programming%207dcf39589230406d98662b9562c792f0.md)
- 재귀식의 차이
    - optimum을 묻는 문제의 경우 min, max 등이 재귀식에 포함
    - counting DP 재귀식은 다양한 state들의 합인 경우가 많음
        - 예) Climbing Stairs에서도 dp(i) = dp(i-1) + dp(i-2)
- base case의 차이
    - optimum - state가 어떤 bound를 벗어나면 base case는 0이 됨
        - 예) [[**188. Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/description/) (🪂)**](188%20Best%20Time%20to%20Buy%20and%20Sell%20Stock%20IV%20(%F0%9F%AA%82)%2066d8df6e12fc45498219aa1d37d25af0.md) - day나 trx_remain이 한계에 도달하면 바로 0
        - 예2) [[**1143. Longest Common Subsequence**](https://leetcode.com/problems/longest-common-subsequence/description/)](1143%20Longest%20Common%20Subsequence%2006fdbe2b7c1e4d6e9d1832737d94dffc.md) - 어느 한쪽의 string 다 소진하면 바로 0 (왜냐면 “”과 아무 string의 LCS는 “”이기 때문)
    - coungting DP - base case가 0이 아닌 경우가 와왕 있음
        - 왜냐면 recurrence relation이 대개 다른 state 간의 합으로 이루어지기 때문에, base case가 0이면 0끼리 더하게 되서 어떤 다른 값으로 이어지지 않을 수 있기 때문에
        - 논리적 사고로 base case를 찾아라
            - 예) Climbing Stairs: 계단 1개를 올라가는 방법은 1개, 계단 2개를 올라가는 방법은 2개(1개 올라가고 다시 1개 or 2개를 한꺼번에)
        

## Kadane’s Algorithm

- 주어진 array의 maximum sum subarray를 O(n) 시간과 O(1) space로 얻을 수 있는 알고리즘
    - array 한 번 iteration, 상수 사용
- integer variable current를 가지고 array iteration
    - 각 index i에서 내리는 결정
        - i이전의 element들이 keep할 가치가 있는지
        - 버리는 게 나은지
- 특히 input array에 음수가 포함되어 있으면 카데인 알고가 유용
    - current가 음수가 되면 다시 초기화하고 그 index에서 시작하는 새로운 subarray를 고려
- 수도 코드
    
    ```python
    # input: nums
    best = -float('inf')
    current = 0
    n = len(nums)
    for i in range(n):
    	current = max(current + nums[i], nums[i])
    	best = max(best, current)
    return best 
    ```
    
- 기존 DP 처럼 array(function), recurrence relation, base case 식으로 framework를 따르진 않지만, 그래도 DP 카테고리에 포함됨
    - optimal sustructure 사용 - current의 이전 위치에서 끝나는 maximum subarray를 저장하며 iteration을 진행하기 때문에

# DP for Paths in a Matrix

## Pathing Problems

- input으로 matrix가 들어오고, matrix 위를 어떻게 옮겨다녀야 하는지 규칙을 제공
- 뒤로 돌아가기(moving backward)가 금지되어 있을 때 DP를 사용하는 것이 유용
    - 예) 오른쪽, 아래로만 이동이 가능한 경우
    - counting DP랑 결합되어서 도달 가능한 모든 방법의 수와 같은 식으로 문제가 나오기도 함
    - 반대로 4 방향 모두 이동할 수 있으면 graph나 BFS로 푸는 것이 적절
- 재귀식이 주로 traversal rule과 직접적으로 연결되어 있기 때문에 덜 어려운 편
    - 문제도 비슷비슷해서 general approach를 아는 것이 중요

## Example 62.Unique Paths

- pathing 문제에 있어서는 bottom-up 접근법이 더 직관적
- An array that answers the problem for a given state
    - position - (row, col)
    - state `dp[row][col]`
        - top-left corner에서 시작해 row, col 칸까지 도달하는 방법의 개수를 담고 있음
    - return value `dp[m-1][n-1]`
        - m: num rows, n: num cols
- A recurrence relation to transition between states
    - 오른쪽 아래로만 이동 가능 = 현재 있는 칸에 도달하기 위해서는
        - 바로 위쪽이나 바로 왼쪽 칸에서 왔다는 의미
        - 바로 위쪽: row-1, col
        - 바로 왼쪽: row, col-1
    - 현재 칸에 도달하기 위한 방법의 수 = 바로 위쪽에서 오는 방법의 수 + 바로 왼쪽에서 오는 방법의 수
        - `dp[row][col] = dp[row-1][col] + dp[row][col-1]`
        - 만약 row, col 값이 out of bounds 이면 dp[r][c] = 0
- Base cases
    - counting DP의 경우, base case는 non-zero로 설정되는 경우가 많다고 했음
        - zero로 설정될 경우 재귀식에서의 어떤 항들은 0에서 더 나아갈 수가 없어서
    - 이 문제에서는 top-left corner에서 시작
        - 시작점까지 도달할 수 있는 방법은 몇 개? 1개. 그냥 거기 있는 것.
        - `dp[0][0] = 1`
- AC code (bottom-up)
    
    ```python
    class Solution:
        def uniquePaths(self, m: int, n: int) -> int:
            # array
            dp = [[0] * n for _ in range(m)]
            # base case 
            dp[0][0] = 1
            # recurrence relation
            for i in range(m):
                for j in range(n):
                    if i == 0 and j == 0: continue
                    if i == 0: # no way of coming from upper cell 
                        dp[i][j] = dp[i][j-1] 
                    elif j == 0: # no way of coming from left cell 
                        dp[i][j] = dp[i-1][j]
                    else:
                        dp[i][j] = dp[i][j-1] + dp[i-1][j]
            return dp[-1][-1]
    ```
    
- AC code (top-down)
    - 보통은 top-down이 intuitive 하기 때문에 덜 효율적인데도 사용하는 거지만, pathing problems에 대해서는 bottom-up이 더 intuitive 하기 때문에 사용하는 merit가 없긴 함
    - completeness를 위해 넣은 것뿐
    
    ```python
    class Solution:
        def uniquePaths(self, m: int, n: int) -> int:
            memo = {}
            # function
            def recur(i, j):
                # base case
                if i < 0 or j < 0:
                    return 0
                if i == 0 and j == 0:
                    return 1 
                # check memoized
                if (i, j) in memo:
                    return memo[(i, j)]
                # recurrence relation
                from_top = recur(i-1, j)
                from_left = recur(i, j-1)
                memo[(i, j)] = from_top + from_left
                return memo[(i, j)]
            
            return recur(m-1, n-1)
    ```
    

# More Practice Problems