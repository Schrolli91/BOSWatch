<?php
session_start();
unset($_SESSION["username"]);
unset($_SESSION["isadmin"]);
header("Location: index.php");
?>
