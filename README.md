### Fast support on https://bwcc.boswatch.de (Mattermost-Server)
#### Forum: https://boswatch.de

### Arbeiten an BOSWatch 3 gestartet
#### Work on BOSWatch 3 has started
## see: https://boswatch.de/index.php?thread/29-boswatch-3/


|Branch|Code Qualität|CI-Build|
|---|---|---|
|master|[![Codacy Badge](https://img.shields.io/codacy/grade/d512976554354a199555bd34ed179bb1/master.svg)](https://www.codacy.com/app/Schrolli91/BOSWatch/dashboard?bid=3763821)|[![Build Status](https://travis-ci.org/Schrolli91/BOSWatch.svg?branch=master)](https://travis-ci.org/Schrolli91/BOSWatch)|
|develop|[![Codacy Badge](https://img.shields.io/codacy/grade/d512976554354a199555bd34ed179bb1/develop.svg)](https://www.codacy.com/app/Schrolli91/BOSWatch/dashboard?bid=3763820)|[![Build Status](https://travis-ci.org/Schrolli91/BOSWatch.svg?branch=develop)](https://travis-ci.org/Schrolli91/BOSWatch)|


**Unterstützung gesucht**

Zur Weiterentwicklung des Programms benötigen wir Deine Mithilfe - bitte melde dich per Issue, wenn du Anwender in einem verschlüsselten POCSAG-Netz und im (legalen) Besitz des dazugehörigen Schlüssels bist.
In der Zukunft wollen wir die Möglichkeit schaffen, codierte Nachrichten zu entschlüsseln (und nur dann, wenn der Schlüssel bekannt ist!), dafür brauchen wir Dich als Tester!

**Readme ist veraltet** - bitte im [Wiki](https://github.com/Schrolli91/BOSWatch/wiki) nachschauen!

![# BOSWatch](/boswatch.png)

:satellite: Python Script to receive and decode German BOS Information with rtl_fm and multimon-NG :satellite:

#### WICHTIG
**Es wird darauf hingewiesen, dass für die Teilnahme am BOS-Funk nur nach den Technischen Richtlinien der BOS zugelassene Funkanlagen verwendet werden dürfen.**
**Der BOS-Funk ist ein nichtöffentlicher mobiler Landfunk. Privatpersonen gehören nicht zum Kreis der berechtigten Funkteilnehmer.** _(Quelle: TR-BOS)_

#### Notice:
The intercept of the German BOS radio is **strictly prohibited** and will be prosecuted. the use is **only authorized** personnel permitted.
The software was developed using the Multimon-NG code, a function in the real operation can not be guaranteed.


**Please** only use Code from **master**-Branch - thats **the only stable!**

beta-branch is for beta-test of new features

unless you are developer you can use the develop-Branch - may be unstable!

### Features
##### Implemented features:
**list is not complete!**
- FMS, ZVEI and POCSAG512/1200/2400 decoding and displaying
- Plugin support for easy functional extension
- Filtering double alarms with adjustable time and check width
- Filtering allowed, denied and range of POCSAG RIC´s
- Filtering data for each typ/plugin combination with RegEX
- All configurations in a seperate config file
- Data validation (plausibility test)
- Description look-up from csv-files
- Logfiles for better troubleshooting
- verbose/quiet mode for more/none information
- Ready for use BOSWatch as daemon
- possibility to start plugins asynchron
- NMA Error Handler
- multicastAlarm for transmission optimized networks


### Plugins
If you want to code your own Plugin, see `plugins/README.md`.

##### Implemented plugins:
please look at the wiki page


### Configuration
##### boswatch.py
Take a look into the folder /config/
Rename `config.template.ini` to `config.ini`
In the Section `[BOSWatch]` you can set double_alarm_time etc.
In the Section `[Plugins]` you can activate or deactivate the Plugins
For each plugin that requires configurations, a own Section with his name is available

For the other functions see "Usage" below.

##### Filtering Functions (RegEX)
For the RegEX filter functions see Section `[Filters]`
http://www.regexr.com/ - RegEX test tool an documentation

If RegEX is enabled - only alloewd data will pass !

Syntax: `INDIVIDUAL_NAME = TYP;DATAFIELD;PLUGIN;FREQUENZ;REGEX` (separator `;`)
- `TYP` = the data typ (FMS|ZVEI|POC)
- `DATAFIELD` = the field of the data array (see readme.md in plugin folder)
- `PLUGIN` = the name of the plugin to call with this filter (* for all)
- `FREQUENZ` = the frequenz to use the filter (for more SDR sticks (* for all))
- `REGEX` = the RegEX

only ZVEI to all plugins with 25### at 85.5MHz
`testfilter = ZVEI;zvei;*;85500000;25[0-9]{3}`

only POCSAG to MySQL with the text "ALARM:" in the message
`pocTest = POC;msg;MySQL;*;ALARM:`

##### Web frontend (obsolete)
old data in folder `/exampeAddOns/simpleWeb/`

~~Put the files in folder /wwww/ into your local webserver folder (f.e. /var/www/).
Now you must edit the "config.php" with your userdata to your local database.
Take a look into the parser.php for the parsing functions~~


### Usage
please look at the wiki page

### Installation
please look at the wiki page

If you want to use BOSWatch as a daemon, you have to set your
configuration in `service/boswatch.sh` and copy it to `/etc/init.d`.
Then you can start BOSWatch with `sudo /etc/init.d/boswatch.sh start`.
For configuration-details see `service/README.md`.

##### Big thanks
to smith_fms and McBo from Funkmeldesystem.de - Forum for Inspiration and Groundwork!
