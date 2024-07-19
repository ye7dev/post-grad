# 42. Trapping Rain Water

Status: done, in progress
Theme: DP
Created time: January 17, 2024 2:46 PM
Last edited time: January 17, 2024 3:50 PM

- Process
    - 왼쪽, 오른쪽 값을 구한 다음 거기서 min을 구하고 거기서 self를 빼면 됨
    - 왼쪽 값
        - base case i = 0. 무조건 자기 높이
        - index 증가시켜가면서 자기를 포함, 지금까지 최대 높이만을 남겨둠
            - left_height = max(left_height, height[i])
    - 오른쪽 값
        - base case i = n-1. 무조건 자기 높이
        - index 감소해가면서 자기를 포함, 지금까지 최대 높이만을 남겨 둠
    - 각 index마다 min(left, right) - height[i] 구해서 양수면 누적 합에 더함
    - dp 적인 사고 방식은 모르겠고 우선은 brute force로 풀자
- AC 코드
    - by myself ~~Brute Force~~ 알고 보니 이게 dp네~! 🪇
        - right max는 뒤에서부터 구해가는 거라 순차 for loop에 넣기가 어려웠음
            - 인덱스가 n-i에서 시작해서, 0에서 시작하는 cur_water를 구할 수는 없었음
        
        ```python
        class Solution:
            def trap(self, height: List[int]) -> int:
                n = len(height)
                water_sum = 0
        
                left_max, right_max = [0] * n, [0] * n
                left_max[0] = height[0]
                right_max[-1] = height[-1]
                
                for i in range(n-2, -1, -1):
                    right_max[i] = max(right_max[i+1], height[i])
                for i in range(1, n):
                    left_max[i] = max(left_max[i-1], height[i])
                    cur_water = min(left_max[i], right_max[i]) - height[i]
                    water_sum += cur_water
                return water_sum
        ```
        
- Editorial