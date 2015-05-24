#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger

import httplib #for the HTTP request
import urllib #for the HTTP request with parameters
import base64 #for the HTTP request with User/Password

from includes import globals  # Global variables


def bosMonRequest(httprequest, params, headers):
	try:
		httprequest.request("POST", "/telegramin/"+globals.config.get("BosMon", "bosmon_channel")+"/input.xml", params, headers)
	except:
		logging.exception("request to BosMon failed")
	else:	
		httpresponse = httprequest.getresponse()
		if str(httpresponse.status) == "200": #Check HTTP Response an print a Log or Error
			logging.debug("BosMon response: %s - %s", str(httpresponse.status), str(httpresponse.reason))
		else:
			logging.warning("BosMon response: %s - %s", str(httpresponse.status), str(httpresponse.reason))

		
def run(typ,freq,data):
	try:
		#ConfigParser
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("BosMon"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")

		try:
			#Initialize header an connect to BosMon-Server
			headers = {}
			headers['Content-type'] = "application/x-www-form-urlencoded"
			headers['Accept'] = "text/plain"
			if globals.config.get("BosMon", "bosmon_user"):
				headers['Authorization'] = "Basic {0}".format(base64.b64encode("{0}:{1}".format(globals.config.get("BosMon", "bosmon_user"), globals.config.get("BosMon", "bosmon_password"))))
			logging.debug("connect to BosMon")
			httprequest = httplib.HTTPConnection(globals.config.get("BosMon", "bosmon_server"), globals.config.get("BosMon", "bosmon_port"))
			#debug-level to shell (0=no debug|1)
			httprequest.set_debuglevel(0)
		except:
			logging.exception("cannot connect to BosMon")

		else:
			if typ == "FMS":
				logging.debug("Start FMS to BosMon")
				try:
					#BosMon-Telegramin expected assembly group, direction and tsi in one field
					#structure (binary as hex in base10): 
					#     Byte 1: assembly group; Byte 2: Direction; Byte 3+4: tactic short info 
					info = 0
					#assembly group:
					info = info + 1          # + b0001 (Assumption: is in every time 1 (no output from multimon-ng))
					#direction:
					if data["direction"] == "1":
						info = info + 2      # + b0010
					#tsi:
					if "IV" in data["tsi"]:
						info = info + 12     # + b1100
					elif "III" in data["tsi"]:
						info = info + 8      # + b1000
					elif "II" in data["tsi"]:
						info = info + 4      # + b0100
					# "I" is + b0000 => nothing to do...
					
					params = urllib.urlencode({'type':'fms', 'address':data["fms"], 'status':data["status"], 'info':info, 'flags':'0'})
					logging.debug(" - Params: %s", params)
					bosMonRequest(httprequest, params, headers)
				except:
					logging.exception("FMS to BosMon failed")

			elif typ == "ZVEI":
				logging.debug("Start ZVEI to BosMon")
				try:
					params = urllib.urlencode({'type':'zvei', 'address':data["zvei"], 'flags':'0'})
					logging.debug(" - Params: %s", params)
					bosMonRequest(httprequest, params, headers)
				except:
					logging.exception("ZVEI to BosMon failed")

			elif typ == "POC":
				logging.debug("Start POC to BosMon")
				try:
					#BosMon-Telegramin expected "a-d" as RIC-sub/function
					data["function"] = data["function"].replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")
					params = urllib.urlencode({'type':'pocsag', 'address':data["ric"], 'flags':'0', 'function':data["function"], 'message':data["msg"]})
					logging.debug(" - Params: %s", params)
					bosMonRequest(httprequest, params, headers)
				except:
					logging.exception("POC to BosMon failed")
			
			else:
				logging.warning("Invalid Typ: %s", typ)	

		finally:
			logging.debug("close BosMon-Connection")
			httprequest.close()
			
	except:
		logging.exception("")