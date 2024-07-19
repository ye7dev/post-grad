# 1987. Number of Unique Good Subsequences

Status: in progress
Theme: DP
Created time: February 5, 2024 1:52 PM
Last edited time: February 7, 2024 2:19 PM

- Progress
    - no editorial → 너무 오랜시간 쏟지 말것
    - 문제 이해
        - binary string binary
        - good subseq of binary : not empty and no leading zeros
            - leading zeros: 첫 1보다 앞에 오는 0
                - 예) Consider the binary string **`001101`**. Here, the first two zeros (**`00`**) are the leading zeros.
            - no leading zeros → “0” 빼고는 모두 1로 시작해야 한다
        - binary에서 unique good subsequence의 개수를 찾아라
    - 과정
        - 우선 자기 자신은 무조건 하나의 good subsequence
        - 자기 자신이 0이면 더 안 붙이고 1이면 뭘 더 붙여서 발전 가능
        - set은 어떻게 구하지? 어디 다 저장해놔야 하나?
        - binary 최대 길이는 10^5
        - 어쨌든 outer loop는 end, end보다 작은 그 앞의 원소 대상으로 inner loop는 start
        - bin(integer) 하면 string이 나온다
            - 이걸 다시 integer로 바꾸려면 int(binary num, 2)로 밑을 2로 지정해줘야 한다
        - 각 이진수에 대한 cell value가 0
        - 0의 개수 1의 개수 해야 하나
            - 그렇지만 101에서 110이 나올 순 없다
    - Hint
        - unique good subsequences 개수는 모든 가능한 subsequences 개수 중 unique decimal 값의 개수와 같다
- Trial
    - bottom-up → 예제는 다통과함(소 뒷걸음질…)
        
        ```python
        class Solution:
            def numberOfUniqueGoodSubsequences(self, binary: str) -> int:
                n = len(binary)
        
                '''
                dp = [0] * (n+1)
                dp[0] = 1 
                last_seen = {0:-1, 1: -1}
                for i in range(n):
                    dp[i+1] = 2 * dp[i]
                    char = int(binary[i])
                    if last_seen[char] != -1:
                        dp[i+1] -= dp[last_seen[char]]
                    last_seen[char] = i
                print(dp)
                '''
                dp = {i:[""] for i in range(n+1)}
                seen_int = set()
                for i in range(n):
                    char = binary[i]
                    dp[i+1] = dp[i]
                    for subseq in dp[i]:
                        if subseq != "" and subseq[0] == "0":
                            continue 
                        new_seq = subseq+char 
                        if int(new_seq, 2) not in seen_int:
                            seen_int.add(int(new_seq, 2))
                    dp[i+1].append(new_seq)      
                return len(seen_int)
        ```
        
- Solutions
    - leading zero가 없는 경우부터 count
        - 마지막 원소가 0인 subsequence의 개수를 ends_zero,
            - 0으로 시작하는 게 subsequence 개수가 아니다
        - 마지막 원소가 1인 subsequence의 개수를 ends_one 라고 하면
            
            → 둘 다 0에서 시작한다 
            
        - 새로운 원소 0을 만났을 때
            - ends_zero 뒤에 붙여도 되고, ends_one에 붙여도 된다
            - 그리고 새로운 원소를 붙인 모든 new subsequence들은 마지막 원소가 0이 된다
                
                → ends_zero = (ends_zero + ends_one)
                
        - 새로운 원소 1을 만났을 때
            - ends_zero 뒤에 붙여도 되고, ends_one 뒤에 붙여도 된다
            - 그리고 새로운 원소를 붙인 모든 new subsequence들은 마지막 원소가 1이 된다
                
                → ends_one = (ends_zero + ends_one)
                
            - 이 때, 위에서 count 한 new subsequence들은 모두 길이가 2 이상
                
                → 1 혼자 하나의 subsequence로 존재하는 경우도 세어줘야 
                
                → ends_one = (ends_zero + ends_one) + 1 
                
            - 1 혼자서도 ends_one에 count 될 수 있는 이유는, 이 뒤에 뭐가 오든 길이 2 이상의 new subseq를 만들 수 있기 때문
                - 10, 11
                - 그러나 0의 경우 ends_zero에 count 될 수 없다. 왜냐면 01, 00은 모두 invalid subseq라서
        - has_zero
            - 주어진 s를 통틀어 0이 한번이라도 나왔으면 1, 아니면 0
            - 재귀식 다 돌고 최종 return 전에 하나 더해준다
        - 예)
            - 001
                - ends_zero, ends_one은 모두 0에서 시작
                - 첫번째 숫자는 0
                    
                    → ends_zero = (ends_zero + ends_one)
                    
                    → 0 = 0 + 0 
                    
                    ⇒ 재귀식 count에는 들어가지 않고, has_zero만 1이 된 상태에서 다음 index로 넘어간다 
                    
                - 두번째 숫자도 0
                    
                    → ends_zero = (ends_zero + ends_one) = 0 + 0 = 0 
                    
                    ⇒ 여기서도 재귀식 count로는 변화없음 
                    
                - 세번째 숫자는 1
                    
                    → ends_one = (ends_one + ends_zero) = 0 + 0 = 0
                    
                    → 여기다가 1 혼자 존재하는 subsequence count 하면 1 
                    
                - 모든 숫자 다 돌고 마지막 값 return 하기 전에 has_zero 확인
                    
                    → 1이다 
                    
                    ⇒ 최종 답은 ends_zero (=0) + ends_one(=1) + 1 = 2 
                    
- AC 코드
    
    ```python
    class Solution:
        def numberOfUniqueGoodSubsequences(self, binary: str) -> int:
            mod = 10 ** 9 + 7
            n = len(binary)
            dp = [[0, 0] for _ in range(n+1)]
            # dp[i]: considering binary[:i]
            # dp[i][0]: # of uniq, good, subseq ending with 0 
            # dp[i][1] : # of uniq, good, subseq ending with 1 
    
            # base case: dp[0] -> [0, 0] (auto covered)
            has_zero = False
            for i in range(n):
                if binary[i] == '0':
                    has_zero = True 
                    # append zero to both subsequences
                    dp[i+1][0] = (dp[i][0] + dp[i][1]) % mod
                    dp[i+1][1] = dp[i][1] 
                else:
                    # count solo one (valid seed for next subseq)
                    dp[i+1][1] = (dp[i][0] + dp[i][1] + 1) % mod  
                    dp[i+1][0] = dp[i][0]
            return (sum(dp[i+1]) + has_zero) % mod
    ```