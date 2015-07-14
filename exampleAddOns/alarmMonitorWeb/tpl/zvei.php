		

	<b>Last ZVEI alarms</b>
	<table border="1" style="width: 400px;">
	<tr style="font-weight: bold;">
		<td>ID</td>
		<td>Datum - Zeit</td>
		<td>Schleife</td>
	</tr>
	<?php 
	
		//read ZVEI
	$db->query("SELECT id, time, zvei FROM ".$tableZVEI." ORDER BY id DESC LIMIT 50");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['zvei'] = $Rows;
	
		foreach ($tpl['zvei'] as $zvei)
		{
			
			$time = strtotime($zvei['time']);
			$time = date("d.m.Y H:i:s", $time);
			
			echo "<tr>";
			echo "<td>". $zvei['id'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". $zvei['zvei'] . "</td>";
			echo "</tr>";
		}
	?>
	</table>
