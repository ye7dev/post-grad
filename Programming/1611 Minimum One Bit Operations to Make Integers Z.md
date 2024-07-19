# 1611. Minimum One Bit Operations to Make Integers Zero

Status: done, in progress, with help, 🏋️‍♀️
Theme: DP, 🧱
Created time: January 31, 2024 4:52 PM
Last edited time: February 1, 2024 11:52 AM

- Progress
    - 문제 이해
        - 아래의 연산을 최소 몇 번 써야 n → 0으로 바꿀 수 있겠는가?
        - 연산 1
            - n의 binary 표현에서 제일 오른쪽 자리 (0th bit)를 바꿀 수 있다
            - n ^ 1
                - 5^1 = 4, 4 ^1 = 5
            - 1 → 0, 0→1
            - 01 → 00 처럼 맨 앞자리가 0이어도 가능
        - 연산2
            - (i-1)th bit가 1로 되어 있고,  (i-2)th부터 0th bit까지 0으로 되어 있는 경우, i번째 bit를 바꿀 수 있다
                - 11000 → 01000
            - **"(*i*−2)th through 0th bits"**: This refers to a sequence of bits in a binary number or array, starting from the bit at position *i*−2 and continuing down to the bit at position 0. Position 0 is the rightmost bit, also known as the least significant bit (LSB).
            - 1 << 3
                - 1000 → 8
            - 1 << i-1
                - 10…0(총 i자리 이진수) → 2**(i-1)
            - 0번째 bit가 1인 경우에도 1번째 bit를 0으로 바꿀 수 있다
                - `11" -> "01" with the 2nd operation since the 0th bit is 1`
        - 0 ≤ n ≤ 10 ** 9
- Hint
    1. 가장 쉬운 방법은 왼쪽에서부터 1인 bit를 없애나가는 것 
    2. 2^k인 경우부터 먼저 해봐라 ?
        - 2^k
            
            2^0 = 1 → 1
            
            2^1 = 2 = 10 → 11 → dp(1)
            
            2^2 = 4 = 100 → 101 → 111 → 110 → dp(2)
            
            2^3 = 8 = 1000 → 1001 → 1011 → 1010 → 1110 → ???
            
- AC 코드
    - 이런 거 나오면 진짜 눈치 챙기라는 소리 밖에는…
    
    ```python
    class Solution:
        def minimumOneBitOperations(self, n: int) -> int:
            if n == 0:
                return 0
            k = 0
            curr = 2 ** k
    
            while curr * 2 <= n:
                # stop condition: 2 ** (k+1) > n -> don't increase k 
                k += 1
                curr *= 2 
            
            # curr: n보다 크지 않은 2의 거듭 제곱 수 중에 가장 큰 수(MSB)
            def f(k):
                return 2 ** (k+1) -1
    
            return f(k) - self.minimumOneBitOperations(n ^ curr)
    ```
    
- Editorial
    - **Approach 1: Math and Recursion**
        - Intuition
            - set bit (값이 1인 bit)를 0으로 만들어야 함
            - 가장 오른쪽 bit를 제외하고는 모두 두번째 연산을 통해서만 0이 될 수 있음 → 두번째 연산을 수행할 수 있는 적절한 모양으로 숫자를 바꿔야 함
                - 예) n = 19 : 10011 → 11000으로 먼저 변환을 해야 두번째 연산 수행 가능
            - 가장 간단한 2의 거듭제곱부터 처리
                - 이런 숫자들은 맨 왼쪽 bit 하나만 1이고 나머지는 모두 0임
                - 예) k=4 → 2^4 = 16 → 10000
                - 2의 거듭제곱인 n을 0으로 만들기 위해서는 3가지 단계를 거쳐야
                    1. k-1 bit(0-indexed)를 1로 만들어야 함 
                        - k-1 = 3 → 11000으로 만들어야
                    2. 두번째 operation을 사용해서 가장 왼쪽 bit를 0으로 만듦 
                        - 01000
                    3. 남은 숫자들을 같은 방식으로 처리
                        - k-1 = 3번째 bit를 0으로 만들기
                - 그림
                    
                    ![Untitled](Untitled%20100.png)
                    
            - 두 개의 연산은 모두 reversible (critical observation)
                - 둘 다 오직 하나의 bit만 뒤집음
                - 어쨌든 결론은 x → y 가는 데 걸리는 최소 연산 수나, y → x 가는 데 걸리는 최소 연산 수가 같다는 것
            - `f(k)` : 2^k → 0으로 가는데 걸리는 최소 연산 수
                - 위의 세 단계에서 걸리는 연산의 합이 될 것
                - step1
                    - 처음 시작할 때는 제일 앞쪽의 1 말고 나머지 k개의 bit는 모두 0인 상태
                    - step1을 수행하고 나면, 제일 앞쪽의 1 말고, 나머지 k개의 bit는 다시 맨 앞이 1이 된 상태고, 나머지 k-1개의 bit는 0이 된 상태
                    - step1은 0을 2^k-1로 만드는 것과 동일 - critical observation에 의해, 2^k-1 → 0으로 만드는 것과 동일
                        
                        ![Untitled](Untitled%20101.png)
                        
                    
                    ⇒ step1 cost:  `f(k-1)`
                    
                - step2
                    - 연산 2 수행해서 맨 앞 bit를 0으로 변경
                    
                    ⇒ step2 cost: 1 
                    
                - step3
                    - repeat the process
                    - 남은 숫자는 2^(k-1)
                    
                    ![Untitled](Untitled%20102.png)
                    
                    ⇒ step3 cost: f(k-1)
                    
                
                ⇒ 다 합치면 1 + 2 * f(k-1)
                
                - 코드
                    - base case 1을 2^1-1로 표기하면, f(1) = 1 + 2 * f(0) = 1 + 2 * (2 - 1) = 1 + 2^2 -2 = 2^2 -1
                    - 아래 코드를 그대로 돌리면 O(k)가 나올 텐데 그냥 수식 정리해서 2^(k+1) -1 으로 사용하면 상수 시간이면서 memoization 같은 추가적인 overhead도 필요하지 않다
                    
                    ```python
                    def f(k):
                    	if k == 0:
                    			return 1 # 2^0 = 1
                    	else:
                    			return 1 + 2 * f(k-1)
                    ```
                    
            - n이 2의 거듭제곱이 아닌 경우
                - 문제를 두 부분으로 분할
                    - 그림
                        
                        ![Untitled](Untitled%20103.png)
                        
                    1. n에서 the most significant bit 위치 확인
                        - 예를 들어 position k인 경우, 따로 떼서 보면 2^k의 값을 갖고 있는 것 → binary 표현으로 하면 10…0(전체 자리 수는 k+1, 0의 개수는 k)
                        - 얘는 2의 거듭제곱 수이기 때문에 수식에 의해 2^(k+1)-1의 연산을 통해 0으로 만들 수 있다는 것을 알고 있음
                    2. 남은 오른쪽 부분 (`n'`)
                        - 우리는 이 값을 n (⊕: XOR 연산) 2^k를 통해 얻을 수 있음
                            - The XOR operation returns 1 if the bits are different, and 0 if the bits are the same.
                            - n이나 2^k나 k+1 자리의 이진수이고, 제일 왼쪽(MSB) = 1 → 같기 때문에 무조건 0
                            - 나머지 k 자리에 대해
                                - 2^k는 늘 0
                                - n이 0인 부분은 해당 자리에서의 bit 값이 같으니까 0이 나오고, n이 1인 부분은 해당 자리에서의 bit 값이 다르니까 1이 나올 것임
                            - 그래서 결국 나머지 k자리 부분은 n 그대로 나올 것
                        - n’ → 0으로 가려면 몇 번의 연산이 필요할까?
                            - n’에 대해 recursive 함수 수행하면 됨
                                - n’에서 MSB 분리하고, 연산 수에 2^(k+1)-1 더하고, 또 남는 부분에서 MSB 분리하고, 연산 수 더하고…
                - 재귀함수
                    - base case: n’ = 0일 때. 2^0이 아니라 남는 부분의 수가 정말로 0이라는 뜻(n’은 2의 거듭제곱 수가 아님) → 이미 0이라 아무 연산도 필요하지 않음. return 0
                    - A(x)가 x → 0으로 가는 최소 연산 수라고 할 때, n’→0까지 드는 연산 수는 A(n’)
                    - 그럼 정답은 1의 f(k) (=2^(k+1)-1) + A(n’)?
            - f(k) + A(n’)이 아니라 f(k) - A(n’)인 이유
                - reminder
                    - k is the position of the most significant bit in n
                    - f(k) is the number of operations required to reduce 2^k → 0 (2의 거듭제곱 수)
                    - n’  is the value of n with the most significant bit removed
                    - A(x) the number of operations required to reduce an arbitrary x → 0 (x는 2의 거듭제곱 수가 아님)
                - 예) n = 10 : 1010 vs. n = 8: 1000
                    - 1010 → 1100 변환하는 건 0010 → 0100 변환하는 비용과 동일
                    - 1000 → 1100 변환하는 건 0000 → 0100 변환하는 비용과 동일
                    - 0000 → 0100 가는 것보다 0010 → 0100 가는 비용이 더 적게 듦(0010이 0000보다 0100에 가깝기 때문에)
                        
                        ⇒ 1010 → 1100 변환 비용이 1000 → 1100 변환 비용 보다 적게 듦 
                        
                    - 그리고 1000 → 1100 변환 과정에서 1010 → 1100이 등장함
                        - 1000 → 1001 → 1011 → 1010 → 1100 → … → 0
                        - 위의 전체 과정은 f(k) (0 → 2^k 가는 비용)
                        - 검은색 부분은 A(n’)
                            - 2의 거듭제곱인 수에서 원래 구하려고 했던 n으로 가는 비용
                            - the critical observation에 의해 이건  n → 2^k와 비용이 같음
                            - n과 2^k는 k+1번째 bit는 동일하고, 나머지 부분 n’가 다름. 따라서 n → 2^k 비용은 0 → n’과 동일
                                - 예) 1000 vs 1010 → 0000 vs. 0010 (n’)
                            - 0→ n’ 비용은 A(n’)
                        - 빨간색 부분은 ans (n - 16- → 0 reduce 하는 비용)
                        
                        ⇒ 따라서 f(k) = A(n’) + ans
                        
        - 알고리즘
            1. n == 0 → 0을 return
            2. k = 0, curr = 1 로 초기화. curr은 2^k
            3. 2^(k+1) ≤ n 이면 2의 거듭제곱 승수를 늘린다 - k를 늘린다 
                - n의 MSB에 도달하기 위해
            4. return 2^(k+1) - 1 - minimumOneBitOperation(n⊕curr)
                - minimumOneBitOperation(n⊕curr)
                    - A(n’)에 해당하는 부분. n → 2^k와 동일 (n’ → 0)