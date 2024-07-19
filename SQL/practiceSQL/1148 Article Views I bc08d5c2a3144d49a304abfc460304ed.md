# 1148. Article Views I

Tags: Easy
Date: June 21, 2024

- exists 복습
    - where절 안에 들어감
    - from으로 가져온 테이블의 각 행 (포함 구문 테이블의 각 행)을 한번씩 모두 where 절 뒤에 대입해봄
    - exists 다음에 오는 상관 쿼리는 select 1으로 시작하는 경우가 많음
        - 특정 행이 상관 쿼리에 있는 조건에 부합해서 select 1인 행으로 나오면, exists 한 것이므로 해당 행의 정보를 select에서 요구하는 대로 가져다 줌
    - [x]  exists 넣은 쿼리에서는 모든 행의 정보가 가져와졌다. 왜지?
        
        ```sql
        SELECT author_id
        FROM Views
        WHERE exists (SELECT 1
                        FROM Views
                        WHERE author_id = viewer_id);
        ```
        
        - 포함 구문 테이블에 alias를 안해서 서브 쿼리가 상관 쿼리가 되지 못했다.
        - 따라서 비상관 쿼리를 먼저 실행하면 행이 무조건 있기 때문에 포함 구문 테이블에 있는 모든 행을 가져온듯
    - [x]  상관쿼리로 만든 쿼리는 왜 세번째 문제에서 자꾸 틀렸지?
        
        ```sql
        SELECT distinct author_id as id
        FROM Views AS V1
            WHERE EXISTS (
                SELECT 1
                FROM Views AS V2
                WHERE V2.viewer_id = V1.author_id
            )
        ORDER BY 1; 
        ```
        
        - author_id가 다른 행에서 viewer_id로 존재하는지 여부를 확인합니다.
            - 같은 행에서 두 id가 같아야 하는게 아니라 V1의 author_id가 V2의 어떤 행의 viewer_id로 들어가 있기만 하면 1이 return 되어서 해당 행 반환
    - 굳이 상관 쿼리로 만들어서 풀고 싶으면
        
        ```sql
        SELECT DISTINCT author_id AS id
        FROM Views AS V1
        WHERE EXISTS (
            SELECT 1
            FROM Views AS V2
            WHERE V2.viewer_id = V1.author_id
            AND V2.author_id = V2.viewer_id
        )
        ORDER BY 1;
        ```
        
- AC 코드
    
    ```sql
    # Write your MySQL query statement below
    SELECT distinct author_id as id
    FROM Views
    WHERE author_id = viewer_id
    ORDER BY 1; 
    ```