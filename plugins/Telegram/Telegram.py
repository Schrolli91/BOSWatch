#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Plugin to send FMS-, ZVEI- and POCSAG-messages via Telegram
@author: Peter Laemmle
@requires: Telegram BOT token, Telegram chat ID, library python-telegram-bot and optional googlemaps
"""

#
# Imports
#
import logging # Global logger
import httplib, urllib, telegram, googlemaps
from includes import globals  # Global variables

# Helper function, uncomment to use
from includes.helper import configHandler
from includes.helper import timeHandler

# local variables
BOTTokenAPIKey = None
BOTChatIDAPIKey = None
RICforLocationAPIKey = None
GoogleAPIKey = None

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
	global BOTTokenAPIKey
	global BOTChatIDAPIKey
	global RICforLocationAPIKey
	global GoogleAPIKey

	configHandler.checkConfig("Telegram")
	BOTTokenAPIKey = globals.config.get("Telegram","BOTTokenAPIKey")
	BOTChatIDAPIKey = globals.config.get("Telegram","BOTChatIDAPIKey")
	RICforLocationAPIKey = globals.config.get("Telegram","RICforLocationAPIKey")
	GoogleAPIKey = globals.config.get("Telegram","GoogleAPIKey")
	
	return


##
#
# Main function of plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of the Plugin.
	If necessary the configuration hast to be set in the config.ini.
	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset
	@type    data: map of data (structure see interface.txt)
	@param   data: Contains the parameter for dispatch
	@type    freq: string
	@keyword freq: frequency of the SDR Stick
	@requires:  If necessary the configuration hast to be set in the config.ini.
	@return:    nothing
	@exception: nothing, make sure this function will never thrown an exception
	"""
	
	global BOTTokenKey
	global BOTChatIDAPIKey
	global RICforLocationAPIKey
	global GoogleAPIKey

	try:
		#if configHandler.checkConfig("Telegram"): #read and debug the config (let empty if no config used)

			########## User Plugin CODE ##########
			if typ == "POC":
				logging.debug("Compose output from POCSAG-message")
				# compose message content
				output = timeHandler.curtime()+"\n"+data["ric"]+"("+data["functionChar"]+")\n"+data["description"]+"\n"+data["msg"]
				
				# Initiate Telegram Bot
				logging.debug("Initiate Telegram BOT")
				bot = telegram.Bot(token='%s' % BOTTokenAPIKey)	

				# Send message to chat via Telegram BOT API
				logging.debug("Send message to chat via Telegram BOT API")
				bot.sendMessage('%s' % BOTChatIDAPIKey, output)

				# Generate location information only for specific RIC
				if data["ric"] == RICforLocationAPIKey:				
					# Generate map
					logging.debug("Extract address from POCSAG message")
					address = "+".join(data["msg"].split(')')[0].split('/',1)[1].replace('(',' ').split())

					logging.debug("Retrieve maps from Google")
					url = "+".join(["http://maps.googleapis.com/maps/api/staticmap?markers=", address, "&size=480x640&maptype=roadmap&zoom=16&key=", GoogleAPIKey])
					urllib.urlretrieve(url, "overview_map.png")
					url = "+".join(["http://maps.googleapis.com/maps/api/staticmap?markers=", address, "&size=240x320&scale=2&maptype=hybrid&zoom=17&key=", GoogleAPIKey])
					urllib.urlretrieve(url, "detail_map.png")

					# Send message and map with Telegram
					logging.debug("Send message and maps via Telegram BOT")
					bot.sendPhoto('%s' % BOTChatIDAPIKey, open('overview_map.png', 'rb'))
					bot.sendPhoto('%s' % BOTChatIDAPIKey, open('detail_map.png', 'rb'))

					# Geocoding of address
					logging.debug("Geocode address")
					gcode = googlemaps.Client(key='%s' % GoogleAPIKey)
					gcode_result = gcode.geocode(address)
					logging.debug("Send location via Telegram BOT API")
					bot.sendLocation('%s' % BOTChatIDAPIKey, gcode_result[0]['geometry']['location']['lat'], gcode_result[0]['geometry']['location']['lng'])

			elif typ == "FMS":
				logging.debug("FMS not supported yet")
			elif typ == "ZVEI":
				logging.debug("ZVEI not supported yet")
			else:
				logging.warning("Invalid Typ: %s", typ)
			########## User Plugin CODE ##########

except:
		logging.error("unknown error")
logging.debug("unknown error", exc_info=True)
