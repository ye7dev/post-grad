# 746. Min Cost Climbing Stairs (🪂)

Status: done, in progress
Theme: DP
Created time: January 9, 2024 3:56 PM
Last edited time: January 9, 2024 4:10 PM

- Process
    - 원래는 memo를 사용했는데 변수로 대체해야 할 것 같음
    - 우선 재귀식을 짜자
        - 원래 state : dp(i): i step까지 도달하는 최소한의 비용 → top이 0-indexed로 따지면 n이기 때문에, 0부터 n+1까지의 공간이 필요했음
        - 그리고 base case는 공짜로 갈 수 있는 start 지점인 0과 1
        - dp(n) = min(dp(n-2) + cost[n-2], dp(n-1) + cost[n-1])
    - 여기도 결국 이전 두단계에 대한 정보만 필요함
- array 대신 변수 쓴 버전의 DP 🪇
    - edge case에서 한번 삐끗했음. cost 최소 길이가 2인데, 이 경우 도달해야 하는 top은 2(0, 1, 2)라서 공짜 start 지점을 넘어섬 → 돈을 한 번은 내고 0에서 2만큼 가거나 1에서 1만큼 가야 2에 도착 가능. 둘 중 더 cost가 적은 경로를 선택
    
    ```python
    class Solution:
        def minCostClimbingStairs(self, cost: List[int]) -> int:
            # edge case
            if len(cost) == 2:
                return min(cost)
            
            # base case: starting from 0, 1 is for free
            one_step_back = 0 
            two_step_back = 0
    
            # iteration of the recurrence relation
            n = len(cost)
            for i in range(2,n+1):
                temp = one_step_back
                one_step_back += cost[i-1]
                two_step_back += cost[i-2]
                one_step_back = min(one_step_back, two_step_back) # dp(i)
                two_step_back = temp # dp(i-1)
            
            return one_step_back
    ```