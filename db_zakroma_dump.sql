CREATE DATABASE  IF NOT EXISTS `db_zakroma` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_zakroma`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: db_zakroma
-- ------------------------------------------------------
-- Server version	8.4.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `empl_id` int unsigned NOT NULL AUTO_INCREMENT,
  `empl_name` varchar(45) DEFAULT NULL,
  `empl_surmane` varchar(45) DEFAULT NULL,
  `empl_patronymic` varchar(45) DEFAULT NULL,
  `empl_birthday` date DEFAULT NULL,
  `empl_phone` varchar(16) DEFAULT NULL,
  `empl_login` varchar(45) DEFAULT NULL,
  `empl_password_hash` varchar(255) DEFAULT NULL,
  `usg_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`empl_id`),
  KEY `fk_usg_idx` (`usg_id`),
  CONSTRAINT `fk_usg` FOREIGN KEY (`usg_id`) REFERENCES `user_group` (`usg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Артём','Соколов','Михайлович','1988-01-01','3766062125921','admin','scrypt:32768:8:1$MbDqlbqgK7UjVkNu$aa51eb9dbae03d5dbc672f2ca2cf087f23f3f665ea293366f92047c6d21aa3d7c48455035dd914157d1d82a1366dcd60960c6c9b66eaec05836578f77e702403',1),(2,'София','Жданова','Матвеевна','2004-01-09','79037841837428','director','scrypt:32768:8:1$BZ4anQGpGGV5Kbg5$e4c0b305da73cbfa18bea8c594b62455dac1af56f1e066a4a9795978c86a8b552225b23e6494bb6f97ae22f729eaa0eceaca1fafea6a494b7fa4df36261a653f',2),(3,'Евгений','Семериков','Афродитович','2002-01-09','3766062125944','manager','scrypt:32768:8:1$kGH3mj8YEzjKWKiu$2c3f8a5fbc894e7829490cc804c75e7590c04b0c3ee8a7fc0b5645da97b0c61c974d13590185f3e2bdc98c347f0a9011ff43d459f3c1a68109af83a94130d65e',3);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice` (
  `inv_id` int unsigned NOT NULL AUTO_INCREMENT,
  `sup_id` int unsigned NOT NULL,
  `inv_time_dep` date NOT NULL,
  `inv_all_cost` int unsigned NOT NULL,
  `inv_status` int DEFAULT NULL,
  PRIMARY KEY (`inv_id`),
  UNIQUE KEY `inv_id_UNIQUE` (`inv_id`),
  KEY `sup_id_idx` (`sup_id`),
  CONSTRAINT `sup_id` FOREIGN KEY (`sup_id`) REFERENCES `supplier` (`sup_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
INSERT INTO `invoice` VALUES (9,1,'2024-11-16',566000,1),(10,2,'2024-11-16',124000,1),(11,1,'2024-11-16',10000,0),(12,2,'2024-11-16',5400,1);
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoiced_products_report`
--

DROP TABLE IF EXISTS `invoiced_products_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoiced_products_report` (
  `ipr_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pr_cat_id` int unsigned DEFAULT NULL,
  `pr_id` int unsigned DEFAULT NULL,
  `ipr_count` int DEFAULT NULL,
  `ipr_avg_price` float DEFAULT NULL,
  `iprp_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`ipr_id`),
  KEY `fk_2pr_id_idx` (`pr_id`),
  KEY `fk_2prcat_id_idx` (`pr_cat_id`),
  KEY `fk_iprp_id_idx` (`iprp_id`),
  CONSTRAINT `fk_2pr_id` FOREIGN KEY (`pr_id`) REFERENCES `product` (`pr_id`),
  CONSTRAINT `fk_2prcat_id` FOREIGN KEY (`pr_cat_id`) REFERENCES `product_category` (`pr_cat_id`),
  CONSTRAINT `fk_iprp_id` FOREIGN KEY (`iprp_id`) REFERENCES `invoiced_products_report_period` (`iprp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoiced_products_report`
--

LOCK TABLES `invoiced_products_report` WRITE;
/*!40000 ALTER TABLE `invoiced_products_report` DISABLE KEYS */;
INSERT INTO `invoiced_products_report` VALUES (11,7,11,50,400,5),(12,3,3,500,100,5),(13,5,7,600,1100,5);
/*!40000 ALTER TABLE `invoiced_products_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoiced_products_report_period`
--

DROP TABLE IF EXISTS `invoiced_products_report_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoiced_products_report_period` (
  `iprp_id` int unsigned NOT NULL AUTO_INCREMENT,
  `iprp_year` int DEFAULT NULL,
  `iprp_month` int DEFAULT NULL,
  PRIMARY KEY (`iprp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoiced_products_report_period`
--

LOCK TABLES `invoiced_products_report_period` WRITE;
/*!40000 ALTER TABLE `invoiced_products_report_period` DISABLE KEYS */;
INSERT INTO `invoiced_products_report_period` VALUES (5,2024,11);
/*!40000 ALTER TABLE `invoiced_products_report_period` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `pr_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pr_cat_id` int unsigned NOT NULL,
  `pr_units_measure` varchar(16) NOT NULL,
  `pr_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`pr_id`),
  UNIQUE KEY `pr_code_UNIQUE` (`pr_id`),
  KEY `pr_cat_id_idx` (`pr_cat_id`),
  CONSTRAINT `pr_cat_id` FOREIGN KEY (`pr_cat_id`) REFERENCES `product_category` (`pr_cat_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,1,'шт.','Совочек'),(2,2,'шт.','Моющее средство'),(3,3,'кг','Мука пшеничная'),(4,3,'л','Молоко пастеризованное'),(5,4,'шт.','Смартфон'),(6,4,'шт.','Ноутбук'),(7,5,'шт.','Футболка мужская'),(8,5,'шт.','Штаны женские'),(9,6,'шт.','Ручка шариковая'),(10,6,'шт.','Блокнот А5'),(11,7,'шт.','Кукла Барби'),(12,7,'шт.','Конструктор LEGO'),(13,8,'шт.','Стул деревянный'),(14,8,'шт.','Стол компьютерный'),(15,9,'кг','Корм для собак'),(16,9,'л','Шампунь для животных'),(17,10,'шт.','Крем для лица'),(18,10,'шт.','Шампунь для волос');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_capacity`
--

DROP TABLE IF EXISTS `product_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_capacity` (
  `pc_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pr_id` int unsigned NOT NULL,
  `pc_price` int unsigned NOT NULL,
  `pc_amount` int unsigned NOT NULL,
  `pc_time_update` date NOT NULL,
  PRIMARY KEY (`pc_id`),
  UNIQUE KEY `pc_id_UNIQUE` (`pc_id`),
  UNIQUE KEY `pr_id` (`pr_id`,`pc_price`),
  KEY `pr_id_idx` (`pr_id`),
  CONSTRAINT `pr_id` FOREIGN KEY (`pr_id`) REFERENCES `product` (`pr_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_capacity`
--

LOCK TABLES `product_capacity` WRITE;
/*!40000 ALTER TABLE `product_capacity` DISABLE KEYS */;
INSERT INTO `product_capacity` VALUES (24,11,400,50,'2024-11-16'),(25,3,100,500,'2024-11-16'),(26,7,1000,500,'2024-11-16'),(27,7,1200,100,'2024-11-16'),(28,4,60,90,'2024-11-16');
/*!40000 ALTER TABLE `product_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_category` (
  `pr_cat_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pr_cat_name` varchar(45) NOT NULL,
  PRIMARY KEY (`pr_cat_id`),
  UNIQUE KEY `pr_cat_id_UNIQUE` (`pr_cat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category` DISABLE KEYS */;
INSERT INTO `product_category` VALUES (1,'Детские товары'),(2,'Бытовая химия'),(3,'Продукты питания'),(4,'Электроника'),(5,'Одежда'),(6,'Канцелярские товары'),(7,'Игрушки'),(8,'Мебель'),(9,'Товары для животных'),(10,'Косметика и уход');
/*!40000 ALTER TABLE `product_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_in_invoice`
--

DROP TABLE IF EXISTS `product_in_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_in_invoice` (
  `pinv_id` int unsigned NOT NULL AUTO_INCREMENT,
  `pr_id` int unsigned NOT NULL,
  `inv_id` int unsigned NOT NULL,
  `pinv_amount` int unsigned NOT NULL,
  `pinv_price` int unsigned NOT NULL,
  PRIMARY KEY (`pinv_id`),
  UNIQUE KEY `pinv_id_UNIQUE` (`pinv_id`),
  KEY `pr_id_idx` (`pr_id`),
  KEY `inv_id_idx` (`inv_id`),
  KEY `pr_id_idx1` (`pr_id`),
  KEY `inv_id_idx1` (`inv_id`),
  CONSTRAINT `inv_id` FOREIGN KEY (`inv_id`) REFERENCES `invoice` (`inv_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `pr_id_pii` FOREIGN KEY (`pr_id`) REFERENCES `product` (`pr_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_in_invoice`
--

LOCK TABLES `product_in_invoice` WRITE;
/*!40000 ALTER TABLE `product_in_invoice` DISABLE KEYS */;
INSERT INTO `product_in_invoice` VALUES (9,11,9,40,400),(10,3,9,500,100),(11,7,9,500,1000),(12,11,10,10,400),(13,7,10,100,1200),(14,9,11,1000,10),(15,4,12,90,60);
/*!40000 ALTER TABLE `product_in_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `sup_id` int unsigned NOT NULL AUTO_INCREMENT,
  `sup_phone` varchar(16) NOT NULL,
  `sup_town` varchar(45) NOT NULL,
  `sup_name` varchar(45) NOT NULL,
  `sup_surname` varchar(45) DEFAULT NULL,
  `sup_patronymic` varchar(45) DEFAULT NULL,
  `sup_bank_name` varchar(45) NOT NULL,
  `sup_bank_acc_numb` varchar(45) NOT NULL,
  `sup_login` varchar(45) DEFAULT NULL,
  `sup_password_hash` varchar(255) DEFAULT NULL,
  `usg_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`sup_id`),
  UNIQUE KEY `sup_id_UNIQUE` (`sup_id`),
  KEY `fk2_usg_idx` (`usg_id`),
  CONSTRAINT `fk2_usg` FOREIGN KEY (`usg_id`) REFERENCES `user_group` (`usg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES (1,'79091838468','тверь','Игорь','Егоров','Васильевич','зелёный','124141245454353','supplier1','scrypt:32768:8:1$VJVZjM2WiyPDIaYt$d023412935eb9aa506be4f8eab5fc077b95c259f4f06730244fbc563b3a415241cb86b1204a9cb5e319fd1d74297e8fa3494aea03a3fad60f6f051e6f14d55f0',4),(2,'74956585887','тула','Виктор','Вихорьков','Олегович','жёлтый','213141142421412','supplier2','scrypt:32768:8:1$yjLUGZYiWjOZ0QjH$802895a7cfbe9a20cbf6eece0b4dcc80573976bd6f2ab836dde124f0c71e91e1992057d7ae90cc539a39bbde6b74b99bf079f17d03084767505ab0c6345bd2a4',4);
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_group` (
  `usg_id` int unsigned NOT NULL AUTO_INCREMENT,
  `usg_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`usg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_group`
--

LOCK TABLES `user_group` WRITE;
/*!40000 ALTER TABLE `user_group` DISABLE KEYS */;
INSERT INTO `user_group` VALUES (1,'admin'),(2,'director'),(3,'manager'),(4,'supplier');
/*!40000 ALTER TABLE `user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'db_zakroma'
--

--
-- Dumping routines for database 'db_zakroma'
--
/*!50003 DROP PROCEDURE IF EXISTS `generate_invoiced_products_report` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `generate_invoiced_products_report`(IN report_year INT, IN report_month INT)
proc_label:BEGIN
    DECLARE fk_iprp_id INT;

    -- Проверка на наличие записи в таблице периодов отчета
    SELECT iprp_id INTO fk_iprp_id
		FROM invoiced_products_report_period
		WHERE iprp_year = report_year AND iprp_month = report_month;

	IF fk_iprp_id IS NOT NULL THEN
        SELECT 1 AS p_status, 'Отчёт за указанный период уже существует.' AS message;
        LEAVE proc_label;
    END IF;

    -- Если запись не найдена, создаем новую
    IF fk_iprp_id IS NULL THEN
        INSERT INTO invoiced_products_report_period (iprp_year, iprp_month)
        VALUES (report_year, report_month);
        SET fk_iprp_id = LAST_INSERT_ID();
    END IF;

    -- Генерация отчета и сохранение данных в таблицу
    INSERT INTO invoiced_products_report (
        pr_cat_id,
        pr_id,
        ipr_count,
        ipr_avg_price,
        iprp_id
    )
    
    SELECT 
        pr_cat_id,                           -- Категория товара
        pr_id,                               -- ID товара
        SUM(pinv_amount) AS total_count,     -- Общее количество товара
        AVG(pinv_price) AS avg_price,      	 -- Средняя стоимость единицы
        fk_iprp_id                           -- ID периода отчета
    FROM 
		invoice
	JOIN   
        product_in_invoice USING(inv_id)
    JOIN 
        product USING(pr_id)
    WHERE 
        YEAR(inv_time_dep) = report_year 
        AND MONTH(inv_time_dep) = report_month
        AND inv_status = 1
    GROUP BY
        pr_cat_id, pr_id;
        
	SELECT 0 AS p_status, 'Отчёт создан успешно.' AS message;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-20 21:24:02
