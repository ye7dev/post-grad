# Factorial Trailing Zeroes

Status: done
Theme: math
Created time: November 1, 2023 3:11 PM
Last edited time: November 2, 2023 4:56 PM

- 나의 풀이
    - 가장 손쉬운 방법
        - n! 구해서 10으로 몇 번 나눌 수 있는지
        - ~~n!이 10의 4승 이하니까 for문 4번 돌면 될 것~~. n 자체가 10^4 이하. 근데 이 때 시간 복잡도는 O(N)
    - O(log N)으로 구할 수 있는 방법은 없을까?
        - 2와 5가 몇 개 있는지 알 수 있으면 될 텐데…근데 결국 1부터 N까지 모든 수를 다 돌아야 하지 않나? 어떻게…?
    - 1350 → 4자리 수. 가장 0이 많이 나오는 경우는 1000 = 10^3
        - 근데 이거 썼다가 limit 걸림
            
            ```python
            for i in range(len(str(fac))-1, 0, -1):
                if fac % 10**i == 0:
                    return i
            # ValueError: Exceeds the limit (4300) for integer string conversion; 
            # use sys.set_int_max_str_digits() to increase the limit
            ```
            
    - fac 계산 → base 10으로 하는 math log → 정수 만들기 위해 floor 썼는데 실패
    - 1000 나누기 10 = 몫: 100, num_zero = 1 → 나누기 10 = 몫: 10, num_zero =2 → 나누기 10 = 몫: 1, num_zero = 3
        - 근데 왜 n=30 일 때 output은 32가 나오고, 답은 7…
        - 1234 나누기 10 = 몫: 123, num_zero = 1, 나머지 4
        - 나머지 0인 경우 추가하고, 나눠지는 수를 몫으로 update 하는 코드 넣어서 해결. 그러나 효율 개선 필요
- O(log N) solution
    - 10은 2와 5로 만들어지고, 보통 2는 5보다 많기 때문에, 5가 몇 개 등장하냐가 핵심
    - 어차피 N을 5로 나누다 보면 1과 N 사이에 있는 5의 배수를 다 얻게 됨
    - N을 5로 나누고 몫을 count에 더하고, 다시 그 몫을 5로 나누고…
    
    ```python
    class Solution:
        def trailingZeroes(self, n: int) -> int:
            count = 0
            while n > 0:
                n //= 5
                count += n
            return count
    ```