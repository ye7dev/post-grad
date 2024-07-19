# 22. Generate Parentheses

Status: done, in progress
Theme: Divide & Conquer
Created time: November 29, 2023 12:42 PM
Last edited time: December 5, 2023 11:55 PM

- 쿨다운 미디엄
    - 전혀 쿨하지 않았고요..
- Editorial
    - Brute force
        - 2n의 길이의 모든 조합을 만든 다음 valid 한 것만 골라내기
        - queue & BFS 사용해서 길이 2n을 가진 모든 string을 생성
            - 그림
                
                ![Untitled](Untitled%20108.png)
                
            - enqueue 2개의 새로운 string
                - cur_string 길이: i → new string 길이: i+1
                - `cur_string` + `)` , `cur_string` + `(`
            - string 길이가 2n에 도달할 때까지 반복
            - 더 자세히 얘기하면 seed = “”
                
                → pop (first element 부터) → 여기서는 “” out → 여기에 각각 ), ( 붙여서 다시 queue에 집어넣음 
                
        - valid string 가려내기
            - 각 길이2n의 string들은 `(` n개, `)` n개를 갖고 있을 것
            - `left_count` 변수로 기록
                - 짝을 만나지 못한 왼쪽 괄호의 개수
                - `(` 만나면 left count += 1
                - `)` 만나면 짝을 만났으니까 left count -= 1
                - 근데 또 left_count = 0인 상태에서 `)` 가 나타나면 invalid
                    - 다르게 말하면 left count가 음수이면 짝을 찾지 못한 `)` 가 있다는 의미
                
                ⇒ 결국 string을 다 돌고 났을 때 `left_count` 가 0이 아니면 왼쪽 괄호든 오른쪽 괄호든 둘 중에 하나는 짝이 없다는 의미 → invalid
                
            - [x]  가이드대로 짜기
    - Backtracking: Keep candidate valid
        - valid string만 생성하기
            - 재귀적으로 길이 2n의 string을 생성해나가는데, 그 과정마다 validity를 체크하고, invalid이면 미완성된 substring을 바로 버림
            - 대신 한 char 전의 상태로 -여기까지는 valid 했으니- backtracking
        - `left_count`, `right_count` 변수 두 개 운용
            - `backtracking(cur_string, left_count, right_count)`
            - left_count < n → 왼쪽 괄호 더 필요. 하나 더 붙이고 left count 숫자도 늘려서 backtracking 재귀 호출
            - left_count > right count → 오른쪽 괄호가 더 필요한 상태이므로, 하나 더 붙이고 right_count 숫자 늘려서 backtracking 호출
            - 
    - Divide & Conquer
        - `F(n)` : 길이 2n이고 valid한 모든 string 집합 → 어떻게 만드는가?
        - valid 한 두 개의 substring concat → fail (redundant computation of the original problem)
            - 예
                - 길이 0의 valid string `F(0)` 과 길이 2n의 valid string `F(n)` 을 concat
                - 길이 2의 valid string `F(1)` 와 길이 2n-2의 valid string `F(n-1)` concat
                - 길이 4의 valids string `F(2)` 와 길이 2n-4의 valid string `F(n-2)` concat
            - 그러나 문제가 있다
                - `F(n)` 을 쪼개려는 목적으로 나눈 건데 오히려 `F(n)` 을 반복적으로 계산해야 하는 패착
                
                ![Untitled](Untitled%20109.png)
                
        - removing the outermost parentheses from the left string
            - 이렇게 하면 subproblem에서 만들어야 하는 괄호 쌍 수가 n-1로 제한
                
                ![Untitled](Untitled%20110.png)
                
            - 근데 그러면 제거했던 한 쌍은 어디서 다시 붙이는가?
                
                ![Untitled](Untitled%20111.png)
                
                - 이렇게 된다고 합니다…
                    
                    ![Untitled](Untitled%20112.png)
                    
        - Catalan numbers
            - `F(n) = F(0)*F(n - 1) + F(1)*F(n - 2) + ... + F(n - 1)*F(0)`
            - this general formula matches exactly with the general formula for Catalan numbers → n번째 카탈란 숫자가 정답
- Editorial 보고 짜기
    - Brute force
        
        ```python
        from collections import deque
        class Solution:
            def generateParenthesis(self, n: int) -> List[str]:
                queue = deque()
                queue.append("")
                # populate 2n strings
                while queue:
                    peek = queue[0] # first in first out 
                    if len(peek) == 2 * n:
                        break 
                    cur_string = queue.popleft()
                    queue.append(cur_string + "(")
                    queue.append(cur_string + ")")
                # check validity
                ans = []
                while queue:
                    cur_string = queue.popleft()
                    left_count = 0
                    for c in cur_string:
                        if c == '(': 
                            left_count += 1 
                        else: 
                            left_count -= 1 
                        if left_count < 0:
                             break 
                    if left_count == 0:
                        ans.append(cur_string)
                return ans
        ```
        
    - Backtracking
        - 알고보면 간접적인 backtracing이었던 것
            
            1. **Implicit Backtracking through Recursion:** Each recursive call creates a new execution context (or a new "frame" on the call stack) with its own variables. When a recursive call is made to add a left parenthesis, a new **`cur_string`** with an additional **`(`** is created and used in that call. The same applies when a right parenthesis is added. After each call completes (either hitting the base case or exploring all possibilities), the function returns to the previous call with the **`cur_string`** of that context, effectively "backtracking" to the previous state.
            
            ```python
            class Solution:
                def generateParenthesis(self, n: int) -> List[str]:
                    ans = []
                    def backtracking(cur_string, left_count, right_count):
                        if left_count == right_count == n:
                            ans.append(cur_string)
                            return 
                        if left_count < n:
                            backtracking(cur_string+"(", left_count+1, right_count)
                        if left_count > right_count:
                            backtracking(cur_string+")", left_count, right_count+1)           
            
                    backtracking("", 0, 0)
                    return ans
            ```
            
        - 명시적인 backtracking-훨씬 빠르다
            
            ```python
            class Solution:
                def generateParenthesis(self, n: int) -> List[str]:
                    ans = []
                    def backtracking(cur_string, left_count, right_count):
                        if left_count == right_count == n:
                            ans.append("".join(cur_string))
                            return 
                        if left_count < n:
                            cur_string.append("(") 
                            backtracking(cur_string, left_count+1, right_count)
                            cur_string.pop()
                        if left_count > right_count:
                            cur_string.append(")")
                            backtracking(cur_string, left_count, right_count+1) 
                            cur_string.pop()          
            
                    backtracking([], 0, 0) # string에는 append, pop method가 없다 
                    return ans
            ```
            
    - Divide & Conquer
        
        ```python
        class Solution:
            def generateParenthesis(self, n: int) -> List[str]:
                if n == 0: return [""]
        
                ans = []
                for left_count in range(n): # 0..n-1
                    for left_string in self.generateParenthesis(left_count):
                        for right_string in self.generateParenthesis(n-1-left_count): 
                            ans.append("(" + left_string +  ")" + right_string)
                
                return ans
        ```
        
- Iterative version 복기
    - stack에서 나오는 애들에게 괄호 한쌍을 더 붙여줘야 하는데 어떻게 붙여야 하는지 모르겠음
        - 제일 먼저 ()가 나온다고 생각해보자
    - 느리지만 내힘으로 짰다~잘했다 🪇
        
        ```python
        class Solution:
            def generateParenthesis(self, n: int) -> List[str]:
                def check_valid(parens):
                    left_count = 0
                    for p in parens:
                        if p == "(":
                            left_count += 1 
                        else:
                            left_count -= 1
                            if left_count < 0:
                                return False
                    if left_count == 0:
                        return True
                    return False
        
                ans = set()
                stack = ["()"]
                while stack:
                    last_pair = stack.pop()
                    if len(last_pair) == n * 2:
                        ans.add(last_pair)
                    else:
                        for i in range(len(last_pair)):
                            temp = last_pair[:i] + '()' + last_pair[i:]
                            if check_valid(temp):
                                stack.append(temp)
        
                return list(ans)
        ```
        
    - last_pair 처리 더 효율적인 방법
        - 현재
            - 중복으로 생성되는 애들을 모두 ans에 집어넣고, ans를 set으로 전환해야 하는 수고로움이 있음
            - 중간과정에서 만들어지는 모든 애들에 대해 validity 검사해서 시간이 오래 걸림
        - 개선안
            - 길이가 2n에 이르러서 ans 추가 대상인 애들만 validity 검사 → 통과한 애들은 append
            - last_pair의 모든 조합에 대해 () 붙이지 말고,
            - (랑 )를 하나씩 따로 따로 붙여서 queue에 append
            - queue는 공백으로 시작
            - dq를 사용해서 first in first out 되게끔 함
        - 코드
            
            ```python
            queue = collections.deque([""])
            while queue:
                cur_string = queue.popleft()
            
                # If the length of cur_string is 2 * n, add it to `answer` if
                # it is valid.
                if len(cur_string) == 2 * n:
                    if isValid(cur_string):
                        answer.append(cur_string)
                    continue
                queue.append(cur_string + ")")
                queue.append(cur_string + "(")
            ```