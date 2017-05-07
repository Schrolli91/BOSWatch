<?php
	//read POCSAG
	$db->query("SELECT id, time, ric, function, functionChar, bitrate, msg, description FROM ".$tablePOC." ORDER BY id DESC");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['poc'] = $Rows;
?>
