<?php
session_start();

if(!isset($_SESSION["username"])){
   echo "<p>Bitte erst <a href=\"index.php\">einloggen</a></p>";
   exit;
}

if($_POST){
  require_once ("config.php");
  require_once ("tpl/mysql.class.php");

  $verbindung = mysql_connect($dbhost, $dbuser , $dbpassword) or die("Verbindung zur Datenbank konnte nicht hergestellt werden");
  mysql_select_db($database) or die ("Datenbank konnte nicht ausgewählt werden");

  $username = $_POST["username"];
  $passwort = $_POST["passwort"];
  $passwort2 = $_POST["passwort2"];

  if($passwort != $passwort2 OR $username == "" OR $passwort == ""){
    echo "Eingabefehler. Bitte alle Felder korekt ausfüllen.";
  }else{
    $passwort = md5($passwort);
    $result = mysql_query("SELECT id FROM ".$tableLOG." WHERE user = '$username'");
    $menge = mysql_num_rows($result);
    if($menge == 0){
      $eintrag = "INSERT INTO ".$tableLOG." (user, password) VALUES ('$username', '$passwort')";
      $eintragen = mysql_query($eintrag);

      if($eintragen == true){
        echo "Benutzername <b>$username</b> wurde erstellt.";
      }else{
        echo "Fehler beim Speichern des Benutzernames.";
      }
    }else{
      echo "Benutzername bereits vorhanden.";
    }
  }
}
?>

<!DOCTYPE HTML>
<html>
        <head>
                <title>BOSwatch - Neuer Benutzer</title>
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



                                        <!-- Nav -->
                                                <nav id="nav">
                                                        <ul>
                                                                <li><a href="show_pocsag.php">Alarme</a></li>
                                                                <li><a href="eintragen.php">Nutzer anlegen</a></li>
								<li><a href="logout.php">Logout</a></li>
                                                        </ul>
                                                </nav>

                                </div>
                        </div>
                <!-- Highlights -->
                        <div class="wrapper style1">
                                <div class="title">Benutzerverwaltung</div>
                                <div  class="container">

                                        <div style="width: 400px;margin-left:auto;margin-right:auto;text-align:center;">

                                                <form action="" method="post">
Username:<br>
<input type="text" size="12"
name="username"><br>

Passwort:<br>
<input type="password" size="24" maxlength="50"
name="passwort"><br>

Passwort wiederholen:<br>
<input type="password" size="24" maxlength="50"
name="passwort2"><br>

<input type="submit" value="Speichern">
</form>

                                                </div>

                                </div>
                        </div>
                                        </div>

                                </div>
                                <div id="copyright">
                                        <ul>
                                                <li style="color:grey;">&copy; BOSWatch</li>
                                        </ul>
                                </div>
                        </div>

        </body>
</html>
