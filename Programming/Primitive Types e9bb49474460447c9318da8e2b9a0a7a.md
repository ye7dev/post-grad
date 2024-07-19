# Primitive Types

- Top tips
    1. bitwise operators, 특히 XOR에 익숙해질 것 
    2. mask 사용법이랑 machine independent way 하게 생성하는 법 [모르는 부분](%E1%84%86%E1%85%A9%E1%84%85%E1%85%B3%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%87%E1%85%AE%E1%84%87%E1%85%AE%E1%86%AB%204aba751fad2448da9e6ab7f6884564b1.md) 
    3. lowermost set bit 관련 아래의 방법을 알아둔다  [모르는 부분](%E1%84%86%E1%85%A9%E1%84%85%E1%85%B3%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%87%E1%85%AE%E1%84%87%E1%85%AE%E1%86%AB%204aba751fad2448da9e6ab7f6884564b1.md) 
        - clear하기, 0으로 만들기, index를 구하기
    4. signedness의 개념과 shifting에서 가지는 함의  [모르는 부분](%E1%84%86%E1%85%A9%E1%84%85%E1%85%B3%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%87%E1%85%AE%E1%84%87%E1%85%AE%E1%86%AB%204aba751fad2448da9e6ab7f6884564b1.md) 
    5. 연산을 가속하기 위해 brute-force small inputs에 대해 cache 사용하는 방법 고려  [모르는 부분](%E1%84%86%E1%85%A9%E1%84%85%E1%85%B3%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%87%E1%85%AE%E1%84%87%E1%85%AE%E1%86%AB%204aba751fad2448da9e6ab7f6884564b1.md) 
    6. parallel, reorder operations에서 commutativity, associativity가 사용됨을 알아둬라  [모르는 부분](%E1%84%86%E1%85%A9%E1%84%85%E1%85%B3%E1%84%82%E1%85%B3%E1%86%AB%20%E1%84%87%E1%85%AE%E1%84%87%E1%85%AE%E1%86%AB%204aba751fad2448da9e6ab7f6884564b1.md) 

### 4.1 Computing the parity of a word

- parity of a binary word
    - binary word: sequence of bits of a fixed length
    - parity: set bit 개수가 홀수인지 짝수인지 → 홀수개면 1, 짝수개면 0
    - parity check → 데이터 저장 및 커뮤니케이션 시에 single bit error를 감지하는데 사용
- bit 조작 연산에서 퍼포먼스 향상의 핵심
    - 한번에 여러 bit를 한꺼번에 처리
    - array-based lookup table에 결과를 caching
- Computing the parity of a collection of bits
    - bit들을 어떻게 그룹 짓냐가 중요하지 않음 - associative 계산
        
        → 64-bit integer의 bit를 4개씩 그룹 → 각 그룹은 non-overlapping 16 bit subword
        
    - 각 그룹의 parity 계산 → 4개의 subresult를 가지고 원래 parity 계산
    - 한 그룹의 parity 계산
        - 2-bit words에 대해 lookup table 생성
        - cache: <0, 1, 1, 0>
            - (00), (01), (10), (11) 의 parity를 각각 표현한 값
        - (11001010)의 parity를 계산한다고 하면, 두 개씩 끊어서 (11), (00), (10), (10)의 parity 계산
            - lookup table에서 살펴보면 0, 0, 1, 1 → (00)(11)의 parity는 00 → (00)의 parity는 0
        - 두 개씩 끊는 것-사실은…
            - (11101010)을 예로 들면 → right shift by 6 (오른쪽으로 여섯칸 밀어서) → 00000011 → cache에서의 index로 사용
            - (11) 다음 두 bit (10)을 얻으려면, right shift by 4 (오른쪽으로 네 칸 밀기) → 00001110 (아직 앞의 11도 남아 있는 상태) → bitwise (00001110) & (00000011) → (00000010)
- XOR of group of bits == 전체 bits의 parity
    - <b63, …, b0>의 parity == <b63, …, b32> ^ <b31, …, b0>의 parity
    - 예) 11010111의 parity
        - 반으로 쪼갠 group bit 1101, 0111 두 subbits에 XOR 연산 실행
        
        → 1010의 parity가 원래 input 11010111의 parity 
        
        - 1010은 다시 둘로 쪼갤 수 있음 10, 10 → XOR 연산하면 00 →
        
        → 00의 parity가 original input의 parity 
        
        - 00을 둘로 쪼개면 0, 0 → XOR 연산하면 0
        
        → 0의 parity 0이 전체의 parity 
        
    - 여기서도 반으로 쪼갠다고 하지만 사실은…
        - 11010111(x)과 00001101 두 개를 비교하는 것
            - 00001101: 원래 input을 오른쪽으로 4칸 민것
                - (x >> 4)
        - 둘을 XOR 하면
            - 각 자리 별로 1이 1개만 있는 데는 1이고 나머지는 모두 0
            - 1101 & 0000 → 1101 (자릿수 맞추기 위한 부분)
            - 0111 & 1101 (진짜 비교하는 파트)  → 1010
            - 전체 결과는 11011010
        - 그 다음 11011010과 00110110 비교
            - 00110110:  11011010를 오른쪽으로 두 칸 민 것( >> 2)
            - 진짜 비교는 마지막 두 자리에서 이루어지는 것이고
            - 나머지는 자리를 맞춰주기 위한 것
            - 전체 결과는 11101100
        - 그 다음 11101100과 01110110 비교
            - 01110110: 11101100 오른쪽으로 한 칸 민것 ( >> 1)
            - 마지막 자리만 비교하면 됨
            - 전체 결과는 10011010
        - 짝수인지 홀수인지 보려면 마지막 전체 결과에 1이랑 and operation 비교
- Variant
    - bitwise 연산, equality check, boolean operator 사용해서 아래의 작업을 O(1)로 수행하는 expression을 써라
        - right propagate the rightmost bit in x
            - 01010000 → 01011111
            - 가장 오른쪽의 set bit을 그보다 더 왼쪽의 0에도 모두 전파하라는 뜻
        - x mod a power of two
            - 77 mod 64 = 13
        - x가 2의 승수인지 테스트

### 4.2 Swap bits (light)

- 64 bit integer: array of 64bits. bit at index 0: Least Significant Bit, bit at index 64: Most significant bit
- indices i에 있는 bit와 indices j에 있는 bit를 swap 하는 문제
    - ***`if (x >> i) & 1 != (x >> j) & 1:`** i와 j 위치의 비트 값이 서로 다른지를 검사하는 것입니다. 여기서 **`& 1`** 연산은 해당 위치의 비트가 1인지 0인지를 추출합니다.
    - ***`if (x >> i) != (x >> j):`** 두 값의 전체 비교
- bit mask 사용해서 특정 자리의 bit값 flipping 하기
    - XOR 연산 사용 : 1^1 = 0, 0^1 =1
    - bit mask 만들기: 1을 i자리 만큼 shift . 두 bit 자리 각각의 mask를 만든 다음, OR 연산으로 합친다

### 4.3 Reverse bits

- 64-bit unsigned integer 받아서, 역순으로 뒤집은 64-bit unsigned integer를 return
    - unsigned integer
        - **Signed integer**는 음수, 0, 양수 값을 모두 표현할 수 있습니다. 이 데이터 타입에서 하나의 비트(보통 가장 왼쪽 비트)는 부호를 나타내며, 나머지 비트는 값의 크기를 표현합니다.
        - **Unsigned integer**는 0과 양의 정수 값만을 표현할 수 있습니다. 모든 비트가 숫자의 크기를 나타내기 때문에, 동일한 비트 수를 가진 signed integer보다 두 배 더 큰 최대값을 표현할 수 있습니다.
- 16-bit 씩 끊어서 4개 그룹으로 나눈 뒤, 각 그룹에서 reverse를 하고, 마지막으로 그룹 간 순서도 역순으로 배치함으로써 최종 reverse 결과를 얻는다
    - 이 때 lookup table A 사용 → A[y]: y 그룹의 bit-reversal을 담고 있음
- 예) 8 bit integer, 2 bit lookup table keys
    - table: rev = <(00), (10), (01), (11)>
    - input: 10010011 → 10/01/00/11
    - output: rev[11], rev[00], rev[01], rev[10]

### 4.4 Find a closest integer with the same weight (light)

- weight: non-negative integer x를 binary로 표현했을 때 set bit의 개수
    - 예) 92 = 1011100(2) → weight of 92: 4
- input: non-negative integer x
- output: x와 다르지만 같은 weight를 가지면서 x와의 절대값차가 최소인 숫자 y
- k1 > k2 일 때, 두 Indices에 위치한 bit를 flip 하는 경우
    - k1 위치의 bit가 가리키는 값 2^k1
    - k2 위치의 bit가 가리키는 값 2^k2
    - k1>k2 → 2^k1 > 2^k2
    - 둘 다 0일 때 1로 flip 하면 2^k1 + 2^k2가 원래 input 숫자와 절대값 차이일 텐데
        - 문제 요구사항은 변경된 수와 원래 숫자 사이의 차를 최대한 작게 해야 함
        - 따라서 이 경우는 제외됨
    - 저 두 bit를 flip 할 때 원래 숫자와 가질 수 있는 가장 작은 차이는 2^k1 - 2^k2
        - 한 bit는 0에서 1로, 다른 bit는 1에서 0으로 flip 하는 상황으로 가정했나봄 ?
    - 이 차이를 최소화하기 위해서는 k1은 최대한 작게, k2는 최대한 k1에 가까운 값이여야 함
- weight가 같은 숫자를 return 해야 하기 때문에, index k1에 위치한 bit와 k2에 위치한 bit 값이 서로 달라야 함 - 그래야 flip 했을 때 전체 set bit 개수가 그대로 유지됨
    
    → smallest k1은 LSB(least significant bit)가 아니면서 가장 오른쪽 위치, k2는 k1와 다른 bit 값을 가진 바로 다음 오른쪽 자리여야 
    
    ⇒ 서로 값이 다른 두 개의 연속된 bit를 swap 
    

### 4.7 Compute pow(x, y)

- double x와 integer y를 가지고 x^y 값을 계산, overfow, underflow는 무시
- 같은 결과를 더 적은 곱셈을 사용해서 얻는 것이 목표
    - 예) 1.1 ^ 21
        - 1.1을 21번 곱하는 대신
        - 1.1^2를 한번 구한 뒤, 그 값을 10번 곱하면 곱셈 수를 훨씬 줄일 수 있음
- non-negative y를 가정
    - 예) x^(1010(2)) = x^(101(2)) + 101(2)) = x^(101(2)) * x^(101(2))
        
        → x^(101(2)) = x^(100(2)) + 1(2)) = x^(100(2)) * x(1(2)) = x(100(2)) * x 
        
        → x^(100(2)) = x^(10(2) + 10(2)) = x^(10(2)) * x^(10(2))
        
    
    ⇒ y의 least significant bit가 0이면 (x^(y/2))^2, 1이면 x*(x^(y/2))^2
    
- y가 음수인 경우
    - 위에서 x를 1/x로, y를 -y로 바꾸면 됨

### 4.8 Reverse Digits

- input: integer → output: reversed integer
    - 예) 24 → 42, -314 → -413
- string으로 하는 대신, 10의 나머지 활용해서 수행
    - 예) -314 → 314로 바꿔둔다
        - result = 0
            - result * 10 = 0
            - 314 % 10 = 4
            
            → result = 4 
            
            - 314 = 314//10 = 31
        - result = 4
            - result * 10 = 40
            - 31 % 10 = 1
            
            → result = 41
            
            - 31 // 10 = 3
        - result = 41
            - result * 10 = 410
            - 3 % 10 = 3
            
            → result = 413
            
            - 3 // 10 = 0 → while loop ends
        
        ⇒ -314<0 → 413 * -1 = -413이 정답 
        

### 4.9 Check if a decimal integer is a palindrome

- input: integer → output: palindrome인지 아닌지
- 우선 음수라면 무조건 False. 앞에 부호가 붙으니까
- string으로 바꿔서 확인하는 방법은 O(n) - n은 자릿수
- 공간복잡도를 더 줄이는 방법
    - 자릿수 n은 floor(log_10_x)+1
    - least significant digit: x % 10
    - most significant digit: x // (10 **(n-1))
        - 예) 4500 → 1000으로 나눠야 4를 얻을 수 있음
            - 자릿수는 4 → 10**4 = 10000 로 다섯자리 숫자가 됨
    
    ⇒ iteratively the most, least significant digit을 비교
    
    ⇒ 이미 비교된 부분은 input에서 제외 
    

### 4.11 Rectangle Intersection

- X축과 Y축에 평행한 직사각형들이 있을 때, non-empty intersection을 갖는 두 직사각형이 있는지 테스트 하라
- Intuition
    - X와 Y 차원을 독립적으로 간주하라
    - 문제에서 명시하지 않았기 때문에 boundary도 직사각형의 일부로 간주
    - 직사각형이 교차하는 다양한 경우의 수 존재
        - 부분적으로 겹치는 영역이 있는 경우, 한쪽이 다른 한쪽을 포함, 한 변을 공유하는 경우, 한 꼭지점을 공유하는 경우, 교차하는 경우, T자를 만드는 경우 등
    - 그러므로, 여집합을 생각하는 게 더 나은 접근법 - 두 직사각형이 겹치지 않는 건 하나만 존재
        - 어떤 두 사각형에 대해, X값 집합이 교차하지 않고, Y값 집합도 교차하지 않으면 두 사각형을 겹칠일 없음

### Later

- 4.5 Compute product without arithmetical operators
- 4.6 Compute quotient without arithmetical operators
- 4.10 Generate uniform random numbers