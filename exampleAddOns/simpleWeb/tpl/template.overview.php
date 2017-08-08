<div>
	<b>Last data (max. 25)</b>
	<table style="width: 800px;">
		<tr class="tableHead">
			<td>ID</td>
			<td>Datum - Zeit</td>
			<td>Typ</td>
			<td>Daten</td>
			<td>Beschreibung</td>
			<td></td>
		</tr>
		<?php
			foreach ($tpl['lastAla'] as $lastAla)
			{

				$time = strtotime($lastAla['time']);
				$time = date("d.m.Y H:i:s", $time);

				echo "<tr>";
				echo "<td>". $lastAla['id'] . "</td>";
				echo "<td>". $time . "</td>";
				echo "<td>". $lastAla['typ'] . "</td>";
				echo "<td>". $lastAla['data'] . "</td>";
				echo "<td>". $lastAla['description'] . "</td>";
				echo "<td><a href='index.php?" . $lastAla['typ'] . "&id=" . $lastAla['id'] . "'><img src='gfx/lupe.png' alt='show'></a></td>";
				echo "</tr>";
			}
		?>
	</table>
</div>
