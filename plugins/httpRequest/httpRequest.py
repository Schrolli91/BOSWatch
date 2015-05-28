#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
httpRequest-Plugin to dispatch FMS-, ZVEI- and POCSAG - messages to an URL

@author: Bastian Schroll

@requires: httpRequest-Configuration has to be set in the config.ini
"""

import logging # Global logger
import httplib #for the HTTP request
from urlparse import urlparse #for split the URL into url and path

from includes import globals  # Global variables


def run(typ,freq,data):
	"""
	This function is the implementation of the httpRequest-Plugin.
	It will send the data to an URL via http Request

	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  httpRequest-Configuration has to be set in the config.ini
	
	@return:    nothing
	@exception: Exception if ConfigParser failed
	@exception: Exception if http Request failed
	@exception: Exception if http Response failed
	"""
	try:
		#ConfigParser
		logging.debug("reading config file")
		try:
			for key,val in globals.config.items("httpRequest"):
				logging.debug(" - %s = %s", key, val)
		except:
			logging.exception("cannot read config file")
			
		
		try:
			logging.debug("send %s HTTP request", typ)
			
			if typ == "FMS":
				url = globals.config.get("httpRequest", "fms_url")
			elif typ == "ZVEI":
				url = globals.config.get("httpRequest", "zvei_url")
			elif typ == "POC":
				url = globals.config.get("httpRequest", "poc_url")	
			else:
				logging.warning("Invalid Typ: %s", typ)	
			
			httprequest = httplib.HTTPConnection(url)
			httprequest.request("HEAD", url)	
			
		except:
			logging.exception("cannot send HTTP request")
		else:
			
			try:	
				httpresponse = httprequest.getresponse()
				if str(httpresponse.status) == "200": #Check HTTP Response an print a Log or Error
					logging.debug("HTTP response: %s - %s" , str(httpresponse.status), str(httpresponse.reason))
				else:
					logging.warning("HTTP response: %s - %s" , str(httpresponse.status), str(httpresponse.reason))
			except: #otherwise
				logging.exception("cannot get HTTP response")
				
		finally:
			logging.debug("close HTTP-Connection")
			httprequest.close()
	
	except:
		logging.exception("unknown error")