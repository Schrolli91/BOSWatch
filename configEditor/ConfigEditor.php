<?PHP 
// Mit diesem script kann die config.ini von BOSWatch editiert werden. 
// Da das script mit dem user des php interpreder läuft (bei ubuntu ist es 'www-data') muss diesem das schreibrecht auf diese Datei gewährt werden.
// Dateiberechtigung mit 'sudo chmod o+w config.ini' ändern. ACHTUNG das gibt allen usern die Schreibberechtigung!
// Die Beschreibungsdatei 'config_description.txt' beinhaltettt die Beschreibungen für alle Abschnitte und Parameter.
// Author: Karl-Heinz Ziegler 
// Version 2.0 27.01.2017 
//
//
$source = '/opt/boswatch/BOSWatch/config/config.ini'; // Pfad zur config.ini
$sourceDescription = '/opt/boswatch/BOSWatch/configEditor/config_description.txt';// Pfad zur Beschreibungsdatei 
if (is_writable($source)) {
	if (isset($_POST['senden'])){
		if ($_POST['senden'] == 'Speichern') {
			$fp = fopen ($source,"w");
			fwrite ($fp,"");
			//Datei leeren
			fclose ($fp);
			$fp = fopen ($source,"a");
			unset ($_POST['senden']);
			$sectionOld ='';
			foreach ($_POST as $rawsection=>$keys) {
				$section = explode ('|',$rawsection);
				if ($sectionOld != $section[0]){
					fwrite ($fp,"[".$section[0]."]\n");
				}
				fwrite ($fp,$section[1]);
				fwrite ($fp, "=");
				fwrite ($fp, $keys);
				fwrite ($fp, "\n");
				$sectionOld = $section[0];
			}
			fclose ($fp);
		}
	}
}else {
	echo "<h1 style='color:red'>Die Datei $source ist nicht schreibbar!</h1>";
}
$configContent = myreadinifile($source);

$configContentDesc = myreadiniDescfile($sourceDescription);

echo"<form method='post'>"; 
foreach ($configContent as $section=>$keys){
	echo "<fieldset>";
	echo "<legend>".$section."</legend>";
	if (isset($configContentDesc[$section]['description'])){
		echo $configContentDesc[$section]['description'];
		echo "<br>";
	}
	foreach ($keys as $key=>$val) {
		$toolTip = $configContentDesc[$section][$key];
		echo "<strong>$key</strong><br>";
		if ($toolTip != ''){
			echo $toolTip;
		}
		echo"<input type='text' name='".$section."|".$key."'value='".$val."' size='30'";
		echo"<br>";
		echo"<br>";
		echo"<br>";
		}
	echo "<input type='submit' name='senden' value='Speichern'>";
	echo "</fieldset>";
	}
echo "</form>";
function myreadinifile ($fileSource){
$data = file_get_contents($fileSource); //read the file
$configExplode = explode("\n", $data); //create array separate by new line
foreach ($configExplode as $rkey=>$rvalue){
	preg_match('/^\[.*/',$rvalue,$rkeyvalue);
	if(isset($rkeyvalue[0])){
		$rsection=ltrim($rkeyvalue[0],"[");
		$rsection=rtrim($rsection,"]");
	}
	if (isset($rkeyvalue[0])){
		$teststring =$rkeyvalue[0];
	}
	else{
		$teststring ='';
	}
	if ($rvalue!=$teststring){
		$valueContent=explode("=",$rvalue);
		$valueContent[1]=str_replace('"','',$valueContent[1]);
		$returnString[$rsection][trim($valueContent[0])]=$valueContent[1];
	}
	
}
return $returnString;
}
function myreadiniDescfile ($fileSource){
$data = file_get_contents($fileSource); //read the file
preg_match_all('/(^\[.*\/.*\]\s)/m'  , $data,$sections); //create array separate by new line
preg_match_all('/(^\[.*\/.*\]\s)/m'  , $data,$sections); //create array separate by new line
$values=preg_split('/(^\[.*\/.*\]\s)/m'  ,$data,-1);
unset($section);
foreach ($sections[0] as $key=>$section){
	$rsection=ltrim($section,"[");
	$rsection=rtrim(trim($rsection),"]");
	$explodestring=explode("/",$rsection);
	$nkey=$key+1;
	$returnstring [$explodestring[0]][$explodestring[1]]=nl2br($values[$nkey]);
}
return $returnstring;
}
?>
