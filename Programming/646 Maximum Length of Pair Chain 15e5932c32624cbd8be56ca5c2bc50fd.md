# 646. Maximum Length of Pair Chain

Status: done, in progress
Theme: DP, Longest Increasing Subsequence
Created time: January 18, 2024 2:47 PM
Last edited time: January 18, 2024 3:30 PM

- Process
    - 정렬해서 쭉 세어가면 되지 않을까 했는데 어차피 LIS 방식으로 하면 자기보다 앞에 있는 모든 원소를 한번씩 체크하고 넘어가기 때문에 상관없긔
    - 근데 pair를 아무 순서로 가져다가 써도 된다는 점에서 subsequence 문제랑은 달라짐
    - 근데 그럼 dp를 어떻게 쓰나? 정렬을 해야 의미가 생기지 않나
    - 정렬을 할 때 Lambda x[0] or x[1]?
        - [a, b] [c, d] 일 때 b < c 여야 하는데
        - a < b는 보장 되고
        - c < d도 보장됨
        - a <c 여도 b<c는 보장 안됨
            - a < b < d, a < c < d
            - b > c 인 경우
                - c < d. b > d 이면 [c, d] 뒤에 [a, b가 올 수 있음]
        - b<d 이면 b<d, c<d 이지만 b<c는 보장 안되긴 마찬가지
            - a<b<d,
        - 정렬은 어느 한쪽만 되는 거고 나머지는 dp로 메꿔라 대충 이런 문제인듯
        - b vs c, d vs a
            - d vs a는 자동으로 d가 더 큼
                - a < c 인데 c < d 니까
                - pair2 → pair1인 경우는 자동으로 생략되는 것과 마찬가지
            - 그럼 봐야 할 것은 pair1 → pair2가 가능한지
- AC 코드 (🪇)
    - all by myself bottom-up
        
        ```python
        class Solution:
            def findLongestChain(self, pairs: List[List[int]]) -> int:
                n = len(pairs)
                # base case: each pair is pair chain with length 1 
                dp = [1] * n
                
                # sort pairs
                sorted_pairs = sorted(pairs, key=lambda x: x[0])
        
                for j in range(1, n):
                    for i in range(j):
                        a, b = sorted_pairs[i]
                        c, d = sorted_pairs[j]
                        if b < c:
                            dp[j] = max(dp[i]+1, dp[j])
                
                return max(dp)
        ```
        
    - editorial bottom-up
        - 다른 것보다 iteration order에서 효율적일 수 있을 듯
        
        ```python
        class Solution:
            def findLongestChain(self, pairs: List[List[int]]) -> int:
                n = len(pairs)
                pairs.sort()
                dp = [1] * n
                ans = 1
        
                for i in range(n - 1, -1, -1):
                    for j in range(i + 1, n):
                        if pairs[i][1] < pairs[j][0]:
                            dp[i] = max(dp[i], 1 + dp[j])
                    ans = max(ans, dp[i])
                return ans
        ```
        
        - i, j 봐야 하는 값의 개수
            - prefix: j의 start가 고정
                - cur 고정, prev는 0부터 j-1까지 모든 위치의 원소
                - update 대상은 dp[j]
            
            ```python
            for j in range(1, n): # n-1개 
                for i in range(j): # 하나의 j당 j-1
            ```
            
            - suffix: j의 stop이 고정
                - 가장 앞에 위치한(most previous?) 원소가 고정
                - 나머지는 그 뒤부터 맨 끝까지 위치한 모든 원소
                - update 대상은 dp[i]
            
            ```python
            for i in range(n - 1, -1, -1):
                for j in range(i + 1, n):
            ```
            
            - 솔직히 여기서는 크게 차이는 게 안느껴지는데 어쨌든 후자가 더 효율적인 경우가 많다고 함
                - update 대상도 outer loop로 동일
    - 두 개를 합친 버전
        
        ```python
        class Solution:
            def findLongestChain(self, pairs: List[List[int]]) -> int:
                n = len(pairs)
                # base case: each pair is pair chain with length 1 
                dp = [1] * n
                
                # sort pairs
                sorted_pairs = sorted(pairs, key=lambda x: x[0])
        
                max_len = 1
                for i in range(n-1, -1, -1):
                    for j in range(i+1, n):
                        a, b = sorted_pairs[i]
                        c, d = sorted_pairs[j]
                        if b < c:
                            dp[i] = max(dp[j]+1, dp[i])
                    max_len = max(dp[i], max_len)
                    
                return max_len
        ```