-- MySQL Database Structure for the BOSWatch MySQL Plugin
-- @author: Bastian Schroll

-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 03. Apr 2015 um 11:16
-- Server Version: 5.5.41
-- PHP-Version: 5.4.39-0+deb7u1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

-- --------------------------------------------------------

--
-- Datenbank anlegen `boswatch`
--

CREATE DATABASE IF NOT EXISTS boswatch;
USE boswatch; 

-- --------------------------------------------------------

--
-- Benutzer erstellen für Datenbank `boswatch`
--

GRANT ALL ON * to 'boswatch'@'localhost' identified by 'boswatch';
FLUSH PRIVILEGES;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_fms`
--

CREATE TABLE IF NOT EXISTS `bos_fms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `fms` char(8) NOT NULL,
  `status` char(1) NOT NULL,
  `direction` char(1) NOT NULL,
  `directionText` char(10) NOT NULL,
  `tsi` varchar(3) NOT NULL,
  `description` text,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_pocsag`
--

CREATE TABLE IF NOT EXISTS `bos_pocsag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `ric` char(7) NOT NULL,
  `function` int(1) NOT NULL,
  `functionChar` char(1),
  `bitrate` int(4),
  `msg` text,
  `description` text,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_zvei`
--

CREATE TABLE IF NOT EXISTS `bos_zvei` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `zvei` char(5) NOT NULL,
  `description` text,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_signal`
--

CREATE TABLE IF NOT EXISTS `bos_signal` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `time` DATETIME NOT NULL,
    `ric` VARCHAR(7) NOT NULL DEFAULT '0',
    PRIMARY KEY (`ID`)
)  ENGINE=MYISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_weblogin`
--

CREATE TABLE IF NOT EXISTS `bos_weblogin` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user` VARCHAR(150) DEFAULT NULL,
    `password` VARCHAR(32) DEFAULT NULL,
    `isadmin` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`id`)
)  ENGINE=MYISAM DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1;

INSERT INTO `bos_weblogin` (`id`, `user`, `password`, `isadmin`) VALUES (NULL, 'admin', '21232f297a57a5a743894a0e4a801fc3', '1');

-- --------------------------------------------------------

--
-- Schedule für Tabelle `bos_pocsag`
--
CREATE EVENT IF NOT EXISTS `Delete POCSAG Entries > 3 Months` 
	ON SCHEDULE EVERY 1 DAY 
    STARTS '2016-01-01 00:00:00' 
    ON COMPLETION PRESERVE ENABLE 
    DO 
		DELETE FROM bos_pocsag WHERE time < DATE_SUB(NOW(),INTERVAL 3 MONTH);
		

-- --------------------------------------------------------

--
-- Schedule für Tabelle `bos_fms`
--

CREATE EVENT IF NOT EXISTS `Delete FMS Entries > 3 Months` 
	ON SCHEDULE EVERY 1 DAY 
    STARTS '2016-01-01 00:00:00' 
    ON COMPLETION PRESERVE ENABLE 
    DO 
		DELETE FROM bos_fms WHERE time < DATE_SUB(NOW(),INTERVAL 3 MONTH);
		
-- --------------------------------------------------------

--
-- Schedule für Tabelle `bos_zvei`
--
        
CREATE EVENT IF NOT EXISTS `Delete ZVEI Entries > 3 Months` 
	ON SCHEDULE EVERY 1 DAY 
    STARTS '2016-01-01 00:00:00' 
    ON COMPLETION PRESERVE ENABLE 
    DO 
		DELETE FROM bos_zvei WHERE time < DATE_SUB(NOW(),INTERVAL 3 MONTH); 

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
