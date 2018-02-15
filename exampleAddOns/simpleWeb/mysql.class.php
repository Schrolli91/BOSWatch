<?php class Database
/**
Simple Database Class (C) by Bastian Schroll
**/
{
    //Variablen
    private $conn = null;
    private $result = null;
    private $show_error = 1;

    /**
     * Database::__construct()
     *
     * Stellt eine Verbung mit der MySQL Datenbank fest
     *
     * @param mixed $host Hostname des Datenbank Server
     * @param mixed $user Username des Datenbank Nutzers
     * @param mixed $password Passwort des Datenbank Nutzers
     * @param mixed $database Name der Datenbank
     * @param integer $show_error Zeige Fehlermeldungen
     * @return TRUE/FALSE
     */
    function __construct($host, $user, $password, $database, $show_error = 1)
    {
        $this->show_error = $show_error;
        @$this->conn = mysqli_connect($host, $user, $password);
        if ($this->conn == false)
        {
            $this->error("Keine Verbindung zum Datenbank Server!", mysqli_error($this->conn));
            return false;
        }

        if (!@mysqli_select_db($this->conn, $database))
        {
            $this->error("Datenbank nicht gefunden!", mysqli_error($this->conn));
            return false;
        }
        return true;
    }

    /**
     * Database::query()
     *
     * Fuehrt einen MySQL Query aus
     *
     * @param mixed $query Auszufuehrender Query
     * @return Result-Handler/FALSE
     */
    function query($query)
    {
        $this->result = @mysqli_query($this->conn, $query);
        if ($this->result == false)
        {
            $this->error("Fehlerhafte Datenbank Anfrage!", mysqli_error($this->conn));
            return false;
        }
        return $this->result;
    }

    /**
     * Database::fetchAssoc()
     *
     * Liefert alle gefundnen Datensaetze als Assoc
     *
     * @param mixed $result Externer Result-Handler
     * @return gefundene Datensaetze als Assoc
     */
    function fetchAssoc($result = null)
    {
        if ($result != null)
        {
            return @mysqli_fetch_assoc($result);
        } else
        {
            return @mysqli_fetch_assoc($this->result);
        }
    }

    /**
     * Database::count()
     *
     * Zaehlt alle gefundenen Datensaetze
     *
     * @param mixed $result Externer Result-Handler
     * @return Anzahl gefundener Datensaetze
     */
    function count($result = null)
    {
        if ($result != null)
        {
            return @mysqli_num_rows($result);
        } else
        {
            return @mysqli_num_rows($this->result);
        }
    }

    /**
     * Database::closeConnection()
     *
     * Schliesst die bestehende MySQL Verbindung
     *
     * @return TRUE/FALSE
     */
    function closeConnection()
    {
        if (!@mysqli_close($this->conn))
        {
            $this->error("Verbindung zur Datenbank konnte nicht getrennt werden!", mysql_error());
            return false;
        }
        return true;
    }

    /**
     * Database::error()
     *
     * Gibt eine Interne Fehlermeldung aus
     *
     * @param mixed $error_msg Text der Fehlermeldung
     * @param mixed $sql_err MySQL Fehlermeldung per mysql_error()
     * @return NULL
     */
    private function error($error_msg, $sql_err)
    {
        if ($this->show_error)
        {
            echo "<br><strong>MySQL Error: $error_msg</strong><br>$sql_err";
            return true;
            //exit();
        }
    }

} ?>
