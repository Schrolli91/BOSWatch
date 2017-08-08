<!DOCTYPE html>
<html lang="en">

<head>

		<?php include '../includes/head.php'; ?>
</head>


    
    
    
    
    
    
    
    
<body>

    <div id="wrapper">

        <?php include '../includes/navbar.php'; ?>

        
        
        
        
        
        
        
        
        
    
    
    
    
    
    <div id="page-wrapper">
            <div class="row">
                <div class="col-md-12">
                    <h1 class="page-header">Einstellungen  
					
					<input type='submit' class='pull-right btn btn-primary' name='senden' value='Speichern'> 
					<a>   </a>
					<input type='submit' style="margin-right:15px" class='pull-right btn btn-danger' name='senden' value='Neustart'>
					
					</h1>
                </div>
                
               
            </div>
            <!-- /.row -->
            <div class="row">
                
                    
             
<?PHP
// Mit diesem script kann die config.ini von BOSWatch editiert werden.
// Da das script mit dem user des php interpreder läuft (bei ubuntu ist es 'www-data') muss diesem das schreibrecht auf diese Datei gewährt werden.
// Dateiberechtigung mit 'sudo chmod o+w config.ini' ändern. ACHTUNG das gibt allen usern die Schreibberechtigung!
//
// Author: Karl-Heinz Ziegler
// Version 1.0 06.01.2017

// Pfad zur config.ini
$source = 'config.ini';
//prüfen ob Datei beschreibbar ist
if (is_writable($source)) {
	// prüfen ob formular abgeschickt wurde
	if (isset($_POST['senden'])) {
		$fp = fopen ($source,"w");
		fwrite ($fp,"");
		//Datei leeren
		fclose ($fp);
		$fp = fopen ($source,"a");
		unset ($_POST['senden']);
		$sectionOld = '';
		foreach ($_POST as $rawsection=>$keys) {
			$section = explode ('|',$rawsection);
			if ($sectionOld != $section[0]){
				$sectionOld = $section[0];
				fwrite ($fp,"[".$section[0]."]\n");
			}
			fwrite ($fp,$section[1]);
			fwrite ($fp, "=");
			fwrite ($fp, $keys);
			fwrite ($fp, "\n");
			$sectionOld = $section[0];
		}
		fclose ($fp);

	}
} else{
	echo"<h1 style='color:red'>Die Datei $source ist nicht schreibbar!</h1>";
}
$configContent = parse_ini_file($source,true,INI_SCANNER_RAW);
    echo"<form method='post'>";
foreach ($configContent as $section=>$keys) {
echo "<div class='col-lg-5'><div class='panel panel-default'>";                      
echo "<div class='panel-heading'>";
echo $section;
echo "</div>";                         
echo "<div class='panel-body'><div class='row'><div class='col-lg-12'>";

$pkey = "";
foreach ($keys as $key=>$val) {
    $test = 'desc_'.$pkey;
if (0 == strcmp($key, $test)) {
 echo "<p class='help-block'>".$val."</p>";  
}
else {    
    
        echo "<div class='form-group'>";
        echo "<label>".$key."</label>";
    #    echo "</div>";
		
		echo "<input class='form-control' name='".$section."|".$key."' value='".$val."'></input>";
        
       echo "</div>";
}

$pkey = $key;
}

echo " </div></div></div></div></div>";
                       


}
echo "</form>";


?>
                        
                        
                               </div>
                    <!-- /.panel -->
                    
                
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->

		
		    <!-- jQuery -->
    <script src="../vendor/jquery/jquery.min.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="../vendor/bootstrap/js/bootstrap.min.js"></script>

    <!-- Metis Menu Plugin JavaScript -->
    <script src="../vendor/metisMenu/metisMenu.min.js"></script>

    <!-- DataTables JavaScript -->
    <script src="../vendor/datatables/js/jquery.dataTables.min.js"></script>
    <script src="../vendor/datatables-plugins/dataTables.bootstrap.min.js"></script>
    <script src="../vendor/datatables-responsive/dataTables.responsive.js"></script>

    <!-- Custom Theme JavaScript -->
    <script src="../dist/js/sb-admin-2.js"></script>

    <!-- Page-Level Demo Scripts - Tables - Use for reference -->
    
    
        </body>
    </html>