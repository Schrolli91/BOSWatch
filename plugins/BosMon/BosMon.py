#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
BOSWatch-Plugin to dispatch FMS-, ZVEI- and POCSAG - messages to BosMon

-U {The BosMon hompage<http://www.bosmon.de>}

@author: Jens Herrmann

@requires: BosMon-Configuration has to be set in the config.ini
"""

import logging # Global logger

import httplib #for the HTTP request
import urllib #for the HTTP request with parameters
import base64 #for the HTTP request with User/Password

from includes import globals  # Global variables

##
#
# onLoad (init) function of plugin
# will be called one time by the pluginLoader on start
#
def onLoad():
	"""
	While loading the plugins by pluginLoader.loadPlugins()
	this onLoad() routine is called one time for initialize the plugin

	@requires:  nothing
	
	@return:    nothing
	"""
	# nothing to do for this plugin
	return

##
#
# do BosMon-Request
#
def bosMonRequest(httprequest, params, headers):
	"""
	This local function dispatch the BosMon-Request

	@type  httprequest: HTTPConnection
	@param httprequest: An HTTPConnection-Object that represents an open connection to a BosMon-Instance
	@type  params:      string of urlencoded data
	@param params:      Contains the parameter for transfer to BosMon.
	@type  headers:     map
	@param headers:     The headers argument should be a mapping of extra HTTP headers to send with the request.
	
	@return:    nothing
	@exception: Exception if HTTP-Request failed
	"""
	try:
		#
		# BosMon/HTTP-Request
		#
		httprequest.request("POST", "/telegramin/"+globals.config.get("BosMon", "bosmon_channel")+"/input.xml", params, headers)
	except:
		logging.error("request to BosMon failed")
		logging.debug("request to BosMon failed", exc_info=True)
		raise
	else:	
		# 
		# check HTTP-Response
		#
		httpresponse = httprequest.getresponse()
		if str(httpresponse.status) == "200": #Check HTTP Response an print a Log or Error
			logging.debug("BosMon response: %s - %s", str(httpresponse.status), str(httpresponse.reason))
		else:
			logging.warning("BosMon response: %s - %s", str(httpresponse.status), str(httpresponse.reason))

##
#
# Main function of BosMon-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the BosMon-Plugin.
	It will send the data to an BosMon-Instance via http
	
	The configuration for the BosMon-Connection is set in the config.ini.
	If an user is set, the HTTP-Request is authenticatet.

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending to BosMon
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter for dispatch to BosMon.
	@type    freq: string
	@keyword freq: frequency is not used in this plugin

	@requires:  BosMon-Configuration has to be set in the config.ini
	
	@return:    nothing
	"""
	try:
		#
		# ConfigParser
		#
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("BosMon"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.error("cannot read config file")
			logging.debug("cannot read config file", exc_info=True)
		else: # Without config, plugin couldn't work

			try:
				#
				# Initialize header an connect to BosMon-Server
				#
				headers = {}
				headers['Content-type'] = "application/x-www-form-urlencoded"
				headers['Accept'] = "text/plain"
				# if an user is set in the config.ini we will use HTTP-Authorization
				if globals.config.get("BosMon", "bosmon_user"):
					# generate b64encoded autorization-token for HTTP-request
					headers['Authorization'] = "Basic {0}".format(base64.b64encode("{0}:{1}".format(globals.config.get("BosMon", "bosmon_user"), globals.config.get("BosMon", "bosmon_password"))))
				logging.debug("connect to BosMon")
				# open connection to BosMon-Server
				httprequest = httplib.HTTPConnection(globals.config.get("BosMon", "bosmon_server"), globals.config.get("BosMon", "bosmon_port"), timeout=5)
				# debug-level to shell (0=no debug|1)
				httprequest.set_debuglevel(0)
			except:
				logging.error("cannot connect to BosMon")
				logging.debug("cannot connect to BosMon", exc_info=True)
				# Without connection, plugin couldn't work
				return

			else:
				#
				# Format given data-structure to compatible BosMon string
				#
				if typ == "FMS":
					logging.debug("Start FMS to BosMon")
					try:
						# BosMon-Telegramin expected assembly group, direction and tsi in one field
						# structure (binary as hex in base10): 
						#     Byte 1: assembly group; Byte 2: Direction; Byte 3+4: tactic short info 
						info = 0
						# assembly group:
						info = info + 1          # + b0001 (Assumption: is in every time 1 (no output from multimon-ng))
						# direction:
						if data["direction"] == "1":
							info = info + 2      # + b0010
						# tsi:
						if "IV" in data["tsi"]:
							info = info + 12     # + b1100
						elif "III" in data["tsi"]:
							info = info + 8      # + b1000
						elif "II" in data["tsi"]:
							info = info + 4      # + b0100
						# "I" is nothing to do     + b0000
						
						params = urllib.urlencode({'type':'fms', 'address':data["fms"], 'status':data["status"], 'info':info, 'flags':'0'})
						logging.debug(" - Params: %s", params)
						# dispatch the BosMon-request 
						bosMonRequest(httprequest, params, headers)
					except:
						logging.error("FMS to BosMon failed")
						logging.debug("FMS to BosMon failed", exc_info=True)
						return

				elif typ == "ZVEI":
					logging.debug("Start ZVEI to BosMon")
					try:
						params = urllib.urlencode({'type':'zvei', 'address':data["zvei"], 'flags':'0'})
						logging.debug(" - Params: %s", params)
						# dispatch the BosMon-request 
						bosMonRequest(httprequest, params, headers)
					except:
						logging.error("ZVEI to BosMon failed")
						logging.debug("ZVEI to BosMon failed", exc_info=True)
						return

				elif typ == "POC":
					logging.debug("Start POC to BosMon")
					try:
						# BosMon-Telegramin expected "a-d" as RIC-sub/function
						params = urllib.urlencode({'type':'pocsag', 'address':data["ric"], 'flags':'0', 'function':data["functionChar"], 'message':data["msg"]})
						logging.debug(" - Params: %s", params)
						# dispatch the BosMon-request 
						bosMonRequest(httprequest, params, headers)
					except:
						logging.error("POC to BosMon failed")
						logging.debug("POC to BosMon failed", exc_info=True)
						return
				
				else:
					logging.warning("Invalid Typ: %s", typ)	

			finally:
				logging.debug("close BosMon-Connection")
				try: 
					httprequest.close()
				except:
					pass

	except:	
		# something very mysterious
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)