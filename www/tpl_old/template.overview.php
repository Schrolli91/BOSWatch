 
 <?php
 $seite = $_GET["seite"];
 if(!isset($seite))
 {
 $seite =1;
 }
 $eintraege_pro_seite = 50;
 $start = $seite * $eintraege_pro_seite - $eintraege_pro_seite;
 $result = mysql_query("SELECT id FROM ".$tablePOC");

	$tpl['zvei'] = $Rows;
			//read POCSAG
	$db->query("SELECT id, time, ric, funktion, text, description FROM ".$tablePOC." ORDER BY id DESC LIMIT 50");
	$Rows = array();
	while ($daten = $db->fetchAssoc())
	{
		$Rows[] = $daten;
	}
	$tpl['poc'] = $Rows;
?>

 
 
<table border="1" style="font-size:75%;text-align:left;
				 
				 margin-left:auto;
				 margin-right:auto;				 
border-style:solid;
				 border-width:0.25px;
				 border-collapse:collapse;">
        <tr style="		font-family="Helvetica";
				font-weight:bold;">
                
                <td style="font-weight:bolder;width:200px;">Datum - Uhrzeit</td>
                <td style="font-weight:bolder;width:100px;">Funktion</td>
                <td style="font-weight:bolder;width:120px;">Einheit</td>
                <td style="font-weight:bolder;width:;">Alarmtext</td>
                <td style="font-weight:bolder;">RIC</td>
                <td style="font-weight:bolder;"> </td>
        </tr>
        <?php 
                foreach ($tpl['poc'] as $poc)
                {
                        
                        $time = strtotime($poc['time']);
                        $time = date("d.m.Y H:i:s", $time);
                        $tvpn = 'TVPN';
                        
                        echo "<tr>";
                        echo "<td>". $time . "</td>";
                        
                        if ($poc['funktion'] == 1) 
                        	echo "<td>A. hö. Drg.</td>";
                        if ($poc['funktion'] == 2) 
                    		echo "<td>Alarm</td>";
                   	    if ($poc['funktion'] == 3) 
                        	echo "<td>Einsatz</td>";
                        if ($poc['funktion'] == 4) 
                        	echo "<td>Einsatz abbrechen</td>";
                        
                        
                        echo "<td>". $poc['description'] . "</td>";
                        echo "<td>". $poc['text'] . "</td>";
                        echo "<td>". $poc['ric'] . $poc['funktion'] . "</td>";
                        echo "<td style=\"color:red;\">". $poc['funktion'] . "</td>";
                        echo "</tr>";
                }
        ?>
        </table>


