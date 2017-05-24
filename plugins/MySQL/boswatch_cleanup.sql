-- Cleanup-routines for boswatch-tables

use boswatch;
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
