SELECT inv_id, inv_time_dep, sup_id, pr_cat_id, pr_cat_name, pr_id, pr_name
FROM invoice JOIN product_in_invoice USING(inv_id)
             JOIN product USING(pr_id)
             JOIN product_category USING(pr_cat_id)
WHERE inv_time_dep >= %s AND inv_time_dep <= %s
ORDER BY inv_time_dep;