#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
POCSAG Decoder

@author: Bastian Schroll
@author: Jens Herrmann

@requires: Configuration has to be set in the config.ini
"""

import logging
import time #timestamp for doublealarm
import re #Regex for validation

from includes import globals  # Global variables

##
#
# Simple Filter
#
def isAllowed(poc_id):
	"""
	Simple Filter Functions (Allowed, Denied and Range)

	@type    poc_id: string
	@param   poc_id: POCSAG Ric

	@requires:  Configuration has to be set in the config.ini
	
	@return:    True if the Ric is allowed, other False
	@exception: none
	"""
	# 1.) If allowed RICs is set, only they will path, 
	#       If RIC is the right one return True, else False
	if globals.config.get("POC", "allow_ric"):
		if poc_id in globals.config.get("POC", "allow_ric"):
			logging.debug("RIC %s is allowed", poc_id)
			return True
		else:
			logging.debug("RIC %s is not in the allowed list", poc_id)
			return False
	# 2.) If denied RIC, return False
	elif poc_id in globals.config.get("POC", "deny_ric"):
		logging.debug("RIC %s is denied by config.ini", poc_id)
		return False
	# 3.) Check Range, return False if outside def. range
	elif int(poc_id) < globals.config.getint("POC", "filter_range_start"):
		logging.debug("RIC %s out of filter range (start)", poc_id)
		return False
	elif int(poc_id) > globals.config.getint("POC", "filter_range_end"):
		logging.debug("RIC %s out of filter range (end)", poc_id)
		return False
	return True

##
#	
# POCSAG Decoder Function
# validate -> check double alarm -> log
#
def decode(freq, decoded):
	"""
	Export POCSAG Information from Multimon-NG RAW String and call alarmHandler.processAlarm()

	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    decoded: string
	@param   decoded: RAW Information from Multimon-NG

	@requires:  Configuration has to be set in the config.ini
	
	@return:    nothing
	@exception: Exception if POCSAG decode failed
	"""
	bitrate = 0
	timestamp = int(time.time())#Get Timestamp                  
	
	if "POCSAG512:" in decoded:
		bitrate = 512
		poc_id = decoded[20:27].replace(" ", "").zfill(7)
		poc_sub = decoded[39].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
		
	elif "POCSAG1200:" in decoded:
		bitrate = 1200
		poc_id = decoded[21:28].replace(" ", "").zfill(7)
		poc_sub = decoded[40].replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
		
	elif "POCSAG2400:" in decoded:
		bitrate = 2400
		poc_id = decoded[21:28].replace(" ", "").zfill(7)
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
			if isAllowed(poc_id):
				#check for double alarm
				if poc_id == globals.poc_id_old and timestamp < globals.poc_time_old + globals.config.getint("POC", "double_ignore_time"):
					logging.info("POCSAG%s double alarm: %s within %s second(s)", bitrate, globals.poc_id_old, timestamp-globals.poc_time_old)
					#in case of double alarm, poc_double_ignore_time set new
					globals.poc_time_old = timestamp 
				else:
					logging.info("POCSAG%s: %s %s %s ", bitrate, poc_id, poc_sub, poc_text)
					data = {"ric":poc_id, "function":poc_sub, "msg":poc_text, "bitrate":bitrate, "description":poc_id}
					# Add function as character a-d to dataset
					data["functionChar"] = data["function"].replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")
					# If enabled, look up description
					if globals.config.getint("POC", "idDescribed"):
						from includes import descriptionList
						data["description"] = descriptionList.getDescription("POC", poc_id)
					# processing the alarm
					from includes import alarmHandler
					alarmHandler.processAlarm("POC",freq,data)
	
					globals.poc_id_old = poc_id #save last id
					globals.poc_time_old = timestamp #save last time		
			else:
				logging.info("POCSAG%s: %s is not allowed", bitrate, poc_id)
		else:
			logging.warning("No valid POCSAG%s RIC: %s", bitrate, poc_id)