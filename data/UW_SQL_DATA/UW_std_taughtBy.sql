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
-- Table structure for table `taughtBy`
--

DROP TABLE IF EXISTS `taughtBy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `taughtBy` (
  `course_id` int NOT NULL DEFAULT '0',
  `p_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`course_id`,`p_id`),
  KEY `FK_2` (`course_id`),
  KEY `FK_1` (`p_id`),
  CONSTRAINT `FK_taught_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_taught_person` FOREIGN KEY (`p_id`) REFERENCES `person` (`p_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taughtBy`
--

LOCK TABLES `taughtBy` WRITE;
/*!40000 ALTER TABLE `taughtBy` DISABLE KEYS */;
INSERT INTO `taughtBy` VALUES (0,40),(1,40),(2,180),(3,279),(4,107),(7,415),(8,297),(9,235),(11,52),(11,57),(11,298),(11,324),(11,331),(12,79),(12,211),(12,407),(13,72),(13,342),(14,124),(15,292),(16,79),(16,240),(18,107),(18,213),(18,290),(18,326),(18,373),(18,375),(19,5),(19,370),(20,180),(21,22),(21,99),(23,179),(24,79),(24,150),(24,211),(24,240),(24,407),(27,165),(27,331),(28,394),(29,298),(30,290),(32,319),(34,179),(36,181),(38,104),(38,124),(38,204),(38,255),(39,415),(40,165),(40,298),(40,378),(41,351),(44,171),(44,293),(44,415),(46,335),(48,107),(48,213),(48,375),(49,64),(49,189),(49,248),(49,263),(50,171),(51,5),(51,18),(51,166),(52,168),(53,189),(53,248),(57,150),(61,107),(62,101),(63,335),(64,79),(66,165),(66,298),(67,394),(68,201),(68,324),(68,331),(71,5),(74,104),(74,124),(75,267),(76,319),(77,52),(77,165),(77,324),(79,72),(80,98),(80,101),(80,180),(82,407),(84,324),(88,235),(89,394),(91,331),(93,351),(97,324),(98,103),(101,279),(101,394),(103,201),(104,165),(104,181),(104,364),(108,279),(110,351),(115,72),(115,342),(116,375),(117,181),(118,351),(119,324),(120,82),(120,235),(121,52),(122,378),(123,150),(124,9),(124,46),(124,335),(125,351),(126,165),(128,150),(129,213),(129,373),(132,319),(134,240),(136,394),(137,165),(138,335),(139,235),(141,150),(143,211),(143,407),(144,278),(144,331),(146,335),(147,52),(147,57),(147,165),(147,201),(147,324),(147,331),(147,364),(148,351),(149,331),(150,351),(151,82),(151,179),(151,234),(151,235),(151,267),(151,290),(153,342),(153,394),(156,240),(157,72),(157,342),(157,394),(158,240),(159,394),(160,331),(161,201),(161,298),(161,331),(162,213),(164,351),(165,75),(165,141),(165,181),(165,231),(165,364),(166,235),(167,98),(168,240),(170,79),(170,211),(170,407),(172,46),(172,335),(173,171),(174,267);
/*!40000 ALTER TABLE `taughtBy` ENABLE KEYS */;
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

-- Dump completed on 2024-11-20 17:46:44