SELECT sup_password_hash AS stored_password_hash, sup_id AS user_id, usg_name AS user_group
FROM supplier JOIN user_group USING(usg_id)
WHERE sup_login = %s;