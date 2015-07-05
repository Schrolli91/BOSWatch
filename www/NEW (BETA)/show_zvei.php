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
		<title>BOSwatch - ZVEI</title>
		<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
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
							<h1><img src="gfx/logo.png" alt="logo"></img></h1>
						</div>
					
					<!-- Nav -->
						<nav id="nav">
							<ul>
								<li><a href="show_pocsag.php">POCSAG</a></li>
								<li><a href="show_fms.php">FMS</a></li>
								<li><a href="show_zvei.php">ZVEI</a></li>
								<li><a href="prefs.php">Einstellungen</a></li>
							</ul>
						</nav>

				</div>
			</div>
		
		
		
		<!-- Highlights -->
			<div class="wrapper style3">
				<div class="title">ZVEI</div>
				<div id="highlights" class="container" style="text-align: left; width:95%; padding: 10px auto;font-size:90%;">
					
							<?php
		

				include("tpl/zvei.php");
		
		?>	
					
						
					
				</div>
			</div>

		<!-- Footer -->
					
					</div>
				
		
				<div id="copyright">
					<ul>
						<li style="color:grey">&copy; BOSWatch</li><li style="color:grey">Design: <a href="http://html5up.net">HTML5 UP</a></li>
					</ul>
		
			</div>

	</body>
</html>