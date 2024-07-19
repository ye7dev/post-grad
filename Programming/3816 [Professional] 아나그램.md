# 3816. [Professional] 아나그램

Created time: April 18, 2024 9:20 PM
Last edited time: April 21, 2024 10:20 AM

- 문제
    
    아나그램이란 문자열의 문자들을 모두 사용하여 재배열한 것을 의미한다.
    
    “abc”의 아나그램은 “abc”, “acb”, “bac”, “bca”, “cab”, “cba” 총 6개이다.
    
    문자열 S1, S2이 차례대로 주어진다. S2의 부분문자열 중 S1의 아나그램인 것의 개수를 구하는 프로그램을 작성하라.
    
    **[입력]**
    
    첫 줄에 테스트케이스의 개수 T가 주어진다. (T ≤ 20)
    
    각 테스트케이스의 첫 줄에 S1, S2가 사이에 공백을 갖고 띄어져 있다.
    
    S1과 S2는 영문 소문자로만 이루어져 있다. (1 ≤ |S1| ≤ |S2| ≤ 100,000)(|S1|, |S2|는 문자열 S1, S2의 길이)
    
    **[출력]**
    
    각 테스트케이스마다 한 줄에 걸쳐, 테스트케이스 수 “#(TC) “를 출력하고, 해당 테스트케이스의 아나그램인 것의 개수를 출력한다.
    
- ideas
    1. substring은 슬라이딩 윈도우 
    2. 애너그램은 순서 상관 없이 구성 요소 개수만 동일하면 됨 → count 
        - counter 함수 쓸 때보다 메모리 효율성 있다고 함
        - 알파벳 하나에 대한 index 구할 때 주의 : ord 함수 사용
            - ord(’a’) = 97, ord(’z’) = 122
            
            → 어떤 문자의 index를 구하려면 97을 빼야 함 → 0~25 
            
    3. 각 시작점에서 슬라이딩 윈도우 했을 때 알파벳 카운트가 타겟과 일치하면 애너그램이라는 의미이므로 정답에 하나 추가 
    4. 하나의 시작점 봤으면 거기서는 더 볼 필요 없으므로 다음 시작점으로 이동 
- bit array로 부분 집합 구하는 방법 까먹음
    1. 모든 원소 조합 (2**n == 1 << n)에 대해 돌면서 (i)
    2. 각 자릿수에 대해 돌면서 (j)
    3. j번째 자리에 i의 bit가 set bit(1)이면 ← `if j & (1 << j)`
    4. subset에 j번째 요소 추가 
- substring은 연속적인 요소로 구성되어야 함
    
    → 슬라이딩 윈도우 가능 
    
- Trial
    - #1 bit array & set 사용
        - 이러면 anagram이 아니라 같은 알파벳이 여러개 들어가 있는 경우도 카운트 되어서 실제보다 훨씬 큰 숫자가 나옴
        
        ```python
        def get_anagram(s1, s2):
            n = len(s2)
            num_ana = 0
            for i in range(2**n):
                substring = ""
                for j in range(n):
                    if i & (1 << j):
                        substring += s2[i]
                if set(substring) == set(s1):
                    num_ana += 1 
            return num_ana
                    
        
        T = int(input())
        for t in range(1, T+1):
            fixed,substr = input().split()
            ans = get_anagram(fixed, substr)
            print(f'#{t} {ans}')
        ```
        
- AC 코드
    
    ```python
    def count_alphabet(string, start, end):
        alpha_count = [0] * 26
        for i in range(start, end):
            char_idx = ord(string[i])-ord('a')
            alpha_count[char_idx] += 1
        return alpha_count
    
    T = int(input())
    for t in range(1, T+1):
        short, long = input().split()
        short_len, long_len = len(short), len(long)
        short_count = count_alphabet(short, 0, short_len)
    
        i, ans = 0, 0
        while i <= long_len - short_len:
            long_count = count_alphabet(long, i, i + short_len)
            if short_count == long_count:
                ans += 1
            i += 1
    
        print(f'#{t} {ans}')
    ```