README (Website)

Installation:
1. kompletten Ordner in das /var/www/ Verzeichnis eures Raspberrys oder was auch immer kopieren.
Bemerkung: Es muss ein funktionierender MySQL Server aufgesetzt sein.
2. Dann die passende Tabelle erstellen für die Logindaten (SQL-Datei liegt in /www/MySQL-Database/)
3. Dann folgenden Datein die Logindaten für die MySQL Datenbanken eingeben: 
		—>config.php
		—>eintragen.php
		—>login.php
4. Den Webbrowser eures Vertrauens mit der IP des Hosts füttern, und mit folgenden Daten ausprobieren:
Benutzername: 	Test
Passwort:	Test
4. Dann folgendes im Browser eingeben: http://IP-des-Boswatch-Hosts/eintragen.html
	Dort dann Benutzernamen und Passwort eintragen.
5. Bei Erfolg umbedingt den Testuser manuell löschen, ansonsten, kommt jeder rein.
6. eintragen.html und eintragen.php aus dem Ordner ausschneiden, da sonst das ganze Script bis jetzt noch nichts nützt.
7. Verbesserungsvorschläge nehme ich gerne an.(Vorher unten lesen!!!)


P.S.: Die Webseite befindet sich in einem sehr frühen Stadium.




Folgendes muss noch getan werden: 

--> Ordnerstruktur überarbeiten
--> Rahmen um die Tabellen --> Ausrichten etc.
--> Mobile Ansicht erstellen
--> Issuse mit den Googlefonts beheben (bei nicht vorhandener Internetverbindung lädt die Seite nicht)
--> Ungenutzte Dateien entfernen
--> MySQL Datei für die Datenbank erstellen
--> Die Seite "Einstellungen" komplett erarbeiten (habe ich noch nicht wirklich ein Lösungsansatz für) 
—> Logout button
-> … 


