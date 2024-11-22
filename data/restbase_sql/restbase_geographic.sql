-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: db.relational-data.org    Database: restbase
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
-- Table structure for table `geographic`
--

DROP TABLE IF EXISTS `geographic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `geographic` (
  `city` varchar(255) NOT NULL,
  `county` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `geographic`
--

LOCK TABLES `geographic` WRITE;
/*!40000 ALTER TABLE `geographic` DISABLE KEYS */;
INSERT INTO `geographic` VALUES ('alameda','alameda county','bay area'),('alamo','contra costa county','bay area'),('albany','alameda county','bay area'),('alviso','santa clara county','bay area'),('american canyon','unknown','bay area'),('angwin','napa county','napa valley'),('antioch','contra costa county','bay area'),('aptos','santa cruz county','bay area'),('aromas','unknown','unknown'),('atherton','san mateo county','bay area'),('banta','unknown','unknown'),('belmont','san mateo county','bay area'),('belvedere tiburon','marin county','bay area'),('ben lomond','santa cruz county','bay area'),('benicia','solano county','bay area'),('berkeley','alameda county','bay area'),('bethel island','unknown','unknown'),('big sur','monterey county','monterey'),('bodega bay','sonoma county','bay area'),('boulder creek','santa cruz county','bay area'),('brentwood','contra costa county','bay area'),('brisbane','san mateo county','bay area'),('burlingame','san mateo county','bay area'),('byron','unknown','bay area'),('calistoga','napa county','napa valley'),('campbell','santa clara county','bay area'),('capitola','unknown','bay area'),('carmel','monterey county','monterey'),('castro valley','alameda county','bay area'),('castroville','monterey county','monterey'),('cerritos','los angeles county','los angeles area'),('charlotte','unknown','unknown'),('clayton','contra costa county','bay area'),('colma','san mateo county','bay area'),('columbia','tuolumne county','yosemite and mono lake area'),('concord','contra costa county','bay area'),('corte madera','marin county','bay area'),('cotati','sonoma county','bay area'),('crockett','unknown','bay area'),('cupertino','santa clara county','bay area'),('daly city','san mateo county','bay area'),('danville','contra costa county','bay area'),('davenport','santa cruz county','bay area'),('davis','yolo county','sacramento area'),('dixon','solano county','bay area'),('dublin','alameda county','bay area'),('eagan','unknown','unknown'),('east palo alto','san mateo county','bay area'),('el cerrito','contra costa county','bay area'),('el granada','san mateo county','bay area'),('el sobrante','contra costa county','bay area'),('emeryville','alameda county','bay area'),('fairfield','solano county','bay area'),('felton','unknown','bay area'),('forestville','sonoma county','bay area'),('fort bragg','mendocino county','northern california'),('foster city','san mateo county','bay area'),('freedom','unknown','unknown'),('fremont','alameda county','bay area'),('gilroy','santa clara county','bay area'),('glen ellen','sonoma county','bay area'),('grass valley','unknown','unknown'),('half moon bay','san mateo county','bay area'),('hayward','alameda county','bay area'),('healdsburg','sonoma county','bay area'),('hercules','contra costa county','bay area'),('hollister','san benito county','northern california'),('inverness','marin county','bay area'),('jenner','sonoma county','bay area'),('kensington','unknown','bay area'),('kenwood','sonoma county','bay area'),('la honda','san mateo county','bay area'),('lafayette','contra costa county','bay area'),('larkspur','marin county','bay area'),('livermore','alameda county','bay area'),('los altos','santa clara county','bay area'),('los gatos','santa clara county','bay area'),('mammoth lakes','unknown','yosemite and mono lake area'),('mare island','unknown','unknown'),('marietta','unknown','unknown'),('marina','monterey county','monterey'),('martinez','contra costa county','bay area'),('menlo park','san mateo county','bay area'),('mill valley','marin county','bay area'),('millbrae','san mateo county','bay area'),('milpitas','santa clara county','bay area'),('montara','san mateo county','bay area'),('monte vista','unknown','unknown'),('monterey','monterey county','monterey'),('moraga','unknown','bay area'),('morgan hill','santa clara county','bay area'),('moss beach','san mateo county','bay area'),('moss landing','monterey county','monterey'),('mountain view','santa clara county','bay area'),('napa','napa county','napa valley'),('newark','alameda county','bay area'),('novato','marin county','bay area'),('oakland','alameda county','bay area'),('oakley','contra costa county','bay area'),('oakville','napa county','napa valley'),('orinda','contra costa county','bay area'),('pacheco','unknown','unknown'),('pacific grove','monterey county','monterey'),('pacifica','san mateo county','bay area'),('palo alto','santa clara county','bay area'),('pengrove','sonoma county','bay area'),('pescadero','san mateo county','bay area'),('petaluma','sonoma county','bay area'),('piedmont','alameda county','bay area'),('pinole','contra costa county','bay area'),('pittsburg','contra costa county','bay area'),('pleasant hill','contra costa county','bay area'),('pleasanton','alameda county','bay area'),('port costa','unknown','unknown'),('portola valley','san mateo county','bay area'),('redwood city','san mateo county','bay area'),('richmond','contra costa county','bay area'),('rio del mar','unknown','unknown'),('rio vista','solano county','bay area'),('rodeo','unknown','unknown'),('rohnert park','sonoma county','bay area'),('rutherford','napa county','napa valley'),('saint helena','napa county','napa valley'),('salinas','monterey county','monterey'),('san anselmo','marin county','bay area'),('san bruno','san mateo county','bay area'),('san carlos','san mateo county','bay area'),('san francisco','san francisco county','bay area'),('san jose','santa clara county','bay area'),('san juan bautista','san benito county','northern california'),('san leandro','alameda county','bay area'),('san lorenzo','alameda county','bay area'),('san martin','santa clara county','bay area'),('san mateo','san mateo county','bay area'),('san pablo','contra costa county','bay area'),('san rafael','marin county','bay area'),('san ramon','contra costa county','bay area'),('santa clara','santa clara county','bay area'),('santa cruz','santa cruz county','bay area'),('santa rosa','sonoma county','bay area'),('saratoga','santa clara county','bay area'),('sausalito','unknown','bay area'),('scotts valley','unknown','bay area'),('seaside','monterey county','monterey'),('sebastopol','sonoma county','bay area'),('sonoma','sonoma county','bay area'),('sonora','tuolumne county','yosemite and mono lake area'),('soquel','unknown','bay area'),('south lake tahoe','el dorado county','lake tahoe'),('south san francisco','san mateo county','bay area'),('suisun city','solano county','bay area'),('sunnyvale','santa clara county','bay area'),('tahoe city','placer county','lake tahoe'),('tahoe vista','placer county','lake tahoe'),('tiburon','marin county','bay area'),('tracy','san joaquin county','unknown'),('tres pinos','unknown','unknown'),('ukiah','mendocino county','northern california'),('union city','alameda county','bay area'),('vacaville','solano county','bay area'),('vallejo','solano county','bay area'),('vancouver','unknown','unknown'),('walnut creek','contra costa county','bay area'),('watsonville','santa cruz county','bay area'),('west pittsburg','contra costa county','bay area'),('winters','yolo county','sacramento area'),('woodside','san mateo county','bay area'),('yountville','napa county','napa valley');
/*!40000 ALTER TABLE `geographic` ENABLE KEYS */;
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

-- Dump completed on 2024-11-21 17:18:31