<?php
	//read FMS
	$db->query("SELECT id, time, fms, status, direction, directionText, tsi, description FROM ".$tableFMS." ORDER BY id DESC");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['fms'] = $Rows;
?>
