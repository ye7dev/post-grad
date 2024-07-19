# 877. Stone Game

Created time: June 15, 2024 2:26 PM
Last edited time: June 15, 2024 8:06 PM

- 문제 이해
    - 짝수 더미 - 각 더미는 piles[i] 개수의 (양의 정수) 돌을 가지고 있음
    - 가장 많은 돌의 개수를 가지고 게임을 끝내는 것
    - 모든 더미의 돌의 개수를 합하면 홀수 - 동점은 없다
    - 앨리스가 시작 → 밥이 이어서
        - 각 turn에서 자기 차례인 사람이 가장 앞이나 뒤에서 돌을 가져감. 더미 전체의 돌을
        - 돌더미가 더 이상 없을 때까지 반복하다가, 가장 많은 돌을 가진 사람이 이기는 게임
    - 앨리스가 이기게 되면 True return
- scratch
    - 앨리스가 경기를 시작하기 때문에 짝수 index(0부터) turn
    - turn에서 맨 앞 더미를 가져가거나
    - 맨 뒤 더미를 가져가거나
    - base case
        - index가 len(더미)면 게임이 끝나는 것
    - recursive
        
        a […] → ab[…] or a[…]b 
        
        […]a → b[…]a or […]ba
        
    - 둘 다 optimal 하다는 게 문제…
        - 우선 알리스 입장에서 최적인 쪽으로 문제를 풀어보자
- AC 코드
    - recursive + memo
        - 매우 느리지만 해결
        
        ```jsx
        class Solution:
            def stoneGame(self, piles: List[int]) -> bool:
                n = len(piles)
                total = sum([piles[i] for i in range(n)])
                memo = {}
                def recur(i, stones):
                    # check memo
                    state = (i, tuple(stones))
                    if state in memo:
                        return memo[state]
                    
                    # base case 
                    if len(stones) == 0:
                        return 0
                    if len(stones) == 1:
                        return stones[0]
                    
                    # recursive case
                    front = max(recur(i+2, stones[2:]), recur(i+2, stones[1:-1]))
                    take_front = stones[0] + front 
                    end = max(recur(i+2, stones[:-2]), recur(i+2, stones[1:-1]))
                    take_end = stones[-1] + end
        
                    # save memo
                    memo[state] = max(take_front, take_end)
        
                    return memo[state]
        
                alice_gain = recur(0, piles)
                if alice_gain * 2 > total:
                    return True
                return False
                        
        
        ```
        
    - after editorial
        
        ```python
        class Solution:
            def stoneGame(self, piles: List[int]) -> bool:
                n = len(piles)
                memo = {}
                def recur(i, j, is_alice): # inclusive
                    # check memo
                    state = (i, j, is_alice)
                    if state in memo:
                        return memo[state]
        
                    # base case
                    if i > j: # invalid range
                        return 0
        
                    # state transition
                    if is_alice: # max strategy
                        take_head = piles[i] + recur(i+1, j, not is_alice)
                        take_tail = piles[j] + recur(i, j-1, not is_alice)
                        memo[state] = max(take_head, take_tail)
        
                    else: # bob has to minimize alice's score
                        take_head = -piles[i] + recur(i+1, j, not is_alice)
                        take_tail = -piles[j] + recur(i, j-1, not is_alice)
                        memo[state] = min(take_head, take_tail)
        
                    return memo[state]
        
                return recur(0, n-1, True) > 0
        
        ```
        
- Editorial
    - Bob이 점수를 딸 때마다 Alice의 점수로부터 빼기
    - dp(i, j): pile[i..j]가 남았을 때 alice가 딸 수 있는 최대 점수
        - dp(i+1, j)와 dp(i, j-1)의 관계로 식 세우기
    - 자기 차례인 선수는 최대 2개의 move를 가질 수 있음
        - 누구 차례인지는 (j-i-N) % 2로 알 수 있음
            - 전체 원소 개수: N
            - j-i: 현재 남은 돌더미의 개수
            - N - (j-i) = 이미 가져간 돌더미의 개수 = 현재까지 플레이한 게임 수
            - N - (j-i) = - ((j-i) - N) 이고, (a-b) % 2와 (b-a) % 2는 같다고 한다
            - 그래서 수식에서 (j-i-N)으로 쓴 듯
    - 내가 세운 수식이랑 같은데, 이제 alice말고 bob의 입장에서도 고려한 내용이 있음
        - 첫번째 게임의 경우, j = N-1, i = 0. N-1-N = -1. -1%2 = 1. alice 순서
            - 앞의 더미 + dp(나머지 범위), 뒤의 더미 + dp(나머지 범위) 중 max를 가져간다
        - 두번째 게임의 경우, bob 순서
            - bob의 입장에서 더 큰 점수를 가져간다 = alice 입장에서는 더 큰 점수를 잃는다
            - 앨리스 입장에서 수식이 쓰이기 때문에 -piles[k] + dp(나머지 범위)가 되는데, bob 이 자신의 입장에서 최적화로 play 한다고 하면, 이 값을 작게 만들어야 한다.