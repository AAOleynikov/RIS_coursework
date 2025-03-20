INSERT INTO product_capacity (pr_id, pc_price, pc_amount, pc_time_update)
SELECT
    pr_id,
    pinv_price,
    pinv_amount,
    CURDATE()
FROM
    invoice
JOIN
    product_in_invoice USING (inv_id)
WHERE
    inv_id = %s
ON DUPLICATE KEY UPDATE
    pc_amount = pc_amount + VALUES(pc_amount),
    pc_time_update = CURDATE();