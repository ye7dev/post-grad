# 1626. Best Team With No Conflicts

Created time: May 21, 2024 4:18 PM
Last edited time: May 21, 2024 5:29 PM

- 문제 이해
    
    전체 점수가 가장 높은 팀을 선택해야 
    
    팀의 점수는 팀 안의 모든 선수들의 점수의 합
    
    충돌이 일어나면 안됨 - 어린 선수가 연장자보다 높은 점수를 내서는 안됨 
    
    - 동갑 사이에서는 발생하지 않음
    
    score, age가 주어질 때, 가장 높은 overall score를 구해라 
    
- scratch
    
    자기보다 어린 가장 최근 index가 어디에 있는지 어떻게 저장하지? 
    
    리스트를 앞에서부터 다돌아야 하나 
    
    scores
    
    [1,3,7,3,2,4,10,7,5]
    ages 
    [4,5,2,1,1,2,4,1,4]
    
    idx = 4일 때 score[idx-1] = 3, ages[idx-1] = 1
    
    → 3, 5의 경우 나이는 많지만 점수가 같기 때문에 conflict 아니라서 더할 수 있음 
    
    →  바로 뒤의 7,2의 경우 나이도 많고 점수도 높아서 idx와는 conflict 아님 
    
    - 근데 53 27끼리 conflict가 남
    
    | idx  | 4 |
    | --- | --- |
    | score | 3 |
    | age | 1 |
    
    dp[2] = 4, dp[3] = 7
    
- Trial
    - 예제 + 10/149
        
        ```python
        class Solution:
            def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
                n = len(scores)
                dp = [0] * (n+1)
                dp[1] = scores[0]
                # base case
                for i in range(2, n+1):
                    prev = 0
                    for j in range(1, i):
                        if ages[j-1] < ages[i-1] and scores[j-1] < scores[i-1]:
                            prev = max(prev, dp[j])
                        elif ages[j-1] == ages[i-1]:
                            prev = max(prev, dp[j])
                        elif ages[j-1] > ages[i-1] and scores[j-1] > scores[i-1]:
                            prev = max(prev, dp[j])
                    dp[i] = max(prev + scores[i-1], dp[i-1])
                #print(dp)
                return dp[-1]
        ```
        
    - 11/149
        
        ```python
        class Solution:
            def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
                n = len(scores)
                dp = [0] * (n+1)
                dp[1] = scores[0]
                # base case
                for i in range(2, n+1):
                    prev = 0
                    for j in range(1, i):
                        # i is older 
                        if ages[j-1] < ages[i-1] and scores[j-1] > scores[i-1]:
                            continue
                        # j is older
                        elif ages[j-1] > ages[i-1] and scores[j-1] < scores[i-1]:
                            continue 
                        else:
                            prev = max(prev, dp[j])
                    dp[i] = max(prev + scores[i-1], dp[i-1])
                return dp[-1]
        ```
        
- Editorial
    
    ```python
    ageScorePair.sort()
    for i in range(n):
        for j in range(i - 1, -1, -1):
            # If the players j and i could be in the same team.
            if ageScorePair[i][1] >= ageScorePair[j][1]:
                # Update the maximum score for the ith player.
                dp[i] = max(dp[i], ageScorePair[i][1] + dp[j])
    ```
    
    - j는 무조건 i보다 나이가 적음
    - ageScorePair[i][1] >= ageScorePair[j][1]: 점수도 i보다 작거나 같다는 뜻
    
- AC 코드
    - house robber랑 다르게 직전 index 선택하고 이번 index도 선택할 수 있어서 max(dp[i-1], dp[i]) 비교하는 건 없다
    
    ```python
    class Solution:
        def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
            n = len(scores)
            age_score_pair = []
            for i in range(n):
                age_score_pair.append((ages[i], scores[i]))
            age_score_pair.sort() ⭐️
            ans = 0
            dp = [0] * n
            # base case 
            for i in range(n):
                dp[i] = age_score_pair[i][1]
                ans = max(ans, dp[i])
            
            for i in range(1, n):
                for j in range(i-1, -1, -1):
                    if age_score_pair[i][1] >= age_score_pair[j][1]:
                        dp[i] = max(dp[i], dp[j] + age_score_pair[i][1])
                ans = max(ans, dp[i])
            
            return ans
    ```