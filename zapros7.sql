SELECT 
    o.order_id,
    c.last_name,
    c.first_name,
    c.middle_name,
    p.name,
    o.order_date,
    o.discount_percent
FROM Orders o
JOIN Clients c ON o.client_id = c.client_id
JOIN Products p ON o.product_id = p.product_id
WHERE c.last_name LIKE 'Â%' 
   OR c.last_name LIKE 'Î%'
ORDER BY c.last_name;