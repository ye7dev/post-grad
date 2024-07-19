# 1045. Customers Who Bought All Products

Tags: Intermediate
Date: July 13, 2024

```sql
SELECT c.customer_id
FROM Customer c
GROUP BY c.customer_id
HAVING COUNT(DISTINCT c.product_key) = (SELECT COUNT(*) FROM Product p);
```

- DISTINCT로 세야 하는 점 주의!
    - 왜냐면 Customer table의 customer_id, product_key 행이 중복으로 있을 수 있기 때문에