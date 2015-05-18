#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables

import httplib #for the HTTP request
import urllib #for the HTTP request with parameters
import base64 #for the HTTP request with User/Password

def run(typ,frequenz,daten):
	logging.debug("BosMon Plugin called")
	logging.debug(" - typ: " +typ)
	try:
		#get BosMon-Config
		bosmon_server = globals.config.get("BosMon", "bosmon_server")
		bosmon_port = globals.config.get("BosMon", "bosmon_port")
		bosmon_user = globals.config.get("BosMon", "bosmon_user")
		bosmon_password = globals.config.get("BosMon", "bosmon_password")
		bosmon_channel = globals.config.get("BosMon", "bosmon_channel")
		logging.debug(" - Server: " +bosmon_server)
		logging.debug(" - Port: " +bosmon_port)
		logging.debug(" - User: " +bosmon_user)
		logging.debug(" - Channel: " +bosmon_channel)

		if typ == "FMS":
			logging.warning("FMS not implemented in BosMon plugin")
		
		elif typ == "ZVEI":
			logging.warning("ZVEI not implemented in BosMon plugin")
		
		elif typ == "POC":
			logging.debug("Start POC to BosMon")
			try:
				#Defined data structure:
				#   daten["ric"]
				#   daten["function"]
				#   daten["msg"]
				#BosMon-Telegramin expected "a-d" as RIC-sub/function
				daten["function"] = daten["function"].replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d")
				params = urllib.urlencode({'type':'pocsag', 'address':daten["ric"], 'flags':'0', 'function':daten["function"], 'message':daten["msg"]})
				logging.debug(" - Params:" +params)
				headers = {}
				headers['Content-type'] = "application/x-www-form-urlencoded"
				headers['Accept'] = "text/plain"
				if bosmon_user:
					headers['Authorization'] = "Basic {0}".format(base64.b64encode("{0}:{1}".format(bosmon_user, bosmon_password)))
				httprequest = httplib.HTTPConnection(bosmon_server, bosmon_port)
				httprequest.request("POST", "/telegramin/"+bosmon_channel+"/input.xml", params, headers)
				httpresponse = httprequest.getresponse()
				if str(httpresponse.status) == "200": #Check HTTP Response an print a Log or Error
					logging.debug("BosMon response: "+str(httpresponse.status)+" - "+str(httpresponse.reason))
				else:
					logging.warning("BosMon response: "+str(httpresponse.status)+" - "+str(httpresponse.reason))
			except:
				logging.warning("POC to BosMon failed")
		else:
			logging.warning("typ '"+typ+"' undefined in BosMon plugin")
	except:
		logging.exception("Error in BosMon Plugin")