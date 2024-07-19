# 3814. [Professional] 평등주의

Created time: April 18, 2024 7:06 PM
Last edited time: April 18, 2024 9:19 PM

4 2 3 7 6

2 기준으로 보면 2 0 1 5 4 → K는 5라서 

- Trial
    - 예제만 통과
        
        ```python
        def is_possible(mid_val):
            chance = K
            i = 1
            prev, cur = nums[i-1], nums[i]
            while i < N:
                if abs(cur-prev) <= mid_val:
                    prev = cur
                    i += 1
                    if i == N:
                        return True
                    else:
                        cur = nums[i]
                        continue
                need_help = abs(cur-prev)-mid_val
                if need_help > chance:
                    return False
                chance -= need_help
                if cur > prev:
                    prev = cur - need_help
                else:
                    prev = cur
                i += 1
                if i == N:
                    return True
                else:
                    cur = nums[i]
            return True
        
        T = int(input())
        for t in range(1, T+1):
            N, K = map(int, input().split())
            nums = list(map(int, input().split()))
            low, high = 0, max(nums)-min(nums)
            while low < high:
                mid = (low + high) // 2
                if is_possible(mid):
                    high = mid
                else:
                    low = mid + 1
            print(f'#{t} {low}')
        ```
        
- validate 함수 수정해서 AC
    
    ```python
    def is_possible(mid):
        copy_arr = nums[:]
        opr_cnt = 0
    
        for i in range(N-1):
            gap = copy_arr[i + 1] - copy_arr[i]  # 1, 0 -> N-1, N-2
            if gap > mid:
                opr_cnt += (gap - mid)
                copy_arr[i + 1] -= (gap - mid)
                if opr_cnt > K:
                    return False
    
        for i in range(N-1, 0, -1):
            gap = copy_arr[i - 1] - copy_arr[i]  # N-2, N-1 -> 0, 1
            if gap >= mid:
                opr_cnt += (gap - mid)
                copy_arr[i - 1] -= (gap - mid)
                if opr_cnt > K:
                    return False
    
        return True
    
    T = int(input())
    for t in range(1, T+1):
        N, K = map(int, input().split())
        nums = list(map(int, input().split()))
        low, high = 0, max(nums)-min(nums)
        while low < high:
            mid = (low + high) // 2
            if is_possible(mid):
                high = mid
            else:
                low = mid + 1
        print(f'#{t} {low}')
    ```
    
    - Lessons
        - 최댓값을 최소로~ 이런 문제는 parametric search의 trigger다
        - validate 함수 짜기 연습 더 해야…
        - 이 문제에서는
            1. 원래 array를 얕은 복사한다 (리스트 오브 리스트거나 하면 딥카피)
                - 얕은 복사해도 복사본에 반영된 수정이 원래 객체에 반영되지는 않는다
            2. 오른쪽 수 - 왼쪽 수, 진행 방향은 오른쪽으로 한번 쭉 순회하면서
                - 뒤의 수와 앞의 수 차이를 구하고 (diff)
                - 이 차이가 mid보다 크면 연산 적용해야 하는 정도 (diff와 mid 차이)를 계산
                - 복사된 array에서 뒤에 수에 diff와 mid 차이 만큼 빼준다
                - 이 때 diff와 mid 차이가 K보다 크면 return False
            3. 왼쪽 수 - 오른쪽 수, 진행 방향은 왼쪽으로 또 한번 쭉 순회하면서
                - 2에서 업데이트된 숫자와 그 앞 수 간의 차이가 어떤지 확인
                - 2와 같으 방식으로 체크
            4. 다 돌고도 중간에 False return 안했으면 return True