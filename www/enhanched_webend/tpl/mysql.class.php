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
        @$this->conn = mysql_connect($host, $user, $password);
        if ($this->conn == false)
        {
            $this->error("Keine Verbindung zum Datenbank Server!", mysql_error());
            return false;
        }

        if (!@mysql_select_db($database, $this->conn))
        {
            $this->error("Datenbank nicht gefunden!", mysql_error());
            return false;
        }
        return true;
    }

    /**
     * Database::query()
     *
     * F�hrt einen MySQL Query aus
     *
     * @param mixed $query Auszuf�hrender Query
     * @return Result-Handler/FALSE
     */
    function query($query)
    {
        $this->result = @mysql_query($query, $this->conn);
        if ($this->result == false)
        {
            $this->error("Fehlerhafte Datenbank Anfrage!", mysql_error());
            return false;
        }
        return $this->result;
    }

    /**
     * Database::fetchAssoc()
     *
     * Liefert alle gefundnen Datens�tze als Assoc
     *
     * @param mixed $result Externer Result-Handler
     * @return gefundene Datens�tze als Assoc
     */
    function fetchAssoc($result = null)
    {
        if ($result != null)
        {
            return @mysql_fetch_assoc($result);
        } else
        {
            return @mysql_fetch_assoc($this->result);
        }
    }

    /**
     * Database::count()
     *
     * Z�hlt alle gefundenen Datens�tze
     *
     * @param mixed $result Externer Result-Handler
     * @return Anzahl gefundener Datens�tze
     */
    function count($result = null)
    {
        if ($result != null)
        {
            return @mysql_num_rows($result);
        } else
        {
            return @mysql_num_rows($this->result);
        }
    }

    /**
     * Database::closeConnection()
     *
     * Schlie�t die bestehende MySQL Verbindung
     *
     * @return TRUE/FALSE
     */
    function closeConnection()
    {
        if (!@mysql_close($this->conn))
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
