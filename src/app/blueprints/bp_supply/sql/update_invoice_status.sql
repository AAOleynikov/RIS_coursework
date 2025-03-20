UPDATE invoice
SET inv_time_dep = CURDATE(), inv_status = 1
WHERE inv_id = %s;

