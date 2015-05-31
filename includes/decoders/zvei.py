#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
ZVEI Decoder

@author: Bastian Schroll

@requires: Configuration has to be set in the config.ini
"""

import logging
import time #timestamp for doublealarm
import re #Regex for validation

from includes import globals  # Global variables

##
#
# ZVEI Decoder Function
# validate -> check double alarm -> log      
#
def decode(freq, decoded):
	"""
	Export ZVEI Information from Multimon-NG RAW String and call alarmHandler.processAlarm()

	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    decoded: string
	@param   decoded: RAW Information from Multimon-NG

	@requires:  Configuration has to be set in the config.ini
	
	@return:    nothing
	@exception: Exception if ZVEI decode failed
	"""
	timestamp = int(time.time())#Get Timestamp                  

	zvei_id = decoded[7:12] #ZVEI Code  
	zvei_id = removeF(zvei_id) #resolve F
	if re.search("[0-9]{5}", zvei_id): #if ZVEI is valid
		if zvei_id == globals.zvei_id_old and timestamp < globals.zvei_time_old + globals.config.getint("ZVEI", "double_ignore_time"): #check for double alarm
			logging.info("ZVEI double alarm: %s within %s second(s)", globals.zvei_id_old, timestamp-globals.zvei_time_old)
			globals.zvei_time_old = timestamp #in case of double alarm, zvei_double_ignore_time set new
		else:
			logging.info("5-Ton: %s", zvei_id)
			data = {"zvei":zvei_id}
			from includes import alarmHandler
			alarmHandler.processAlarm("ZVEI",freq,data)

			globals.zvei_id_old = zvei_id #save last id
			globals.zvei_time_old = timestamp #save last time
	else:
		logging.warning("No valid ZVEI: %s", zvei_id)
	

def removeF(zvei):
	"""
	Resolve the F from the repeat Tone

	@type    zvei: string
	@param   zvei: ZVEI Information
	
	@return:    ZVEI without F
	@exception: none
	"""
	if "F" in zvei:
		zvei_old = zvei
		for i in range(1, 5):
			if zvei[i] == "F":
				zvei = zvei.replace("F",zvei[i-1],1)
		logging.debug("resolve F: %s -> %s", zvei_old, zvei)
	return zvei