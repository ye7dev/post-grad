# Kadane’s algorithm

Status: algorithm
Theme: DP
Created time: November 17, 2023 2:21 PM
Last edited time: November 17, 2023 3:13 PM

- maximum sum subarray을 찾기 위한 DP적 접근법
    
    c.f. subarray vs. subsequence
    
    `subarray` : by deleting some or no elements without changing the order of the remaining elements
    
    `subsequence` : a contiguous sequence of elements within an array
    
- 변수 2개 운용-max_ending_here, max_so_far
    - max_ending_here: 이번 원소까지 고려했을 때 나올 수 있는 최대합
        - 이전 상태 + 현재 원소 vs. 현재 원소
        - 이전 합에 현재 원소를 더하냐 vs. 현재 원소만 데리고 가냐(현재 원소에서 다시 시작하냐)
    - max_so_far: array 전체를 돌면서 나올 수 있는 최대 합. 각 위치에서의 max_ending_here 비교 하고 최대값 저장
        - 반드시 negative infinity에서 시작해야 한다 → 아니면 오답 나옴