<table border="1"  >
	<tr style="font-weight: bold;">
	<!--	<td>ID</td>
		 -->
		<td>Einheit</td>
		<td>Text</td>
		<td>Datum - Zeit</td>
		<td>RIC</td>
		<td>F</td>
	</tr>
	<?php 
	
	$db->query("SELECT id, time, ric, funktion, text, description FROM ".$tablePOC." ORDER BY id DESC LIMIT 100");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['poc'] = $Rows;
	
	
		foreach ($tpl['poc'] as $poc)
		{
			
			$time = strtotime($poc['time']);
			$time = date("d.m.Y H:i:s", $time);
			
			echo "<tr>";
		//	echo "<td>". $poc['id'] . "</td>";
		//	
			echo "<td>". $poc['description'] . "</td>";
			echo "<td>". $poc['text'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". $poc['ric'] . "</td>";
			echo "<td>". $poc['funktion'] . "</td>";
			echo "</tr>";
		}
	?>
	</table>