SELECT pr_id AS product_id, pr_name AS product_name, pr_cat_name AS product_category_name,
pr_units_measure AS product_units_measure
FROM product JOIN product_category USING(pr_cat_id);