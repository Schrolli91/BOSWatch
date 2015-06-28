#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
FMS Decoder

@author: Bastian Schroll

@requires: Configuration has to be set in the config.ini
"""

import logging # Global logger
import re      # Regex for validation

from includes import globals  # Global variables
from includes import doubleFilter  # double alarm filter

##
#
# FMS decoder function
# validate -> check double alarm -> log      
#
def decode(freq, decoded):
	"""
	Export FMS Information from Multimon-NG RAW String and call alarmHandler.processAlarm()

	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    decoded: string
	@param   decoded: RAW Information from Multimon-NG

	@requires:  Configuration has to be set in the config.ini
	
	@return:    nothing
	@exception: Exception if FMS decode failed
	"""
	fms_service = decoded[19]            # Organisation
	fms_country = decoded[36]            # Bundesland
	fms_location = decoded[65:67]        # Ort
	fms_vehicle = decoded[72:76]         # Fahrzeug
	fms_status = decoded[84]             # Status
	fms_direction = decoded[101]         # Richtung
	fms_directionText = decoded[103:110] # Richtung (Text)
	fms_tsi = decoded[114:117]           # Taktische Kruzinformation
		
	if "CRC correct" in decoded: #check CRC is correct  
		fms_id = fms_service+fms_country+fms_location+fms_vehicle+fms_status+fms_direction # build FMS id
		# if FMS is valid
		if re.search("[0-9a-f]{8}[0-9a-f]{1}[01]{1}", fms_id): 
			# check for double alarm
			if doubleFilter.checkID("FMS", fms_id):
				logging.info("FMS:%s Status:%s Richtung:%s TSI:%s", fms_id[0:8], fms_status, fms_direction, fms_tsi)
				data = {"fms":fms_id[0:8], "status":fms_status, "direction":fms_direction, "directionText":fms_directionText, "tsi":fms_tsi, "description":fms_id[0:8]}
				# If enabled, look up description
				if globals.config.getint("FMS", "idDescribed"):
					from includes import descriptionList
					data["description"] = descriptionList.getDescription("FMS", fms_id[0:8])
				# processing the alarm
				try:
					from includes import alarmHandler
					alarmHandler.processAlarm("FMS", freq, data)
				except:
					logging.error("processing alarm failed")
					logging.debug("processing alarm failed", exc_info=True)
					pass
			# in every time save old data for double alarm
			doubleFilter.newEntry(fms_id)
		else:
			logging.warning("No valid FMS: %s", fms_id)    
	else:
		logging.warning("FMS CRC incorrect")