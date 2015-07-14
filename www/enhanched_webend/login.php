<?php 
session_start(); 
?> 

<?php
require_once ("config.php"); 
$verbindung = mysql_connect($dbhost, $dbuser , $dbpassword) 
or die("Verbindung zur Datenbank konnte nicht hergestellt werden"); 
mysql_select_db($tableLOG) or die ("Datenbank konnte nicht ausgewählt werden"); 

$username = $_POST["username"]; 
$passwort = md5($_POST["password"]); 

$abfrage = "SELECT username, passwort FROM" $tableLOG "WHERE username LIKE '$username' LIMIT 1"; 
$ergebnis = mysql_query($abfrage); 
$row = mysql_fetch_object($ergebnis); 

if($row->passwort == $passwort) 
    { 
    $_SESSION["username"] = $username; 
    header("Location: /show_pocsag.php");  
    } 
else 
    { 
    echo "Benutzername und/oder Passwort waren falsch. <a href=\"login.html\">Login</a>"; 
    } 

?>
