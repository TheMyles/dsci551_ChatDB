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
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `course_id` int NOT NULL,
  `courseLevel` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `course_courseLevel` (`courseLevel`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (5,'Level_300'),(11,'Level_300'),(18,'Level_300'),(104,'Level_300'),(124,'Level_300'),(146,'Level_300'),(147,'Level_300'),(165,'Level_300'),(8,'Level_400'),(20,'Level_400'),(21,'Level_400'),(24,'Level_400'),(27,'Level_400'),(28,'Level_400'),(30,'Level_400'),(38,'Level_400'),(41,'Level_400'),(44,'Level_400'),(45,'Level_400'),(48,'Level_400'),(49,'Level_400'),(51,'Level_400'),(52,'Level_400'),(53,'Level_400'),(57,'Level_400'),(62,'Level_400'),(68,'Level_400'),(75,'Level_400'),(80,'Level_400'),(82,'Level_400'),(89,'Level_400'),(93,'Level_400'),(97,'Level_400'),(107,'Level_400'),(110,'Level_400'),(118,'Level_400'),(122,'Level_400'),(125,'Level_400'),(126,'Level_400'),(128,'Level_400'),(137,'Level_400'),(143,'Level_400'),(148,'Level_400'),(151,'Level_400'),(154,'Level_400'),(157,'Level_400'),(159,'Level_400'),(161,'Level_400'),(164,'Level_400'),(174,'Level_400'),(0,'Level_500'),(1,'Level_500'),(2,'Level_500'),(3,'Level_500'),(4,'Level_500'),(7,'Level_500'),(9,'Level_500'),(12,'Level_500'),(13,'Level_500'),(14,'Level_500'),(15,'Level_500'),(16,'Level_500'),(19,'Level_500'),(23,'Level_500'),(29,'Level_500'),(32,'Level_500'),(34,'Level_500'),(35,'Level_500'),(36,'Level_500'),(39,'Level_500'),(40,'Level_500'),(46,'Level_500'),(50,'Level_500'),(54,'Level_500'),(56,'Level_500'),(61,'Level_500'),(63,'Level_500'),(64,'Level_500'),(65,'Level_500'),(66,'Level_500'),(67,'Level_500'),(71,'Level_500'),(74,'Level_500'),(76,'Level_500'),(77,'Level_500'),(79,'Level_500'),(83,'Level_500'),(84,'Level_500'),(85,'Level_500'),(86,'Level_500'),(87,'Level_500'),(88,'Level_500'),(91,'Level_500'),(98,'Level_500'),(101,'Level_500'),(103,'Level_500'),(108,'Level_500'),(109,'Level_500'),(114,'Level_500'),(115,'Level_500'),(116,'Level_500'),(117,'Level_500'),(119,'Level_500'),(120,'Level_500'),(121,'Level_500'),(123,'Level_500'),(129,'Level_500'),(131,'Level_500'),(132,'Level_500'),(134,'Level_500'),(135,'Level_500'),(136,'Level_500'),(138,'Level_500'),(139,'Level_500'),(141,'Level_500'),(144,'Level_500'),(149,'Level_500'),(150,'Level_500'),(152,'Level_500'),(153,'Level_500'),(155,'Level_500'),(156,'Level_500'),(158,'Level_500'),(160,'Level_500'),(162,'Level_500'),(166,'Level_500'),(167,'Level_500'),(168,'Level_500'),(169,'Level_500'),(170,'Level_500'),(172,'Level_500'),(173,'Level_500');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
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

-- Dump completed on 2024-11-20 17:46:30
