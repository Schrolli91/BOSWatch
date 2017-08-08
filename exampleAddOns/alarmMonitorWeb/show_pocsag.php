<!DOCTYPE HTML>

<?php 
session_start(); 
?> 

<?php 
if(!isset($_SESSION["username"])) 
   { 
   echo "Bitte erst <a href=\"login.html\">einloggen</a>"; 
   exit; 
   } 
?> 

<?php
require_once ("config.php");
require_once ("tpl/parser.php");
require_once ("tpl/mysql.class.php");
$db = new Database($dbhost, $dbuser, $dbpassword, $database, 1); //Show Error = 1!
include("tpl/a_header.php");
?>
	<div class="wrapper style3">
		<div class="title">POCSAG</div>
			<div id="highlights" class="container" style="">
<?php
				include("tpl/pocsag.php");
	include("tpl/a_footer.php");
?>	