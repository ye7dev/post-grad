# 312. Burst Balloons

Created time: May 27, 2024 7:37 PM
Last edited time: May 28, 2024 11:01 AM

- 문제 이해
    - nums[i]: i번째 풍선에 써있는 숫자
    - 모든 풍선을 터트려야 함 - 얻을 수 있는 최대 점수는?
    - i번째 풍선을 터트리면
        - nums[i-1] * nums[i] * nums[i+1]의 동전을 얻게 될 것
            
            = 양 옆 풍선에 써있는 점수를 얻는 다는 의미 
            
        - i-1이 0보다 작거나 i+1이 n-1보다 큰 경우, 값을 1로 대치
- [[**546. Remove Boxes**](https://leetcode.com/problems/remove-boxes/description/?envType=problem-list-v2&envId=50vtr1g3)](546%20Remove%20Boxes%20029d1c6280684a229c8585a875647353.md) 에서 얻은 가장 큰 교훈: external information을 state 정의로 끌어와라
    
    **`Side notes`**: In case you are curious, for the problem "**leetcode 312. Burst Balloons**", the external information to subarray `nums[i, j]` is the two numbers (denoted as `left` and `right`) adjacent to `nums[i]` and `nums[j]`, respectively. If we absorb this extra piece of information into the definition of `T(i, j)`, we have `T(i, j, left, right)` which represents the maximum coins obtained by bursting balloons of subarray `nums[i, j]` whose two adjacent numbers are `left` and `right`. The original problem will be `T(0, n - 1, 1, 1)` and the termination condition is `T(i, i, left, right) = left * right * nums[i]`. The recurrence relations will be: `T(i, j, left, right) = max(left * nums[k] * right + T(i, k - 1, left, nums[k]) + T(k + 1, j, nums[k], right))` where `i <= k <= j` (here we interpret it as that the balloon at index `k` is the last to be burst. Since all balloons can be the last one so we try each case and choose one that yields the maximum coins). For more details, refer to [dietpepsi 's post](https://discuss.leetcode.com/topic/30746/share-some-analysis-and-explanations).
    
- 모르겠는 점
    
    recursive case에서 right 처리를 어떻게 해줘야 할지 모르겠음 
    
    → right는 변화 없을 듯
    
    문제는…리스트가 중간 원소가 삭제 된 상태에서 업데이트가 되어야 할 듯 같이 넣어줘야 하나? 
    
- AC 코드
    
    ```python
    class Solution:
        def maxCoins(self, nums: List[int]) -> int:
            n = len(nums)
            memo = {}
            def recur(i, j, left, right):
                # check memo
                state = (i, j, left, right)
                if state in memo:
                    return memo[state]
                # base case
                if j == i: 
                    return left * nums[i] * right 
                # recursive 
                temp = 0
                for k in range(i, j+1):
                    left_gain = recur(i, k-1, left, nums[k])
                    right_gain = recur(k+1, j, nums[k], right)
                    cur_gain = left * nums[k] * right
                    temp = max(temp, left_gain + right_gain + cur_gain)
                memo[state] = temp 
                return memo[state]
                
            return recur(0, n-1, 1, 1)
            
    ```
    
    - left, i, …, k-1, k, k+1, …, j, right가 있을 때
        - 보라색 파트, 초록색 파트를 처리하고 나면 left, k, right만 남는다!!!