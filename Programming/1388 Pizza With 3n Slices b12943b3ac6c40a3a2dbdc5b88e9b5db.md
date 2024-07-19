# 1388. Pizza With 3n Slices

Created time: May 19, 2024 6:23 PM
Last edited time: May 19, 2024 9:40 PM

- 문제 이해
    
    피자를 3의 배수 사이즈로 자름 
    
    앨리스는 내 조각의 바로 왼쪽(360도까지 고려해서) 조각을 고를 것 
    
    밥은 내 조각의 바로 오른쪽 조각을 고를 것(360도 고려)
    
    피자 남은 조각이 없을 때까지 반복 
    
    시계 방향으로 피자 조각 사이즈가 주어질 때, 내가 고를 수 있는 최대 피자 조각 sum을 찾아라 
    
    피자 조각 수는 500미만의 3의 배수
    
- scratch
    
    house robber with 360도 문제 같군 
    
    [x, 8, 6, 1, x, x] 일 때 내가 8을 고르면 자동으로 1을 어떻게 제할 수 있지 
    
    - 8의 index는 1
    - 1의 index는 3
        - 거꾸로 따지면 -3
    
    조각 3개씩 슬라이딩 윈도우로 합치면 어떻게 되지 
    
    [1, 2, 3, 4, 5, 6]
    
    [1-2-6, 2-1-3, 3-2-4, 5-4-6, 6-5-1]
    
    = [-7, -4, -3, -5, 0] → 6 을 고른다
    
    [0, 2, 3, 4, 0, 0]
    
    [2-3-4, 3-2-4, 4-3-2]
    
    = [-5, -3, -1] → 4를 고른다 
    
    2의 인덱스는 1, 4의 인덱스는 3 
    
    3 + 4 = 7 → 7%6 = 1 
    
    dp[i][j] : i번째로 slice를 택할 때, j번째 조각을 가져가면서 얻을 수 있는 이익 
    
    뭔가 다음으로 선택할 수 있는 인덱스는 
    
- Editorial
    - circular array(m=3n)에서 n개의 non-adjacent element를 고르는 것
        - 0이랑 m-1도 동시에 고를 수 없다
    - 총 2개의 경우가 있음
        - m-1번째 element를 고르지 않는다 → linear array(0~m-2)에서 n개의 non-adjacent element를 고른다
        - 0번째 element를 고르지 않는다 → linear array(1~m-1)에서 n개의 non-adjacent element를 고른다
- Trial
    - 점화식 미흡
        
        ```python
        class Solution:
            def maxSizeSlices(self, slices: List[int]) -> int:
                m = len(slices)
                n = m // 3
                def get_max_sum(arr):
                    # dp[i]: j번째 집까지 고려했을 때, 선택한 집이 i개일 때 얻을 수 있는 max 이익     
                    arr_len = len(arr)
                    dp = [[0] * (arr_len+1) for _ in range(n+1)]
                    # base case
                    for j in range(1, arr_len+1):
                        dp[1][j] = max(dp[1][j-1], arr[j-1])
                    # recursive case
                    for i in range(2, n+1):
                        for j in range(1, arr_len+1):
                            dp[i][j] = max(dp[i-1][j-1], dp[i-2][j-1] + arr[j-1])
                    return dp[-1][-1]
                skip_first = get_max_sum(slices[1:])
                skip_last = get_max_sum(slices[:-1])
                return max(skip_first, skip_last)
        
        ```
        
- AC 코드
    
    ```python
    class Solution:
        def maxSizeSlices(self, slices: List[int]) -> int:
            m = len(slices)
            n = m // 3
            def get_max_sum(arr):
                arr_len = len(arr)
                if n == 0 or arr_len == 0:
                    return 0
                dp = [[0] * (arr_len + 1) for _ in range(n + 1)]
    
                # base case: 선택한 집이 1개일 때
                for j in range(1, arr_len + 1):
                    dp[1][j] = max(dp[1][j - 1], arr[j - 1])
    
                # recursive case: 선택한 집이 2개 이상일 때
                # 집을 두 개 이상 선택하려면, 고려하는 집도 최소 2개 이상이어야 함 
                for i in range(2, n + 1):
                    for j in range(2, arr_len + 1):
                        dp[i][j] = max(dp[i][j - 1], dp[i - 1][j - 2] + arr[j - 1])
                return dp[n][arr_len]
            skip_first = get_max_sum(slices[1:])
            skip_last = get_max_sum(slices[:-1])
            return max(skip_first, skip_last)
    
    ```