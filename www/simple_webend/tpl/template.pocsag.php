<b>Last POCSAG data</b>
<table style="width: 1000px;">
	<tr class="tableHead">
		<td>ID</td>
		<td>Datum - Zeit</td>
		<td>RIC</td>
		<td>Funktion</td>
		<td>Bitrate</td>
		<td>Nachricht</td>
		<td>Beschreibung</td>
	</tr>
	<?php
		foreach ($tpl['poc'] as $poc)
		{

			$time = strtotime($poc['time']);
			$time = date("d.m.Y H:i:s", $time);

			if(!empty($_GET['id']) && $_GET['id'] == $poc['id']){
				echo "<tr class='highlight'>";
			}
			else{
				echo "<tr>";
			}
			echo "<td>". $poc['id'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". $poc['ric'] . "</td>";
			echo "<td>". $poc['function'] . " = " . $poc['functionChar'] . "</td>";
			echo "<td>". $poc['bitrate'] . "</td>";
			echo "<td>". $poc['msg'] . "</td>";
			echo "<td>". $poc['description'] . "</td>";
			echo "</tr>";
		}
	?>
</table>
