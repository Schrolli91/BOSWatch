<html lang="de">

<head>
		<?php include '../includes/head.php'; ?>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">  

</head>

<body>
    <div id="wrapper">
	<?php include '../includes/navbar.php'; ?>
	
		<!-- Page Content -->
        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">Tables</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-12">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            POCSAG Nachrichten
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
      
	  <div style="margin-bottom:10px">
					Sichtbarkeit: 
					<button type="button" class="btn btn-default"><a class="toggle-vis" data-column="0">ID</a></button>
					<button type="button" class="btn btn-default"><a class="toggle-vis" data-column="1">Einheit</a></button>
					<button type="button" class="btn btn-default"><a class="toggle-vis" data-column="2">Text</a></button>
					<button type="button" class="btn btn-default"><a class="toggle-vis" data-column="3">Zeit</a></button>
					<button type="button" class="btn btn-default"><a class="toggle-vis" data-column="4">RIC</a></button>
					<button type="button" class="btn btn-default"><a class="toggle-vis" data-column="5">SubRic</a></button>

					<br>
				</div>

	  
							<table id="POCTable" class="table table-striped table-bordered " cellspacing="10" width="100%">
                                <thead>
									<tr>
									<th>ID</th>
									<th>Einheit</th>
									<th>Text</th>
									<th>Zeit</th>
									<th>RIC</th>
									<th>F</th>
									</tr>
								</thead>
									<tbody>
	


<?php
$mysqli = new mysqli("localhost", "boswatch", "password", "boswatch");
if ($mysqli->connect_errno) {
    die("Verbindung fehlgeschlagen: " . $mysqli->connect_error);
}
mysqli_set_charset($mysqli, "utf8");
$sql = "SELECT * FROM bos_pocsag LIMIT 5000";
$statement = $mysqli->prepare($sql);

$statement->execute();
 
$result = $statement->get_result();
 
 

 
//Alternativ mit fetch_assoc():
while($row = $result->fetch_assoc()) {
  echo "<tr class='gradeA'>";
  echo "<td>".$row['id']."</td>";
  echo "<td>".$row['description']."</td>";
  echo "<td>".$row['msg']."</td>";
  echo "<td>".$row['time']."</td>";
  echo "<td>".$row['ric']."</td>";
  echo "<td>".$row['function']."</td>";
  echo "</tr>";

}
 
?>

									</tbody>
                            </table>
                            <!-- /.table-responsive -->
                           
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
			
			
			        </div>
        <!-- /#page-wrapper -->
	
	
	</div>
	
	
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
    <script>
    $(document).ready(function() {
        var table = $('#POCTable').DataTable({
            "responsive": "true"
        });
		
	 $('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();
 
        // Get the column API object
        var column = table.column( $(this).attr('data-column') );
 
        // Toggle the visibility
        column.visible( ! column.visible() );
    } );
		
    });
    </script>
		</body>
		</html>
			
			