# 494. Target Sum

Created time: May 17, 2024 3:33 PM
Last edited time: May 17, 2024 4:33 PM

- scratch
    
    [[5685. [Professional] 초등학생](https://swexpertacademy.com/main/code/problem/problemDetail.do?problemLevel=4&problemLevel=5&problemLevel=6&contestProbId=AWXRzHv6h_YDFAUo&categoryId=AWXRzHv6h_YDFAUo&categoryType=CODE&problemTitle=professional&orderBy=FIRST_REG_DATETIME&selectCodeLang=ALL&select-1=6&pageSize=10&pageIndex=2)](5685%20%5BProfessional%5D%20%E1%84%8E%E1%85%A9%E1%84%83%E1%85%B3%E1%86%BC%E1%84%92%E1%85%A1%E1%86%A8%E1%84%89%E1%85%A2%E1%86%BC%209d927b465c9f4cebb01b1f0fb84f9cf9.md) 랑 비슷한 문제 같은데 음수도 target으로 나올 수 있음. 
    
- Trial
    - 모르겠다
        
        ```python
        class Solution:
            def findTargetSumWays(self, nums: List[int], target: int) -> int:
                n = len(nums)
                dp = [[0] * (target + 1) for _ in range(n+1)]
                # base case
                dp[0][0] = 1  
                dp[1][nums[0]] = 1 
                # recursive case 
                for i in range(1, n+1):
                    for j in range(target+1):
                        for k in range(i):
                            if j - nums[k] >= 0:
                                dp[i][j] += dp[i-1][j-nums[k]]
                            if j + nums[k] <= target:
                                dp[i][j] += dp[i-1][j+nums[k]]
                return dp[n][target]
        ```
        
    - 108/140
        
        ```python
        class Solution:
            def findTargetSumWays(self, nums: List[int], target: int) -> int:
                n = len(nums)
                total = sum(nums) # index range: -total ~ total -> + total -> 0~2*total
                if abs(total) < target:
                    return 0 
                dp = [[0] * (2 * total + 1) for _ in range(n+1)]
                # base case
                dp[n][2 * total] = 1 # target: total 
                dp[n][0] = 1 # target: -total
                dp[1][total + nums[0]] = 1 
                dp[1][total - nums[0]] = 1
                if nums[0] == 0:
                    dp[1][total] += 1
                # dp[0][0] = 1? or not?
        
                # recursive case
                for i in range(2, n+1):
                    cur_num = nums[i-1]
                    for j in range(-total, total+1):
                        # ... + cur_num = value -> ... = value - cur_num
                        if cur_num == 0:
                            dp[i][j + total] += dp[i-1][j+ total]
                            continue
                        if -total <= j - cur_num :
                            dp[i][j + total] += dp[i-1][j-cur_num + total]
                        # ... - cur_num = value -> ... = value + cur_num 
                        if j + cur_num <= total:
                            dp[i][j + total] += dp[i-1][j + cur_num + total]
                return dp[n][total + target]
        
        ```
        
        - 반례 : [0,0,0,0,0,0,0,0,1]
            
            +, - 0 하면 값은 하나지만 방법 자체는 두 개로 봐야 할 것 같은데… 
            
- Editorial
    
    <aside>
    📌 dp state
    
    - dp[i][val] : nums[i]까지 사용해서 val-total(sum(nums)) 값을 만드는 방법의 수
    - val: 0~2*total → val-total: -total~total 까지 가능!!!
        - 물론 개수로 따지면 2*total + 1
    </aside>