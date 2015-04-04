![# BOSWatch](/www/gfx/logo.png)

Python Script to Recive and Decode German BOS Information with rtl_fm and multimon-NG

**Please** only use Code from **master-Branch** - thats the only stable!

### Features
#####Implemented Features:
- FMS and ZVEI decoding and Displaying
- Filtering double alarms with adjustable time
- FMS and ZVEI validation (plausibility test)
- MySQL Database Support for FMS and ZVEI
- All configurations in seperate File "config.ini"
- simple Web Frontend with Data Parsing

#####Features for the Future:
- extensive filtering options
- POCSAG 512,1200,2400 support (need RAW data from multimon-ng)
- automatic Audio recording at alarm
- Web Frontend with Overview and configuration

### Configuration
##### boswatch.py
The configuration for the Script you can find in config.ini
- You can set the ignore time for double alarms in seconds.
- To use the script with MySQL Support set "useMySQL = 1" and the Userdata to your local MySQL Database.

For the other Functions see "Usage" below.

##### Web Frontend
Put the Files in Folder /wwww/ into your local Webserver Folder (/var/www/).
Now you must edit the "config.php" with your Userdata to your local Database.

### Usage
`sudo python boswatch.py -f 85.235M -a FMS ZVEI -s 50`
Starts boswatch at Frequency 85.235 MHz with the Demodulation Functions FMS and ZVEI.
Squelch level is set to 50

Help to all usable Parameters with `sudo python boswatch.py -h`

```
usage: boswatch.py [-h] -f FREQ [-d DEVICE] [-e ERROR] -a
                   {FMS,ZVEI,POC512,POC1200,POC2400}
                   [{FMS,ZVEI,POC512,POC1200,POC2400} ...] [-s SQUELCH] [-v]

BOSWatch is a Python Script to Recive and Decode BOS Information with rtl_fm
and multimon-NG

optional arguments:
  -h, --help            show this help message and exit
  -f FREQ, --freq FREQ  Frequency you want to listen
  -d DEVICE, --device DEVICE
                        Device you want to use (Check with rtl_test)
  -e ERROR, --error ERROR
                        Frequency-Error of your Device in PPM
  -a {FMS,ZVEI,POC512,POC1200,POC2400} [{FMS,ZVEI,POC512,POC1200,POC2400} ...],
  --demod {FMS,ZVEI,POC512,POC1200,POC2400} [{FMS,ZVEI,POC512,POC1200,POC2400} ...]
                        Demodulation Functions
  -s SQUELCH, --squelch SQUELCH
                        Level of Squelch
  -v, --verbose         Shows more Information

More Options you can find in the extern config.ini File in this Folder
```

### Installation
You can easy install BOSWatch with the install.sh Script.
- Download the install.sh in any Folder you want.
- Make it executeable `sudo chmod +x install.sh`
- And use the script  `sudo sh install.sh`

Now the script downloads and compile all needed data.
At the end you can find the Programm in `/home/pi/bos/BOSWatch`

### Requirements
- RTL_SDR (rtl_fm)
- Multimon-NG
- MySQL Connector for Python

##### optional
- Webserver with PHP
- MySQL Database Server

Thanks to smith_fms and McBo from [Funkmeldesystem.de - Forum](http://www.funkmeldesystem.de/) for Inspiration and Groundwork!

######Greetz Schrolli
