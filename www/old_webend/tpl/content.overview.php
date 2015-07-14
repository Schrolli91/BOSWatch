<?php


//read all
$db->query("SELECT id, time, concat(fms, ' Stat:', status, ' Dir:', directionText) as data, description, 'fms' AS typ FROM ".$tableFMS." UNION ALL SELECT id, time, zvei as data, description, 'zvei' AS typ FROM ".$tableZVEI." UNION ALL SELECT id, time, concat(ric, ' ', functionChar) as data, description, 'pocsag' AS typ FROM ".$tablePOC." ORDER BY time DESC LIMIT 25");
$Rows = array();
while ($daten = $db->fetchAssoc())
{
	$Rows[] = $daten;
}
$tpl['lastAla'] = $Rows;
