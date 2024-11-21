-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: db.relational-data.org    Database: UW_std
-- ------------------------------------------------------
-- Server version	8.0.31-google

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `person` (
  `p_id` int NOT NULL DEFAULT '0',
  `professor` varchar(11) NOT NULL DEFAULT '0',
  `student` varchar(11) NOT NULL DEFAULT '0',
  `hasPosition` varchar(11) NOT NULL DEFAULT '0',
  `inPhase` varchar(40) DEFAULT NULL,
  `yearsInProgram` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`p_id`),
  KEY `person_hasPosition` (`hasPosition`),
  KEY `person_inPhase` (`inPhase`),
  KEY `person_yearInProgram` (`yearsInProgram`),
  KEY `person_professor` (`professor`),
  KEY `person_student` (`student`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES (3,'0','1','0','0','0'),(4,'0','1','0','0','0'),(5,'1','0','Faculty','0','0'),(6,'0','1','0','Post_Quals','Year_2'),(7,'1','0','Faculty_adj','0','0'),(9,'0','1','0','Post_Generals','Year_5'),(13,'0','1','0','Post_Generals','Year_7'),(14,'0','1','0','Post_Generals','Year_10'),(15,'0','1','0','Post_Quals','Year_3'),(18,'0','1','0','Pre_Quals','Year_3'),(19,'0','1','0','Pre_Quals','Year_1'),(20,'0','1','0','Pre_Quals','Year_1'),(21,'0','1','0','Post_Generals','Year_5'),(22,'1','0','Faculty_eme','0','0'),(23,'0','1','0','0','0'),(27,'0','1','0','Pre_Quals','Year_1'),(29,'1','0','Faculty_adj','0','0'),(31,'0','1','0','0','0'),(35,'0','1','0','0','0'),(36,'0','1','0','0','0'),(37,'0','1','0','Pre_Quals','Year_1'),(38,'0','1','0','0','0'),(39,'0','1','0','0','0'),(40,'1','0','Faculty','0','0'),(41,'0','1','0','Post_Quals','Year_5'),(42,'0','1','0','Pre_Quals','Year_1'),(45,'0','1','0','Post_Generals','Year_5'),(46,'1','0','Faculty','0','0'),(51,'0','1','0','Pre_Quals','Year_2'),(52,'1','0','Faculty','0','0'),(57,'1','0','0','0','0'),(58,'0','1','0','0','0'),(61,'0','1','0','0','0'),(62,'0','1','0','Pre_Quals','Year_2'),(63,'0','1','0','Post_Generals','Year_5'),(64,'1','0','0','0','0'),(67,'0','1','0','Post_Generals','Year_6'),(68,'0','1','0','Post_Generals','Year_5'),(70,'0','1','0','Pre_Quals','Year_1'),(71,'0','1','0','0','0'),(72,'1','0','Faculty','0','0'),(73,'0','1','0','Post_Quals','Year_4'),(75,'0','1','0','Post_Generals','Year_6'),(76,'0','1','0','0','0'),(77,'0','1','0','0','0'),(79,'1','0','Faculty','0','0'),(80,'0','1','0','Post_Generals','Year_6'),(81,'0','1','0','Post_Generals','Year_6'),(82,'1','0','Faculty','0','0'),(83,'0','1','0','Post_Quals','Year_5'),(84,'0','1','0','0','0'),(85,'0','1','0','0','0'),(86,'0','1','0','0','0'),(87,'0','1','0','0','0'),(88,'0','1','0','0','0'),(89,'0','1','0','Post_Generals','Year_5'),(90,'0','1','0','0','0'),(92,'0','1','0','Post_Generals','Year_5'),(94,'0','1','0','Pre_Quals','Year_1'),(96,'0','1','0','Post_Generals','Year_5'),(98,'1','0','Faculty','0','0'),(99,'0','1','0','Post_Quals','Year_2'),(100,'0','1','0','Post_Quals','Year_5'),(101,'1','0','Faculty','0','0'),(102,'0','1','0','0','0'),(103,'1','0','Faculty_aff','0','0'),(104,'1','0','Faculty','0','0'),(105,'0','1','0','0','0'),(107,'1','0','Faculty','0','0'),(108,'0','1','0','0','0'),(111,'1','0','Faculty_adj','0','0'),(113,'0','1','0','Post_Generals','Year_4'),(115,'1','0','Faculty','0','0'),(116,'0','1','0','Pre_Quals','Year_3'),(118,'0','1','0','Post_Generals','Year_4'),(119,'0','1','0','0','0'),(122,'0','1','0','Post_Quals','Year_4'),(123,'0','1','0','0','0'),(124,'1','0','Faculty','0','0'),(125,'0','1','0','0','0'),(126,'0','1','0','Post_Quals','Year_5'),(129,'0','1','0','Post_Generals','Year_6'),(130,'0','1','0','Post_Generals','Year_8'),(131,'0','1','0','0','0'),(138,'0','1','0','0','0'),(139,'0','1','0','Post_Quals','Year_3'),(140,'0','1','0','0','0'),(141,'0','1','0','Post_Generals','Year_6'),(142,'0','1','0','Post_Generals','Year_9'),(144,'0','1','0','0','0'),(146,'0','1','0','0','0'),(148,'0','1','0','Post_Quals','Year_5'),(149,'0','1','0','Post_Quals','Year_5'),(150,'1','0','Faculty','0','0'),(154,'0','1','0','Post_Quals','Year_4'),(155,'0','1','0','Pre_Quals','Year_2'),(157,'0','1','0','Post_Quals','Year_4'),(158,'0','1','0','0','0'),(159,'0','1','0','Post_Quals','Year_2'),(161,'0','1','0','Post_Generals','Year_7'),(163,'0','1','0','Post_Quals','Year_4'),(165,'1','0','Faculty','0','0'),(166,'1','0','0','0','0'),(167,'0','1','0','0','0'),(168,'1','0','Faculty','0','0'),(171,'1','0','Faculty','0','0'),(172,'0','1','0','Pre_Quals','Year_1'),(175,'0','1','0','Post_Generals','Year_2'),(176,'0','1','0','Post_Quals','Year_2'),(178,'0','1','0','0','0'),(179,'1','0','Faculty','0','0'),(180,'1','0','Faculty','0','0'),(181,'1','0','0','0','0'),(182,'0','1','0','Post_Quals','Year_3'),(183,'0','1','0','Pre_Quals','Year_4'),(185,'1','0','Faculty_adj','0','0'),(186,'0','1','0','Pre_Quals','Year_1'),(187,'0','1','0','Pre_Quals','Year_1'),(188,'0','1','0','0','0'),(189,'1','0','Faculty_adj','0','0'),(190,'0','1','0','0','0'),(191,'0','1','0','Post_Quals','Year_4'),(193,'0','1','0','Pre_Quals','Year_1'),(195,'0','1','0','0','0'),(198,'0','1','0','0','0'),(200,'0','1','0','Post_Quals','Year_4'),(201,'1','0','Faculty','0','0'),(203,'0','1','0','0','0'),(204,'0','1','0','Post_Generals','Year_6'),(205,'0','1','0','Pre_Quals','Year_1'),(206,'0','1','0','Post_Generals','Year_6'),(207,'0','1','0','0','0'),(208,'0','1','0','Post_Quals','Year_4'),(211,'1','0','Faculty','0','0'),(212,'0','1','0','Post_Generals','Year_7'),(213,'1','0','Faculty','0','0'),(214,'0','1','0','0','0'),(217,'0','1','0','Post_Generals','Year_5'),(218,'0','1','0','Post_Generals','Year_12'),(222,'0','1','0','Pre_Quals','Year_1'),(223,'0','1','0','0','0'),(226,'0','1','0','Post_Quals','Year_4'),(228,'0','1','0','Post_Quals','Year_3'),(230,'0','1','0','0','0'),(231,'1','0','0','0','0'),(232,'0','1','0','0','0'),(233,'0','1','0','Pre_Quals','Year_1'),(234,'1','0','Faculty','0','0'),(235,'1','0','Faculty','0','0'),(237,'0','1','0','0','0'),(239,'0','1','0','Post_Quals','Year_4'),(240,'1','0','Faculty','0','0'),(241,'0','1','0','Post_Quals','Year_3'),(242,'0','1','0','Post_Generals','Year_5'),(248,'1','0','0','0','0'),(249,'0','1','0','Post_Generals','Year_7'),(253,'0','1','0','Post_Generals','Year_5'),(255,'0','1','0','Post_Generals','Year_5'),(257,'0','1','0','Post_Generals','Year_7'),(258,'0','1','0','0','0'),(259,'0','1','0','0','0'),(261,'0','1','0','0','0'),(262,'0','1','0','Post_Generals','Year_7'),(263,'0','1','0','Post_Generals','Year_6'),(265,'0','1','0','Post_Generals','Year_9'),(266,'0','1','0','Post_Quals','Year_5'),(267,'1','0','0','0','0'),(269,'0','1','0','0','0'),(270,'0','1','0','Pre_Quals','Year_1'),(271,'0','1','0','0','0'),(272,'0','1','0','Post_Quals','Year_2'),(274,'0','1','0','0','0'),(275,'0','1','0','Post_Generals','Year_5'),(276,'0','1','0','Pre_Quals','Year_3'),(277,'0','1','0','Pre_Quals','Year_1'),(278,'0','1','0','Pre_Quals','Year_2'),(279,'1','0','Faculty','0','0'),(280,'0','1','0','Pre_Quals','Year_3'),(283,'0','1','0','Pre_Quals','Year_1'),(284,'0','1','0','Post_Quals','Year_3'),(286,'0','1','0','Post_Quals','Year_3'),(287,'0','1','0','0','0'),(288,'0','1','0','Post_Generals','Year_5'),(290,'1','0','Faculty','0','0'),(292,'1','0','Faculty_aff','0','0'),(293,'1','0','Faculty_aff','0','0'),(294,'0','1','0','0','0'),(296,'0','1','0','0','0'),(297,'1','0','Faculty_eme','0','0'),(298,'1','0','Faculty','0','0'),(299,'0','1','0','Pre_Quals','Year_3'),(300,'0','1','0','Post_Generals','Year_8'),(303,'0','1','0','Post_Quals','Year_4'),(306,'0','1','0','0','0'),(309,'0','1','0','Post_Quals','Year_3'),(310,'0','1','0','0','0'),(311,'0','1','0','Post_Quals','Year_3'),(312,'0','1','0','Pre_Quals','Year_4'),(314,'0','1','0','Post_Generals','Year_4'),(315,'0','1','0','0','0'),(317,'0','1','0','0','0'),(318,'0','1','0','Pre_Quals','Year_5'),(319,'1','0','Faculty','0','0'),(320,'0','1','0','Post_Quals','Year_3'),(321,'0','1','0','0','0'),(322,'0','1','0','0','0'),(324,'1','0','Faculty','0','0'),(325,'0','1','0','0','0'),(326,'1','0','0','0','0'),(327,'0','1','0','0','0'),(328,'0','1','0','0','0'),(331,'1','0','Faculty','0','0'),(333,'0','1','0','Pre_Quals','Year_2'),(335,'1','0','Faculty','0','0'),(340,'0','1','0','0','0'),(342,'1','0','Faculty','0','0'),(343,'0','1','0','Pre_Quals','Year_1'),(347,'0','1','0','0','0'),(348,'0','1','0','Post_Quals','Year_3'),(349,'1','0','Faculty_adj','0','0'),(350,'0','1','0','0','0'),(351,'1','0','Faculty','0','0'),(352,'0','1','0','Post_Generals','Year_5'),(353,'0','1','0','Post_Quals','Year_4'),(354,'0','1','0','0','0'),(356,'0','1','0','0','0'),(357,'0','1','0','Post_Quals','Year_4'),(358,'0','1','0','0','0'),(361,'0','1','0','Post_Generals','Year_6'),(362,'0','1','0','Post_Quals','Year_3'),(363,'0','1','0','Pre_Quals','Year_3'),(364,'1','0','0','0','0'),(368,'0','1','0','Post_Generals','Year_4'),(370,'1','0','0','0','0'),(373,'1','0','Faculty','0','0'),(374,'0','1','0','Post_Generals','Year_12'),(375,'1','0','Faculty_eme','0','0'),(376,'0','1','0','Post_Quals','Year_4'),(377,'0','1','0','Pre_Quals','Year_1'),(378,'1','0','Faculty','0','0'),(380,'0','1','0','Post_Generals','Year_6'),(381,'0','1','0','Post_Generals','Year_10'),(382,'0','1','0','Post_Quals','Year_3'),(383,'0','1','0','Pre_Quals','Year_2'),(384,'0','1','0','Post_Quals','Year_3'),(390,'0','1','0','Pre_Quals','Year_2'),(391,'0','1','0','Post_Quals','Year_4'),(392,'0','1','0','0','0'),(393,'1','0','Faculty','0','0'),(394,'1','0','Faculty','0','0'),(397,'0','1','0','0','0'),(398,'0','1','0','Pre_Quals','Year_1'),(400,'0','1','0','0','0'),(401,'0','1','0','0','0'),(402,'0','1','0','Pre_Quals','Year_2'),(403,'0','1','0','Post_Generals','Year_12'),(404,'0','1','0','Post_Generals','Year_4'),(406,'0','1','0','Post_Generals','Year_5'),(407,'1','0','Faculty','0','0'),(408,'0','1','0','Pre_Quals','Year_2'),(410,'0','1','0','0','0'),(411,'0','1','0','Post_Generals','Year_6'),(412,'0','1','0','Post_Quals','Year_3'),(415,'1','0','Faculty','0','0'),(416,'0','1','0','Pre_Quals','Year_1'),(417,'0','1','0','Pre_Quals','Year_1'),(418,'0','1','0','Post_Quals','Year_3'),(419,'0','1','0','Post_Generals','Year_7'),(420,'0','1','0','0','0'),(422,'0','1','0','Post_Quals','Year_3'),(424,'0','1','0','0','0'),(426,'0','1','0','Post_Quals','Year_5'),(427,'0','1','0','Post_Quals','Year_4'),(428,'0','1','0','0','0'),(429,'0','1','0','Post_Quals','Year_5'),(431,'0','1','0','Pre_Quals','Year_2'),(432,'0','1','0','Post_Quals','Year_5'),(435,'0','1','0','Post_Quals','Year_4');
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-20 17:46:39
