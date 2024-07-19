# 403. Frog Jump

Status: done, in progress
Theme: DP
Created time: November 22, 2023 10:34 PM
Last edited time: November 23, 2023 3:46 PM

- [x]  해설 보자 ;;
- 문제 이해
    
    `stones = [0,1,3,5,6,8,12,17]`
    
    무조건 첫번째 돌에서 출발, 1칸 jump
    
    0에서 출발, 1칸 jump → 1에 도착
    
    이전에 jump한 칸 수가 1이므로 0, 1, 2칸 jump 가능
    
    이 때 유의해야 하는게 칸이 stones list에서의 index 차이를 의미하는 게 아니라 숫자 값의 차이를 의미 → array 숫자들은 모두 오름차순 
    
- 과정
    
    상태 update 할 때 한번에 취할 수 있는 상태가 3개나 됨 
    
    중간에 5→8은 6을 거치지 않고 이동
    
- 코드 (dp)-끝까지 다 돌아야 해서 좀 느림
    
    ```python
    class Solution:
        def canCross(self, stones: List[int]) -> bool:
            n = len(stones)
            dp = [[False]*(n+1) for _ in range(n)]
            dp[0][1] = True 
    
            for i in range(1, n):
                for j in range(i):
                    jump = stones[i] - stones[j]
                    if jump <= n and dp[j][jump] is True:
                        dp[i][jump] = True
                        if jump-1 >= 0:
                            dp[i][jump-1] = True
                        if jump+1 <= n:
                            dp[i][jump+1] = True 
                        if i == n-1:
                            return True 
            return False
    ```
    
- 코드 (hashset)-중간에 바로 return 해서 빠름
    
    ```python
    from collections import defaultdict
    class Solution:
        def canCross(self, stones: List[int]) -> bool:
            if len(stones) == 0: return True 
            jump_dict = defaultdict(set) # key: stone value, value: avail jump steps
            jump_dict[0].add(1) 
            
            for i in range(len(stones)-1):
                stone = stones[i]
                for step in jump_dict[stone]:
                    reach = step + stone 
                    if reach == stones[-1]: 
                        return True 
                    jump_dict[reach].add(step)
                    if step-1 > 0:
                        jump_dict[reach].add(step-1)
                    jump_dict[reach].add(step+1)
            
            return False
    ```
    
- 남의 코드 python으로 번역(dp 아니고 hash set 사용)
    
    ```python
    from collections import defaultdict
    def canCross(stones):
    	if len(stones) == 0: return True 
    	jump_dict = defaultdict(set) # key: stone value, value: avail jump steps
    	jump_dict[0].append(1) 
    	
    	for i in range(len(stones)-1):
    		stone = stones[i]
    		for step in jump_dict[stone]:
    			reach = step + stone 
    			if reach == stones[-1]: 
    				return True 
    			#if len(jump_dict[reach]) != 0:
    			jump_dict[reach].add(step)
    			if step-1 > 0:
    				jump_dict[reach].add(step-1)
    			jump_dict[reach].add(step+1)
    	
    	return False
    ```
    
- Bottom-up
    - 1D
        - dp[i]: stones[i]에서 취할 수 있는 가능한 모든 jump size
        
        <aside>
        ⭐ 1. i보다 앞에 있는 모든 stone[j]에 대해, stone[j]에서 stone[i]로 가는 데 걸리는 거리: dist
        2. dist가 dp[j], 즉, stones[j]에서 취할 수 있는 jump 크기에 있다면 j에서 i로 갈 수 있다는 뜻
        3. j에서 i까지 오는데 dist 만큼 걸렸으므로, i에서 다음 jump로 dist-1, dist, dist+1 이동 가능
        
        </aside>
        
    - 2D
        - dp[i][k]: stone[i]에서 k크기의 jump가 가능한지 True/False
        
        <aside>
        ⭐ The maximum jump size the frog can make at each stone if possible
        // stone:        0, 1, 2, 3, 4, 5
        // jump size:  1, 2, 3, 4, 5, 6 (suppose frog made jump with size k + 1 at each stone)
        
        </aside>
        
        ```python
        def canCross(stones):
        	n = len(stones)
        	dp = [[False]*(N+1) for _ in range(N)]
        	dp[0][1] = True 
        	
        	for i in range(1, N):
        		for j in range(i):
        			jump = stones[i]-stones[j]
        			if jump <= N and dp[j][jump] is True:
        					dp[i][jump] = True 
        				# jump 크기 만큼 뛰어서 i에 도달 성공 -> i에게 허락된 점프 사이즈 추가 
        				if jump-1 >= 0:
        						dp[i][jump-1] = True
        				if jump+1 <= N:
        						dp[i][jump+1] = True 
        				# table 다 채우고 마지막에 체크
        				if i == N-1:
        						return True 
        		
        	return False
        ```