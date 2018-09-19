# BOSWatch 3.0



Python 3
Verpacken der Funktionalitäten in Klassen um OOP-Grundsätze zu erreichen.



## Dekodierung und Auswertung trennen.

### Client:
 - reine Dekodierung mittels rtl-fm und multimon
 - Keine Filter usw. nur die Dekoder, Daten verpacken, verschicken
 - per TCP Socket an den Server
 - versch Eingabequellen (DVB-T Stick, Audio Eingang)

 ### Server:
 - Empfängt die TCP Socket Pakete der einzelnen Clients
 - Durch doubleFiltering fallen doppelt eingehende Alarme der Clienten sowieso raus
 - Danach Filterung nach neuen Filterkonzept
 - dann call an die plugins



## Konfiguration:
- Alle Einstellungen werden in einer Datenbank mittels Django abgebildet.
- Die Schnittstelle bildet eine API die direkt auf die Datenbank zugreifen kann.
- Clienten sollen im Endausbau in der Regel nur noch einen Namen bekommen und danach den Server selber finden. ( MAGIC Paket)
  - Der Client bekommt seine Konfiguration vom Master mitgeteilt ( aus der DB).
- Die Einstellungen werden alle über einen Web Interface gepflegt. 


## Organisationsstruktur

- Die Organisation bei BOSWatch ist per definition eine Baumstruktur
- Jedes Objekt der Organisationsstruktur (Feuerwehren,Bereiche,Einheiten)  kann __mehrere__ Autos und __einen__ Standort haben.
- Ein Fahrzeug kann __einer__ FMS Kennung zugeordnet sein.
- Ein Standort kann __mehrere__ Einheiten beherbergen.


## Pluginaufruf

- Ein Plugin hat eine Standard Konfiguration. 
- Ein Plugin kann __mehrere__ Instanzen haben.
- Eine Plugininstanz kann die Standard konfiguration des geerbten Plugins überschreiben.

- Ein Plugin kann von *einem Fahrzeug, einer Einheit oder einem Standort* aufgerufen werden.
- Ein Plugin kann zusätzlich noch auf Grund der darunter liegenden Einheiten aufgerufen werden.
<br>Ein Beispiel: 
 - Fuerwehr Musterhausen
   - Bereich 1
     - Einheit 11
     - Einheit 12 
<br>Sollte nun in diesem Beispiel Einheit 11 alarmiert werden. so bekommen die Einheiten "Bereich1" und "FeuerwehrMusterhausen" jeweils einen "Informations-Alarm" dieser kann je nach einstellung wie ein echer Alarm abgearbeitet werden. 


## Plugins:

Wie unter "Organisation" beschrieben benötigt das Plugin verschiedene Aufrufe.

```
Erstelle-Plugin
Erstelle-Plugininstanz

Start-Plugin
Start-PluginInstanz

Alarmiere-Plugininstanz ( ARRAY{
                             Art der Nachricht,  
                             Text, 
                             Zeit, 
                             Eingangszeit} , 
                         alarmierteEINHEIT, 
                         originEINHEIT ( falls durch Organisationsvererbung alarmiert worden ist ) 
                         alarmierterSTANDORT, 
                         alarmierteFAHRZEUGE,  
                         ARRAY{
                             PLUGIN-CONFIG,
                             PLUGININSTANZ-CONFIG} 
                         )


```

Grundsätzlich kann durch dieses Vorgehen in einem Plugin auf jedes Feld zugriffen werden. 



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
