	<b>Last FMS alarms</b>
	<table border="1" style="width: 800px;">
		<tr style="font-weight: bold;">
			<td>ID</td>
			<td>Datum - Zeit</td>
			<td>FMS</td>
			<td>Stat.</td>
			<td>Richt.</td>
			<td>TKI</td>
		</tr>
	<?php 
	
		//read FMS
	$db->query("SELECT id, time, fms, status, direction, tsi FROM ".$tableFMS." ORDER BY id DESC LIMIT 50");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['fms'] = $Rows;
	
		foreach ($tpl['fms'] as $fms)
		{
		
			$time = strtotime($fms['time']);
			$time = date("d.m.Y H:i:s", $time);
		
			echo "<tr>";
			echo "<td>". $fms['id'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". $fms['fms'] . "</td>";
			echo "<td>". $fms['status'] . "</td>";
			echo "<td>". $fms['direction'] . "</td>";
			echo "<td>". $fms['tsi'] . "</td>";
			echo "</tr>";
		}
	?>
	</table>