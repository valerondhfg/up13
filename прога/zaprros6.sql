SELECT DISTINCT c.*
FROM Clients c
JOIN Orders o ON c.client_id = o.client_id
JOIN Products p ON o.product_id = p.product_id
WHERE p.type = 'спальный'
  AND p.country = 'Германия'
  AND o.discount_percent >= 14;