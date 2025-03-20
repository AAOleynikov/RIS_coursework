SELECT employee.empl_password_hash AS stored_password_hash,
 user_group.usg_name AS user_group, employee.empl_id AS user_id
FROM employee
JOIN user_group ON employee.usg_id = user_group.usg_id
WHERE employee.empl_login = %s;
