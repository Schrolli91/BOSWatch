----
-- phpLiteAdmin database dump (https://bitbucket.org/phpliteadmin/public)
-- phpLiteAdmin version: 1.9.6
-- Exported: 1:18pm on March 5, 2016 (CET)
-- database file: /var/www/html/database/boswatch_all.sqlite
----
BEGIN TRANSACTION;

----
-- Table structure for bos_pocsag
----
CREATE TABLE 'bos_pocsag' (
'id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
'time' DATETIME NOT NULL,
'ric' TEXT NOT NULL DEFAULT '0',
'function' INTEGER NOT NULL DEFAULT 0 ,
'functionChar' TEXT NOT NULL DEFAULT '0',
'msg' TEXT NOT NULL DEFAULT '0',
'bitrate' INTEGER NOT NULL,
'description' TEXT NOT NULL DEFAULT '0');

----
-- Data dump for bos_pocsag, a total of 0 rows
----
COMMIT;
