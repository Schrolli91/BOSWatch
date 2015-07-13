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
  `fms` varchar(8) NOT NULL,
  `status` varchar(1) NOT NULL,
  `direction` varchar(1) NOT NULL,
	`directionText` text(10) NOT NULL,
  `tsi` varchar(3) NOT NULL,
	`description` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_pocsag`
--

CREATE TABLE IF NOT EXISTS `bos_pocsag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `ric` varchar(7) NOT NULL DEFAULT '0',
  `funktion` int(1) NOT NULL,
	`funktionChar` text(1) NOT NULL,
  `msg` text NOT NULL,
	`bitrate` int(4) NOT NULL,
	`description` text NOT NULL,
  KEY `ID` (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_zvei`
--

CREATE TABLE IF NOT EXISTS `bos_zvei` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `zvei` varchar(5) NOT NULL DEFAULT '0',
	`description` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
