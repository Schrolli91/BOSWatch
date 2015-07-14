<b>Last FMS data</b>
<table style="width: 1000px;">
	<tr class="tableHead">
		<td>ID</td>
		<td>Datum - Zeit</td>
		<td>FMS</td>
		<td>Stat.</td>
		<td>Richt.</td>
		<td>TKI</td>
		<td>Beschreibung</td>
	</tr>
	<?php
		foreach ($tpl['fms'] as $fms)
		{

			$time = strtotime($fms['time']);
			$time = date("d.m.Y H:i:s", $time);

			echo "<tr>";
			echo "<td>". $fms['id'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". $fms['fms'] . "</td>";
			echo "<td>". $fms['status'] . "</td>";
			echo "<td>". $fms['direction'] . " = " . $fms['directionText'] . "</td>";
			echo "<td>". $fms['tsi'] . "</td>";
			echo "<td>". $fms['description'] . "</td>";
			echo "</tr>";
		}
	?>
</table>
