SELECT 
    c.last_name,
    c.first_name,
    c.middle_name,
    p.name,
    p.country,
    o.discount_percent
FROM Orders o
JOIN Clients c ON o.client_id = c.client_id
JOIN Products p ON o.product_id = p.product_id
WHERE p.type = 'спальный'
  AND p.country = 'Германия'
  AND o.discount_percent >= 14;