<b>Letzte Alarme</b>
<table border="1"  >
	<tr style="font-weight: bold;">
		<td>Datum</td>
		<td>Einheit</td>
		<td>Text</td>
	</tr>
	<?php
	$db->query("SELECT time,msg,description FROM ".$tablePOC." ORDER BY id DESC LIMIT 100");
	$Rows = array();
	while ($daten = $db->fetchAssoc()){
		$Rows[] = $daten;
	}
	$tpl['poc'] = $Rows;
		foreach ($tpl['poc'] as $poc){
			$time = strtotime($poc['time']);
			$time = date("d.m.Y H:i:s", $time);

			echo "<tr>";
			echo "<td>".$time."</td>";
			echo "<td>".$poc['description']."</td>";
			echo "<td>".$poc['msg']."</td>";
			echo "</tr>";
		}
	?>
</table>
