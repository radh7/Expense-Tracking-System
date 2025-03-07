CREATE DATABASE  IF NOT EXISTS `expense_manager` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `expense_manager`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: expense_manager
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `expense_date` date NOT NULL,
  `amount` float NOT NULL,
  `category` varchar(255) NOT NULL,
  `notes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (3,'2025-01-02',50,'Entertainment','Movie tickets'),(4,'2025-01-02',150,'Shopping','New shoes'),(5,'2025-01-03',100,'Food','Dinner at a restaurant'),(11,'2025-01-02',400,'Food','Groceries for the week'),(12,'2025-01-02',80,'Entertainment','Concert tickets'),(13,'2025-01-02',100,'Shopping','Clothes'),(14,'2025-01-02',50,'Other','Gasoline'),(15,'2025-01-03',60,'Food','Dinner at a restaurant'),(16,'2025-01-03',20,'Entertainment','Video rental'),(17,'2025-01-03',120,'Shopping','Gadgets'),(18,'2025-01-03',15,'Other','Coffee'),(19,'2025-01-04',25,'Food','Lunch'),(20,'2025-01-04',200,'Shopping','Home supplies'),(21,'2025-01-04',10,'Other','Parking'),(22,'2025-01-05',350,'Rent','Shared rent payment'),(23,'2025-01-05',40,'Food','Snacks'),(24,'2025-01-05',75,'Entertainment','Theater tickets'),(25,'2025-01-05',100,'Shopping','Books'),(26,'2025-01-05',15,'Other','Miscellaneous'),(27,'2025-01-06',30,'Food','Breakfast'),(28,'2025-01-06',100,'Shopping','Shoes'),(29,'2025-01-06',80,'Entertainment','Movies'),(30,'2025-01-06',15,'Other','Public transport'),(31,'2025-02-01',1200,'Rent','Monthly rent payment'),(32,'2025-02-01',300,'Food','Groceries for the week'),(33,'2025-02-01',50,'Entertainment','Movie tickets'),(34,'2025-02-01',150,'Shopping','New shoes'),(35,'2025-02-01',20,'Other','Bus fare'),(36,'2025-02-02',400,'Food','Groceries for the week'),(37,'2025-02-02',80,'Entertainment','Concert tickets'),(38,'2025-02-02',100,'Shopping','Clothes'),(39,'2025-02-02',50,'Other','Gasoline'),(40,'2025-02-03',60,'Food','Dinner at a restaurant'),(41,'2025-02-03',20,'Entertainment','Video rental'),(42,'2025-02-03',120,'Shopping','Gadgets'),(43,'2025-02-03',15,'Other','Coffee'),(44,'2025-02-04',25,'Food','Lunch'),(45,'2025-02-04',200,'Shopping','Home supplies'),(46,'2025-02-04',10,'Other','Parking'),(47,'2025-02-05',350,'Rent','Shared rent payment'),(48,'2025-02-05',40,'Food','Snacks'),(49,'2025-02-05',75,'Entertainment','Theater tickets'),(50,'2025-02-05',100,'Shopping','Books'),(51,'2025-02-05',15,'Other','Miscellaneous'),(52,'2025-03-01',1000,'Rent','Monthly rent payment'),(53,'2025-03-01',250,'Food','Groceries for the week'),(54,'2025-03-01',40,'Entertainment','Cinema tickets'),(55,'2025-03-01',100,'Shopping','Clothes'),(56,'2025-03-01',20,'Other','Public transport'),(62,'2025-01-15',10,'Shopping','Bought potatoes'),(63,'2025-01-01',1227,'Rent','Monthly rent payment'),(64,'2025-01-01',300,'Food','Groceries for the week'),(65,'2025-01-01',1200,'Rent','Monthly rent payment'),(66,'2025-01-01',300,'Food','Groceries for the week');
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-26 15:01:53