# BOSWatch 3.0
============


Verpacken der Funktionalitäten in Klassen um OOP-Grundsätze zu erreichen.



## Dekodierung und Auswertung trennen.

### Client:
 - reine Dekodierung mittels rtl-fm und multimon
 - Keine Filter usw. nur die Dekoder, Daten verpacken, verschicken
 - per TCP Socket an den Server

 ### Server:
 - Empfängt die TCP Socket Pakete der einzelnen Clients
 - Durch doubleFiltering fallen doppelt eingehende Alarme der Clienten sowieso raus
 - Danach Filterung usw. dann call an die plugins



## Konfiguration:
- Alle Einstellungen in INI File
- Einziges Argument beim Start des Clienten ist der Name der INI (-v -q -t sollen auch bleiben)
- So werden mehrere Sticks auf einem Rechner einfach möglich ohne BOSWatch Ordner kopieren zu müssen

### Client:

```
[Server]
IP    = 127.0.0.1
PORT  = 23

[Client]
Name      = BOSWatch Client 1
LogDir    = log/

[Stick]
device    = 0
Frequency = 85...M
PPMError  = 0
Squelch   = 0
gain      = 100

[Decoder]
FMS       = 0
ZVEI      = 0
POC512    = 0
POC1200   = 1
POC2400   = 0
```

### Server:
```
[Server]
PORT  = 23

[Filter]
...

[Plugins]
MySQL     = 1
template  = 0
...
```

### Plugin:
- Konfigurations Datei für Plugin mit in den Plugin Ordner
- Plugin läd bei Bedarf seine Config selbst, die geht BOSWatch ja nichts an
- Aktuell wird eine ewig lange Config geladen, obwohl 90% der Plugins nicht genutzt werden



## Filterung
Ein Vernünftiges Filterkonzept sollte aufgestellt werden, welches bei POC, FMS und ZVEI gleichermaßen funktioniert
und daher nicht 3 mal implementiert erden muss.



## Versions Überprüfung

über die LIB sched.py - https://docs.python.org/3/library/sched.html - können Zeitgesteuerte Events gestartet werden.
Dies kann zur Überprüfung einer neuen Software version verwendet werden.
information des Nutzers muss noch überlegt werden - evtl als "Alarm" absetzen über normalen Plugin weg.



## Code Dokumentation
Dokumentiert werden sollten alle Funktion und Klassen in Doxygen gerechter Notation.
Genaue Erklärung und Bennenung der Tags in der Doxygen Hilfe
```
class Hello:
    ## @brief Short description.
    # Longer description.
    #
    # @param self
    # @param name Another Parameter
    # @return value Returns a Value

    def __init__(self, name):
        ## @brief Constructor
        # Longer description optinal.
        #
        # @param self
        # @param name Another Parameter
        dosomething(12)

    def dosomething(self, x):
        ## @brief Do something
        # Longer description for do something.
        #
        # @param self
        # @param x Another Parameter
        # @return value Returns a 0
        dosomethingelse
        return 0
```
