# 1683. Invalid Tweets

Tags: Easy
Date: June 21, 2024

```sql
SELECT tweet_id
FROM Tweets
WHERE LENGTH(content) > 15;
```

- tweet_id가 primary key라는 조건이 명시적으로 존재
    - 그럼 중복행이 없다는 뜻이므로 안심하고 distinct 따로 안 붙여도 됨
    - cell content 길이를 알기 위해서는 len()이 아니라 `LENGTH()`