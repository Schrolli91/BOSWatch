#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import time #timestamp for doublealarm
import re #Regex for validation

from includes import globals  # Global variables

#ZVEI Decoder Function
#validate -> check double alarm -> log      
def decode(freq, decoded):
	timestamp = int(time.time())#Get Timestamp                  

	zvei_id = decoded[7:12] #ZVEI Code  
	if re.search("[0-9F]{5}", zvei_id): #if ZVEI is valid
		if zvei_id == globals.zvei_id_old and timestamp < globals.zvei_time_old + globals.config.getint("BOSWatch", "zvei_double_ignore_time"): #check for double alarm
			logging.info("ZVEI double alarm: %s within %s second(s)", globals.zvei_id_old, timestamp-globals.zvei_time_old)
			globals.zvei_time_old = timestamp #in case of double alarm, zvei_double_ignore_time set new
		else:
			logging.info("5-Ton: %s", zvei_id)
			data = {"zvei":zvei_id}
			from includes import pluginHandler
			pluginHandler.throwAlarm("ZVEI",freq,data)

			globals.zvei_id_old = zvei_id #save last id
			globals.zvei_time_old = timestamp #save last time
	else:
		logging.warning("No valid ZVEI: %s", zvei_id)