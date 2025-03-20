SELECT pr_id, pr_name, pr_cat_id, pr_cat_name, pinv_amount, pr_units_measure, pinv_price
FROM invoice JOIN product_in_invoice USING(inv_id)
JOIN product USING (pr_id)
JOIN product_category USING(pr_cat_id)
WHERE inv_id = %s;