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
 - Danach Filterung usw. und an call an die plugins



## Konfiguration:
### Client:
- Alle Einstellungen in INI File
- Einziges Argument beim Start des Clienten ist der Name der INI (-v -q -t sollen auch bleiben)
- So werden mehrere Sticks auf einem Rechner einfach möglich ohne BOSWatch Ordner kopieren zu müssen

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
