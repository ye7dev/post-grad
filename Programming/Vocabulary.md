# Vocabulary

- foreign key : column of **binding external data**
- transaction : like a **box** in which you can put many SQL statements and execute them together.
    - **the results of these queries are indeed stored**
    - or **restore the results caused by these queries**.
- ACID
    - Atomicity : regard **a group of queries** as the smallest execution unit in SQ
        - **if a bug is triggered when we are half way through a group of queries for updating anything, the whole batch of updates should be discarded.**.
    - Consistency : `ROLLBACK` keyword in the previous chapter to ensure the correctness of the data and return it to the correct state (before the transaction started).
    - Isolation : solve data problems when traffic increases; it ensures that transactions do not affect each other.
    - Durability : as long as a result has been committed, it must exist in the hard disk data permanently.
- 정규화 : 각각의 독립적인 정보가 한 위치에만 저장되도록 DB 설계를 수정하는 절차
- natural key: entity 정보 중 고유한 값을 가져서 각 행마다 식별할 수 있는 의미를 가지는 열
- surrogate key: entity에서 파생된 정보가 아닌 임의의 고유 식별자로, 일련번호와 같은 가상의 값으로 기본 키의 역할을 하는 열 (주로 AUTO INCREMENT)
- 쿼리 옵티마이저: 쿼리 실행 시 가장 효율적인 방법을 결정
    - from 절에 호출된 테이블에 조인할 순서 및 사용 가능한 인덱스 확인
    - 서버가 쿼리 실행에 필요한 실행 계획 선택