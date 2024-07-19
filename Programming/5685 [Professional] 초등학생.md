# 5685. [Professional] 초등학생

Created time: May 13, 2024 2:36 PM
Last edited time: May 13, 2024 3:40 PM

- 문제 이해
    
    0~20까지의 수만 표현 가능. 음수도 안됨. 계산 과정에서도.
    
    N개의 수가 있고, 앞에 있는 N-1개의 수 사이에 +, -를 넣어서 계산할 때, 마지막 수가 나오게 하는 경우의 수  
    
- 힌트 분석
    
    8+3-2-4+8-7-2-4-0+8=8
    
    8+3-2-4+8-7-2-4 `+` 0+8=8 
    
    - 0은 부호를 바꿔도 값에 영향 없음
    
    8+3 `+` 2 `+` 4 `-` 8-7 `+` 2-4-0+8=8
    
    - ?
    
    8+3+2+4-8-7+2-4 `+` 0+8=8
    
    - 0은 부호를 바꿔도 값에 영향 없음
    
    8+3 `-` 2 `-` 4 `+` 8-7+2 `+`4-0 `-` 8=8
    
    → 솔직히 힌트를 다는 모르겠으나 대충 dp로 풀어야 하는 것 같다 
    
    사실 숫자 순서는 무의미한 게 아닐까? 그냥 몇 개의 카드를 쓸 수 있느냐에 관한것이지. 왜냐면 덧셈 뺄셈은 교환 결합 법칙이 성립하니까 
    
- scratch
    
    8 → dp[8] = 1 ? 
    
    8 + 3 = 11 → dp[11] += 1 
    
    8 - 3 = 5 → dp[5] += 1
    
    식이 압축되는 방향은 하나니까…! 계속 만들어 나가면 될 것 같은데?
    
    → 근데 한 계산이 끝나고 나면 2배로 후보 값이 늘어난다 
    
    8 + 3 + … = sum
    
    sum - (3 … ) = 8 
    
    - 더 시도해볼만한 것들
        - 2 이상의 count를 가진 숫자에 대해 dp[num]은 count 값과 1 중 어느걸 해야 할까? → 지금은 1로 시도한다
        - dp[0] = 1로 자동 base case처리해야할까? → 지금은 따로 처리 안한다
        - 순서…를 근데 마냥 무시할 순 없다. 왜냐면 하나의 숫자를 앞에 한 번 썼으면 다른 곳에는 못 쓰기 때문에…경로는 하나 아닌가? DFS로 풀고 싶은 유혹이 새록새록
        - 0..의 개수는 실제로 nums에0이 몇 개들었는지를 봐야할까?
            - 근데 0은 어떤 숫자를 더하고 빼서도 만들 수 있는데 그냥도 만들 수 있는데…흠
    - dp[n-1][target] = dp[n-2][target-nums[i]] + dp[n-2][target+nums[i]]
    
- AC 코드
    - base case 주의
        - dp[2][nums[0]+nums[1]] = 1, dp[2][nums[0]-nums[1]] = 1 로 무심코 했는데 여기서도 0≤num≤20로 범위 안에 드는지 확인했어야 함. 에러가 안난 걸로 봐서 아마 음수로 나온 경우에도 거꾸로 인덱스로 생각하고 1로 표시한 것 같음.
    
    ```sql
    import sys
    sys.stdin = open('temp_input/sample_input.txt', 'r')
    def get_num_cases():
        res = 0
        # dp[i][j]: nums에서 숫자를 i개까지 썼을 때 j를 만들 수 있는 방법의 개수
        target = nums.pop()
        dp = [[0] * 21 for _ in range(N)] # 숫자 사용 개수: 1~N-1
        # dp[n-1][target] = dp[n-2][target-nums[i]] + dp[n-2][target+nums[i]]
        # base case
        dp[1][nums[0]] = 1
    
        for i in range(1, N-1):
            cur_num = nums[i]
            for j in range(21):
                if 0 <= j + cur_num <= 20:
                    dp[i+1][j+cur_num] += dp[i][j] % 1234567891
                if 0 <= j - cur_num <= 20:
                    dp[i+1][j-cur_num] += dp[i][j] % 1234567891
        return dp[N-1][target] % 1234567891
    
    T = int(input())
    for t in range(1, T+1):
        N = int(input())
        nums = list(map(int, input().split()))
        ans = get_num_cases()
        print(f'#{t} {ans}')
    ```