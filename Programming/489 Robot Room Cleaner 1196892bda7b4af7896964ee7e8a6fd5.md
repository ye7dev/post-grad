# 489. Robot Room Cleaner

Status: in progress, with help, 🏋️‍♀️
Theme: backtracking
Created time: December 4, 2023 9:33 PM
Last edited time: December 6, 2023 2:51 PM

- [x]  완전히는 이해 안가는데 그냥 외워서라도 한번 더 처음부터 끝까지 쭉 풀어보기
- backtracking 실습 문제-hard, premium
- 과정
    - starting 지점을 모르는데 어떻게 find solution을 정의하지?
    - 제대로 하면 청소를 다할 수 있는게 보장된 matrix라고 가정하고 따로 return 지점 두지 말아야 할 듯
    - 벽을 청소할 수 있나?
    - remove를 어떻게 하지? 갔다가 다시 돌아오면 되지. 방향을 반대로 전환해서
    - 내가 짜본 코드
        
        ```python
        class Solution:
            def cleanRoom(self, robot):
                """
                :type robot: Robot
                :rtype: None
                """
                def backtrack(candidate):
                    if not candidate: 
                        return False
                    robot.clean()
                    # down 
                    if backtrack(robot.move()):
                        robot.turnLeft()
                        robot.turnLeft()
                    robot.move()
                    # left 
                    robot.turnLeft()
                    if backtrack(robot.move()):
                        robot.turnRight()
                    robot.move()
                    # right
                    robot.turnRight()
                    if backtrack(robot.move()):
                        robot.turnLeft()
                    robot.move()
                    # up
                    robot.turnLeft()
                    robot.turnLeft()
                    if backtrack(robot.move()):
                        robot.turnRight()
                        robot.turnRight()
                    robot.move()
                    
                backtrack(robot.move())
        ```
        
- Editorial
    - constrained programming
        - 로봇이 한번 움직일 때마다 restriction을 둔다-로봇이 움직이면, 그 cell을 visited 처리한다 → 고려해야 할 조합의 숫자를 줄이는데 도움
        - visited cell은 장애물과 다름 없음
    - backtracking
        - 몇 번 움직인 다음이 로봇이 사방에 visited cell들로 둘러쌓인다고 가정
            - 근데 몇 step 이전에 다른 path로의 가능성을 보여주는 cell도 있었음
            - 그 때 그길로 가지 않았기 때문에 방은 아직 cleaned up 되지 않았음
        - 다른 길을 보여줬던 cell로 돌아와서 대안 path를 탐색한다
            - go back to the cell offering an alternative path
    - right-hand rule
        - 앞으로 계속 가면서 cell을 청소하고 visited marking
        - 장애물을 만날 때마다 오른쪽으로 turn 하고 또 go forward
        - alternative path를 탐색할 때도 분기 지점으로 돌아가서 또 turn right from your last explored direction(직전에 갔던 방향에서 오른쪽으로 돈 방향으로 다시 이동)
    - 언제 멈추냐?
        - 모든 가능한 path를 다 탐색했을 때. 각 visited cell들로부터 4 방향 다 봤을 때
    - 알고리즘
        - `backtrack(cell=(0, 0), direction=0)`
            - cell을 방문 처리하고 clean method call
            - 4개의 방향 탐색-up, right, down, left - 항상 오른쪽으로 돌아야 하기 때문에 방향 전환 순서가 중요
                - 이번 방향의 다음 cell을 체크
                    - 아직 방문 전이고 장애물이 없다면
                        - 전진
                        - 현 상태 유지하며 또 전진 `backtrack(new_cell, new_direction)`
                        - backtrack - go back to the previous cell
                - (바로 위 Line까지 다 돌고 나왔으면 이제 장애물이 있다는 것이기 때문에-도중에 방문한 cell들의 4방향까지 모두 탐색했기 때문에) turn right
    - 코드
        
        ```python
        class Solution:       
            def cleanRoom(self, robot):
                def go_back():
        						# 180도 방향 전환
                    robot.turnRight()
                    robot.turnRight()
        						# 한 칸 이동 
                    robot.move()
        						# 다시 원래 진행 방향으로 총구 전환 
                    robot.turnRight()
                    robot.turnRight()
                    
                def backtrack(cell = (0, 0), d = 0):
        						# current cell conquer
                    visited.add(cell)
                    robot.clean()
                    # going clockwise : 0: 'up', 1: 'right', 2: 'down', 3: 'left'
                    for i in range(4):
                        new_d = (d + i) % 4
        								# cell 값을 이동 방향에 맞게 update
                        new_cell = (cell[0] + directions[new_d][0], \
                                    cell[1] + directions[new_d][1])
                        
        								# 아직 방문 전이고 장애물도 아니라면 
                        if not new_cell in visited and robot.move():
        										# 지금 cell 방문 처리 한 상태서 전진 
                            backtrack(new_cell, new_d)
        										# new_cell에서 cell로 돌아오게 하는 함수!! 
                            go_back()
                        # turn the robot following chosen direction : clockwise
                        robot.turnRight()
            
                # going clockwise : 0: 'up', 1: 'right', 2: 'down', 3: 'left'
                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                visited = set() # 추가 메모리 사용 잊지 말기 
                backtrack()
        ```
        
        - 성질 나서 내가 직접 해본다
            
            
            | (0,0) |  |  |  |
            | --- | --- | --- | --- |
            |  |  |  |  |
            |  |  | obs | (2, 3) |
            - 0,0에서는 up x → right로 전진
                - backtrack(0,1) → up x → right로 전진
                    - backtrack(0, 2) → up x → right로 전진
                        - backtrack(0, 3) → up x → right x → down으로 전진
                            - backtrack(1, 3) → up x(visited) → right x → down으로 전진
                                - backtrack(2, 3) → up x(visited) → right x → down x → left x (obs) → 끝 (for loop 다 돌고 더 수행할 것이 없음
                                - `go_back`
                                    - (1, 3) 기준에서 (2,3) 간 상태. 마지막 진행 방향이 down
                                    - 여기서 turnRight 두번 하면 up
                                    - up으로 한 칸 이동 하면 (2,3) → (1,3)
                                    - 다시 방향 down으로 turnRight 두번
                                - turnRight 한번 더 하면 left. which is our next direction-for loop 마지막. (1,3)에서는 up/right/down 다 봤고 left만 남은 상태
- 복기 하면서 헷갈린 부분
    - up이 좌표가 (-1, 0)과 (1, 0) 중 전자겠지 → 그렇다
    - argument가 d였던 것 같은데 정확히 무슨 의미인지 헷갈림. 현재 진행 방향인가
        
        → 이걸 헷갈린 것이 가장 큰 장애물 
        
    - visited 때문에 cell이 tuple이어야 할 것 같은데 원소는 어떻게 update 해주지? tuple은 immutable인데 → 그냥 원소를 만들어서 tuple로 감싸서 생성을 해버린다
    - 복기하고 수정해서 통과한 코드
        
        ```python
        class Solution:
            def cleanRoom(self, robot):
                """
                :type robot: Robot
                :rtype: None
                """
                # up:0 -> right:1 -> down:2 -> left:3
                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                visited = set()
                def go_back():
                    # 180도 회전
                    robot.turnRight()
                    robot.turnRight()
        						# 반대방향으로 한 걸음 
                    robot.move()
        						# 추가 180도 회전 해서 총 360도 회전 
                    robot.turnRight()
                    robot.turnRight()
        
                def backtrack_robot(cell=(0, 0), d=0):
                    # current cell work : cleaning, marking
                    robot.clean()
                    visited.add(cell)
        
                    # expand
                    for i in range(4):
        								# 좌표 조정
                        new_d = (d + i) % 4
                        new_cell = (cell[0] + directions[new_d][0], \
                                    cell[1] + directions[new_d][1])
                        
                        if new_cell not in visited and robot.move():
                            backtrack_robot(new_cell, new_d)
                            go_back()
        								# 실제 로봇 방향 조정 
                        robot.turnRight()
                
                backtrack_robot()
        ```
        
        - direction 관련하여…
            - d는 처음에 0으로 시작(up)
                
                
                | i = 0 | d + 0 = 0+0 = 0 | d + 0 = 1  |
                | --- | --- | --- |
                | i = 1 | d + 1 = 1  | 2 |
                | i = 2 | d + 2 = 2 | 3 |
                | i = 3 | d+ 3 = 3  | 4 % 4 = 0 |
            - 현재 d가 어디든 up→right→down→left 시계 방향의 cycle 안에서 다음 움직일 순서를 i와 %4로 알게 됨 → which is `new_d`
            - i는 늘 0부터 시작이니까 new_d의 제일 처음 값은 d와 동일
            - go_back()을 하고 나면 다시 총구가 원래 자리로 돌아와있음(360도 회전이기 때문에)
            - 다음 진행 방향은 늘 오른쪽이니까 거기서 turnRight를 무조건 해줘야 함

[1](1%2080493dbdd9484f1c9cd851898ca47fd2.md)