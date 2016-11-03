CREATE DATABASE  IF NOT EXISTS `storeAssist` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `storeAssist`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `card_reader_report`
--

DROP TABLE IF EXISTS `card_reader_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `card_reader_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `store_id` bigint(20) NOT NULL,
  `employee_initials` varchar(45) NOT NULL,
  `reported_date` date NOT NULL,
  `reported_time` time NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index3` (`store_id`,`reported_date`),
  KEY `fk_card_reader_report_1_idx` (`store_id`),
  CONSTRAINT `fk_card_reader_report_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `change_order`
--

DROP TABLE IF EXISTS `change_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `store_id` bigint(20) NOT NULL,
  `ordered_by` varchar(45) NOT NULL,
  `ordered_time` datetime NOT NULL,
  `order_status` varchar(45) NOT NULL,
  `received_by` varchar(45) DEFAULT NULL,
  `received_time` datetime DEFAULT NULL,
  `received_status` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_change_order_1_idx` (`store_id`),
  CONSTRAINT `fk_change_order_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `change_order_details`
--

DROP TABLE IF EXISTS `change_order_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_order_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `change_order_id` bigint(20) NOT NULL,
  `currency_id` int(11) NOT NULL,
  `order_amount` int(11) DEFAULT NULL,
  `received_amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_change_order_details_1_idx` (`change_order_id`),
  KEY `fk_change_order_details_2_idx` (`currency_id`),
  CONSTRAINT `fk_change_order_details_1` FOREIGN KEY (`change_order_id`) REFERENCES `change_order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_change_order_details_2` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cheque_history`
--

DROP TABLE IF EXISTS `cheque_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cheque_history` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cheque_number` int(11) NOT NULL,
  `account_number` bigint(20) NOT NULL,
  `routing_number` int(11) NOT NULL,
  `store_id` bigint(20) NOT NULL,
  `amount` int(11) NOT NULL,
  `auth_code` int(11) NOT NULL,
  `checked_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index2` (`account_number`),
  UNIQUE KEY `index3` (`cheque_number`,`account_number`,`routing_number`),
  KEY `fk_cheque_validation_1_idx` (`store_id`),
  CONSTRAINT `fk_cheque_validation_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `currency`
--

DROP TABLE IF EXISTS `currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `currency`
--

LOCK TABLES `currency` WRITE;
/*!40000 ALTER TABLE `currency` DISABLE KEYS */;
INSERT INTO `currency` VALUES (1,'Twenties',20),(2,'Fives',5),(3,'Ones',1),(4,'Quarters Roll(s)',10),(5,'Dimes Roll(s)',5),(6,'Nickles Roll(s)',2),(7,'Pennies Box(s)',25);
/*!40000 ALTER TABLE `currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drpmpchk`
--

DROP TABLE IF EXISTS `drpmpchk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drpmpchk` (
  `store` tinyint(3) unsigned NOT NULL,
  `bdate` date NOT NULL DEFAULT '0001-01-01',
  `date` date NOT NULL DEFAULT '0001-01-01',
  `hr` tinyint(4) NOT NULL DEFAULT '0',
  `min` tinyint(4) NOT NULL DEFAULT '0',
  `sec` tinyint(4) NOT NULL DEFAULT '0',
  `init` varchar(3) DEFAULT NULL,
  `dipped_yn` char(1) DEFAULT NULL,
  `reader_yn` char(1) DEFAULT NULL,
  PRIMARY KEY (`store`,`bdate`),
  UNIQUE KEY `date_key` (`bdate`,`store`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `drpmpdip`
--

DROP TABLE IF EXISTS `drpmpdip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drpmpdip` (
  `store` tinyint(3) unsigned NOT NULL,
  `bdate` date NOT NULL DEFAULT '0001-01-01',
  `tankno` smallint(5) unsigned NOT NULL,
  `grade` varchar(5) NOT NULL DEFAULT ' ',
  `descr` varchar(30) NOT NULL DEFAULT ' ',
  `inches` decimal(8,2) DEFAULT NULL,
  `gallons` decimal(8,2) DEFAULT NULL,
  `ullage` decimal(8,2) DEFAULT NULL,
  `water_inches` decimal(8,2) DEFAULT NULL,
  `temp` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`store`,`bdate`,`tankno`),
  UNIQUE KEY `date_key` (`bdate`,`store`,`tankno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `it_payment_report`
--

DROP TABLE IF EXISTS `it_payment_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `it_payment_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `store_id` bigint(20) NOT NULL,
  `employee_initials` varchar(45) NOT NULL,
  `reported_date` date NOT NULL,
  `reported_time` time NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index3` (`store_id`,`reported_date`),
  KEY `fk_it_payment_report_1_idx` (`store_id`),
  CONSTRAINT `fk_it_payment_report_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (111,'Employee'),(112,'Manager'),(113,'Admin');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
INSERT INTO `store` VALUES (18,'7-Eleven Store #36104'),(1188,'7-Eleven Store #1188');
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(256) NOT NULL,
  `initials` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','venkat','venkat@scriptbees.com','99a4977789ec484285f7180aa7d6d78921a604600cb462f58e13c050b09e105678918ea67d2ab70ea6f2dd7fdb7c0fae','D'),(2,'manager','madhura','madhura.morajkar@scriptbees.com','2be5b04da0214ffaaa919e6118191f1cc84cad735caf6ed02fca7a2d66ad2a99aecda03aca27c42f6b977a3f586ae31f','M'),(3,'employee','purnesh','purnesh.anugolu@scriptbees.com','116c133ba6144e5998d13a771f94647cd386df4140e63815b76419727605e85be452bb98ad3d6a47230cf878e084aeab','A'),(4,'employee1188','mohan','mohankrishna.v@scriptbees.com','5a5b3734718a4a079a926efe4f9a519869209824396c95ead0cdd79fa91c74c7b365f9d8bae91a9a6858a15989c9a29f','V');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `role_id` int(11) NOT NULL,
  `store_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index5` (`user_id`,`role_id`,`store_id`),
  KEY `fk_user_roles_1_idx` (`user_id`),
  KEY `fk_user_roles_2_idx` (`role_id`),
  KEY `fk_user_roles_3_idx` (`store_id`),
  CONSTRAINT `fk_user_roles_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_roles_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_roles_3` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` VALUES (1,1,113,18),(2,2,112,18),(3,3,111,18),(4,4,111,1188);
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'storeAssist'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
