# 점화식은 제대로 찾았는데 base case가 tricky

- 내가 내린 state 정의
    - dp[i]: i개의 stair에 오르는 비용의 array가 주어졌을 때, top = i+1 번째 stair = index 상으로는 i에 도달하는 비용
        - 우리가 구하고자 하는 답: dp[n] - n개 stair에 오르는 비용의 array가 주어졌을 때, top = n+1, index 상으로는 n에 도달할 때 드는 최소 비용
        - dp[0] : 계단이 0개라서 top이 index 0이지만 도달할 수가 없다. 흠 여기서부터 잘못된 정의란 걸 느꼈어야 했나?
        - dp[1] : 계단은 1개, top은 index 1.
            - index 0에서 시작. cost[0]을 내고 한 칸 올라서 index 1에 도달하면 된다고 생각해서 cost[0]
            
            👽 근데 문제에서 You can either start from the step with index `0`, or the step with index `1`.
            
            ↳ 굳이 딴지를 걸자면, 원소가 1개 밖에 없을 때도 index 1에서 시작할 수 있는가? 
            
            → 만약 이게 가능하다고 하면 dp[1]은 0이 되어야 
            
            → 이게 안되면 dp[1] = cost[0]
            
    
    ⇒ 두루뭉술한 dp[1]은 오답으로 이어지고 말았다 …
    
- 솔루션에서의 state 정의
    - dp[i]: i번째 계단을 오르는데 드는 비용
    - 따로 early return 조건문 없음
        - len(nums) 최소 값은 2 → 그러니 dp[0], dp[1]은 vaild case 일 수 밖에 없고. description에 따라 두 경우 모두 비용은 0이다
    - return 해야 하는 정답
        - dp[n+1]. dp[n]은 n번째 계단을 오르는데 드는 비용인데, top은 beyond nth stair, n+1 번째 stair이라고 할 수 있다