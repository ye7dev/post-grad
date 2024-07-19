# DP 복습

Status: summary
Theme: DP
Created time: November 17, 2023 4:24 PM
Last edited time: November 17, 2023 4:52 PM

- Trapping Water Problems
    1. left_max[i]: 맨 앞부터 i까지 봤을 때 가장 높은 높이 
    2. right_max[i]: 나 다음부터 끝까지 봤을 때 가장 높은 높이 
    3. water_trapped: min(left_max[i], right_max[i])-height[i]
    4. 왼쪽 경계 오른쪽 경계 중 더 키작은 쪽이 물 가둘 수 있는 limit 
    5. base case는 0, n-1 
- Best time to buy and sell stock IV
    1. dp[i][j]: day j까지 봤을 때 최대 i번의 거래에서 실현 가능한 최대 이익