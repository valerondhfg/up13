SELECT 
    c.last_name,
    c.first_name,
    SUM(p.price * (1 - o.discount_percent/100)) AS total_spent
FROM Orders o
JOIN Clients c ON o.client_id = c.client_id
JOIN Products p ON o.product_id = p.product_id
GROUP BY c.client_id
ORDER BY total_spent DESC;