<!DOCTYPE HTML>
<!--
	Escape Velocity by HTML5 UP
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->

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
?>

					
							<?php
		
				include("tpl/a_header.php");
						?>
		<!-- Highlights -->
			<div class="wrapper style3">
				<div class="title">FMS</div>
				<div id="highlights" class="container" style="">
				<?php
				include("tpl/fms.php");
				include("tpl/a_footer.php");
		?>	
					
						
	