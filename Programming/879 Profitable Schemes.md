# 879. Profitable Schemes

Created time: May 19, 2024 6:00 AM
Last edited time: May 19, 2024 6:21 PM

- 문제 이해
    
    i번째 범죄 → profit[i] 발생, group[i]명의 범죄가 연루
    
    어느 한 범죄에 연루된 사람은 다른 범죄에 참여 못함
    
    범죄의 subset을 구하라 - 다 합쳐서 최소 minProfit 만큼의 이익을 생성하면서, 최대 n명이 참가하도록 
    
    이런 조합이 몇 개나 나올 수 있는지 
    
    - 예제
        - 첫번째 범죄 → group2, profit 2
        - 두번째 범죄 → gorup2, profit 3 → ok
        - 누적 → group 4, profit → ok
- scratch
    - 저장해야 하는 값
        - 해당 범죄 자체의 성공 여부
        - 누적 성공 여부 - subset sum 같은 것도 필요하고
        - 아직 범죄에 연루 안된 사람이 몇 명인지도 필요하고
    - 이렇게 저장해야 하는 값이 여러 종류 일 경우, dp table을 어떻게 관리해야 하는가?
    - 어쨌든 가장 큰 제약은 사람 수인데
    - memoization도 있고, global 변수도 있으면 어떻게 해야 하나?
        - 일반적으로 전역 변수와 메모이제이션은 별도로 사용하는 것이 좋습니다. DP 문제를 해결할 때 전역 변수를 메모이제이션과 함께 사용하는 것은 일반적이지 않으며, 코드의 복잡성을 증가시킬 수 있습니다. 주로 메모이제이션을 사용하는 것이 더 나은 접근법입니다
- Editorial
    - Top-down
        - 이번 범죄를 subset에 추가하거나 안하거나
        - recursive function parameter
            - index, count, profit
            - index - 현재 고려하고 있는 범죄의 index
            - count - current subset에 참가한 총 범죄자의 수
            - profit - current subset을 가지고 생성한 이익의 합계
        - base case
            - index = 0, count = 0, profit = 0
        - state 개수를 줄일 수 있는 추가적인 방법
            - 실제 profit이 얼마인지는 중요하지 않고, minProfit을 넘기만 하면 된다
            - 넘기만 하면 current selection을 profitable scheme으로 표시할 수 있다
            - 어떤 state의 profit은 min(profit, minProfit)으로 저장할 수 있다 → profit은 minProfit보다 작거나 같은 값으로만 표시 → memoization에서 state 많이 줄일 수 있음
    - Bottom-up
        - dp state
            - dp[index][count][profit] 삼차원 dp 되시겠다~
            - idx: 0~m (m에 도달하면 모든 그룹 다 본 것)
            - count: 0~n (사람 제한)
            - profit: 0~maxProfit
                - minProfit 보다 더 큰 이익에 대해서는 굳이 그 수치대로 저장할 필요 없다. 어차피 minProfit 넘기만 하면 방법이 하나 생기는 거니까
        - base case
            - minProfit이 0도 될 수 있다는 걸 고려하면 count도 0이 될 수 있다
            - 모든 crime을 다 보고 나서 index가 m에 도착한 상태에서, 사람 수가 n 이하인 모든 경우에 대해, minProfit (사실 그 이상이더라도 여기서 clipping 됨)을 달성한 경우는 모두 1
            - 나머지 base case - index가 m에 도달했는데 profit이 min 못 넘겼다던가 사람이 n이 됐는데 profit이 min 못 넘겼다던가는 모두 0이라 어차피 default 값이라 손댈필요 없음
        - recurrence relation
            - index는 거꾸로 돌고, num_ppl와 profit은 모두 정방향으로 돈다는 점 유의
                - select + skip
                - skip: 이번 index에 대한 값 - group[i], profit[i]-을 현재 state에 반영하지 않은 채 index만 하나 늘리는 경우
                - select: 이번 index에 대한 값을 현재 state에 반영하면서 index 늘리는 경우
                    - 이 때 기존 사람 수와 현재 사람 수를 더해서 n이 넘으면 안된다
                    - profit이 min 수치보다 커지는 경우, minProfit으로 클리핑한다 - dp 공간 절약
- Trial
    - Top-down
        - TLE (예제 통과 + 7/45)
            
            ```python
            class Solution:
                def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
                    m = len(group)
                    global total_count
                    total_count = 0
                    memo = {}
                    def recur(idx, count, pro):
                        global total_count
                        # check memo
                        state = (idx, count, pro)
                        if state in memo:
                            return memo[state]
                        # base case
                        if count == n or idx == m:
                            if pro >= minProfit:
                                total_count += 1 
                            memo[state] = total_count
                            return  
                        # recursive case
                        # consider current group
                        cur_profit, cur_count = profit[idx], group[idx]
                        
                        if count + cur_count <= n:
                            recur(idx+1, count+cur_count, pro+cur_profit)
                        # skip current group 
                        recur(idx+1, count, pro)
                    recur(0, 0, 0)
                    return total_count % (10 ** 9 + 7)
            
                        
            
            ```
            
- AC 코드
    - Top-down
        - 전역 변수 사용 안함. 사실 어려운 건 없었다
        
        ```python
        class Solution:
            def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
                m = len(group)
         
                memo = {}
                def recur(idx, count, pro):
                    # check memo
                    state = (idx, count, pro)
                    if state in memo:
                        return memo[state]
                    # base case
                    if count == n or idx == m:
                        if pro >= minProfit:
                            return 1
                        return 0   
                    # recursive case
                    # consider current group
                    cur_profit, cur_count = profit[idx], group[idx]
                    select = 0
                    if count + cur_count <= n:
                        select = recur(idx+1, count+cur_count, min(pro+cur_profit, minProfit))
                    # skip current group 
                    skip = recur(idx+1, count, pro)
        
                    # save memo
                    memo[state] = select + skip 
                    return memo[state]
                
                return recur(0, 0, 0) % (10 ** 9 + 7)
        
                    
        
        ```
        
    - Bottom-up
        
        ```python
        class Solution:
            def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
                m = len(group)
                # idx, num_ppl, profit 
                dp = [[[0] * (minProfit + 1) for _ in range(n+1)] for _ in range(m+1)]
                # base case
                # idx == m & profit: minProfit (+a) -> 1 
                for num_ppl in range(n+1):
                    dp[m][num_ppl][minProfit] = 1 
                # idx == m 이면서 < minProfit 이거나 ppl == n 이면서 < minProfit 이면 모두 0 -> 따로 넣을 필요 없음
                for idx in range(m-1, -1, -1):
                    for num_ppl in range(n+1):
                        for pro in range(minProfit+1): 
                            skip = dp[idx+1][num_ppl][pro]
                            select = 0
                            cur_ppl, cur_profit = group[idx], profit[idx]
                            if num_ppl + cur_ppl <= n:
                                select = dp[idx+1][num_ppl +cur_ppl][min(minProfit, pro + cur_profit)]
                            dp[idx][num_ppl][pro] = (skip + select) % (10 **9 + 7)
                return dp[0][0][0]
        
        ```