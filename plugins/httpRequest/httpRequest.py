#!/usr/bin/python
# -*- coding: cp1252 -*-

#########
# USAGE
#
#	Config
# ======
# to read a option from config File
# VALUE = globals.config.get("SECTION", "OPTION")
#
# Data from boswatch.py
# =====================
# use data["KEY"] for Alarm Data from boswatch.py
# for usable KEYs in different Functions (FMS|ZVEI|POC) see interface.txt
#
# LOG Messages
# ============
# send Log Messages with logging.LOGLEVEL("MESSAGE")
# usable Loglevels debug|info|warning|error|exception|critical
# if you use .exception in Try:Exception: Construct, it logs the Python EX.message too

import logging # Global logger
import httplib #for the HTTP request

from includes import globals  # Global variables


def run(typ,freq,data):
	try:
		#ConfigParser
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("httpRequest"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")
			
########## User Plugin CODE ##########
		try:
			logging.debug("send %s HTTP request", typ)
			
			if typ == "FMS":
				httprequest = httplib.HTTPConnection(globals.config.get("httpRequest", "fms_url"))
				httprequest.request("HEAD", "/")		
			elif typ == "ZVEI":
				httprequest = httplib.HTTPConnection(globals.config.get("httpRequest", "zvei_url"))
				httprequest.request("HEAD", "/")	
			elif typ == "POC":
				httprequest = httplib.HTTPConnection(globals.config.get("httpRequest", "poc_url"))
				httprequest.request("HEAD", "/")	
			else:
				logging.warning("Invalid Typ: %s", typ)	
				
		except:
			loggin.exception("cannot send HTTP request")
		else:
			
			try:	
				httpresponse = httprequest.getresponse()	
				if str(httpresponse.status) == "200": #Check HTTP Response an print a Log or Error
					logging.debug("HTTP response: %s - %s" , str(httpresponse.status), str(httpresponse.reason))
				else:
					logging.warning("HTTP response: %s - %s" , str(httpresponse.status), str(httpresponse.reason))
			except NameError: #if var httprequest does not exist
				logging.exception("no HTTP request been sended")
			except: #otherwise
				logging.exception("cannot get HTTP response")
				
		finally:
			logging.debug("close HTTP-Connection")
			httprequest.close()
########## User Plugin CODE ##########
			
	except:
		logging.exception("unknown error")