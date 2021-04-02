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
INSERT INTO `diningHall` VALUES (1,'Bates','7:30am to 7:30pm',0),(2,'Lulu','7am to 11pm',60),(3,'Pom','7:30am to 7:30pm',2),(4,'Stone-D','7:30am to 7:30pm',10),(5,'Tower','7:30am to 7:30pm',10);
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
INSERT INTO `feedback` VALUES ('@sclark4 your rating is a disgrace, this ice cream will always be 5 star worthy how dare u',5,'asypeck',95,'2021-03-31 21:38:27'),('I wish this was vegetarian.',3,'fx1',79,'2021-03-28 21:15:21'),('filling but not very flavorful',4,'ggabeau',1,'2021-03-29 20:54:42'),('soooo  goood',5,'ggabeau',7,'2021-03-28 13:25:53'),('yummmm',5,'ggabeau',11,'2021-03-28 13:21:21'),('can\'t tell if it\'s because its tofu or if its because it was prepared poorly but either way not great :/',2,'ggabeau',17,'2021-04-01 21:57:01'),('yes',5,'ggabeau',55,'2021-03-28 20:22:01'),('We want s\'more!!!',5,'ggabeau',95,'2021-03-29 21:30:32'),('Excellent with hot sauce',4,'sanderso',136,'2021-04-01 14:26:55'),('Taco Tuesday at Lulu was great! The cilantro crema was weirdly sweet though.',4,'sclark4',1,'2021-03-20 13:56:00'),('The croissant sandwich is ok, but I wish the fried eggs were not cooked so hard',3,'sclark4',2,'2021-03-20 13:56:00'),('Reminds me of panera',4,'sclark4',8,'2021-03-26 10:32:15'),('Ye Ole Reliable breakfast burrito-- I can always count on having an adequate breakfast when I see this on the menu.',3,'sclark4',9,'2021-03-25 20:29:27'),('I would travel cross campus in moderately-bad weather to eat this salmon.',4,'sclark4',18,'2021-03-22 19:40:11'),('Literally so good, I\'m obsessed with this dish!',5,'sclark4',31,'2021-03-22 19:35:34'),('It\'s the simple things in life that make your day... surprise waffle sundaes in Lulu made my week!',5,'sclark4',34,'2021-03-31 16:32:01'),('Why are we putting crunchy vegetables on pizza again? It hurts me.',2,'sclark4',36,'2021-03-26 11:15:43'),('I love a classic bean dish done well... and this one is impressive despite the appearance– highly recommend!',4,'sclark4',39,'2021-03-26 13:09:50'),('Not a fan.',2,'sclark4',55,'2021-03-28 17:00:41'),('This is the absolute best soup when you\'re feeling under the weather!',4,'sclark4',56,'2021-03-28 17:01:24'),('I can\'t remember the last time I had red meat that wasn\'t dry... this reminded me of what meat is supposed to taste like.',5,'sclark4',79,'2021-03-28 20:42:40'),('Man I never thought I would appreciate an untoasted bagel this much but wow 10/10 would recommend. #BringBackBreakfastBreads',4,'sclark4',80,'2021-03-29 19:39:29'),('After Lulu\'s Indian Spiced Meatballs last week, my expectations were high. But if I\'m being honest, Tower just didn\'t measure up. Amazing effort, but by comparison, these felt just ok.',3,'sclark4',81,'2021-03-29 19:41:20'),('I\'m a huge fan of eggplant... covered in cheese... how can I resist?',4,'sclark4',84,'2021-03-29 19:53:53'),('Cloudy with a chance of a great dinner!',4,'sclark4',85,'2021-03-29 20:27:17'),('Hot take: Graham Central is only top tier ice cream when it feels rare.',4,'sclark4',95,'2021-03-31 16:45:37'),('So creamy! ',4,'sclark4',134,'2021-03-31 16:18:39'),('One of my favorite breakfasts! I dare you to try it with hot sauce and honey on top ;)',5,'sclark4',136,'2021-04-01 13:10:08');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food`
--

DROP TABLE IF EXISTS `food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `food` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `lastServed` date DEFAULT NULL,
  `type` set('breakfast','lunch','dinner','all day') DEFAULT NULL,
  `did` int(11) DEFAULT NULL,
  PRIMARY KEY (`fid`),
  KEY `did` (`did`),
  CONSTRAINT `food_ibfk_1` FOREIGN KEY (`did`) REFERENCES `diningHall` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food`
--

LOCK TABLES `food` WRITE;
/*!40000 ALTER TABLE `food` DISABLE KEYS */;
INSERT INTO `food` VALUES (1,'Taco Bowl','2021-03-29','lunch',2),(2,'Egg Sandwich','2021-03-31','breakfast',5),(4,'Split Pea & Ham Soup','2021-03-01','lunch',1),(5,'Hawaiian Pizza','2021-03-02','lunch',1),(6,'Chicken California Club','2021-03-13','lunch',1),(7,'Garlic Breadsticks','2021-03-13','lunch',1),(8,'Broccoli and Cheddar Soup','2021-03-15','lunch',1),(9,'Breakfast Burrito','2021-03-31','lunch',2),(10,'Cream of Mushroom Soup','2021-03-19','lunch',1),(11,'Apple Cinnamon Pancakes','2021-03-19','breakfast',1),(12,'Funfetti Cake','2021-03-19','all day',3),(14,'Chicken Alfredo','2021-03-19','dinner',2),(15,'Yogurt Parfait','2021-04-01','lunch',2),(16,'cinnamon roll','2021-03-19','all day',1),(17,'Scrambled Tofu','2021-04-01','breakfast',1),(18,'Miso-Glazed Salmon','2021-03-19','dinner',1),(19,'Vegan Cheese Tomato & Basil Pizza','2021-04-01','lunch',5),(20,'Chocolate-Chip Cookie','2021-03-31','all day',2),(21,'Roasted Butternut Squash','2021-03-19','lunch',1),(22,'Lentil and Sausage Soup','2021-03-19','lunch',1),(23,'Tofu Gyro Bowl','2021-03-19','lunch',2),(24,'Chicken Noodle Soup','2021-03-19','dinner',1),(25,'Beignet','2021-03-19','breakfast',1),(27,'Pork Sausage','2021-04-01','lunch',1),(28,'Coconut Lentil Soup','2021-03-19','lunch',1),(29,'Raisin French Toast','2021-03-19','lunch',1),(30,'Tomato Soup','2021-03-19','lunch',1),(31,'Saag Paneer','2021-03-19','lunch',2),(32,'Garam Masala Eggplant','2021-03-19','lunch',2),(33,'Chana Masala','2021-03-31','lunch',2),(34,'Waffle Sundae','2021-03-19','dinner',2),(35,'Chicken California Club','2021-03-19','all day',5),(36,'BLT Pizza','2021-03-26','lunch',5),(37,'Tuna Melts','2021-03-26','lunch',1),(39,'White Bean Cassoulet','2021-03-26','lunch',2),(40,'Turkey Tortilla Soup','2021-03-27','lunch',2),(41,'Turkey Ranch Pita','2021-03-27','lunch',2),(44,'Philly Cheesesteak Pizza','2021-03-27','lunch',2),(55,'Pasta Fagioli Soup','2021-03-28','lunch',1),(56,'Carrot & Ginger Soup','2021-03-28','lunch',5),(79,'London Broil','2021-03-28','dinner',2),(80,'Everything Bagel','2021-03-29','breakfast',2),(81,'Indian Spiced Meatballs','2021-03-29','lunch',5),(83,'Shrimp Scampi','2021-03-29','dinner',5),(84,'Eggplant Parmesan','2021-03-29','dinner',5),(85,'Meatball Sub','2021-03-31','dinner',1),(86,'Sesame Hoisin Crispy Chicken Legs','2021-03-29','dinner',1),(93,'Pita Chips and Hummus','2021-03-29','all day',2),(95,'Graham Central Station','2021-03-31','all day',5),(121,'Herb Roasted Plum Tomatoes','2021-03-30','dinner',2),(134,'Chicken Tikka Masala','2021-03-31','lunch',5),(136,'Croissant Egg Sandwich','2021-04-01','breakfast',2),(137,'egg salad','2021-04-01','lunch',2);
/*!40000 ALTER TABLE `food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `foodPics`
--

DROP TABLE IF EXISTS `foodPics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `foodPics` (
  `fid` int(11) NOT NULL DEFAULT '0',
  `filename` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`fid`),
  CONSTRAINT `foodPics_ibfk_1` FOREIGN KEY (`fid`) REFERENCES `food` (`fid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foodPics`
--

LOCK TABLES `foodPics` WRITE;
/*!40000 ALTER TABLE `foodPics` DISABLE KEYS */;
INSERT INTO `foodPics` VALUES (1,'1.JPG'),(7,'7.jpeg'),(9,'9'),(11,'11.jpg'),(15,'15.jpg'),(79,'79.jpg'),(81,'81.JPG'),(83,'83.JPG'),(84,'84.JPG');
/*!40000 ALTER TABLE `foodPics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labels`
--

DROP TABLE IF EXISTS `labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labels` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `allergen` set('none','eggs','fish','milk','peanuts','shellfish','soy','tree nut','wheat') DEFAULT NULL,
  `preference` set('none','gluten sensitive','vegan','vegetarian','kosher','halal') DEFAULT NULL,
  `ingredients` varchar(80) DEFAULT NULL,
  `fid` int(11) DEFAULT NULL,
  PRIMARY KEY (`lid`),
  KEY `fid` (`fid`),
  CONSTRAINT `labels_ibfk_1` FOREIGN KEY (`fid`) REFERENCES `food` (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labels`
--

LOCK TABLES `labels` WRITE;
/*!40000 ALTER TABLE `labels` DISABLE KEYS */;
INSERT INTO `labels` VALUES (2,'eggs,milk,wheat','none','none',2),(3,'none','vegan','avocado, tomato, onion, chicken (optional)',1),(11,'fish','none','salmon,miso,herbs',18),(12,'none','vegan','tomato,basil',19),(13,'eggs','none','chocolate',20),(14,'milk','none','mushroom, noodles',10),(15,'wheat','none','apples',11),(17,'milk','none','chicken,pasta,cheese',14),(18,'milk','vegetarian','strawberry or plain greek yogurt with granola',15),(19,'eggs','vegetarian','egg,cream-cheese frosting, cinnamon sugar',16),(20,'soy','vegan','tofu,herbs',17),(21,'fish','none','salmon,soy',18),(22,'none','vegan','tomato,herbs',19),(23,'eggs','vegetarian','eggs,chocolate',20),(24,'eggs','none','eggs,bacon,sausage',9),(25,'eggs','none','eggs,sprinkles,icing,flour',12),(26,'none','none','peas,ham,black pepper',4),(27,'milk,wheat','none','pineapple,cheese,tomato',5),(28,'milk,wheat','none','chicken',6),(29,'milk,soy,wheat','vegetarian','flour,garlic,butter',7),(30,'milk,soy,wheat','none','broccoli',8),(31,'soy','vegetarian','butternut squash, olive oil',21),(32,'soy','gluten sensitive','lentil,sausage',22),(33,'milk','vegetarian','tofu',23),(34,'wheat','none','chicken,carrots',24),(35,'eggs','none','eggs,flour,powdered sugar',25),(37,'none','gluten sensitive','pork',27),(38,'milk','vegetarian','coconut, milk, lentils',28),(39,'eggs','vegetarian','raisins,eggs',29),(40,'wheat','vegan','tomatoes',30),(41,'milk','vegetarian','spinach, paneer',31),(42,'none','vegan','eggplant',32),(43,'none','vegetarian','chickpeas, onions',33),(44,'milk','vegetarian','ice cream, whipped cream, hot fudge, strawberries',34),(45,'wheat','none','turkey bacon, avocado, chicken',6),(46,'milk','none','Bacon, lettuce, tomato',36),(47,'milk','none','tuna,cheese',37),(48,'eggs','none','tuna,cheese',37),(49,'none','vegetarian','white beans, potato, tomatoes',39),(50,'milk','gluten sensitive','turkey,corn',40),(51,'milk','none','turkey,wheat',41),(52,'wheat','none','beef,cheese',44),(60,'wheat','vegan,vegetarian','pasta',55),(84,'','gluten sensitive','steak, gravy',79),(85,'wheat','vegetarian','Bagel, cream cheese',80),(86,'eggs,milk,soy,wheat','none','tamarind sauce, meatballs',81),(88,'shellfish,wheat','none','shrimp, pasta',83),(89,'eggs,wheat','vegetarian','mozzerella, eggplant, breading, parmesan',84),(90,'eggs,milk,wheat','none','bread, mozzerella, tomato sauce, beef',85),(91,'soy,wheat','none','chicken, sesame oil, hoisin sauce',86),(98,'wheat','vegan','chips, hummus',93),(100,'milk','vegetarian','ice cream ',95),(126,'none','vegan,vegetarian','tomatoes',121),(139,'milk','none','chicken, greek yogurt, tomatoes',134),(140,'milk','none','chicken',134),(141,'eggs,milk,wheat','none','croissant, cheese, fried egg, turkey sausage',136),(142,'eggs','vegetarian','egg, mayo, bread, celery',137);
/*!40000 ALTER TABLE `labels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proPics`
--

DROP TABLE IF EXISTS `proPics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proPics` (
  `username` varchar(225) NOT NULL DEFAULT '',
  `filename` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`username`),
  CONSTRAINT `proPics_ibfk_1` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proPics`
--

LOCK TABLES `proPics` WRITE;
/*!40000 ALTER TABLE `proPics` DISABLE KEYS */;
INSERT INTO `proPics` VALUES ('admin','admin.jpeg'),('asypeck','asypeck.jpg'),('ggabeau','ggabeau.jpg'),('ggabeau3','ggabeau3.jpg'),('ggabeau4','ggabeau4.jpg'),('sanderso','sanderso.jpg'),('sclark4','sclark4.jpg');
/*!40000 ALTER TABLE `proPics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `username` varchar(15) NOT NULL,
  `password` varchar(30) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `classYear` enum('2021','2022','2023','2024','Davis Scholar') DEFAULT NULL,
  `favoriteDH` int(11) DEFAULT NULL,
  `hashed` varchar(225) DEFAULT NULL,
  `favoriteFood` varchar(225) DEFAULT NULL,
  `allergies` varchar(225) DEFAULT NULL,
  `preferences` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `favoriteDH` (`favoriteDH`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`favoriteDH`) REFERENCES `diningHall` (`did`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('admin','soYummy!','Administrator','2021',1,'$2b$12$zMTmxGXf5IBeKkPZ2EVyb.psMH7bBWWtkf9Esd15JbcmCalnK7M9q','i don\'t eat food','eggs, fish, milk, peanuts, shellfish, soy, tree nut, wheat','gluten sensitive, vegan, vegetarian, kosher, halal'),('asypeck','NONE','Adrienne Sypeck','2021',1,'NONE','mac & cheese','none','none'),('cw4','spring','Catherine Wang','2023',2,NULL,NULL,NULL,NULL),('fx1','123','Fangwen Xia','2023',5,NULL,NULL,NULL,NULL),('ggabeau','123','Gigi Gabeau','2021',1,'$2b$12$5HkL6bRp.kBPZnKsTj7JiOyA7NpCHAFXvHZ18hA9W1GRpD7MHh.de','mac & cheese','none','none'),('ggabeau2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('ggabeau3','123','bloop','2021',1,'$2b$12$bJ6fQ/uiQrmNDIs7LaRvCuB77U6uouW5Q3eSMG5bKgqU3PzvOEbQW','beep','none','none'),('ggabeau4','123','Lil Nas X','2021',2,'$2b$12$4Bkww5lraDqUGY2flcIVKudpBrwwPvaeD6qt8sUNqpY/cpF1BR5oa','montero','none','none'),('ggabeau99',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('lteffera','123','Leah Teffera','2022',1,NULL,'Taco Bowl','',''),('sanderso',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('sclark4','123','Sara Clark','2022',2,NULL,'chickpeas','none','none'),('scott','scott','Scott Anderson','Davis Scholar',4,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2021-04-02  2:48:27
