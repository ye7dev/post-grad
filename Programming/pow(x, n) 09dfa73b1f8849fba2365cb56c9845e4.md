# pow(x, n)

Status: done
Theme: math
Created time: November 1, 2023 3:11 PM
Last edited time: November 2, 2023 4:56 PM

- n이 양수일 때랑 음수일 때 나눠서(음수일 때는 range(-n), *= 1/x)로 했는데 시간 초과 오류
- 남의 풀이
    - n이 음수 양수 관계 없이 양수값만 남기려면 abs(n)
    - 이런 공식이 있다고 함
        
        ![Untitled](Untitled%2010.png)
        
    
    ```python
    class Solution:
        def myPow(self, x: float, n: int) -> float:
            def recur(base=x, pow=abs(n)):
                if pow == 0: return 1 
                elif (pow & 1) == 0: # even 
                    return recur(base*base, pow // 2)
                else: # odd -> even after -1 
                    return base * recur(base*base, (pow-1)//2)
            
            res = recur()
    
            return res if n >= 0 else 1/res
    ```
    
    - 예) x=2, n = 9
        - recur(2, 9)
            
            → return 2 * recur(2^2, (n-1)//2 = 4) 
            
            → n이 짝수. return recur(2^4, 2) 
            
            → n이 짝수. return recur(2^8, 1)
            
            → n이 홀수. return 2^8 * recur(2^16, 0) = return 2^8*1 = 2^8
            
            ⇒ 2 * 2^8 = 2^9