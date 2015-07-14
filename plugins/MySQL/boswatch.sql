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

--
-- Datenbank: `boswatch`
--

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
  PRIMARY KEY `ID` (`ID`)
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

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;