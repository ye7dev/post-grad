# 1000. Minimum Cost to Merge Stones

Created time: June 19, 2024 8:46 PM
Last edited time: June 20, 2024 3:28 PM

- 문제 이해
    - k개의 연속된 더미를 하나로 병합. 병합 비용은 total number of stones in k piles
        - k는 주어진다
    - n개의 더미를 하나로 합치는데 드는 최소 비용을 구하라. 불가능하면 -1을 return
- scratch
    - base case를 어떻게 잡아야 할지 모르겠음
        - length = k인 경우는 merge 가능
        - k보다 작은 경우는? 그대로 두나?
    - merge를 실제 원소를 없애버리는 거 말고 어느 한 쪽으로 값을 밀고 나머지는 0으로 만들면?
- Trial
    - recursive + memo
        
        ```python
        class Solution:
            def mergeStones(self, stones: List[int], k: int) -> int:
                # prefix sum
                n = len(stones)
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stones[i-1] 
                memo = {}
                def recur(i, j, num_pile):
                    # check memo
                    state = (i, j, num_pile)
                    if state in memo:
                        return memo[state]
        
                    # base case
                    if num_pile == 1:
                        if i == j: # no need to merge
                            return 0 
                        elif j - i + 1 < k:
                            return -1
                        elif j - i + 1 == k:
                            return prefix_sum[j+1] - prefix_sum[i]
                        else:
                            return prefix_sum[j+1] - prefix_sum[i] + recur(i, j, k)
                
                    # recursive case
                    ## i <= t, t+1 <= j -> i <= t <= j-1
                    min_cost = float('inf')
                    for t in range(i, j):
                        left = recur(i, t, 1)
                        right = recur(t+1, j, num_pile-1)
                        min_cost = min(min_cost, left + right)
        
                    # save memo
                    memo[state] = min_cost
                    return memo[state]
        
                return recur(0, n-1, 1)
                        
        
                    
        ```
        
- AC 코드
    - recursive + memo
        
        ```python
        class Solution:
            def mergeStones(self, stones: List[int], k: int) -> int:
                # prefix sum
                n = len(stones)
                prefix_sum = [0] * (n+1)
                for i in range(1, n+1):
                    prefix_sum[i] = prefix_sum[i-1] + stones[i-1] 
                    
                memo = {}
                
                def recur(i, j, num_pile):
                    # check memo
                    state = (i, j, num_pile)
                    if state in memo:
                        return memo[state]
        
                    # base case
                    if num_pile == 1:
                        if i == j: # no need to merge
                            return 0 
                        elif j - i + 1 < k:
                            return float('inf')
                        elif j - i + 1 == k:
                            return prefix_sum[j+1] - prefix_sum[i]
                        else:
                            return prefix_sum[j+1] - prefix_sum[i] + recur(i, j, k)
                
                    # recursive case
                    ## i <= t, t+1 <= j -> i <= t <= j-1
                    min_cost = float('inf')
                    for t in range(i, j):
                        left = recur(i, t, 1)
                        right = recur(t+1, j, num_pile-1)
                        min_cost = min(min_cost, left + right)
        
                    # save memo
                    memo[state] = min_cost
                    return memo[state]
        
                ans = recur(0, n-1, 1) 
                if ans == float('inf'):
                    return -1
                return ans
                        
        ```
        
- 고수의 풀이 🥋
    - 3d DP
        
        ```python
        if (j - i + 1 - m) % (K - 1):
            return inf
        ```
        
    - j-i+1: 이번 구간의 길이
        - m: 병합 후에 남아야 하는 element 개수
        
        ➜ j-i+1-m: 이번 병합으로 사라져야 하는 element 개수 
        
        - % (K-1)
            - 한번에 병합할 수 있는 돌의 개수는 K. K개를 병합해서 1개가 되므로, K-1개가 병합으로 사라지는 개수
            - 따라서 (j-1+1-m)을 (K-1)로 나눈 나머지가 0이 아니면, 몇 번을 나눠도 병합되지 못하고 남는 element 개수가 1개 이상이라는 의미
                - inf로 불가능하다고 return
    - 2d DP
        
        ```python
         def dp(i, j):
            if j - i + 1 < K: return 0
            res = min(dp(i, mid) + dp(mid + 1, j) for mid in range(i, j, K - 1))
            if (j - i) % (K - 1) == 0:
                res += prefix[j + 1] - prefix[i]
            return res
        ```
        
        - 3d에서는 불가능한 경우를 inf 비용으로 return 했지만, 여기서는 0으로 return
            - 여기서는 불가능한 경우를 따로 분류하지 않고, 불가능하면 병합 안하고 그대로 원래 원소 개수로 유지된다고 생각하면 됨
        - mid가 K-1 step 씩 뛴다
            - merge 가능한 돌의 개수
                - K → 1
                - K + (K-1)
                    - 예) x x x x x 5개를 3개씩 merge
                        - xxx merge → y + 남은 x 두개는 총 3개 원소 → 다시 merge
                    - K가 merge 해서 1개로 남은 (K-1)개랑 합치면 다시 K가 되어서, 1개로 merge 할 수 있음
                - K + (K-1) + (K-1)
                    - K merge 하면 1개 남음 → 남은 원소들이랑 합치면 다시 K + (K-1) 돼서 merge 가능
            - i = 0, j = 5, K=3이라고 하면
                - mid는 0, 0+(K-1) = 2, 0+2*(K-1) = 0+4 = 4 가능
                    
                    
                    | left | right | total |
                    | --- | --- | --- |
                    | 0..0 → 병합 안하고 그대로 1개 | 1..4 → 2개 남음 | 3개  |
                    | 0..2 → 1개 남음 | 3..4 → 병합 안하고 그대로 2개 | 3개 |
                    | 0..4 → 3개 남음 → 다시 병합하면 1개 남음  | 5..5 → 병합 안하고 그대로 1개  | 2개로 끝나는 듯  |