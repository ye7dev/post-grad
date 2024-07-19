# 338. Counting Bits

Status: in progress
Theme: DP
Created time: November 27, 2023 10:36 PM
Last edited time: November 27, 2023 10:46 PM

- 쿨다운 easy 문제
- base case - n=1 때만 주의해야 했음
- bit operation 써서 멋지게 성공 🪇
- 코드
    
    ```python
    class Solution:
        def countBits(self, n: int) -> List[int]:
            if n == 0: return [0]
            ans = [0] * (n+1)
            ans[1] = 1
            if n == 1: return ans 
    
            for i in range(2, n+1):
                ans[i] = ans[i//2]
                if i & 1:
                    ans[i] += 1 
            return ans
    ```