# Changelog


### __[v#.#]__ - date
##### Added
- Telegram-Plugin: In der generierten Übersichtkarte wird eine Anfahrtsroute integriert. Der Abfahrtsort ist konfiguierbar. [#382](https://github.com/Schrolli91/BOSWatch/pull/382)
##### Changed
- Telegram-Plugin: Aufrufe der Google API erfolgen per SSL und ohne zusätzliche Bibliotheken [#382](https://github.com/Schrolli91/BOSWatch/pull/382)
##### Deprecated
##### Removed
##### Fixed
##### Security


### __[v2.4.1]__ - 23.10.2018
##### Added
- Pushover-Plugin: Priorität für einzelne RIC und ZVEI in config einstellbar [#378](https://github.com/Schrolli91/BOSWatch/pull/378)
##### Changed
- Kleinere Anpassungen im Telegram Plugin (Karten-Generierung) [#380](https://github.com/Schrolli91/BOSWatch/pull/380)
##### Removed
- Notify-my-Andoird Plugin und Logging-Handler wegen Einstellung des Service entfernt [#374](https://github.com/Schrolli91/BOSWatch/pull/374)


### __[v2.4]__ - 17.08.2018
##### Added
- Config Eintrag um Port für MySQL Plugin festzulegen [#345](https://github.com/Schrolli91/BOSWatch/pull/345)
- FMS und ZVEI Support für Pushover Plugin [#352](https://github.com/Schrolli91/BOSWatch/pull/352)
- Benutzerdefinierte Nachrichten für Pushover Plugin in config [#352](https://github.com/Schrolli91/BOSWatch/pull/352)
##### Changed
- multicastAlarm Plugin - RICs die von multicastAlarm genutzt werden, müssen nicht mehr in der config bei allow_ric bzw. filter_range_start/filter_range_end berücksichtigt werden. [#357](https://github.com/Schrolli91/BOSWatch/pull/357)
- FFAgent Plugin - Debug Logging für die alarmHeaders eingebaut zwecks Troubleshooting [#354](https://github.com/Schrolli91/BOSWatch/pull/354)
- multicastAlarm Plugin - Buffer nach jedem Alarm löschen - erlaubt in kombination mit "doubleFilter_check_msg" die Verwendung in Netzen, die zwischen multicastAlarm RICs auch normale Alarme senden. [#370](https://github.com/Schrolli91/BOSWatch/pull/370)
##### Fixed
- Fehler beim Auslesen der netIdent_RIC im MySQL Plugin [#347](https://github.com/Schrolli91/BOSWatch/pull/347)
- FFAgent Plugin - Typo bei alarmHeaders für Live Betrieb gefixt [#354](https://github.com/Schrolli91/BOSWatch/pull/354)


### __[v2.3]__ - 22.12.2017
##### Added
- zuschaltbare POCSAG Multicast-Alarm Funktionalität [#307](https://github.com/Schrolli91/BOSWatch/pull/307)
- Flag in Config um nur letzte Net Ident oder gesamte Historie zu speichern [#317](https://github.com/Schrolli91/BOSWatch/pull/317)
##### Removed
- Beta Branch aus Readme, Installer und Travis-CI entfernt [#324](https://github.com/Schrolli91/BOSWatch/pull/324)
##### Fixed
- Bug in httpRequest Plugin (data Field wurde überschrieben) [#337](https://github.com/Schrolli91/BOSWatch/pull/337)
- Kommentar für FirEmergency Einstellung angepasst [#338](https://github.com/Schrolli91/BOSWatch/pull/338)


### __[v2.2.2]__ - 21.10.2017
##### Added
- Installations Script für Services [#316](https://github.com/Schrolli91/BOSWatch/pull/316)
##### Changed
- Telegram Plugin importiert Google Maps Funktionen nur noch wenn API Key eingetragen ist [#315](https://github.com/Schrolli91/BOSWatch/pull/315)
- Versions Nummer und Branch Name getrennt [3fed1ac](https://github.com/Schrolli91/BOSWatch/commit/3fed1ac12af8690213766e0e81d71c237530ed2c)
##### Deprecated
- Beta Branch wird mit nächstem Update entfernt [Forum](http://boswatch.de/index.php?thread/16-beta-branch-abschaffen/&postID=113#post113)
##### Fixed
- Schreibfehler der Pfadangabe im Installer [#317](https://github.com/Schrolli91/BOSWatch/pull/317)
- Schreibfehler in Service Readme [#313](https://github.com/Schrolli91/BOSWatch/issues/313)
- Einige Code-Style Verbesserungen [#310](https://github.com/Schrolli91/BOSWatch/pull/310)


### __[v2.2.1]__ - 19.09.2017
##### Added
- Neues Service Script [#263](https://github.com/Schrolli91/BOSWatch/pull/263)
- Eigene Message für jeden Typ im Telegram Plugin in der config definierbar [#267](https://github.com/Schrolli91/BOSWatch/pull/267)
- httpRequest Plugin unterstützt nun mehrere URLs [254](https://github.com/Schrolli91/BOSWatch/pull/254)

##### Changed
- Name der csv Dateien geändert um überschreiben bei Update zu vermeiden [#262](https://github.com/Schrolli91/BOSWatch/pull/262)
- Description Liste kann nun zusätzlich Einträge für jede Subric enthalten (POCSAG) [#271](https://github.com/Schrolli91/BOSWatch/pull/271)
- RegEX verbietet nun grundsätzlich alles - Es muss explizit zugelassen werden (wenn RegEX aktiv) [#284](https://github.com/Schrolli91/BOSWatch/pull/284)

##### Fixed
- Bug im SMS77 Plugin behoben [#257](https://github.com/Schrolli91/BOSWatch/issues/257)
- einige Code-Style Verbesserungen


----------------------------


Zum schreiben des Changelog's siehe:
http://keepachangelog.com/de/1.0.0/

### __[v#.#]__ - date
##### Added
##### Changed
##### Deprecated
##### Removed
##### Fixed
##### Security
