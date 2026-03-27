SELECT DISTINCT
    p.name,
    p.type,
    p.price,
    p.country
FROM Products p
INNER JOIN Orders o ON p.product_id = o.product_id
ORDER BY p.price DESC
LIMIT 5;