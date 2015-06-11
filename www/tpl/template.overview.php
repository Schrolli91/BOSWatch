Last alarms for FMS and ZVEI (max. 50)<br><br>
		
<div style="float: left; width: 800px;">
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
		<br>
	<b>Last POCSAG alarms</b>
	<table border="1" style="width: 800px;">
	<tr style="font-weight: bold;">
		<td>ID</td>
		<td>Datum - Zeit</td>
		<td>RIC</td>
		<td>Funktion</td>
		<td>Text</td>
	</tr>
	<?php 
		foreach ($tpl['poc'] as $poc)
		{
			
			$time = strtotime($poc['time']);
			$time = date("d.m.Y H:i:s", $time);
			
			echo "<tr>";
			echo "<td>". $poc['id'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". $poc['ric'] . "</td>";
			echo "<td>". $poc['funktion'] . "</td>";
			echo "<td>". $poc['text'] . "</td>";
			echo "</tr>";
		}
	?>
	</table>
</div>
		
<div style="float: right; width: 400px;">
	<b>Last ZVEI alarms</b>
	<table border="1" style="width: 400px;">
	<tr style="font-weight: bold;">
		<td>ID</td>
		<td>Datum - Zeit</td>
		<td>Schleife</td>
	</tr>
	<?php 
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
</div>
