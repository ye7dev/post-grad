# H-Index

Status: done, in progress, 🏋️‍♀️
Theme: Programmers, sort
Created time: April 3, 2024 11:02 AM
Last edited time: April 3, 2024 1:40 PM

- 어떤 과학자가 발표한 논문 `n`편 중, `h`번 이상 인용된 논문이 `h`편 이상이고 나머지 논문이 h번 이하 인용되었다면 `h`의 최댓값이 이 과학자의 H-Index입니다
    - [3, 0, 6, 1, 5] → [0, 1, 3, 5, 6]
- Trial
    
    ```python
    def solution(citations):
        answer = 0
        citations.sort()
        max_h = -1
        n = len(citations)
        for i in range(len(citations)):
            h = citations[i]
            if n-i >= h:
                max_h = max(max_h, h)
        
        return max_h
    ```
    
- 반례
    - [5, 5, 5, 5], n = 4
        
        i = 0 → h = 5 → 4-0 = 4 < H 
        
        위의 코드로 하면 max_h = -1 
        
    - `h`번 이상 인용된 논문이 `h`편 이상
        - [0, 1, 3, 5, 6]
            - 0번 이상 인용된 논문은 0편 이상 (5)
            - 1번 이상 인용된 논문은 1편 이상 (4)
            - 2번 이상 인용된 논문은 2편 이상 (3)
            - 3번 이상 인용된 논문은 3편 이상 (3)
            - 4번 이상 인용된 논문은 4편 이상? X (2)
            
            → H_idx = 3 
            
        - [5, 5, 5, 5]
            - 1번 이상 인용된 논문은 1편 이상 (4)
            - 2번 이상 인용된 논문은 2편 이상 (4)
            - 3번 이상 인용된 논문은 3편 이상 (4)
            - 4번 이상 인용된 논문은 4편 이상 (4)
            
            → H_idx = 4
            
            - citation[0] ≥ idx: n-idx
        
- AC 코드
    
    ```python
    def solution(citations):
        answer = 0
        citations.sort(reverse=True)
        n = len(citations)
        max_h = 0
        for i, cite in enumerate(citations):
            cur_h = min(i+1, cite)
            max_h = max(max_h, cur_h)
        return max_h
    ```