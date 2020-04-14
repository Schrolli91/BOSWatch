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
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Datenbank anlegen `boswatch`
--

CREATE DATABASE IF NOT EXISTS 'boswatch' DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE 'boswatch';

-- --------------------------------------------------------

--
-- Benutzer erstellen für Datenbank `boswatch`
--

GRANT ALL ON * to 'boswatch'@'localhost' identified by 'root';
FLUSH PRIVILEGES;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_fms`
--

CREATE TABLE IF NOT EXISTS `bos_fms` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `time` DATETIME NOT NULL,
    `fms` VARCHAR(8) NOT NULL,
    `status` VARCHAR(1) NOT NULL,
    `direction` VARCHAR(1) NOT NULL,
    `directionText` TEXT(10) NOT NULL,
    `tsi` VARCHAR(3) NOT NULL,
    `description` TEXT NOT NULL,
    PRIMARY KEY (`ID`)
)  ENGINE=MYISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_pocsag`
--

CREATE TABLE IF NOT EXISTS `bos_pocsag` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `time` DATETIME NOT NULL,
    `ric` VARCHAR(7) NOT NULL DEFAULT '0',
    `function` INT(1) NOT NULL,
    `functionChar` TEXT(1) NOT NULL,
    `msg` TEXT NOT NULL,
    `bitrate` INT(4) NOT NULL,
    `description` TEXT NOT NULL,
    PRIMARY KEY (`ID`),
    KEY `POCSAG_RIC_IDX` (`ric`)
)  ENGINE=MYISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1;

-- rename old columns including little error-prevention
#ALTER IGNORE TABLE `bos_pocsag` change `funktion` `function` INT(1);
#ALTER IGNORE TABLE `bos_pocsag` change `funktionChar` `functionChar` TEXT(1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_zvei`
--

CREATE TABLE IF NOT EXISTS `bos_zvei` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `time` DATETIME NOT NULL,
    `zvei` VARCHAR(5) NOT NULL DEFAULT '0',
    `description` TEXT NOT NULL,
    PRIMARY KEY (`ID`)
)  ENGINE=MYISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bos_signal`
--

CREATE TABLE IF NOT EXISTS `bos_signal` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `time` DATETIME NOT NULL,
    `ric` VARCHAR(7) NOT NULL DEFAULT '0',
    PRIMARY KEY (`ID`)
)  ENGINE=MYISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
