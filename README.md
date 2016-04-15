![# BOSWatch](/boswatch.png)

:satellite: Python Script to receive and decode German BOS Information with rtl_fm and multimon-NG :satellite:

#### Notice:
The intercept of the German BOS radio is **strictly prohibited** and will be prosecuted. the use is **only authorized** personnel permitted.
The software was developed using the Multimon-NG code, a function in the real operation can not be guaranteed.


**Please** only use Code from **master**-Branch - thats **the only stable!**

unless you are developer you can use the develop-Branch - may be unstable!

### Features
##### Implemented features:
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

##### Features for the future:
- more plugins
- other Ideas per Issues please


###Plugins
If you want to code your own Plugin, see `plugins/README.md`.

##### Implemented plugins:

|Plugin|Function|FMS|ZVEI|POC|
|-----|---------|:-:|:--:|:-:|
|MySQL|insert data into MySQL database|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|httpRequest|send a request with parameter to an URL|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|eMail|send Mails with own text|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|BosMon|send data to BosMon server|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|firEmergency|send data to firEmergency server|:x:|:white_check_mark:|:white_check_mark:|
|jsonSocket|send data as jsonString to a socket server|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|NMA|send data to Notify my Android|:white_check_mark:|:white_check_mark:|:white_check_mark:|
|Sqlite|insert data into Sqlite database|:x:|:x:|:white_check_mark:|
|prowl|send data to Prowl (iOS Push)|:x:|:x:|:white_check_mark:|

- for more Information to the plugins see `config.ini`

##### Plugins for the Future:
- Ideas per Issues please


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

No filter for a combination typ/plugin = all data will pass

Syntax: `INDIVIDUAL_NAME = TYP;DATAFIELD;PLUGIN;FREQUENZ;REGEX` (separator `;`)
- `TYP` = the data typ (FMS|ZVEI|POC)
- `DATAFIELD` = the field of the data array (See interface.txt)
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
`sudo python boswatch.py -f 85.235M -a FMS ZVEI`
Starts boswatch at frequency 85.235 MHz with the demodulation functions FMS and ZVEI.
Parameter -f/--freq and -a/--demod are required!

Help to all usable parameters with `sudo python boswatch.py -h`

```
usage: boswatch.py [-h] -f FREQ [-d DEVICE] [-e ERROR] -a
                   {FMS,ZVEI,POC512,POC1200,POC2400}
                   [{FMS,ZVEI,POC512,POC1200,POC2400} ...] [-s SQUELCH] [-v]

optional arguments:
  -h, --help            				show this help message and exit
  -f FREQ, --freq FREQ  				Frequency you want to listen
  -d DEVICE, --device DEVICE			Device you want to use (Check with rtl_test)
  -e ERROR, --error ERROR				Frequency-Error of your device in PPM
  -a {FMS,ZVEI,POC512,POC1200,POC2400} [{FMS,ZVEI,POC512,POC1200,POC2400} ...],
  --demod {FMS,ZVEI,POC512,POC1200,POC2400} [{FMS,ZVEI,POC512,POC1200,POC2400} ...]
										Demodulation functions
  -s SQUELCH, --squelch 				SQUELCH	level of squelch
  -u, --usevarlog         				Use '/var/log/boswatch' for logfiles instead of subdir 'log' in BOSWatch directory
  -v, --verbose         				Shows more information
  -q, --quiet           				Shows no information. Only logfiles
```


### Installation
You can easy install BOSWatch with the install.sh Script.
- Download the install.sh in any folder you want.
- Make it executeable `sudo chmod +x install.sh`
- And use the script  `sudo sh install.sh`

Now the script downloads and compile all needed data.
At the end you can find BOSWatch in `~/boswatch/`
Rename `config.template.ini` to `config.ini` and configure
In case of an error during the installation, check the logfile in `~/boswatch/install/setup_log.txt`

Caution, script don't install a webserver with PHP and MySQL.
So you have to make up manually if you want to use MySQL support.
Database Structure `boswatch.sql` in the MySQL Plugin Folder

If you want to use BOSWatch as a daemon, you have to set your
configuration in `service/boswatch.sh` and copy it to `/etc/init.d`.
Then you can start BOSWatch with `sudo /etc/init.d/boswatch.sh start`.
For configuration-details see `service/README.md`.

### Requirements
- RTL_SDR (rtl_fm)
- Multimon-NG
- Python Support
- MySQL Connector for Python (for MySQL-plugin)

Thanks to smith_fms and McBo from Funkmeldesystem.de - Forum for Inspiration and Groundwork!


### Code your own Plugin
See `plugins/README.md`

