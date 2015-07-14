<?php


//read all
$db->query("SELECT id, time, fms as data, 'fms' AS typ FROM ".$tableFMS." UNION ALL SELECT id, time, zvei as data, 'zvei' AS typ FROM ".$tableZVEI." UNION ALL SELECT id, time, ric as data, 'pocsag' AS typ FROM ".$tablePOC." ORDER BY time DESC LIMIT 25");
$Rows = array();
while ($daten = $db->fetchAssoc())
{
	$Rows[] = $daten;
}
$tpl['lastAla'] = $Rows;
