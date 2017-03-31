<?PHP 
// Mit diesem script kann die config.ini von BOSWatch editiert werden. 
// Da das script mit dem user des php interpreder läuft (bei ubuntu ist es "www-data") muss diesem das schreibrecht auf diese Datei gewährt werden.
// Dateiberechtigung mit "sudo chmod o+w config.ini" ändern. ACHTUNG das gibt allen usern die Schreibberechtigung!
// Die Beschreibungsdatei "config_description.txt" beinhaltettt die Beschreibungen für alle Abschnitte und Parameter.
// Author: Karl-Heinz Ziegler 
// Version 2.2 26.02.2017 
//
//
error_reporting(E_ALL);
ini_set("display_errors", 1);
$source = "/opt/boswatch/BOSWatch/config/config.ini"; // Pfad zur config.ini
$sourceDescription = "/opt/boswatch/BOSWatch/config/config_description.txt";// Pfad zur Beschreibungsdatei 
if (is_writable($source)) {
	if (isset($_POST["senden"])){
		if ($_POST["senden"] == "Speichern") {
			$fp = fopen ($source,"w");
			fwrite ($fp,"");
			//Datei leeren
			fclose ($fp);
			$fp = fopen ($source,"a");
			unset ($_POST["senden"]);
			$sectionOld ="";
			foreach ($_POST as $rawsection=>$keys) {
				//var_dump ($rawsection);
				$section = explode ("|",$rawsection);
				//var_dump ($section);
				//echo"#############<br>";
				//var_dump ($keys);
				//echo"+++++++++++++<br>";
				if ($sectionOld != $section[0]){
					fwrite ($fp,"[".$section[0]."]\n");
				}
				//Kommentar schreiben
				if ($section[2] == "description"){
					//var_dump($keys);
				        $textrows = explode("\n",$keys);
						foreach($textrows as $row){ 
						fwrite ($fp,";".$row."\n");
					}
				}
				//Option mit Wert schreiben
				if ($section[2] == "key"){
					fwrite ($fp,$section[1]);
					fwrite ($fp, "=");
					fwrite ($fp, $keys);
					fwrite ($fp, "\n");
					fwrite ($fp, "\n");
				}
				$sectionOld = $section[0];
			}
			fclose ($fp);
		}
	}
}else {
	echo "<h1 style='color:red'>Die Datei $source ist nicht schreibbar!</h1>";
}
$configContent = parse_ini_file($source,true);

$configContentDesc = myreadiniDescfile($sourceDescription);
echo"<form method='post'>";
foreach ($configContent as $section=>$keys){
	echo "<fieldset  style='border-width:3px;border-style:dotted'>";
	echo "<legend>".$section."</legend>";
	if (isset($configContentDesc[$section]["description"]["value"])){
		echo "<textarea style='border-style:none' name='".$section."|description|sescription' rows='".$configContentDesc[$section]["description"]["rowcount"]."' cols='100' readonly >".$configContentDesc[$section]["description"]["value"]."</textarea>";
		echo "<br>";
	}
	foreach ($keys as $key=>$val) {
		$tooltip ="";
		$row ="";
		if (isset($configContentDesc[$section][$key]["value"])){
			$toolTip = $configContentDesc[$section][$key]["value"];
			$row = $configContentDesc[$section][$key]["rowcount"];
		}
		echo "<strong>$key</strong><br>";
		if ($toolTip != ""){
			echo "<textarea name='".$section."|".$key."|description' rows='".$row."' cols='100' readonly>".$toolTip."</textarea>";
		echo"<br>";
		}
		echo"<input type='text' name='".$section."|".$key."|key' value='".$val."' size='30' pattern ='[^!()=\"]*' title ='Folgende Zeichen sind nicht erlaubt ! ( ) = \" '";
		echo"<br>";
		echo"<br>";
		echo"<br>";
		}
	echo "<input type='submit' name='senden' value='Speichern'>";
	echo "</fieldset>";
	}
echo "</form>";
function myreadiniDescfile ($fileSource){
$data = file_get_contents($fileSource); //read the file
preg_match_all("/(^\[.*\/.*\]\s)/m"  , $data,$sections); //create array separate by new line
$values=preg_split("/(^\[.*\/.*\]\s)/m"  ,$data,-1);
unset($section);
foreach ($sections[0] as $key=>$section){
	$rsection=ltrim($section,"[");
	$rsection=rtrim(trim($rsection),"]");
	$explodestring=explode("/",$rsection);
	$nkey=$key+1;
	$rowcount=substr_count($values[$nkey],"\n");
	$values[$nkey]=rtrim($values[$nkey]);
	$returnstring [$explodestring[0]][$explodestring[1]]["value"]=$values[$nkey];
	$returnstring [$explodestring[0]][$explodestring[1]]["rowcount"]= $rowcount;
}
return $returnstring;
}
?>
