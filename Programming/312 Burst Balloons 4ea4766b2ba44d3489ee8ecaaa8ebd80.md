# 312. Burst Balloons

Status: done
Theme: DP
Created time: November 7, 2023 1:05 PM
Last edited time: May 27, 2024 7:31 PM

- matrix chain multiplication 개념 응용
- kick : [1] + nums + [1] → -1이나 len(nums)에 해당하는 경우는 1로 두고 계산하라는 조항 이용
- state dp[i][j]가 의미하는 바를 명확히 이해하지 못해 애를 먹었음
    - padding을 한 nums를 가지고 dp를 채워가는 상황
    - i와 j는 boundary의 역할만 하고, 사실은 i+1부터 j-1까지의 풍선을 하나씩 터트리는 상황에서, 풍선을 터트려 얻을 수 있는 가장 많은 동전의 수를 저장하는 것
        
        → 자연히 end에서 return 하는 값은 dp[0][n-1]. n = len(nums)이고, nums[0]과 nums[n-1] 모두 padding에 해당하는 1. 따라서 그 사이의 풍선을 어떤 순서로 터트렸을 때 얻을 수 있는 가장 많은 동전의 수가 우리가 최종으로 얻으려는 값 
        
- base case: 경계 시작과 끝 점이 연속이라서 사이에 들어있는 풍선이 없는 경우 → 당연히 0
    - 어차피 dp 테이블 초기화를 0으로 해서 코드에서는 따로 분리 X
- transition: 그보다 미리 처리된 왼쪽 풍선들로 얻을 수 있는 최대값 + 마지막으로 지목한 풍선을 터트릴 때 얻게 되는 동전 + 그보다 미리 처리된 오른쪽 풍선들로 얻을 수 있는 최대값
    
    ```python
    # nums = [3, 1, 5, 8] -> padding -> [1, 3, 1, 5, 8, 1]
    L = 4 
    i = 0
    j = 4 # i+L = 0+4 = 4
    k = 2 # k: 1~4
    
    dp[0][4] = dp[0][2] + nums[0] * nums[2] * nums[4] + dp[2][4]
    # dp[0][4]: 1~3 풍선을 터트릴 때 얻을 수 있는 가장 최대 동전 수 
    # dp[0][2]: 1번 풍선을 먼저 터트릴 때 얻을 수 있는 최대값 
    # dp[2][4]: 3번 풍선을 먼저 터트릴 때 얻을 수 있는 최대값
    # 앞에 두 개의 경우를 미리 dp table에서 가져왔다 = 1번, 3번 풍선을 터트린 상태 
    # -> 0, 2, 4번 풍선만 남아 있다 
    # -> 이 세 개에서 2번 풍선을 마지막으로 터트릴 때 얻을 수 있는 금액이
    # nums[0] * nums[2] * nums[4]
    ```
    
    - 나중에 나온 좋은 답안
        
        **`Side notes`**: In case you are curious, for the problem "**leetcode 312. Burst Balloons**", the external information to subarray `nums[i, j]` is the two numbers (denoted as `left` and `right`) adjacent to `nums[i]` and `nums[j]`, respectively. If we absorb this extra piece of information into the definition of `T(i, j)`, we have `T(i, j, left, right)` which represents the maximum coins obtained by bursting balloons of subarray `nums[i, j]` whose two adjacent numbers are `left` and `right`. The original problem will be `T(0, n - 1, 1, 1)`and the termination condition is `T(i, i, left, right) = left * right * nums[i]`. The recurrence relations will be: `T(i, j, left, right) = max(left * nums[k] * right + T(i, k - 1, left, nums[k]) + T(k + 1, j, nums[k], right))` where `i <= k <= j` (here we interpret it as that the balloon at index `k` is the last to be burst. Since all balloons can be the last one so we try each case and choose one that yields the maximum coins). For more details, refer to [dietpepsi 's post](https://discuss.leetcode.com/topic/30746/share-some-analysis-and-explanations).