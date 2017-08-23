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
if(($_SESSION["username"])!="admin") 
   { 
   echo "Sie sind nicht berechtigt fuer diesen Bereich"; 
   exit; 
   } 
?> 


<?php	
// Parse with sections
include("tpl/a_header.php");
?>
		<!-- Highlights -->
			<div class="wrapper style3">
				<div class="title">Einstellungen</div>
				<div id="highlights" class="container" style="">
				<!--
				<tr>
				<td>Filter Range Start:</td><td>
<input type="text" size="24" maxlength="50" value="
<?php
$ini_array = parse_ini_file("config.ini");
echo($ini_array['filter_range_start']);
?>
"></td></tr><tr>
		<td>Filter Range End: </td><td>   
<input type="text" size="24" maxlength="50" value="
<?php
$ini_array = parse_ini_file("config.ini");
echo($ini_array['filter_range_end']);
?>
"></td>
</tr>-->
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
