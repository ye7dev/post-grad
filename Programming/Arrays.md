# Arrays

- contiguous block of memory
- A[i] 값을 가져오는 것(retrieving)과 갱신하는 것의 TC는 O(1)
- full array에 삽입 시에 resizing 발생
    - 추가적인 memory를 차지하는 새로운 array를 할당한 다음, 원래 array에 있던 요소를 붙여넣기
    - 삽입의 worst-case time을 더 증가시킴
        - 그러나 새로운 array가 원래 array보다 상수 factor만큼 크다면, 삽입에 소요되는 평균 시간은 상수로 유지될 것- resizing이 잦지 않기 때문에
- 원소 삭제 시, 빈 자리를 메꾸기 위해 , 삭제한 자리 오른쪽에 있는 모든 원소를 왼쪽으로 한칸씩 옮겨야 함
    
    → TC는 O(n-i). n: array size, i: 삭제한 자리 
    
    - 새로운 원소를 삽입할 때도 마찬가지
- Array boot camp
    - input: integer array → 짝수 값을 가진 원소가 먼저 나오도록 재정렬 하기
    - O(n)의 공간을 사용하면 쉽지만, 추가적인 공간 할당 없이 풀어야 하도록 요구되면?
    - array 문제 풀 때 누릴 수 있는 장점: array 양 끝에 있는 원소에 쉽게 접근 가능
    - 문제 해결을 위해 array를 세 개의 하위 array로 분할: 짝수, unclassified, 홀수
        - 시작할 때는 전체 array가 unclassified에 들어가 있고, 짝수/홀수 subarray는 빈 상태
    - unclassified를 돌면서 swap을 통해 Even/ Odd는 늘려가고, unclassified는 줄여가는 전략
        - unclassified의 원소를 boundaries of Even, Odd subarrays로 보냄
- TOP TIPS
    - array itself를 사용해서 공간복잡도를 O(1)로 줄이는 더 미묘한 solution이 있기 마련
    - 앞에서부터 array를 채워나가는 것은 느리기 때문에 가능하면 뒤에서부터 채운다
    - entry를 지우는 대신(그럼 그보다 오른쪽에 있는 원소를 모두 한칸씩 왼쪽으로 shifting 해야 하기 대문에), overwriting을 고려해라
    - integer encoded by an array의 경우, array 뒤에서부터 숫자를 처리하는 게 좋다. 또는 array를 뒤집어서 least-significant digit이 첫번째 entry가 오도록 한다
    - subarray에 대해 작동하는 코드를 익숙하게 써야 한다
    - off-by-1 에러를 만들기 쉽다 - 0-indexed라서 마지막 element 뒤의 원소까지 읽지 않도록 주의
    - array의 integrity(정렬된 상태, 같은 값들끼리 모아두는 것등)를 지키는 것은 return 단계에서만 걱정하면 됨
    - element의 분포를 미리 아는 경우 좋은 자료구조가 된다
        - 예) 길이 W의 boolean array는 하나의 subset of {0, 1, …, W-1}을 표현하기 좋은 방식
            - 해당 subset이 pool에서 i값을 포함하고 있는지 여부는 bool_arr[i]가 True, False인지만 보면 됨
    - 2D array를 다룰 때는 row와 col에 대해 parallel logic을 사용해라
    - specification을 simulate 하는게 더 펴한 경우가 있다
        - 예) n * n matrix에 대해 spiral 순서로 원소를 넣을 때 i번째 원소를 찾는 코드를 쓰는 대신, 시작부터 output을 계산한다 (??)
- Know your array libraries
    - copy
        - B = A vs. B = list(A)
        - copy.copy(A) vs. copy.deepcopy(A)
        - B = A[:] ← shallow copy
    - k만큼 왼쪽으로 shift 해서 rotate
        - 12345 → 34512
        - A[k:] + A[:k]
    - product of sets
        - A=[1, 3, 5] x B=[’a’, ‘b’] → [(x, y) for x in A for y in B] → [(1, ‘a’), (1, ‘b’), …, (5, ‘b’)]

### 5.1 The Dutch national Flag problem

- quicksort 알고리즘
    - pivot 골라서 그보다 작은 값을 가진 원소는 모두 앞으로 보내고, 그보다 큰 값을 가진 원소는 모두 뒤로 보냄
    - pivot 기준으로 나뉜 두 subarray는 다시 재귀적으로 정렬
- duch flag partitioning
    - pivot보다 작은 원소가 먼저 나오고, 그 다음에 pivot과 같은 원소들, 그 다음엔 pivot보다 큰 원소들이 나오게끔
- input: array A, index i → A[i]보다 작은 원소들, 그 다음에 A[i]와 같은 원소들, 그 다음에 A[i]보다 큰 원소들이 나오게 재정렬하는 함수
    - O(n)의 추가 공간을 사용할 수 있다면 어려운 문제가 아님
        - 세 개의 list를 별도로 만들어서 원소 돌면서 나눠서 넣으면 된다. → TC : O(n)
    - TC를 늘리면서 SC를 줄이는 방법
        - 각 iteration에서 자기보다 뒤에 있으면서 pivot보다 작은 원소를 찾자마자, exchange(swap) → 뒤에 있던 원소를 자기랑 바꾸면서 앞으로 보냄 = pivot보다 작은 원소들이 모여 있는 subarray로 원소를 옮김 (앞쪽으로)
        - 두번째 단계에서는 각 iteration에서 자기보다 앞에 있으면서 pivot보다 큰 원소를 찾자마자 swap → 앞에 있던 원소를 자기랑 바꾸면서 뒤로 보냄 = pivot보다 큰 원소들이 모여 있는 subarray (뒤쪽 부분)으로 원소를 옮김
    - 여기서 TC를 더 줄이는 방법
        - pivot보다 작은 원소를 앞쪽으로 보낸 뒤
            - 보내는 위치는 iteration current index보다 상대적으로 뒤에 있는 다른 위치가 아니라
            - 상수를 두고 0에서 시작해서 점점 뒤로 가도록 함 (앞에서부터 채워가기 때문에 다음으로 원소가 들어갈 수 있는 공간이 어디인가 생각)
        - 두번째 pass에서 더 큰 원소를 뒤쪽으로 보냄
            - 보내는 위치는 iteration current index보다 상대적으로 앞에 있는 다른 위치가 아니라
            - 상수를 두고 n-1에서 시작해서 점점 앞으로 가도록 함. 뒤에서부터 원소를 채우기 때문에 다음으로 원소를 보낼 수 있는 곳은 그보다 하나 앞인 곳
    - 더 복잡하고 실행시간 짧은 방법
        - TC는 input size와 실행시간 사이의 관계식 ≠ 절대적인 실행 시간
        - 한 번의 pass로 pivot보다 작거나, 같거나, 큰 원소를 모두 분류
        - 두번째 접근법 처럼 smaller, larger index를 변수 하나에 넣고 사용
        - 그러나 equal 변수도 사용

### 5.6 Buy and sell a stock once

- 주어진 day range에 걸쳐 하나의 주식을 사고 팔 때 얻을 수 있는 최대 이익을 구해라
- 주식 구매/판매는 어떤 날의 시작에서만 이루어질 수 있다.
- 판매는 구매 다음날에만 가능하다
- input: daily stock price → output: max profit
- Brute force
    - j > i 일 때, index 쌍 i, j 를 가지고 S[j]-S[i]가 so_far_max_difference인지 확인해나가는 식
    - outer loop i는 0 → n-1 (이 때 n-1은 다음 원소가 없기 때문에 inner loop 돌지 않아서 사실상 마지막 값은 n-2라고 봐야)
        - inner loop j는 i+1 → n-1
            - inclusive range라서 n-1-i-1+1 = n-1-i element를 돌게 됨
            - 하나의 j에 대해 S[j]-S[i]를 구하고, so_far_max인지 비교하고, so_far_max를 update 하는 과정은 모두 O(1) 소요
    
    ⇒ TC = sum_over(i: 0→ n-2) (n-1-i) = (n-1)*n/2 → O(n^2) 
    
    - additional memory 사용은 상수 → SC = O(1)이라고 봐야하는 듯?
- Divide-and-conquer
    - S를 두 개의 subarray로 나눔 S[0:n//2], s[n//2:n]
    - 각 subarray에 대한 best result 구한 뒤 두 개를 combine(max)
        - T(n/2) * 2
    - 근데, 최적의 판매 시점과 구매 시점이 서로 다른 subarray에 존재하는 경우
        - 구매는 무조건 앞쪽 subarray에서, 판매는 무조건 뒤쪽 array에서
        
        → max profit은 max(뒤쪽) - min(앞쪽) 
        
        - 각 subarray를 한번씩만 돌면 얻을 수 있음.→ O(n)
    - ⇒ recurrence relation T(n) = 2 * T(n/2) + O(n) ⇒ O(nlogn)
        1. **초기 단계**: 크기가 **`n`**인 문제를 해결하기 위해, 두 개의 크기가 **`n/2`**인 하위 문제로 나눕니다. 이 단계의 비용은 **`(n)`**입니다.
        2. **하위 단계**: 각 하위 문제는 다시 같은 방식으로 처리됩니다. 따라서, 각각의 하위 문제는 **`2 * T(n/4) + O(n/2)`**의 비용이 들고, 전체적으로는 **`2 * (2 * T(n/4) + O(n/2))`**가 됩니다. 이는 **`4 * T(n/4) + 2 * O(n/2)`**로 간소화할 수 있으며, 결과적으로 이 단계의 비용도 **`O(n)`**입니다.
        3. **재귀적 반복**: 이 과정을 계속 반복하면, **`n`**이 1이 될 때까지 각 단계에서 **`O(n)`**의 작업이 필요합니다. 트리의 각 레벨에서 작업의 총량은 **`O(n)`**이며, 트리의 깊이는 **`logn`**입니다(각 단계에서 문제의 크기가 반으로 줄기 때문에).
        4. **총합**: 따라서, 모든 단계에서의 총 작업량은 각 단계에서 **`O(n)`**이며, 단계의 수가 **`logn`**이므로 전체 작업량은 **`O(nlogn)`**이 됩니다.
        - 두 시간 복잡도 O(n))과 O(nlog⁡n)을 합칠 때, 전체 복잡도는 두 항 중 더 큰 영향을 미치는 항으로 결정됩니다. 여기서 O(n)은 선형 시간 복잡도를 나타내고, O(nlog⁡n)은 선형 로그 시간 복잡도를 나타냅니다.
            
            →  복잡도를 합친 O(n)+O(nlog⁡n)의 경우, nlog⁡n항이 n항보다 더 크게 증가합니다. 따라서, 전체 복잡도는 더 큰 영향을 미치는 O(nlog⁡n)으로 결정됩니다.
            
    - 구현 시에 몇 가지 코너 케이스 고려해야 - 빈 array 들어오는 경우, 원소가 하나인 array가 들어오는 경우, 가격이 Monotonically 감소하는 array의 경우(이를 체크하는 함수를 따로 짜야하려나?)
- DP
    - 어떤 날에 판매함으로서 얻을 수 있는 최대 이익은 그보다 앞선 날들 중 주식 가격이 가장 낮은 날의 가격에 의해 결정됨
    - input array를 돌면서
        - so_far_min_price를 keep tracking
        - current element-so_far_min_price > so_far_max_profit 이면 update the so_far_max

### 5.12 Samle Offline data

- input: array of distinct element, size → input array에서 size 크기의 subset을 구하라
    - 모든 subset들이 나올 확률은 동일해야 한다
    - input array에다가 결과를 return 하라(?)
- size k의 random subset이 주어졌을 때, k+1 사이즈의 random subset을 만드는 방식으로 진행해나가야 함
    - 추가되는 하나의 원소는 랜덤하게 선택되어야 함
    - k=1일 때 이 문제는 trivial
        - random number generator 호출 1번 → 거기서 나온 값에 mod n = r → A[0] ↔ A[r] swap
        - 정답은 A[0] (input array에 결과를 넣으라는 말이 이 말이었군
    - k> 1
        - k=1일 때의 과정을 거친 뒤, 같은 과정을 A[1:n]에 대해서 반복
            - r은 mod n-1 하고 A[1:n][0] ↔ A[r] 하면 되려나?
        - 최종적으로 A[:k]가 random subset
    - size k의 모든 subset이 만들어질 확률이 비슷하면, size k+1의 subset들도 모두 나올 확률이 같다

### 5.18 Compute the spiral ordering of a 2D array

- 2D array를 spiral order로 쓰는 법
- case analysis → divide-and-conquer
- uniform way of adding the boundary
    - 첫번째 row에 n-1개 넣는다 → last-column에도 n-1개 넣는다 → 마지막 row에도 역순으로 n-1개 넣는다 → 첫번째 column에도 역순으로 n-1개 넣는다
        - → ↓ ← ↑
    - 이렇게 하고나면 (n-2) * (n-2)의 2D array가 남는다
    - 계속하다보면 outer most elements of n * n → (n-2) * (n-2) → (n-4) * (n-4) …
    - n이 홀수인 경우 center가 1 x 1인 corner case 발생

### 5.15 Compute a random subset

- 5.12 처럼 풀면 array 만들고 → 거기서 subset 만들기
    - array 만들기: O(n) 공간/시간 복잡도
    - subset 만들기: O(k) 시간
- k가 n보다 훨씬 작으면, array의 대부분은 Untouched 상태 (A[i] = i)
    - 공간복잡도를 O(n) → O(k)로 줄일 방법이 있다
        - 알고리즘에 의해 값이 변한 entries만 사전에 담아서 저장 (A[i] ≠ i)
- hash table H 사용
    - i가 H에 안 들어 있으면, A[i] = i라는 암묵적 의미
    - i가 H에 들어 있으면 H[i]: array A에서 현재 i에 들어 있는 값. i에 mapping되어 있는 값. True A[i]
- H는 비어 있는 채로 시작 → k iterations of…
    1. current index i보다 크거나 같은 애들 중에 index 하나 고르기(r) i → n-1
        - n-1-i+1 = n-i 개 중 하나
    2. 경우의 수 확인 
        - A[i] = i인지 아닌지
            - 아니면 hash table에서 H[i]가 가져오고
        - A[r] = r인지 아닌지
            - 아니면 hash table에서 H[r] 가져오고
    3. hash table 통해 swap
        - hash_table[i], hash_table[r] = r에 mapping된 값, i에 mapping된 값