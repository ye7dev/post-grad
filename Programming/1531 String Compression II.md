# 1531. String Compression II

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP
Created time: January 31, 2024 1:37 PM
Last edited time: January 31, 2024 4:52 PM

- Trial
    - dp 안에 counter 넣기
        - recurrence relation 못 찾음
        
        ```python
        from collections import Counter
        class Solution:
            def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
                count = Counter(s)
                encoded = ""
                for c in count:
                    if count[c] == 1:
                        encoded += c
                    else:
                        combi = c + str(count[c])
                        encoded += combi
                # edge case 
                if k == 0:
                    return len(encoded)
        
                keys = list(count.keys())
                
                 # dp[i][c]: min len of encoded string after deleting char c for the i th deletion
                dp = [[Counter(s) for _ in range(len(count))] for _ in range(k)]
        
                # base case
                for i in range(len(keys)):
                    c = keys[i]
                    if count[c] == 1 or count[c] % 10 == 0:
                        dp[0][i]['c'] -= 1 
                
                # recurrence relation
                for chance in range(2, k):
                    for i in range(len(keys)):
                        c = keys[i]
                        if count[c] <= 0:
                            continue
        ```
        
    - post-editorial: top-down
        - base case를 모르겠다, 그리고 return 시작점도 모르겠다
        
        ```python
        class Solution:
            def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
                memo = {}
                n = len(s)
                # edge case
                if n == 1:
                    return 1 
                # function
                def recur(i, last_letter, last_count, chance):
                    state = (i, last_letter, last_count, chance)
                    if i == n:
                        return 0
        
                    cur_letter = s[i]
                    # delete
                    delete = recur(i+1, last_letter, last_count, chance-1)
                    # not delete - same letter
                    if last_letter == cur_letter:
                        not_delete = recur(i+1, last_letter, last_count+1, chance)
                        #if last_count in [1, 9, 99]:                    
                            #not_delete += 1 
                    # not delete - diff letter
                    else:
                        if i == 0:
                        not_delete = 1 + len(last_count) + recur(i+1, cur_letter, 1, chance)
                    memo[state] = min(delete, not_delete)
                    return memo[state]
                    
                return recur(0, "", 0, k)
        ```
        
    - memo version(TLE)
        
        ```python
        class Solution:
            def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
                memo = {}
                n = len(s)
                # function
                def recur(i, last_letter, last_count, chance):
                    state = (i, last_letter, last_count, chance)
                    if chance < 0:
                        return float('inf')
                    if i == n:
                        return 0
        
                    cur_letter = s[i]
                    # delete
                    delete = recur(i+1, last_letter, last_count, chance-1)
                    # not delete - same letter
                    if last_letter == cur_letter:
                        not_delete = recur(i+1, last_letter, last_count+1, chance)
                        if last_count in [1, 9, 99]:                    
                            not_delete += 1 
                    # not delete - diff letter
                    else:
                        not_delete = 1 + recur(i+1, cur_letter, 1, chance)
                    memo[state] = min(delete, not_delete)
                    return memo[state]
                    
                return recur(0, "", 0, k)
        ```
        
- Progress
    - 문제 이해
        - 연속으로 2번 이상 나오는 동일한 문자를 대체 → 그 문자랑 나온 횟수로
            - 예) aabccc → a2bc3
        - 한번만 나오는 문자에 대해서는 1을 따로 붙이지 않는다
        - s, k가 주어질 때, s로부터 최대 k개의 문자를 지울 수 있음
            - run-length encoded version of s의 길이가 최소가 되도록
        - s를 run-length encoding 했을 때의 길이가 최소화되도록, 최대 k개의 문자를 지울 때, s의 run-length encoded string의 최소 길이를 구하라
    - 과정
        - 동일한 문자가 많을 수록 encoded string의 길이가 짧아지지 않을까?
            - 아 근데 single char의 경우 뒤에 숫자 1을 안 붙여서 최소 길이 1이 됨
            - 연속으로 같은 게 나오는 경우는 최소 2 (문자랑 나온 횟수)
            - 길이를 줄이는 방법은 크게 두 개
                - 문자+횟수의 경우
                    - 횟수를 1로 만들어서 문자만 남도록 만들기
                    - 횟수를 0으로 만들어서 문자도 횟수도 안 남도록 만들기
                - 문자만 있는 경우
                    - 하나 남은 것도 지워서 0으로 만들기
                - 제일 쓸모없는 경우
                    - 횟수를 1 감소 시켜서 여전히 encoded length에 변함이 없도록 만들기
                - 문자가 횟수인 경우도 생각해야 함
        - 예제 - aaabcccd → a3bc3d, k=2
            - bcd 중 두 개를 없애면 6-2=4
        - 사전을 dp 안에 넣는 경우
            - [사전] * n 한 뒤 사전 중 하나를 수정하면 뒤에도 다 수정된다
                
                ```python
                >>> y = [count] * 2
                >>> y[0]['c'] -= 1
                >>> y
                [Counter({'c': 3, 'a': 1, 'b': 1}), Counter({'c': 3, 'a': 1, 'b': 1})]
                ```
                
            - y = [count for _ in range(3)] 해도 마찬가지
            - 그치만 Counter 자체를 여러 개 넣어주면 원소 하나의 key value만 바꿀 수 있다
        - 이전 상태가 뭘까?
        - 개수만 보관하면 될 것 같은데
        
- AC 코드
    - 주어진 기회를 다 썼는데 아직 탐색할 string이 남아 있다면 정답에 고려될 수 없는 경우 → 무한대 값을 부여해서 앞 단계 함수에서 min 적용 시에 배제될 수 있도록 함
    - 원래 내가 했던 생각: letter가 같은 것끼리 묶어서 나오는 줄 알고, letter가 바뀔 때는 앞에 누적된 count랑 letter를 정답에 더해줘야 한다고 생각했음
        - 근데 사실은 새로운 문자가 들어오면 not_delete에서 +1 되고
        - 이 문자의 등장 횟수가 1일 때까지는 encoded string에 포함되지 않음
        - 그러다가 2번째로 등장하면 그 때부터는 횟수도 encoded string에 포함되는데
            - last_letter == cur_letter 이면서 last_count = 1인 경우에 +1 되는 것이 이 상황을 커버함
    - i = 0, last_letter = “” 인 경우
        - not delete same letter인 경우는 존재하지 않는다
        - delete로 쭉 가지치기 하다가 chance가 0보다 작아지면 알아서 무한대가 되면서 min 연산 시에 사라지게 됨
    
    ```python
    class Solution:
        def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
            memo = {}
            n = len(s)
            # function
            @lru_cache(maxsize=None)
            def recur(i, last_letter, last_count, chance):
                state = (i, last_letter, last_count, chance)
                if chance < 0:
                    return float('inf')
                if i == n:
                    return 0
    
                cur_letter = s[i]
                # delete
                delete = recur(i+1, last_letter, last_count, chance-1)
                # not delete - same letter
                if last_letter == cur_letter:
                    not_delete = recur(i+1, last_letter, last_count+1, chance)
                    if last_count in [1, 9, 99]:                    
                        not_delete += 1 
                # not delete - diff letter
                else:
                    not_delete = 1 + recur(i+1, cur_letter, 1, chance)
                
                return min(delete, not_delete)
                
            return recur(0, "", 0, k)
    ```
    
- Editorial
    - **Approach 1: Dynamic Programming**
        - Intuition
            - subproblem: 현재 string이 뭔지, 몇 번의 삭제가 더 허락되는지
                
                ![Untitled](Untitled%2088.png)
                
            - DP state 정의
                - parameter가 무려 4개 ㄷㄷ → top-down으로 푸는 게 정신건강에 이로움
                - state cell 값: 그 state에서 얻을 수 있는 compressed string의 최소 길이
                1. 이미 traverse한 symbol의 개수 
                    
                    → 다음으로 처리할 symbol이 뭔지 알기 위해
                    
                2. 우리가 만들고 있는 compressed string에 추가된 마지막 문자 
                    
                    → 새로운 symbol이 추가되면 compression이 어떻게 변할지 판단하기 위해 
                    
                3. 마지막 문자의 count 
                    
                    → 마지막으로 추가된 문자의 count가 0, 1, 9, 99이면 length of compression 변화 
                    
                    - 예시
                        - a3b5인 상태에서 b를 하나 더 추가하면 a3b6 (변화없음)
                        - a3b9인 상태에서 b를 하나 더 추가하면 a3b10 (자리수가 늘어남)
                4. 문자 삭제 기회가 몇 번 남았는지 
            - recurrence relation
                - 그림
                    
                    ![Untitled](Untitled%2089.png)
                    
                1. 새로운 symbol을 삭제하는 경우 (위, 아래 그림의 오른쪽 가지들
                    - i(전체 string에서 어디까지 봤는지)를 1 증가시키고
                    - k(몇 번의 삭제 기회가 더 남았는지)를 1 감소 시킨다
                2. 새로운 symbol을 붙이는 경우 
                    1. 지금까지 만들어온 string의 마지막 문자와 같은 경우 (위 그림의 왼쪽 가지)
                        - 마지막 문자의 count가 1, 9, 99인 경우 encoded length 1 증가
                        - 그렇지 않은 경우 변화 없음
                    2. 다른 경우 (아래 그림의 왼쪽 가지)
                        - 새로운 문자가 하나 추가되기 때문에 length 1 증가
                    - i는 1 증가시키고 k는 변화 없다