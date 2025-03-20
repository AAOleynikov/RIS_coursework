SELECT inv_id, inv_time_dep, inv_all_cost, sup_id, sup_phone, sup_town, sup_surname,sup_name,
sup_patronymic, sup_bank_name, sup_bank_acc_numb
FROM invoice JOIN supplier USING(sup_id)
WHERE inv_status = 0;