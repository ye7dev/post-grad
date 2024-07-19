# 619. Biggest Single Number

Tags: Easy
Date: July 13, 2024

```sql
SELECT MAX(num) AS num
FROM (
    SELECT *
    FROM MyNumbers
    GROUP BY num 
    HAVING COUNT(*) = 1) AS one_num; 
```

- [x]  HAVING 조건에 맞는 그룹이 없으면 derived table이 뭐로 나오지?
    - select * 했기 때문에 유일한 칼럼 num이 나오고, 조건에 맞는 그룹이 없어서 빈 칸으로 나온다
- [x]  null만 있는 table에서 MAX를 취하면 뭐가 나오지?
    - null이 나온다
    - 값이 없는 빈 칼럼에 MAX를 취해도 NULL이 나온다
- table 생성 remind
    
    ```sql
    CREATE TABLE learning_sql.MyNumbers (
    	num INT PRIMARY KEY); 
    	
    ALTER TABLE learning_sql.MyNumbers
    DROP PRIMARY KEY; # 그래야 칼럼에 중복 값 넣을 수 있음 
    ```
    
- 값 추가 remind
    
    ```sql
    INSERT INTO learning_sql.MyNumbers
    VALUES (8), (8);
    ```