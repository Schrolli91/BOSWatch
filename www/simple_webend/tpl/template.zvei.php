<b>Last ZVEI data</b>
<table style="width: 600px;">
	<tr class="tableHead">
		<td>ID</td>
		<td>Datum - Zeit</td>
		<td>Schleife</td>
		<td>Beschreibung</td>
	</tr>
	<?php
		foreach ($tpl['zvei'] as $zvei)
		{

			$time = strtotime($zvei['time']);
			$time = date("d.m.Y H:i:s", $time);

			if(!empty($_GET['id']) && $_GET['id'] == $zvei['id']){
				echo "<tr class='highlight'>";
			}
			else{
				echo "<tr>";
			}
			echo "<td>". $zvei['id'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". $zvei['zvei'] . "</td>";
			echo "<td>". $zvei['description'] . "</td>";
			echo "</tr>";
		}
	?>
</table>
