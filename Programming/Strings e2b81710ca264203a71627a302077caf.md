# Strings

- s[`~i`]
    - 0 ≤ i < len(S) 일 때 ~i = -(i+1)

### 6.1 Interconvert strings and integer

- library 함수 int는 사용 불가
- functools.reduce
    
    
    from functools import reduce
    
    # 리스트의 모든 원소를 더하는 예제
    
    numbers = [1, 2, 3, 4, 5]
    sum_result = reduce(lambda x, y: x + y, numbers)
    print(sum_result)  # 출력: 15
    
    ```python
    from functools import reduce
    
    # 리스트의 모든 원소를 더하는 예제
    numbers = [1, 2, 3, 4, 5]
    sum_result = reduce(lambda x, y: x + y, numbers)
    print(sum_result)  # 출력: 15
    ```
    
    - 1 + 2 → 3 + 3 → 6+4 → 10+5 = 15
    - **`reduce`**는 리스트의 첫 번째 원소부터 시작하여, 람다 함수를 적용하면서 리스트의 모든 원소를 단일 값으로 축약합니다.
    - 초기값 설정하는 경우
        
        ```python
        from functools import reduce
        
        # 리스트의 모든 원소를 더하되, 초기값을 10으로 설정
        numbers = [1, 2, 3, 4, 5]
        sum_with_initializer = reduce(lambda x, y: x + y, numbers, 10)
        print(sum_with_initializer)  # 출력: 25 (10 + 1 + 2 + 3 + 4 + 5)
        
        ```
        

### 6.2 Base conversion

- b1으로 숫자 만든 다음에 b2 나누기 나머지 이용

### 6.4 Replace and remove

- ‘a’를 ‘d’ 두 개로 대치
- ‘b’는 지워라
- size: 위의 두 연산을 적용하는 원소 수
- 알고리즘
    1. ‘b’들을 지우고 valid string의 최종 개수를 계산 
        - 한 번의 forward iteration
    2. ‘a’를 두 개의 ‘d’로 대체
        - backward iteration
    - 만약 ‘a’ 개수보다 ‘b’의 개수가 더 많으면, valid entries 개수는 감수할 것이고, 반대 경우면 증가할 것

### 6.5 Test palindromicity

- 대문자, 소문자는 무시
- index 두 개 사용
- reversed s 랑 그냥 s랑 해서 앞에서부터 zip으로 묶어서 비교

### 6.6 Reverse all the words in a sentence

- one pass로 보내기 위해서는 finish를 중간 중간 바꿔가면서 reverse 시행
- finish가 공백이 되면 그 앞까지 바꿔버림
- 공백 바로 뒤칸이 다시 새로운 시작점
- reverse 함수는 주어진 구간에서 가장 가장자리에 있는 문자들부터 swap

### 6.7 The Look-and-say problem

- 1에서 시작 → 이전 entry 숫자가 뭔지 읽고, 같은 숫자가 몇 개있는지 개수를 센다??
- 1 → 11
    - 1이 1개니까 one 1
- 11 → 21
    - 1이 두개니까 two one
- 21: one two, one one → 1211 → one one one two two one → 111221
- 개수, 개수만큼 있는 숫자 순서
- n번째 integer sequence가 무엇인지
- itertools.groupby 사용

### 6.8 Convert from roman to decimal

- input: valid roman number string → integer
- I,V,X,L,C,D,M → 1, 5, 10, 50, 100, 500, 1000
- 원래는 valid string이 되려면 non-increasing order로 작성되어야 하지만, 예외사항도 있음
    - I는 V나 X 바로 앞에 올 수 있다
    - X는 L이나 C 바로 앞에 올 수 있다
    - C는 D나 M 바로 앞에 올 수 있다
- exception에 해당하지 않는 symbol들의 합. 예외 사항에 해당되는 경우, larger symbol-smaller symbol
- 예) LIX = 50 + 1 + 10 이 아니라 IX는 예외사항이라 10-1해서 9 → 50 + 9 = 59
- 연속 exception은 허용 안됨
- 시작 값을 맨 끝 값으로 해놓고, index는 그 바로 앞에서 시작해서 1씩 줄여나감
    - 하나씩 index를 줄여가면서 exception에 해당하면 값을 빼고
    - exception에 해당 안하면 값을 더해준다

### 6.10 Write a string sinusoidally

- sinusoidally: 사인파 형태로
- left → right, top → bottom sequence
- 맨 위에 있는 letter부터 e, ,1 → H, l, o, W, r, d → l, o, !
- input string s → sneak string s