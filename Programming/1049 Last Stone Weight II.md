# 1049. Last Stone Weight II

Created time: May 30, 2024 4:44 PM
Last edited time: May 30, 2024 5:18 PM

- scratch
    
    정렬후에는 한쪽방향으로만 해도 될 듯 
    
    memoization이 문제다 
    
- trial
    - 시간 초과 78/90, top_down
        
        ```python
        class Solution:
            def lastStoneWeightII(self, stones: List[int]) -> int:
                memo = {} 
                stones.sort()
                def recur(arr):
                    # check memo
                    state = tuple(arr)
                    if state in memo:
                        return memo[state]
                    
                    m = len(arr)
                    # base case 
                    if m == 0:
                        return 0
                    if m == 1:
                        return arr[0]
        
                    # recursive case
                    min_weight = float('inf')
                    for i in range(m-1):
                        if arr[i+1] - arr[i] == 0:
                            mid = []
                        else:
                            mid = [arr[i+1] - arr[i]]
                        new_arr = arr[:i] + mid + arr[i+2:]
                        new_arr.sort()
                        min_weight = min(min_weight, recur(new_arr))
                        
        
                    memo[state] = min_weight
                    return memo[state]
                
                return recur(stones)
        ```
        
- solution
    - 상상도 못한 접근
        - **for every example, actually certain elements are being added and certain elements are being subtracted-**
            - **for eg: 2 7 4 1 8 1- => (8-7) (4-2) (1-1)**
                - **lets say in first go we smashed these stones- => 1 2 0**
                - **in the second go we can smash 2 and 1 and weight of left stone will be 1 which is minimum**
            
            **=> basically this is equivalent to (8-7) - (4-2) + (1-1) = 8 + 2 + 1 - 7 - 4 - 1-** 
            
            **=> 8 + 2 + 1 - 7 - 4 - 1 this is equal to (8, 2, 1) - (7, 4, 1)**
            
            **=> overall it is equal to dividing the stones array such that their difference is least - which gives us least weight**
            
- AC 코드
    - Top-down
        - 엄청 쉬운 knapsack이었음
        
        ```python
        class Solution:
            def lastStoneWeightII(self, stones: List[int]) -> int:
                memo = {}
                total = sum(stones)
                n = len(stones)
                def recur(i, team_plus):
                    # check memo:
                    state = (i, team_plus) # team_minus = total-team_plus
                    if state in memo:
                        return memo[state]
                    # check base case
                    if i == n:
                        team_minus = total-team_plus
                        return abs(team_plus-team_minus)
                    # recursive case
                    send_left = recur(i+1, team_plus + stones[i])
                    send_right = recur(i+1, team_plus)
                    # save memo 
                    memo[state] = min(send_left, send_right)
                    return memo[state]
                return recur(0, 0)
        ```