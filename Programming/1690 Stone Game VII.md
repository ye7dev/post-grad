# 1690. Stone Game VII

Created time: June 15, 2024 3:46 PM
Last edited time: June 17, 2024 10:36 PM

- 문제 이해
    - n개의 돌
    - 번갈아 가면서 플레이, 가장 왼쪽 혹은 오른쪽에 있는 돌을 제거
    - 이 때 얻는 점수는 남은 돌의 합
        - 그럼 가장 오른쪽 혹은 왼쪽에 있는 돌 중에 가장 작은 점수의 돌을 지워야 겠네
    - 모든 돌이 제거 되었을 때 승자는 더 높은 점수를 가진 사람이지만, bob이 늘 지게 되어 있다
    - 그래서 bob의 전략은 점수 차를 최소화하는 것
        - 반대로 alice는 점수 차를 최대화 하는 것
- Scratch
    - 점수 자체가 아니라 점수 차이를 서로 다른 전략으로 유지하려는 상황은 어떻게 달라지는지 확인하기
- Trial
    - recursive + memo (time out. 58/68)
        
        ```python
        class Solution:
            def stoneGameVII(self, stones: List[int]) -> int:
                memo = {}
                n = len(stones)
                def recur(i, j, is_alice):
                    state = (i, j, is_alice)
                    total = sum(stones[i:j+1])
                    # check memo
                    if state in memo:
                        return memo[state]
                    # check base case
                    if i > j:
                        return 0 
                    # recursive case
                    if is_alice:
                        left_gain = total - stones[j] + recur(i, j-1, not is_alice)
                        right_gain = total - stones[i] + recur(i+1, j, not is_alice)
                        memo[state] = max(left_gain, right_gain)
                    else:
                        left_gain = - total + stones[j] + recur(i, j-1, not is_alice)
                        right_gain = - total + stones[i] + recur(i+1, j, not is_alice)
                        memo[state] = min(left_gain, right_gain)
                    
                    return memo[state]
        
                return recur(0, n-1, True)
        ```
        
    - ~ + prefix_sum (memory out. 65/68)
        
        ```python
        class Solution:
            def stoneGameVII(self, stones: List[int]) -> int:
                memo = {}
                n = len(stones)
                prefix_sum = [0] * (n+1)
                prefix_sum[1] = stones[0]
                for i in range(1,n):
                    prefix_sum[i+1] = prefix_sum[i] + stones[i]
                def recur(i, j, is_alice):
                    state = (i, j, is_alice)
                    total = prefix_sum[j+1] - prefix_sum[i]
                    # check memo
                    if state in memo:
                        return memo[state]
                    # check base case
                    if i > j:
                        return 0 
                    # recursive case
                    if is_alice:
                        left_gain = total - stones[j] + recur(i, j-1, not is_alice)
                        right_gain = total - stones[i] + recur(i+1, j, not is_alice)
                        memo[state] = max(left_gain, right_gain)
                    else:
                        left_gain = - total + stones[j] + recur(i, j-1, not is_alice)
                        right_gain = - total + stones[i] + recur(i+1, j, not is_alice)
                        memo[state] = min(left_gain, right_gain)
                    
                    return memo[state]
        
                return recur(0, n-1, True)
        ```
        
    - ~ + one_player (memory out. 66/68)
        
        ```python
        class Solution:
            def stoneGameVII(self, stones: List[int]) -> int:
                memo = {}
                n = len(stones)
                prefix_sum = [0] * (n+1)
                for i in range(1,n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stones[i-1]
                    
                def recur(i, j):
                    state = (i, j)
                    total = prefix_sum[j+1] - prefix_sum[i]
                    # check memo
                    if state in memo:
                        return memo[state]
                    # check base case
                    if i == j:
                        return 0
                    # recursive case
                    left_gain = total - stones[j] - recur(i, j-1)
                    right_gain = total - stones[i] - recur(i+1, j)
                    memo[state] = max(left_gain, right_gain)
        
                    return memo[state]
        
                return abs(recur(0, n-1))
        ```
        
- Editorial
    - recursive + memo (mle)
        - [[**877. Stone Game**](https://leetcode.com/problems/stone-game/description/?envType=problem-list-v2&envId=50vtr1g3)](877%20Stone%20Game%2093e1ff838dd641f39daf2634eac550f4.md) 에서도 이해하기 조금 어려웠던 부분 - bob의 점수는 음수로 계산된다
            - bob이 alice의 점수를 줄이는 역할을 하기 때문이라고 함
        - 따라서 차를 구할 때도
            - alice 차례에서는 `지금까지의 점수 차이 + 이번에 얻는 점수` 로 이번에 얻는 점수가 차이에 더해지는 반면
            - bob의 차례에서는 `지금까지의 점수 차이 - 이번에 얻는 점수` 로 차이에서 점수가 빼진다
            - 예
                - 돌이 [a, b, c, d] 있다. diff는 0에서 시작
                - alice 입장: a 제거하고 b+c+d 점수 가져감. 현재 diff는 b+c+d
                - bob 입장: d 제거하고 b+c 점수 가져감. 현재 diff는 d
                    - b + c + d (이전 diff) - (b + c) (이번에 얻는 점수)
        - base case
            - start = end일 때 남은 돌은 한 개
            - alice나 bob 누가 이 돌을 제거하던, 남은 돌이 0개라서 얻을 수 있는 점수도 0
    - top-down optimized
        - bob이나 alice 둘 다 점수를 최대화하고자 한다
            - 그러기 위해서는 상대에게 최대한의 maximum difference를 돌려줘야 한다
            - current difference는 현재 점수에서 상대방이 돌려준 difference를 빼야 한다
    - bottom-up
        - base case
            - i == j
                - stone[i:j]에 원소 하나만 있음
                - 둘 중 누가 뭘 가져가도 남는 원소 없어서 difference = 0
        - recursive case
            
            ![Untitled](Untitled%2024.png)
            
            - 재귀식 자체는 동일
                - 맨 앞의 원소를 가져가면 그 뒷부분 범위에 미리 계산된 값
                - 맨 뒤의 원소를 가져가면 그 앞부분 범위에 미리 계산된 값
- AC 코드
    
    ```python
    class Solution:
        def stoneGameVII(self, stones: List[int]) -> int:
            n = len(stones)
            # prefix sum
            prefix_sum = [0] * (n+1)
            for i in range(1, n+1):
                prefix_sum[i] = prefix_sum[i-1] + stones[i-1]
            
            # dp init
            dp = [[0] * n for _ in range(n)]
            
            # base case - auto covered
            ## dp[i][i] = 0 
    
            # recursive case        
            for start in range(n-2, -1, -1):
                for length in range(2, n+1-start): 
                    # inclusive end : length = end + 1 - start
                    end = start + length - 1 # start + length - 1 < n -> length < n+1-start
                    # start+1, ..., end
                    front_gain = prefix_sum[end+1] - prefix_sum[start+1]
                    # start, ..., end-1
                    back_gain = prefix_sum[end] - prefix_sum[start]
                    
                    front_diff = front_gain - dp[start+1][end]
                    back_diff = back_gain - dp[start][end-1]
    
                    dp[start][end] = max(front_diff, back_diff)
            return dp[0][n-1]
    ```