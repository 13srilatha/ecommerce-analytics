SELECT 
    p.product_name,
    p.category,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC;

SELECT 
    c.customer_id,
    c.customer_name,
    c.region,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent,
    ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.region
ORDER BY total_spent DESC
LIMIT 5;

SELECT 
    c.region,
    COUNT(DISTINCT c.customer_id) as customer_count,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue,
    ROUND(AVG(o.total_amount), 2) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;

SELECT 
    status,
    COUNT(*) as order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage,
    SUM(total_amount) as total_amount
FROM orders
GROUP BY status
ORDER BY order_count DESC;

SELECT 
    order_date,
    COUNT(order_id) as orders,
    SUM(total_amount) as revenue,
    ROUND(AVG(total_amount), 2) as avg_order_value
FROM orders
GROUP BY order_date
ORDER BY order_date;

SELECT 
    c.customer_id,
    c.customer_name,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC
LIMIT 3;

SELECT 
    CASE 
        WHEN order_count = 1 THEN 'One-Time Buyer'
        ELSE 'Repeat Customer'
    END as customer_type,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_customer_value
FROM (
    SELECT 
        c.customer_id,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) subquery
GROUP BY customer_type;

SELECT 
    product_id,
    product_name,
    category,
    stock,
    price,
    price * stock as inventory_value
FROM products
WHERE stock < 20
ORDER BY stock ASC;

SELECT 
    CASE 
        WHEN lifetime_value > 50000 THEN 'Premium'
        WHEN lifetime_value > 30000 THEN 'Standard'
        ELSE 'Basic'
    END as customer_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(lifetime_value), 2) as avg_ltv,
    SUM(lifetime_value) as total_ltv
FROM customers
GROUP BY customer_segment
ORDER BY total_ltv DESC;

SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) as product_count,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
