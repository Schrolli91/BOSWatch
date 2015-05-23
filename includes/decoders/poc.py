#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import time #timestamp for doublealarm
import re #Regex for validation

from includes import globals  # Global variables

#POCSAG Decoder Function
#validate -> check double alarm -> log      
def decode(freq, decoded):
	bitrate = 0
	timestamp = int(time.time())#Get Timestamp                  
	
	if "POCSAG512:" in decoded:
		bitrate = 512
		poc_id = decoded[20:27]
		poc_sub = decoded[39].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
		
	elif "POCSAG1200:" in decoded:
		bitrate = 1200
		poc_id = decoded[21:28]
		poc_sub = decoded[40].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
		
	elif "POCSAG2400:" in decoded:
		bitrate = 2400
		poc_id = decoded[21:28]
		poc_sub = decoded[40].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
			
	if bitrate is 0:
		logging.warning("POCSAG Bitrate not found")
	else:
		logging.debug("POCSAG Bitrate: %s", bitrate)
	
		if "Alpha:" in decoded: #check if there is a text message
			poc_text = decoded.split('Alpha:   ')[1].strip().rstrip('<EOT>').strip()
		else:
			poc_text = ""
		
		if re.search("[0-9]{7}", poc_id): #if POC is valid
			if int(poc_id) >= globals.config.getint("BOSWatch", "poc_filter_range_start"):
				if int(poc_id) <= globals.config.getint("BOSWatch", "poc_filter_range_end"):
					if poc_id == globals.poc_id_old and timestamp < globals.poc_time_old + globals.config.getint("BOSWatch", "poc_double_ignore_time"): #check for double alarm
						logging.info("POCSAG%s double alarm: %s within %s second(s)", bitrate, globals.poc_id_old, timestamp-globals.poc_time_old)
						globals.poc_time_old = timestamp #in case of double alarm, poc_double_ignore_time set new
					else:
						logging.info("POCSAG%s: %s %s %s ", bitrate, poc_id, poc_sub, poc_text)
						data = {"ric":poc_id, "function":poc_sub, "msg":poc_text, "bitrate":bitrate}
						from includes import alarmHandler
						alarmHandler.processAlarm("POC",freq,data)
		
						globals.poc_id_old = poc_id #save last id
						globals.poc_time_old = timestamp #save last time		
				else:
					logging.info("POCSAG%s: %s out of filter range (high)", bitrate, poc_id)
			else:
				logging.info("POCSAG%s: %s out of filter range (low)", bitrate, poc_id)
		else:
			logging.warning("No valid POCSAG%s RIC: %s", bitrate, poc_id)