# 956. Tallest Billboard

Created time: May 16, 2024 6:08 PM
Last edited time: May 17, 2024 2:43 PM

- scratch
    
    subset으로 만들 수 있는 값이 엄청 다양쓰 
    
    → 엄청 어려운 문제라고 함. 결국 솔루션 봄 
    
- Trial
    - 예제도 틀림
        
        ```python
        class Solution:
            def tallestBillboard(self, rods: List[int]) -> int:
                dp = [0] * (sum(rods) + 1)
                for r in rods:
                    dp[r] = 1 
                ans = 0
                for i in range(1, len(dp)):
                    for j in range(i):
                        if dp[j] and dp[i-j]:
                            dp[i] += 1
                            if dp[i] >= 2:
                                ans = max(ans, i)
                return ans
        ```
        
- AC 코드 (editorial)
    - 막대 하나 당 기존 dp item 체크
        - 왜냐면 새로운 막대를 기존 수치에 더해봐야 하기 때문
    - 같은 key 값(taller - shorter 차이)에 대해서는 taller 수치가 더 큰 value를 저장한다
        - 예) diff =0 이 우리가 원하는 답이지만, 같은 diff = 0에서도 taller가 가장 큰 경우가 우리가 찾는 max height
        - 이번 막대로 분기한 새 값이 꼭 크란 법이 없기 때문에, new_dp.get(key, 0) 값과 비교해서 더 큰 쪽으로 update 해준다
    - 하나의 막대와, 하나의 기존 상태에 대해 분기할 수 있는 상태는 총 3가지
        - 아무 것도 안하는 것(기존 dp dict 카피하면서 이 선택이 implicitly 취해짐)
        - 짧은 쪽에 막대를 더하는 것
            - 짧은 쪽에 막대를 더해도 여전히 taller가 더 높을 수 있기 때문에 abs 사용해서 diff 구한다
        - 긴 쪽에 막대를 더하는 것
    - 막대 하나에 대해 모든 기존 상태를 대입해봐야 하기 때문에, 막대 순회 for loop이 outer loop
        - 막대 하나를 새로 꺼낼 때마다 dp dict를 copy - 기존 상태를 그대로 가져오도록
        - 새로운 값들은 new_dp dict에 기입하고, 이것이 기존 dp와 다르게 관리되기 때문에, 이번에 업데이트하는 값이, 기존 상태로 들어갈 걱정이 없다
    
    ```python
    class Solution:
        def tallestBillboard(self, rods: List[int]) -> int:
            dp = {0: 0}
            for r in rods:
                new_dp = dp.copy()
                for diff, taller in dp.items():
                    shorter = taller - diff
                    new_dp[diff+r] = max(new_dp.get(diff+r, 0), taller + r)
                    new_diff = abs(diff-r)
                    new_taller = max(taller, shorter + r)
                    new_dp[new_diff] = max(new_dp.get(new_diff, 0), new_taller)
                    
                dp = new_dp
            return dp[0]
    ```