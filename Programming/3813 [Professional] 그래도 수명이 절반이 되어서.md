# 3813. [Professional] 그래도 수명이 절반이 되어서는…

Created time: April 18, 2024 5:07 PM
Last edited time: April 18, 2024 7:04 PM

- 문제 이해
    - maximum subarray 문제 변형 같다
        - 다만 subarray가 여러 개이고, 최대 sum 대신 max값이 가장 작은 subarray를 유지해야 함
- Parametric search
    - 최적화 문제를 결정 문제(예/아니오로 답하는 문제)로 변환함으로써 문제를 해결하는 방법
    - **예시: 최소 스패닝 트리와 파라메트릭 검색**
        
        가중치가 있는 그래프가 주어졌을 때, 특정 가중치 k 이하의 간선만 사용하여 모든 노드를 연결할 수 있는지를 결정하는 문제를 고려해 봅시다.
        
        1. **문제 정의**: 주어진 가중치 k 이하의 간선만을 사용해서 모든 노드가 연결될 수 있는지 결정합니다.
        2. **이진 검색**: 가능한 가중치의 범위 [L,H]에서 중간값 *M*을 파라미터로 사용해 결정 문제를 풉니다.
        3. **결정 알고리즘**: 가중치 M 이하의 간선만을 사용하여 MST를 구성할 수 있는지 확인합니다. 이는 Kruskal의 알고리즘 또는 Prim의 알고리즘을 사용할 수 있습니다.
        4. **결과 해석**:
            - 만약 MST를 구성할 수 있다면, *k*의 최대 가능 범위를 *M* 이하로 좁히고, *H*=*M*으로 설정합니다.
            - 구성할 수 없다면, *L*=*M*+1로 설정하여 범위를 조정합니다.
        5. **종료 조건**: L과 H가 만나거나 교차할 때까지 반복합니다. 결과적으로 L은 최소의 최대 가중치가 됩니다.
    - 우리 문제에 적용해 보면
        1. 문제 정의: wafer age x 이하의 블록만 사용해서 모든 데이터 덩어리를 저장할 수 있는지 결정
        2. 이진 검색: 가능한 wafer age 범위 L, H에서 중간값 M을 파라미터로 사용해 결정문제 해결
        3. 결정 알고리즘: brute force? or kadane’s? 
        4. 결과 해석:
            - 모든 데이터 덩어리 저장할 수 있으면 x의 최대 가능 범위를 M 이하로 좁히고, H=M으로 설정
            - 저장 불가하면 L = M+1로 설정해서 범위 조정
        5. 종료 조건: L, H가 만나거나 교차할 때까지 반복 → 결과적으로 L은 최소의 최대 wafer age가 된다 
- Trial
    - 제한시간 초과 (32/50)
        
        ```python
        def get_min_age():
            low, high = min(w_ages), max(w_ages)
            while low < high:
                mid = (low + high) // 2
                i, j = 0, 0
                while i < N and j < K:
                    num_blocks = data_chunks[j]
                    if max(w_ages[i:i+num_blocks]) > mid:
                        i += 1
                    else:
                        #print(i, j)
                        i += num_blocks
                        if i > N:
                            break
                        j += 1
                if j == K:
                    high = mid
                else:
                    low = mid + 1
            return low
        
        T = int(input())
        for t in range(1, T+1):
            N, K = map(int, input().split())
            w_ages = list(map(int, input().split()))
            data_chunks = list(map(int, input().split()))
            ans = get_min_age()
            print(f'#{t} {ans}')
        ```
        
- AC 코드
    
    ```python
    def check_pass(mid_val):
        chunk_idx = 0
        data_count = 0
        for i in range(N):
            if w_ages[i] <= mid_val:
                data_count += 1
            else:
                data_count = 0
            # 데이터 덩어리 크기를 만족하는지 확인
            if data_count == data_chunks[chunk_idx]:
                chunk_idx += 1
                data_count = 0
                if chunk_idx >= K:
                    return True
        return False
    
    T = int(input())
    for t in range(1, T+1):
        N, K = map(int, input().split())
        w_ages = list(map(int, input().split()))
        data_chunks = list(map(int, input().split()))
        low, high = min(w_ages), max(w_ages)
        while low < high:
            mid = (low + high) // 2
            if check_pass(mid):
                high = mid
            else:
                low = mid + 1
        print(f'#{t} {low}')
    ```
    
    - lessons
        - input이 엄청 큰 경우, 최적화(최대/최소) 문제를 Parametric search로 변환하는 방안 고려
            - 이 문제의 경우 max block 길이가 (1≤N≤200,000)
            - parametric search 사고방식에 적용가능한지 확인
                - 최적화 문제 변환 가능성 (최소값 또는 최대값 찾기)
                - 이진 검색 적용 가능성 (파라미터 조정으로 답의 가능성 탐색)
                - 결정 문제로의 단순화 (특정 조건 만족 여부 확인)
                - 연속적 값 범위 보유 (파라미터가 연속적인 값을 가짐)
        - Parametric search 에서는 mid가 만족하면 High를 mid로, 불만족하면 low를 Mid+1로 하는게 관례인가봄? → 그리고 return은 low
        - 해당 미드 값에 대해 verify 하는 함수를 효율적으로 짜야 시간 초과 막을 ㅜㅅ 있음