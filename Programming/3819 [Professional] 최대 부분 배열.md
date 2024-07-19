# 3819. [Professional] 최대 부분 배열

Created time: April 21, 2024 10:21 AM
Last edited time: April 21, 2024 10:29 AM

- **subarray는 반드시 연속적이어야 하지만**, subsequence는 연속적일 필요가 없습니다.
    - 어떤 한 위치에서 선택할 수 있는 subarray는 두 개 → max_ending_here
        - 직전 subarray에 현재 원소 추가
        - 현재 원소 (부터 다시 시작)
    - 최종 return 값 → max_so_far
        - 모든 자리에서 max_ending_here 값 중 제일 큰 값
- AC 코드
    
    ```python
    def get_max_subsum(arr):
        max_ending_here = max_so_far = arr[0]
        for i in range(1, len(arr)):
            max_ending_here = max(arr[i], max_ending_here + arr[i])
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far
    
    T = int(input())
    for t in range(1, T+1):
        N = int(input())
        A = []
        for _ in range(N):
            A.append(int(input()))
        ans = get_max_subsum(A)
        print(f'#{t} {ans}')
    ```