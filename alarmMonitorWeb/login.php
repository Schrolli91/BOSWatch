<?php
session_start();

require_once ("config.php");
$verbindung = mysql_connect($dbhost, $dbuser , $dbpassword) or die("Verbindung zur Datenbank konnte nicht hergestellt werden");
mysql_select_db($database) or die ("Datenbank konnte nicht ausgewählt werden");

$username = $_POST["username"];
$passwort = md5($_POST["password"]);

$abfrage = "SELECT user, password, isadmin FROM ".$tableLOG." WHERE user = '".$username."' LIMIT 1";
$ergebnis = mysql_query($abfrage);
$row = mysql_fetch_object($ergebnis);

if($row->password == $passwort){
    $_SESSION["username"] = $username;
    $_SESSION["isadmin"] = ($row->isadmin) ? true : false;
    header("Location: show_pocsag.php");
}else{
    echo "Benutzername und/oder Passwort waren falsch. <a href=\"index.php\">Login</a>";
}
?>
