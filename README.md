![# BOSWatch](/www/gfx/logo.png)

Python Script to receive and decode German BOS Information with rtl_fm and multimon-NG

#### Notice:
The intercept of the German BOS radio is **strictly prohibited** and will be prosecuted. the use is **only authorized** personnel permitted.
The software was developed using the Multimon-NG code, a function in the real operation can not be guaranteed.


**Please** only use Code from **master**-Branch - thats **the only stable!**

unless you are developer you can use the develop-Branch - may be unstable!

### Features
##### Implemented Features:
- FMS, ZVEI and POCSAG512/1200/2400 decoding and Displaying
- Plugin support for easy Functions extension
- Filtering double alarms with adjustable time
- Filtering Range of POCSAG RIC´s
- All configurations in seperate config File
- Data validation (plausibility test)
- Logfiles for better Troubleshooting
- verbose/quiet Mode for more/none information

##### Features for the Future:
- extensive filtering options
- more Plugins


###Plugins
##### Implemented Plugins:
- MySQL
- BosMon

##### Plugins for the Future:
- HTTP-Push
- E-mail Notification
- Other Ideas per Issues


### Configuration
##### boswatch.py
Take a look into the Folder /config/
Rename `config.template.ini` to `config.ini`
In the Section `[BOSWatch]` you can set double_alarm_time etc.
In the Section `[Plugins]` you can activate or deactivate the Plugins
For each Plugin that requires configurations a own Section with his Name is available

For the other Functions see "Usage" below.

##### Web Frontend
Put the Files in Folder /wwww/ into your local Webserver Folder (/var/www/).
Now you must edit the "config.php" with your Userdata to your local Database.
For the Parsing Functions take a look into the parser.php 


### Usage
`sudo python boswatch.py -f 85.235M -a FMS ZVEI`
Starts boswatch at Frequency 85.235 MHz with the Demodulation Functions FMS and ZVEI.
Parameter -f/--freq and -a/--demod are required!

Help to all usable Parameters with `sudo python boswatch.py -h`

```
usage: boswatch.py [-h] -f FREQ [-d DEVICE] [-e ERROR] -a
                   {FMS,ZVEI,POC512,POC1200,POC2400}
                   [{FMS,ZVEI,POC512,POC1200,POC2400} ...] [-s SQUELCH] [-v]

optional arguments:
  -h, --help            				show this help message and exit
  -f FREQ, --freq FREQ  				Frequency you want to listen
  -d DEVICE, --device DEVICE		Device you want to use (Check with rtl_test)
  -e ERROR, --error ERROR				Frequency-Error of your Device in PPM
  -a {FMS,ZVEI,POC512,POC1200,POC2400} [{FMS,ZVEI,POC512,POC1200,POC2400} ...],
  --demod {FMS,ZVEI,POC512,POC1200,POC2400} [{FMS,ZVEI,POC512,POC1200,POC2400} ...]
																Demodulation Functions
  -s SQUELCH, --squelch SQUELCH	Level of Squelch
  -v, --verbose         				Shows more Information
  -q, --quiet           				Shows no Information. Only Logfiles
```


### Installation
You can easy install BOSWatch with the install.sh Script.
- Download the install.sh in any Folder you want.
- Make it executeable `sudo chmod +x install.sh`
- And use the script  `sudo sh install.sh`

Now the script downloads and compile all needed data.
At the end you can find BOSWatch in `~/boswatch/`
Rename `config.template.ini` to `config.ini` and configure
In case of an Error during the Installation, check the Logfile in `~/boswatch/install/setup_log.txt`

Caution, script don't install a Webserver with PHP and MySQL.
So you have to make up manually if you want to use MySQL support.


### Requirements
- RTL_SDR (rtl_fm)
- Multimon-NG
- Python Support
- MySQL Connector for Python
