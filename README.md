# BOSWatch
Python Script to Recive and Decode BOS Information with rtl_fm ans multimon-NG

### Fetaures
#####Actual implementet:
- FMS and ZVEI decoding and Displaying
- Filtering double alarms with adjustable time
- ZVEI validation (plausibility test)
- MySQL Database Support for FMS and ZVEI
- All configurations in seperate File "config.ini"

#####Fetaures for the Future:
- extensive filtering options
- POCSAG 512,1200,2400 support
- automatic Audio recording at alarm
- Web Frontend

### Usage
`sudo python boswatch.py -f 85.235M -a FMS ZVEI -s 50`
Starts boswatch at Frequency 85.235 MHz with the Demodulation Functions FMS and ZVEI.
Squelch level is set to 50

Help to all usable Parameters with `sudo python boswatch.py -h`
