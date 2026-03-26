SELECT 
    o.order_id,
    c.last_name,
    c.first_name,
    p.name,
    o.order_date
FROM Orders o
JOIN Clients c ON o.client_id = c.client_id
JOIN Products p ON o.product_id = p.product_id
WHERE strftime('%Y', o.order_date) = '2025';