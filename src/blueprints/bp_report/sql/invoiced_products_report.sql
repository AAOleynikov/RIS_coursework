SELECT
    product_category.pr_cat_id,
    product_category.pr_cat_name,
    product.pr_id,
    product.pr_name,
    invoiced_products_report.ipr_count,
    invoiced_products_report.ipr_avg_price
FROM
    invoiced_products_report
JOIN
    product ON invoiced_products_report.pr_id = product.pr_id
JOIN
    product_category ON product.pr_cat_id = product_category.pr_cat_id
JOIN
    invoiced_products_report_period ON invoiced_products_report.iprp_id = invoiced_products_report_period.iprp_id
WHERE
    invoiced_products_report_period.iprp_year = %s
    AND invoiced_products_report_period.iprp_month = %s;