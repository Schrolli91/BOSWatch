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
<link rel="stylesheet" type="text/css" href="tooltip.css">
</head>
<body>

	<div style="text-align: center; width: 1250px; margin: 0px auto;">

		<img src="gfx/logo.png" alt="BOSWatch"><br>		
		<a href="index.php?overview">[Übersicht]</a> - <a href="index.php?parser">[Parser]</a>
		
		<br><br>	
		<?php
		
			if(isset($_GET['overview']))
			{
				include("content.overview.php");
				include("template.overview.php");
			}
			elseif(isset($_GET['parser']))
			{
				include("content.parser.php");
				include("template.parser.php");
			}
			else
			{
				include("content.overview.php");
				include("template.overview.php");
			}
		
		?>	
	</div>
	
</body>
</html>