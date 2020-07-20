<?php 
session_start(); 
?> 

<?php
require_once ("config.php"); 
$verbindung = mysqli_connect($dbhost, $dbuser , $dbpassword) 
or die("Verbindung zur Datenbank konnte nicht hergestellt werden"); 
mysqli_select_db($verbindung, $database) or die ("Datenbank konnte nicht ausgewählt werden"); 

if (!isset($_POST["username"]) XOR !isset($_POST["password"]))
{
	echo "Fehlende Eingaben - <a href='index.php'>Login</a>";
	exit;
}

$username = $_POST["username"]; 
$passwort = md5($_POST["password"]); 


$abfrage = "SELECT username, passwort FROM ".$tableLOG." WHERE username LIKE '$username' LIMIT 1"; 
$ergebnis = mysqli_query($verbindung, $abfrage); 
$row = mysqli_fetch_object($ergebnis); 

if($row->passwort == $passwort) 
    { 
    $_SESSION["username"] = $username; 
    switch ($_POST["view"]) {
	case 'pocsag':
	header("Location: show_pocsag.php");  
	break;
	case 'zvei':
	header("Location: show_zvei.php");
	break;
	case 'fms':
	header("Location: show_fms.php");
	break;
	default:
	header("Location: show_pocsag.php");
	}
    } 
else 
    { 
    echo "Benutzername und/oder Passwort waren falsch. <a href=\"index.php\">Login</a>"; 
    } 

?>
