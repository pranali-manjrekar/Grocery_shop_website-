/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.5.5-10.1.31-MariaDB : Database - shoptubedb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`shoptubedb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `shoptubedb`;

/*Table structure for table `admin` */

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(125) NOT NULL,
  `lastName` varchar(125) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile` varchar(25) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `confirmCode` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `admin` */

insert  into `admin`(`id`,`firstName`,`lastName`,`email`,`mobile`,`address`,`password`,`type`,`confirmCode`) values (4,'Nur','Mohsin','mohsin@gmail.com','01677876551','Dhaka','$5$rounds=535000$WOAOMdgoK2JpZLY5$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05','manager','0');

/*Table structure for table `orders` */

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `ofname` text NOT NULL,
  `pid` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `oplace` text NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `dstatus` varchar(10) NOT NULL DEFAULT 'no',
  `odate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ddate` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `orders` */

insert  into `orders`(`id`,`uid`,`ofname`,`pid`,`quantity`,`oplace`,`mobile`,`dstatus`,`odate`,`ddate`) values (1,NULL,'Kashmiri Chador',1,2,'Khilkhet, Dhaka','01609876543','no','2018-09-21 18:35:07',NULL),(2,NULL,'Nur Mohsin',1,3,'Khilkhet, Dhaka','01609876543','no','2018-09-21 18:38:55',NULL),(3,NULL,'Nur Mohsin',2,4,'Dhaka','09876543123','no','2018-09-21 18:43:04',NULL),(4,NULL,'Nur Mohsin',4,1,'Manikganj','798345','no','2018-09-21 18:48:47',NULL),(5,NULL,'Nur Mohsin',9,4,'Dhaka, Bangladesh','01609876543','no','2018-09-22 07:31:02',NULL),(6,NULL,'Nur Mohsin',2,1,'Manikganj','01609876543','no','2018-09-22 07:39:29',NULL),(7,9,'Nur Mohsin',2,1,'Manikganj','01609876543','no','2018-09-22 07:40:46',NULL),(8,9,'Nur Mohsin',1,1,'Manikganj','0994','no','2018-09-22 08:34:13',NULL),(9,9,'Kashmiri Chador',12,4,'Dhaka','01609876543','no','2018-09-22 08:51:14','2018-09-29'),(10,9,'Chador',13,1,'Dhaka','01609876543','no','2018-09-22 08:52:05','2018-09-29'),(11,16,'ningesh',5,1,'yes','18655221446','no','2019-12-29 20:53:25','2020-01-05');

/*Table structure for table `product_level` */

DROP TABLE IF EXISTS `product_level`;

CREATE TABLE `product_level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `v_shape` varchar(10) NOT NULL DEFAULT 'no',
  `polo` varchar(10) NOT NULL DEFAULT 'no',
  `clean_text` varchar(10) NOT NULL DEFAULT 'no',
  `design` varchar(10) NOT NULL DEFAULT 'no',
  `chain` varchar(10) NOT NULL DEFAULT 'no',
  `leather` varchar(10) NOT NULL DEFAULT 'no',
  `hook` varchar(10) NOT NULL DEFAULT 'no',
  `color` varchar(10) NOT NULL DEFAULT 'no',
  `formal` varchar(10) NOT NULL DEFAULT 'no',
  `converse` varchar(10) NOT NULL DEFAULT 'no',
  `loafer` varchar(10) NOT NULL DEFAULT 'no',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

/*Data for the table `product_level` */

insert  into `product_level`(`id`,`product_id`,`v_shape`,`polo`,`clean_text`,`design`,`chain`,`leather`,`hook`,`color`,`formal`,`converse`,`loafer`) values (1,1,'no','no','yes','no','no','no','no','no','no','no','no'),(2,2,'no','no','no','no','yes','yes','no','no','no','no','no'),(3,3,'no','no','no','no','no','yes','no','no','no','no','yes'),(4,4,'no','no','no','no','no','yes','yes','no','no','no','no'),(5,5,'no','yes','yes','no','no','no','no','no','no','no','no'),(6,6,'no','yes','yes','no','no','no','no','no','no','no','no'),(7,7,'yes','no','no','yes','no','no','no','no','no','no','no'),(8,8,'no','no','yes','no','no','no','no','no','no','no','no'),(9,9,'yes','no','no','yes','no','no','no','no','no','no','no'),(10,10,'yes','no','yes','no','no','no','no','no','no','no','no'),(14,14,'no','no','no','no','no','yes','yes','no','no','no','no'),(12,12,'yes','no','no','yes','no','no','no','no','no','no','no'),(13,13,'no','no','no','no','no','yes','no','no','no','no','yes'),(15,15,'no','no','no','no','no','yes','no','yes','no','no','no'),(16,16,'no','no','no','no','no','yes','yes','yes','no','no','no'),(17,17,'no','no','no','no','yes','yes','no','no','no','no','no'),(18,18,'no','no','no','no','yes','yes','no','no','no','no','no'),(19,19,'no','no','no','yes','yes','yes','no','no','no','no','no'),(20,20,'no','no','no','no','no','yes','no','no','no','yes','no'),(21,21,'no','no','no','no','no','yes','no','no','yes','no','no');

/*Table structure for table `product_view` */

DROP TABLE IF EXISTS `product_view`;

CREATE TABLE `product_view` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `product_view` */

insert  into `product_view`(`id`,`user_id`,`product_id`,`date`) values (1,9,9,'2018-09-22 07:49:30'),(2,9,7,'2018-09-27 08:17:43'),(3,9,12,'2018-09-22 08:50:59'),(4,9,10,'2018-09-29 08:37:11'),(5,9,5,'2018-09-22 08:49:19'),(6,9,8,'2018-09-21 21:27:50'),(7,9,6,'2018-09-22 07:42:54'),(8,9,1,'2018-09-22 08:33:36'),(9,16,6,'2019-12-29 20:48:46'),(10,16,5,'2019-12-29 20:52:57');

/*Table structure for table `products` */

DROP TABLE IF EXISTS `products`;

CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pName` varchar(100) NOT NULL,
  `price` int(11) NOT NULL,
  `description` text NOT NULL,
  `available` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `item` varchar(100) NOT NULL,
  `pCode` varchar(20) NOT NULL,
  `picture` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

/*Data for the table `products` */

insert  into `products`(`id`,`pName`,`price`,`description`,`available`,`category`,`item`,`pCode`,`picture`,`date`) values (1,'T-Shirt',120,'T-Shirt',4,'tshirt','t-shirt','t-007','MSTS14738.jpg','2018-09-20 12:40:40'),(2,'Baborry wallet',6000,'Baborry-Double-Zipper-Coin-Bag-RFID-Blocking-Men-Wallets-New-Brand-PU-Leather-Wallet-Money-Purses',3,'wallet','wallet','w-004','IMG_1212.jpg','2018-09-20 13:10:28'),(3,'Loafer Shoes',2000,'Loafer black shoes',8,'shoes','shoes','s-001','8544789_5_.jpg','2018-09-20 14:03:57'),(4,'Artificial Belt',1200,'Black artificial belt',9,'belt','belt','b-001','0283BLT.jpg','2018-09-20 14:05:44'),(5,'Polo T-shirt',500,'Polo t-shirt',10,'tshirt','t-shirt','s-002','lp00-2.jpg','2018-09-20 14:10:06'),(6,'T-shirt',300,'Polo colorful t-shirt',12,'tshirt','t-shirt','t-003','yellow_2_.jpg','2018-09-20 14:11:18'),(7,'Tshirt',200,'Design t-shirt',10,'tshirt','t-shirt','t-004','MSTSV14042.jpg','2018-09-20 14:12:11'),(8,'T-shirt',200,'Color t-shirt',20,'tshirt','t-shirt','t-005','MSTS14759.jpg','2018-09-20 14:15:39'),(9,'Men\'s Tshirt',500,'Colorful men\'s t-shirt',20,'tshirt','t-shirt','t-006','MSTSV14046.jpg','2018-09-20 14:27:07'),(10,'Sports tshirt',1000,'Real madrid t-shirt',5,'tshirt','t-shirt','t-007','MSTSV14039.jpg','2018-09-20 14:28:38'),(12,'T-shirt',300,'Design t-shirt',10,'tshirt','t-shirt','t-010','MSTSV14049.jpg','2018-09-20 14:32:04'),(13,'Leather Shoes',2000,'Best leather shoes',10,'shoes','shoes','s-002','8546789_5_.jpg','2018-09-21 16:09:32'),(14,'Belt',2000,'Nice belt',20,'belt','belt','b-003','gbdl18_1.png','2018-10-01 09:17:08'),(15,'Belt',300,'Nice one belt',20,'belt','belt','b-004','101010_1_.jpg','2018-10-01 09:18:09'),(16,'Mens Belt',300,'Mens belt',15,'belt','belt','b-005','image4_2.jpg','2018-10-01 09:19:08'),(17,'Leather Wallet',100,'Leather wallet',10,'wallet','wallet','w-005','Baborry-Double-Zipper-Coin-Bag-RFID-Blocking-Men-Wallets-New-Brand-PU-Leather-Wallet-Money-Purses.jpg_640x640.jpg','2018-10-01 09:21:52'),(18,'Wallet',300,'Wallet',20,'wallet','wallet','w-007','1881_G.jpg','2018-10-01 09:22:43'),(19,'Black walllet',300,'Black mens wallet',20,'wallet','wallet','w-009','image5_1_2.jpg','2018-10-01 09:23:37'),(20,'Men\'s Shoes',1200,'Men\'s shoes',23,'shoes','shoes','s-003','IMG_2429.jpg','2018-10-01 09:26:41'),(21,'Shoes',2000,'Formal Shoes',12,'shoes','shoes','s-004','G51A7054.jpg','2018-10-01 09:27:24');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` varchar(100) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `online` varchar(1) NOT NULL DEFAULT '0',
  `activation` varchar(3) NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`id`,`name`,`email`,`username`,`password`,`mobile`,`reg_time`,`online`,`activation`) values (12,'Mukul','mukul@gmail.com','mukul','$5$rounds=535000$6PJhbzFlfJbcQbza$FbrPa3qqk1RJ5MSffRLO6LrQJXbgO8SudFuBpNf.wR7','','2018-07-23 19:39:14','0','yes'),(9,'Nur Mohsin','mohsin@gmail.com','mohsin','$5$rounds=535000$EnLkwqfGWGcWklRL$q9PbYw/TVXSzs.QpgUouZ3.6BzaPG2eLHkTyv.Qx80D','123456789022','2018-07-21 12:17:57','1','yes'),(14,'Nur Mohsin','khan@gmail.com','khan','$5$rounds=535000$wLKTQexvPQHueUsK$aFrFUXBHjrrAH61EFiYgj8cZECaaz8y6S5XS/zkkHw9','','2018-09-07 14:32:35','0','yes'),(13,'Robin','robin@gmail.com','robin','$5$rounds=535000$uiZc/VCwwa3XCTTe$Ec.JOjy4GkjpAXHtAvGt6pSc6KszajHgcyZy8v6Ivk1','','2018-07-26 18:06:57','0','yes'),(15,'Sujon','sujon@yahoo.com','sujons','$5$rounds=535000$aGykDT1yrocgTaDt$p2dDAMDz9g3N6o/Jj7QJY9B6NnMlUot.DCq/LOsCS13','89345793753','2018-09-08 19:28:36','0','yes'),(16,'ningeshkumar m k','ningesh1406@gmail.com','ningesh','$5$rounds=535000$mAhn.uSIxd5DjRal$5dbchHPO3JezgWNWB4G87EFEZJQDjSA1n8l2/YzEa2.','18655221446','2019-12-29 20:48:19','1','yes');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
