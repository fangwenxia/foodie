-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: foodie_db
-- ------------------------------------------------------
-- Server version	5.5.68-MariaDB

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
-- Table structure for table `diningHall`
--

DROP TABLE IF EXISTS `diningHall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diningHall` (
  `did` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `hours` varchar(40) DEFAULT NULL,
  `waitTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diningHall`
--

LOCK TABLES `diningHall` WRITE;
/*!40000 ALTER TABLE `diningHall` DISABLE KEYS */;
INSERT INTO `diningHall` VALUES (1,'Bates','7:30am to 7:30pm',0),(2,'Lulu','7am to 11pm',5),(3,'Pom','7:30am to 7:30pm',2),(4,'Stone-D','7:30am to 7:30pm',10),(5,'Tower','7:30am to 7:30pm',15);
/*!40000 ALTER TABLE `diningHall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `comment` varchar(280) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `username` varchar(15) NOT NULL DEFAULT '',
  `fid` int(11) NOT NULL DEFAULT '0',
  `entered` datetime DEFAULT NULL,
  PRIMARY KEY (`username`,`fid`),
  KEY `fid` (`fid`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`username`) REFERENCES `student` (`username`),
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`fid`) REFERENCES `food` (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES ('Great!',5,'fx1',3,'2021-03-19 11:51:25'),('Really delicious–the croissant was extra buttery. 10/10 would eat again',5,'lteffera',1001,'2021-03-10 09:13:55'),('The wrap was ok–a little soggy though.',3,'lteffera',1002,'2021-03-16 13:01:43'),('The flavor combo worked for me!! Oddly enough this tasted really good with mashed potatoes. My only complaint was that the fish was too salty.',4,'lteffera',1003,'2021-03-12 18:00:01'),('Pretty good! I wish the bacon was a little crunchier though.',4,'lteffera',1004,'2021-03-14 10:00:01'),('Really soggy pizza–did not approve.',2,'lteffera',1005,'2021-03-16 12:36:56'),('Taco Tuesday at Lulu was great! The cilantro crema was weirdly sweet though.',4,'sclark4',1,'2021-03-18 17:49:38'),('The croissant sandwich is ok, but I wish the fried eggs were not cooked so hard',3,'sclark4',2,'2021-03-18 17:49:38');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food`
--

DROP TABLE IF EXISTS `food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `food` (
  `fid` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `lastServed` date DEFAULT NULL,
  `type` set('breakfast','lunch','dinner','all day') DEFAULT NULL,
  `did` int(11) DEFAULT NULL,
  PRIMARY KEY (`fid`),
  KEY `did` (`did`),
  CONSTRAINT `food_ibfk_1` FOREIGN KEY (`did`) REFERENCES `diningHall` (`did`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food`
--

LOCK TABLES `food` WRITE;
/*!40000 ALTER TABLE `food` DISABLE KEYS */;
INSERT INTO `food` VALUES (0,'Italian Wedding Soup','0000-00-00','lunch',2),(1,'Taco Bowl','2021-03-02','lunch',2),(2,'Egg Sandwich','2021-03-02','breakfast',5),(3,'Beef Stroganoff','2020-04-18','lunch',5),(1001,'Ham Egg & Cheese Croissant','2021-03-10','breakfast',1),(1002,'Caprese Wrap','2021-03-16','lunch',2),(1003,'Miso-Glazed Salmon','2021-03-12','dinner',5),(1004,'Bacon Egg & Cheese on English ','2021-03-14','breakfast',5),(1005,'Vegan Cheese Tomato & Basil Pi','2021-03-16','lunch',5);
/*!40000 ALTER TABLE `food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labels`
--

DROP TABLE IF EXISTS `labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labels` (
  `lid` int(11) NOT NULL,
  `allergen` set('none','eggs','fish','milk','peanuts','shellfish','soy','tree nut','wheat') DEFAULT NULL,
  `preference` set('none','gluten sensitive','vegan','vegetarian','kosher','halal') DEFAULT NULL,
  `ingredients` varchar(80) DEFAULT NULL,
  `fid` int(11) DEFAULT NULL,
  PRIMARY KEY (`lid`),
  KEY `fid` (`fid`),
  CONSTRAINT `labels_ibfk_1` FOREIGN KEY (`fid`) REFERENCES `food` (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labels`
--

LOCK TABLES `labels` WRITE;
/*!40000 ALTER TABLE `labels` DISABLE KEYS */;
INSERT INTO `labels` VALUES (1,'eggs,milk,wheat','','none',2),(2,'none','vegan','guacamole, beans, rice, tofu',1),(3,'wheat','none','egg noodles',3),(398,'eggs','','pork',1001),(399,'milk','vegetarian','cheese',1002),(400,'fish','gluten sensitive','soy',1003),(401,'eggs','','wheat',1004),(402,'wheat','vegan','tomato',1005);
/*!40000 ALTER TABLE `labels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passwords`
--

DROP TABLE IF EXISTS `passwords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passwords` (
  `username` varchar(225) DEFAULT NULL,
  `password` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passwords`
--

LOCK TABLES `passwords` WRITE;
/*!40000 ALTER TABLE `passwords` DISABLE KEYS */;
INSERT INTO `passwords` VALUES ('ggabeau','123'),('fx1','123'),('lteffera','123'),('sclark4','123'),('ggabeau2','111'),('',''),('bobby','bob'),('jill','jill');
/*!40000 ALTER TABLE `passwords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `username` varchar(15) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `favoriteDH` int(11) DEFAULT NULL,
  `favoriteFood` int(11) DEFAULT NULL,
  `classYear` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `favoriteDH` (`favoriteDH`),
  KEY `favoriteFood` (`favoriteFood`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`favoriteDH`) REFERENCES `diningHall` (`did`),
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`favoriteFood`) REFERENCES `food` (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('','',NULL,NULL,NULL),('bobby','bob',NULL,NULL,NULL),('fx1','Fangwen Xia',5,3,'2023'),('ggabeau','Gigi Gabeau',1,1,'2021'),('ggabeau2','Gigi2',NULL,NULL,NULL),('jill','jack',NULL,NULL,NULL),('lteffera','Leah Teffera',1,1001,'2022'),('sclark4','Sara Clark',2,1,'2022');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-19 22:16:49
