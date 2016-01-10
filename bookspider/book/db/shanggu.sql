/*
SQLyog 企业版 - MySQL GUI v7.14 
MySQL - 5.5.5-10.0.19-MariaDB-log : Database - shanggu
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`shanggu` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `shanggu`;

/*Table structure for table `sg_book` */

DROP TABLE IF EXISTS `sg_book`;

CREATE TABLE `sg_book` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '作品id',
  `name` varchar(50) NOT NULL COMMENT '作品名称',
  `author` varchar(20) NOT NULL COMMENT '作者',
  `category` varchar(20) NOT NULL COMMENT '分类',
  `desc` varchar(500) NOT NULL COMMENT '作品简介',
  `write_status` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '状态0连在1完本',
  `img_url` varchar(100) NOT NULL COMMENT '封面地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Table structure for table `sg_chapter_0` */

DROP TABLE IF EXISTS `sg_chapter_0`;

CREATE TABLE `sg_chapter_0` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '章节id',
  `bk_id` int(10) unsigned NOT NULL COMMENT '作品id',
  `name` varchar(100) NOT NULL COMMENT '章节名称',
  `content` text NOT NULL COMMENT '章节内容',
  `publish_time` datetime NOT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`),
  KEY `book_id` (`bk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7522 DEFAULT CHARSET=utf8;

/*Table structure for table `spider_book` */

DROP TABLE IF EXISTS `spider_book`;

CREATE TABLE `spider_book` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(200) NOT NULL COMMENT '作品名称',
  `spider_url` varchar(200) NOT NULL COMMENT '作品采集地址',
  `spider_engine` varchar(50) NOT NULL COMMENT '采集引擎默认为采集域名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `spider_chapter_0` */

DROP TABLE IF EXISTS `spider_chapter_0`;

CREATE TABLE `spider_chapter_0` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `bk_id` int(10) unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `spider_url` varchar(200) NOT NULL,
  `is_spider` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `book_id` (`bk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8439 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
