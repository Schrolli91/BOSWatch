<?php
	//read ZVEI
	$db->query("SELECT id, time, zvei, description FROM ".$tableZVEI." ORDER BY id DESC");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['zvei'] = $Rows;
?>
