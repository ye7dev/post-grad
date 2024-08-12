# 1440. Evaluate Boolean Expression

Tags: Medium

- 문제 이해
    - variable 테이블에 변수별 값이 주어질 때, Expressions 테이블의 식이 True인지 False인지 확인
- 해결 과정
    - string으로 concat 하면 식을 자동으로 evaluate 해주려나?
    - `SELECT IF(6 < 7, TRUE, FALSE)`은 1로 나온다
        - 조건문 true/false 을 string으로 바꾸면 될 듯
    - IF 문 안에 operator를 어떻게 넣어주지?
        - E 테이블 안에 있는 operator도 결국 string이다 → case when으로 해보자 귀찮지만
    - c.f. enum vs. string 자료형
        
        ![Untitled](1440%20Evaluate%20Boolean%20Expression%200013167518c747b5b22f2a9b712ebd29/Untitled.png)