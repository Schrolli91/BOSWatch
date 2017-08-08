<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<?php
require_once ("config.php");
require_once ("parser.php");

require_once ("mysql.class.php");
$db = new Database($dbhost, $dbuser, $dbpassword, $database, 1); //Show Error = 1!
?>


<html>
<head>
<title>BOSWatch</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

	<div style="text-align: center; width: 1250px; margin: 0px auto;">

		<img src="gfx/logo.png" alt="BOSWatch"><br>

		<div id="navi">
			<a href="index.php?overview">Overview</a> -
			<a href="index.php?fms">FMS</a> -
			<a href="index.php?zvei">ZVEI</a> -
			<a href="index.php?pocsag">POCSAG</a> -
			<a href="index.php?parser">Parser</a>
		</div>

		<br><br>
		<?php

			if(isset($_GET['overview']))
			{
				include("tpl/content.overview.php");
				include("tpl/template.overview.php");
			}
			elseif(isset($_GET['fms']))
			{
				include("tpl/content.fms.php");
				include("tpl/template.fms.php");
			}
			elseif(isset($_GET['zvei']))
			{
				include("tpl/content.zvei.php");
				include("tpl/template.zvei.php");
			}
			elseif(isset($_GET['pocsag']))
			{
				include("tpl/content.pocsag.php");
				include("tpl/template.pocsag.php");
			}
			elseif(isset($_GET['parser']))
			{
				include("tpl/content.parser.php");
				include("tpl/template.parser.php");
			}
			else
			{
				include("tpl/content.overview.php");
				include("tpl/template.overview.php");
			}

		?>
	</div>

	<div id="footer">
		BOSWatch Webend | 04/2015 - <?php echo date("m/Y"); ?> | find us on <a href="https://github.com/Schrolli91/BOSWatch" target="_blank">GitHub</a><br>
		Author Webend: <a href="https://github.com/Schrolli91" target="_blank">Bastian Schroll</a>
	</div>

</body>
</html>
