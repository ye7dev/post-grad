# 920. Number of Music Playlists

Status: done, in progress, with help
Theme: DP
Created time: February 1, 2024 2:06 PM
Last edited time: February 1, 2024 3:43 PM

- Progress
    - 문제 이해
        - n개의 서로 다른 음악
        - 듣고 싶은 음악들의 개수: goal
            - goal개의 음악이 하나의 플레이리스트를 구성하는 데, 모두 달라야 하는 것은 아님
        - 플레이리스트 생성 규칙
            1. 모든 노래가 최소 한번은 재생되어야 
            2. 어떤 노래가 다시 재생되려면, 다른 k개의 노래가 재생된 후여야 함 
        - n, goal, k가 주어질 때, 생성 가능한 플레이리스트 개수는? (modulo로 return)
    - 과정
        - 앞에 몇 개 다른 음악 틀었는지를 어떻게 state에 넣어줘야 할지 모르겠음.
        - 5 → 1 까지 와서 다음 목적지가 i 일 때 num_prev
            - 1 → 0
            - 2, 3, 4, 6, 7, 8, 9 → 2
            - 5 → 1…
- Trial
    - Top-down
        
        ```python
        class Solution:
            def numMusicPlaylists(self, n: int, goal: int, k: int) -> int:
                mod = 10 ** 9 + 7
        
                memo = {}
                # function
                def recur(curr, remain, num_prev):
                    # check memo
                    state = (curr, remain, num_prev)
                    if state in memo:
                        return memo[state]
        
                    # base case
                    if remain == 0:
                        return 1 
                    
                    # recurrence relation
                    num_lists = 0
                    for next_song in range(n):
                        if next_song == curr:
                            if num_prev >= k:
                                num_lists += recur(next_song, remain-1, 0)
                        else:
                            num_lists += recur(next_song, remain-1, num_prev+1)
                    memo[state] = num_lists % mod
                    return num_lists
        
                total_num = 0
                for i in range(n):
                    total_num += recur(i, goal-1, k)
                total_num = total_num % mod
                return total_num
        ```
        
- AC 코드
    - Bottom-up
        
        ```python
        class Solution:
            def numMusicPlaylists(self, n: int, goal: int, k: int) -> int:
                mod = 10 ** 9 + 7
                # array
                dp = [[0] * (n+1) for _ in range(goal+1)]
        
                # base case
                dp[0][0] = 1 # empty playlists can contain only zero song
        
                # recurrence relation
                for length in range(1, goal+1):
                    for num_uniq in range(1, n+1):
                        # choosing same song
                        replay = max(num_uniq - k, 0) * dp[length-1][num_uniq]
                        # new song
                        new_song = (n - (num_uniq-1)) * dp[length-1][num_uniq-1]
                        dp[length][num_uniq] = (replay + new_song) % mod
                return dp[goal][n]
        ```
        
    - Top-down
        
        ```python
        class Solution:
            def numMusicPlaylists(self, n: int, goal: int, k: int) -> int:
                mod = 10 ** 9 + 7
                memo = {}
        
                # function
                def recur(length, num_unique):
                    # check memo
                    if (length, num_unique) in memo:
                        return memo[(length, num_unique)]
                    # base case
                    if length == 0 and num_unique == 0:
                        return 1 
                    ## 길이가 0인데 num_unique가 non-zero -> impossible
                    ## 길이가 non-zero 인데 num_unique가 zero -> impossible
                    if length == 0 or num_unique == 0:
                        return 0 
                    
                    # recurrence relation
                    replay = 0
                    if num_unique > k:
                        replay = (num_unique - k) * recur(length-1, num_unique)
                    new_song = (n - (num_unique-1)) * recur(length-1, num_unique-1)
                    memo[(length, num_unique)] = (replay + new_song) % mod
                    return  memo[(length, num_unique)]
        
                return recur(goal, n)
        ```
        
- Editorial
    - **Approach 1: Bottom-up Dynamic Programming**
        - Intuition
            - state definition `dp[i][j]`
                - j개의 unique songs를 담고 있는 길이 i의 가능한 playlist 개수
                    - j ≠ i 라면 → 어떤 노래는 여러번 재생이 된다는 뜻
            - original problem: dp[goal][n]
                - 만들어야 하는 플레이리스트 길이는 goal
                - 위의 state definition에서는 containing exactly 라면서 여기서는 using exactly라고 하는 군
                    - n개를 고려만 하는 것 같은데, state에서는 n개를 모두 포함하고 있는 것처럼 써서 헷갈림
                    - 제약 조건에 보면 n ≤ goal
                        - playlist 길이는 주어진 노래보다 늘 길이가 길다. 따라서 모든 valid playlist는 n개의 unique songs를 갖게 된다
            - base case
                - 0개의 unique songs로 길이 0의 playlist(empty)를 만드는 방법: 1개 - do nothing
                    - dp[0][0] = 1
            - Transitions
                - 아직 플레이리스트에 없는 노래를 추가할 경우: i도 늘고, j도 는다
                    - dp[i-1][j-1] → dp[i][j]
                    - 현재 플레이리스트에 있는 unique songs의 개수는 j-1
                    - 총 n개의 unique songs가 존재하는데 j-1개가 이미 사용되었기 때문에, 새로 추가할 수 있는 노래의 개수는 n-(j-1)
                    
                    ⇒ dp[i][j] += (n-(j-1)) * dp[i-1][j-1]
                    
                - 플레이리스트에 이미 있는 노래를 다시 추가하는 경우(replay) : i만 는다
                    - dp[i-1][j] → dp[i][j]
                    - 현재 플레이리스트에 있는 unique songs의 개수는 j
                        - 이 중에서 너무 최근에 틀었던 노래는 다시 틀 수 없음.
                        - last k played songs는 선택할 수 없다
                        - 따라서 j 개 중 마지막 k개는 리플레이 대상에서 제외되므로 가능한 선택지는 j-k
                    
                    ⇒ dp[i][j] += (j-k) * dp[i-1][j]
                    
    - **Approach 2: Top-down Dynamic Programming (Memoization)**
        - Intuition
            -