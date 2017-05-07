<!DOCTYPE HTML>
<!--
	Escape Velocity by HTML5 UP
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->

<?php
require_once ("config.php");
require_once ("tpl/parser.php");

require_once ("tpl/mysql.class.php");
$db = new Database($dbhost, $dbuser, $dbpassword, $database, 1); //Show Error = 1!
?>

<html>
	<head>
		<title>BOSwatch</title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<meta name="description" content="" />
		<meta name="keywords" content="" />
		<!--[if lte IE 8]><script src="css/ie/html5shiv.js"></script><![endif]-->
		<script src="js/jquery.min.js"></script>
		<script src="js/jquery.dropotron.min.js"></script>
		<script src="js/skel.min.js"></script>
		<script src="js/skel-layers.min.js"></script>
		<script src="js/init.js"></script>
		<noscript>
			<link rel="stylesheet" href="css/skel.css" />
			<link rel="stylesheet" href="css/style.css" />
			<link rel="stylesheet" href="css/style-desktop.css" />
		</noscript>
		<!--[if lte IE 8]><link rel="stylesheet" href="css/ie/v8.css" /><![endif]-->
	</head>
	<body class="no-sidebar">

		<!-- Header -->
			<div id="header-wrapper" class="wrapper">
				<div id="header">
					
					<!-- Logo -->
						<div id="logo">
							<h1><a href="index.html">Willkommen bei BOSWatch</a></h1>
						</div>
					
					<!-- Nav -->
						<nav id="nav">
				<!--			<ul>
								<li><a href="pocsag.php">POCSAG</a></li>
								<li><a href="fms.php">FMS</a></li>
								<li><a href="zvei.php">ZVEI</a></li>
								<li><a href="prefs.php">Einstellungen</a></li>
							</ul>
							-->
						</nav>

				</div>
			</div>
		
		
		
		<!-- Highlights -->
			<div class="wrapper style1">
				<div class="title">LOGIN</div>
				<div  class="container">
					
					<div style="width: 400px;margin-left:auto;margin-right:auto;text-align:center;">
		<form action="login.php" method="post">
		<h1><div> Bitte melden sie sich an!</div></h1><br><br>
Username:<br>
<input type="text" size="24" maxlength="50" 
name="username"><br><br>

Dein Passwort:<br>
<input type="password" size="24" maxlength="50"
name="password"><br>

<input type="submit" value="Login">
</form>
					
						</div>
					
				</div>
			</div>

		<!-- Footer -->
					<div class="row 150%">
						<div class="6u">

					
						</div>
					</div>
					<hr />
				</div>
				<div id="copyright">
					<ul>
						<li style="color:grey;">&copy; BOSWatch</li><li style="color:grey;">Design: <a href="http://html5up.net">HTML5 UP</a></li>
					</ul>
				</div>
			</div>

	</body>
</html>