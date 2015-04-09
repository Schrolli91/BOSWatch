Last alarms for FMS and ZVEI (max. 50)<br><br>
		
<div style="float: left; width: 800px;">
	<b>Last FMS alarms</b>
	<table border="1" style="width: 800px;">
		<tr style="font-weight: bold;">
			<td>ID</td>
			<td>Datum - Zeit</td>
			<td>BOS</td>
			<td>Bundesland</td>
			<td>Ort</td>
			<td>Fahrzeug</td>
			<td>Stat.</td>
			<td>Richt.</td>
			<td>TKI</td>
		</tr>
	<?php 
		foreach ($tpl['fms'] as $fms)
		{
		
			$time = strtotime($fms['time']);
			$time = date("d.m.Y H:i:s", $time);
		
			$fms_id = $fms['service'].$fms['country'].$fms['location'].$fms['vehicle'].$fms['status'].$fms['direction'];
			echo "<tr>";
			echo "<td>". $fms['id'] . "</td>";
			echo "<td>". $time . "</td>";
			echo "<td>". parse("service",$fms_id) . "</td>";
			echo "<td>". parse("country",$fms_id) . "</td>";
			echo "<td>". parse("location",$fms_id) . "</td>";
			echo "<td>". parse("vehicle",$fms_id) . "</td>";
			echo "<td>". $fms['status'] . "</td>";
			echo "<td>". parse("direction",$fms_id) . "</td>";
			echo "<td>". $fms['tsi'] . "</td>";
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
			echo "<td>". parse('zvei',$zvei['zvei']) . "</td>";
			echo "</tr>";
		}
	?>
	</table>
</div>