# 5682. [Professional] 면적

Created time: May 13, 2024 10:05 PM
Last edited time: May 14, 2024 1:18 AM

- 세 꼭지점 주어질 때 삼각형 넓이 구하는 법
    
    ![Untitled](Untitled%2059.png)
    
    → 이래서 0.5로 끝나는 수는 정수.5의 형태로 출력하라고 함 
    
    → 사각형은 삼각형 넓이 *2 하면 되는데, 문제는 4개의 점이 사각형을 이루는지 확인하는 게 더 까다로움 
    
- 네 점이 사각형을 이루는지 확인하는 방법
    
    ### **1. 볼록성 검사**
    
    네 점이 볼록 사각형을 이루는지 확인하기 위해, 각 세 점을 이용해 만들어지는 **벡터들의 외적의 부호가 일관되게 나타나야 합니다. 즉, 모든 삼각형의 외적이 같은 방향을 가리켜야 합니다.**
    
    ### **공식:**
    
    - 세 점 *A*, *B*, *C*가 있을 때, 벡터 *AB*와 *AC*의 외적은 다음과 같이 계산합니다:
        
        ![Untitled](Untitled%2060.png)
        
    - 모든 삼각형 (네 개의 삼각형이 형성됩니다)에 대해 외적을 계산하고, 모든 결과가 같은 부호를 가지는지 확인합니다.
        - AB, AC, BC
        - AC, AD, CD
        - BC, BD, CD
        - AD, BC, CD
    
    ### **2. 대각선 교차 검사**
    
    사각형을 이루기 위해선 두 대각선이 평면 상에서 교차해야 합니다. 이를 위해 각 대각선을 이루는 두 선분이 교차하는지 확인합니다.
    
    ### **교차 검사 공식:**
    
    - 두 선분 *AB*와 *CD*의 교차를 확인하기 위해:
    
    ![Untitled](Untitled%2061.png)
    
    a   c
    
    d   b
    
    → acb, bda 
    
    a   b
    
    d   c
    
    → abc, cda 
    
    a    b
    
    c    d
    
    → abd, dca
    
- Trial
    - chatgpt 삼,사각형 깐깐한 조건 필터링
        
        ```python
        import sys
        sys.stdin = open('temp_input/sample_input.txt', 'r')
        
        from itertools import combinations
        
        def check_trio(a, b, c, half=False):
            x1, y1 = data[a]
            x2, y2 = data[b]
            x3, y3 = data[c]
        
            # if not half:
            #     possible = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
            #     if not possible:
            #         return -1
        
            temp = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
            return 1/2 * abs(temp)
        
        def check_cross(a, b, c, d):
            x1, x2, x3, x4 = [data[idx][0] for idx in (a, b, c, d)]
            y1, y2, y3, y4 = [data[idx][1] for idx in (a, b, c, d)]
            s = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
            tt = (x2 - x1) * (y4 - y1) - (y2 - y1) * (x4 - x1)
        
            if s > 0 and tt < 0:
                return True
            if s < 0 and tt > 0:
                return True
            return False
        
        def check_quatro(a, b, c, d):
            # x1, x2, x3, x4 = [data[idx][0] for idx in (a, b, c, d)]
            # y1, y2, y3, y4 = [data[idx][1] for idx in (a, b, c, d)]
            # first = x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1
            # second = x2 * y1 + x3 * y2 + x4 * y3 + x1 * y4
            # return 0.5 * (first-second)
            sign = None
            for i, j, k in combinations([a, b, c, d], 3):
                x1, y1 = data[i]
                x2, y2 = data[j]
                x3, y3 = data[k]
                vect = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                if sign is None:
                    sign = vect
                else:
                    if sign > 0 and vect > 0:
                        continue
                    elif sign < 0 and vect < 0:
                        continue
                    else:
                        return -1
        
            # ab-cd cross -> acb, adb
            if check_cross(a, b, c, d) and check_cross(c, d, a, b):
                quatro_max = check_trio(a, c, b, True) + check_trio(b, d, a, True)
        
            # ac-bd cross ->  abc, adc
            # if not check_cross(a, c, b, d) or not check_cross(b, d, a, c):
            #     return -1
            temp = check_trio(a, b, c, True) + check_trio(c, d, a, True)
            quatro_max = max(quatro_max, temp)
            temp = check_trio(a, b, d, True) + check_trio(d, c, a, True)
            quatro_max = max(quatro_max, temp)
            return quatro_max
        
        def get_area():
            max_area = 0
            for a, b, c in combinations([i for i in range(N)], 3):
                max_area = max(max_area, check_trio(a, b, c))
        
            for a, b, c, d in combinations([i for i in range(N)], 4):
                max_area = max(max_area, check_quatro(a, b, c, d))
            return max_area
        
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            data = []
            for _ in range(N):
                data.append(list(map(int, input().split())))
            ans = get_area()
            if ans % 1 == 0.5:
                print(f'#{t} {ans:.1f}')
            else:
                print(f'#{t} {int(ans)}')
        ```
        
    - 신발끈 공식 이용 1
        
        ```python
        import sys
        sys.stdin = open('temp_input/sample_input.txt', 'r')
        
        from itertools import combinations
        
        def check_trio(indices):
            a, b, c = indices
            x1, x2, x3 = [data[idx][0] for idx in (a, b, c)]
            y1, y2, y3 = [data[idx][1] for idx in (a, b, c)]
        
            check = (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if check != 0:
                return abs(check) * 0.5
            return -1
        
        def get_area():
            max_area = 0
            for comb in combinations([i for i in range(N)], 4):
                comb = list(comb)
                for i in range(4):
                    rest = comb[:i] + comb[i+1:]
                    a, b, c = rest
                    d = comb[i]
                    temp = check_trio(rest)
                    if temp > 0:
                        max_area = max(max_area, temp)
                        for trio in [(a, b, d), (a, c, d), (b, c, d)]:
                            temp2 = check_trio(trio)
                            if temp2 > 0:
                                max_area = max(max_area, temp + temp2)
                        # if max_area in (100, 31, 12.5):
                        #     print(max_area)
            return max_area
        
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            data = []
            for _ in range(N):
                data.append(list(map(int, input().split())))
            ans = get_area()
            if ans % 1 == 0.5:
                print(f'#{t} {ans:.1f}')
            else:
                print(f'#{t} {int(ans)}')
        ```
        
    - 신발끈 공식 이용 2
        
        ```python
        import sys
        sys.stdin = open('temp_input/sample_input.txt', 'r')
        
        from itertools import combinations
        
        def check_trio(indices):
            a, b, c = indices
            x1, x2, x3 = [data[idx][0] for idx in (a, b, c)]
            y1, y2, y3 = [data[idx][1] for idx in (a, b, c)]
        
            check = (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if check != 0:
                return abs(check) * 0.5
            return -1
        
        def calcul_quad(indices):
            x1, x2, x3, x4 = [data[idx][0] for idx in indices]
            y1, y2, y3, y4 = [data[idx][1] for idx in indices]
        
            first = x1*y2 + x2*y3 + x3*y4 + x4*y1
            second = x2*y1 + x3*y2 + x4*y3 + x1*y4
        
            return 0.5 * (first-second)
        
        def get_area():
            max_area = 0
            for comb in combinations([i for i in range(N)], 4):
                comb = list(comb)
                for i in range(4):
                    rest = comb[:i] + comb[i+1:]
                    a, b, c = rest
                    d = comb[i]
                    temp = check_trio(rest)
                    if temp > 0:
                        max_area = max(max_area, temp)
                        flag = True
                        for trio in [(a, b, d), (a, c, d), (b, c, d)]:
                            if check_trio(trio) < 0:
                                flag = False
                                break
                        if flag:
                            quad_temp = calcul_quad(comb)
                            max_area = max(max_area, quad_temp)
        
            return max_area
        
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            data = []
            for _ in range(N):
                data.append(list(map(int, input().split())))
            ans = get_area()
            if ans % 1 == 0.5:
                print(f'#{t} {ans:.1f}')
            else:
                print(f'#{t} {int(ans)}')
        ```
        
    - 마지막 시도
        - 정답 코드 알수 없지만 메모리도 너무 많이 쓰고…아무튼 이상한 문제다
        
        ```python
        import sys
        sys.stdin = open('temp_input/sample_input.txt', 'r')
        
        from itertools import combinations
        
        def check_trio(indices):
            a, b, c = indices
            x1, x2, x3 = [data[idx][0] for idx in (a, b, c)]
            y1, y2, y3 = [data[idx][1] for idx in (a, b, c)]
        
            check = (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if check != 0:
                return abs(check) * 0.5
            return -1
        
        def calcul_quad(indices):
            x1, x2, x3, x4 = [data[idx][0] for idx in indices]
            y1, y2, y3, y4 = [data[idx][1] for idx in indices]
        
            first = x1*y2 + x2*y3 + x3*y4 + x4*y1
            second = x2*y1 + x3*y2 + x4*y3 + x1*y4
        
            return 0.5 * abs(first-second)
        
        def get_area():
            max_area = 0
            for comb in combinations([i for i in range(N)], 4):
                a, b, c, d = comb
                temp = 0
                flag = True
                for trio in [(a, b, c), (b, c, d), (a, b, d), (a, c, d)]:
                    if check_trio(trio) < 0:
                        flag = False
                    temp = max(temp, check_trio(trio))
                if flag:
                    temp = max(temp, calcul_quad(comb))
                max_area = max(max_area, temp)
        
            return max_area
        
        T = int(input())
        for t in range(1, T+1):
            N = int(input())
            data = []
            for _ in range(N):
                data.append(list(map(int, input().split())))
            ans = get_area()
            if ans % 1 == 0.5:
                print(f'#{t} {ans:.1f}')
            else:
                print(f'#{t} {int(ans)}')
        ```
        
- 더 시도해볼 것
    - **If no three points out of four are collinear**, then we get a quadrilateral.
        - [https://www.geeksforgeeks.org/program-check-three-points-collinear/](https://www.geeksforgeeks.org/program-check-three-points-collinear/)
    - [https://www.codedrome.com/areas-quadrilaterals-from-coordinates-python/](https://www.codedrome.com/areas-quadrilaterals-from-coordinates-python/)
    - [https://www.geeksforgeeks.org/check-whether-triangle-is-valid-or-not-if-three-points-are-given/](https://www.geeksforgeeks.org/check-whether-triangle-is-valid-or-not-if-three-points-are-given/)
    
    → 이 두 개를 합치면 될 것 같음 
    
    - [ ]  세 점이 삼각형 형성하는지 확인 → 확인되면 면적 구하기
    - [ ]  네 점이 사각형 형성하는지 확인 → 확인되면 면적 구하기