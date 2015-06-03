<?php
	//read FMS
	$db->query("SELECT id, time, fms, status, direction, tsi FROM ".$tableFMS." ORDER BY id DESC LIMIT 50");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['fms'] = $Rows;
	
	//read ZVEI
	$db->query("SELECT id, time, zvei FROM ".$tableZVEI." ORDER BY id DESC LIMIT 50");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['zvei'] = $Rows;
			//read POCSAG
	$db->query("SELECT id, time, ric, funktion, text FROM ".$tablePOC." ORDER BY id DESC LIMIT 50");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['poc'] = $Rows;
?>
