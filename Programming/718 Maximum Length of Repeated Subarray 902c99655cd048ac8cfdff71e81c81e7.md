# 718. Maximum Length of Repeated Subarray

Status: done, in progress
Theme: DP
Created time: January 15, 2024 4:44 PM
Last edited time: January 16, 2024 1:05 PM

- Progress
    
    subarray는 무조건 contiguous
    
    empty array는 무조건 일치하는가? 일치하지 근데 그것의 Length를 1이라고 할 수 있는가? 아니 
    
- Trial
    - 23/53
        - 이거는 subsequence에 대한 것 같다.
        - nums1[i-1] == nums2[j-1] 경우에 대한 처사가 달라져야 할 듯
            - 이번 원소만 같으면 그냥 1인데
            - 만약에 앞에서 뭔가 이어서 같았으면 거기에 더해서…
        
        ```python
        class Solution:
            def findLength(self, nums1: List[int], nums2: List[int]) -> int:
                m, n = len(nums1), len(nums2)
                # array
                ## state dp[i][j]: max len of a subarray considering nums1[:i], nums2[:j] 
                dp = [[0] * (n+1) for _ in range(m+1)]
        
                # base case - autocovered
                ## nums[:0] = empty string -> 0 overlap for any subarray
                max_len = 0
                for i in range(1, m+1):
                    for j in range(1, n+1):
                        if nums1[i-1] == nums2[j-1]:
                            dp[i][j] = 1 + dp[i-1][j-1]
                        else:
                            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                        max_len = max(dp[i][j], max_len)
                return max_len
        ```
        
- AC 코드
    - subarray는 무조건 연속으로 같아야 하기 때문에
    - 일단 한번이라도 같지 않아지면 0으로 설정
    - 대신 최대값은 max_len이라는 변수로 들고 다니면 됨
    - index 주의
        - string에서 indexing 할 때
        - dp table에 값을 넣어줄 때
        - 0-indexed인지 1-indexed인제 잘 체크
    - else 문은 어차피 초기화한 값이랑 같아서 없애도 됨-없애는 게 속도에 더 도움이 됨
    
    ```python
    class Solution:
        def findLength(self, nums1: List[int], nums2: List[int]) -> int:
            m, n = len(nums1), len(nums2)
            # array
            ## state dp[i][j]: max len of a subarray considering nums1[:i], nums2[:j] 
            dp = [[0] * (n+1) for _ in range(m+1)]
    
            # base case - autocovered
            ## nums[:0] = empty string -> 0 overlap for any subarray
            max_len = 0
            for i in range(1, m+1):
                for j in range(1, n+1):
                    if nums1[i-1] == nums2[j-1]:
                        dp[i][j] = 1 + dp[i-1][j-1]
                    else:
                        dp[i][j] = 0
                    max_len = max(dp[i][j], max_len)
            return max_len
    ```