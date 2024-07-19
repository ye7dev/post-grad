# 1341. Movie Rating

Tags: Intermediate
Date: July 16, 2024
review?: Yes

- 쿼리 위치도, 실행 순서도 where이 group by 보다 앞이다
- Trial
    
    ```sql
    # Write your MySQL query statement below
    ## get user id who rated the most movies
    WITH num_rating AS
        (SELECT user_id, count(movie_id) AS num_movie
        FROM MovieRating
        GROUP BY user_id),
    
        avg_rating AS
        (SELECT movie_id, avg(rating) AS score
        FROM MovieRating mr
    	    INNER JOIN ON
        WHERE created_at BETWEEN '2020-02-01' AND '2020-02-29'
        GROUP BY movie_id)
    
    SELECT u.name AS results 
    FROM MovieRating mr
        INNER JOIN Users u
        ON mr.user_id = u.user_id
    GROUP BY mr.user_id
    HAVING count(movie_id) = (SELECT MAX(num_movie) FROM num_rating)
    ORDER BY u.name
    LIMIT 1
    
    UNION ALL
    
    SELECT m.title AS results
    FROM MovieRating mr
        INNER JOIN Movies m
        ON mr.movie_id = m.movie_id
    WHERE created_at BETWEEN '2020-02-01' AND '2020-02-29'
    GROUP BY mr.movie_id
    HAVING avg(rating) = (SELECT MAX(score) FROM avg_rating)
    ORDER BY m.title
    LIMIT 1;
    ```
    
- UNION ALL 사용 시 ORDER BY 절이 각각의 SELECT 문에서 사용될 수 없다는 점 때문입니다. ORDER BY는 전체 쿼리의 결과를 정렬할 때만 사용할 수 있습니다. 따라서 각 SELECT 문에서의 ORDER BY 절을 제거하고, 최종 결과에 대해 하나의 ORDER BY 절을 사용해야 합니다.

```sql
# Write your MySQL query statement below
WITH best_movie AS(
    SELECT m.title AS title, AVG(mr.rating) AS score
    FROM MovieRating mr
        INNER JOIN Movies m
        ON mr.movie_id = m.movie_id
    WHERE mr.created_at BETWEEN '2020-02-01' AND '2020-02-29'
    GROUP BY mr.movie_id
    ORDER BY score DESC, m.title
    LIMIT 1),

    best_user AS (
        SELECT u.name AS name, COUNT(mr.movie_id) AS num_rating
        FROM MovieRating mr
            INNER JOIN Users u
            ON mr.user_id = u.user_id
        GROUP BY mr.user_id
        ORDER BY num_rating DESC, u.name
        LIMIT 1
    )

    SELECT name AS results
    FROM best_user
    UNION ALL
    SELECT title AS results
    FROM best_movie
```