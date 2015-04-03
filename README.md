# BOSWatch
Python Script to Recive and Decode BOS Information with rtl_fm ans multimon-NG

### Features
#####Implementeted Features:
- FMS and ZVEI decoding and Displaying
- Filtering double alarms with adjustable time
- FMS and ZVEI validation (plausibility test)
- MySQL Database Support for FMS and ZVEI
- All configurations in seperate File "config.ini"
- simple Web Frontend

#####Features for the Future:
- extensive filtering options
- POCSAG 512,1200,2400 support
- automatic Audio recording at alarm
- Web Frontend with configuration

### Configuration
##### boswatch.py
You can set the ignore time for double alarms in seconds.

To use the script with MySQL Support, you must edit the "config.ini".
Now set "useMySQL = 1" and the Userdata to your local MySQL Database.

For the other Functions see "Usage" below.

##### Web Frontend
Put the Files in Folder /wwww/ into your local Webserver Folder (/var/www/).
Now you must edit the "config.php" with your Userdata to yout local Database.

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
