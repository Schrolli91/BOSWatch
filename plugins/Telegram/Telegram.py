#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Plugin to send FMS-, ZVEI- and POCSAG-messages via Telegram
@author: Peter Laemmle
@requires: Telegram BOT token, Telegram chat ID, library python-telegram-bot and optional requests and json
"""

#
# Imports
#
import logging # Global logger
import telegram
from telegram.error import (TelegramError, Unauthorized, BadRequest, NetworkError)
from includes import globalVars  # Global variables
if globalVars.config.get("Telegram","RICforLocationAPIKey"):
	import requests, json

# Helper function, uncomment to use
from includes.helper import wildcardHandler
from includes.helper import configHandler

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
	BOTTokenAPIKey = globalVars.config.get("Telegram","BOTTokenAPIKey")
	BOTChatIDAPIKey = globalVars.config.get("Telegram","BOTChatIDAPIKey")
	RICforLocationAPIKey = globalVars.config.get("Telegram","RICforLocationAPIKey")
	GoogleAPIKey = globalVars.config.get("Telegram","GoogleAPIKey")

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
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch
	@type    freq: string
	@keyword freq: frequency of the SDR Stick

	@requires:  If necessary the configuration hast to be set in the config.ini.

	@return:    nothing
	@exception: nothing, make sure this function will never thrown an exception
	"""

	try:
		########## User Plugin CODE ##########
		try:
			if typ in ("POC", "FMS", "ZVEI"):
				logging.debug("Read format and compose output for %s-message" % typ)
				# compose message content
				text = globalVars.config.get("Telegram", "%s_message" % typ)
				text = wildcardHandler.replaceWildcards(text, data)

				# Initiate Telegram Bot
				logging.debug("Initiate Telegram BOT")
				bot = telegram.Bot(token='%s' % BOTTokenAPIKey)
				# Send message to chat via Telegram BOT API
				logging.debug("Send message to chat via Telegram BOT API")
				bot.sendMessage('%s' % BOTChatIDAPIKey, text)

				# Generate location information only for specific RIC
				if typ == "POC" and data["ric"] == RICforLocationAPIKey:
					# Generate map
					logging.debug("Extract address from POCSAG message")
					address = "+".join(data["msg"].split(')')[0].split('/',1)[1].replace('(',' ').split())
					# Origin for routing, use format 'City+Street+Number'
					origin = "CityOfDeparture+Street+Number"

					# Retrieve directions using Google API
					logging.debug("Retrieve polylines from Directions API")
					url = "".join(["https://maps.googleapis.com/maps/api/directions/json?origin=", origin, "&destination=", address, "&mode=driving&key=", GoogleAPIKey])
					response = json.loads(requests.get(url).content.decode('utf-8'))
					logging.debug("Directions API return status: %s" % response['status'])
					
					logging.debug("Retrieve maps from Google")
					url = "".join(["https://maps.googleapis.com/maps/api/staticmap?&size=480x640&maptype=roadmap&language=de&path=enc:",
						       response['routes'][0]['overview_polyline']['points'], "&key=", GoogleAPIKey])
					with open("overview_map.png", "wb") as img: img.write(requests.get(url).content)
					url = "".join(["https://maps.googleapis.com/maps/api/staticmap?markers=",
						       address, "&size=240x320&scale=2&maptype=hybrid&zoom=17&language=de&key=", GoogleAPIKey])
					with open("detail_map.png", "wb") as img: img.write(requests.get(url).content)

					# Send message and map with Telegram
					logging.debug("Send message and maps via Telegram BOT")
					bot.sendPhoto('%s' % BOTChatIDAPIKey, open('overview_map.png', 'rb'), disable_notification='true')
					bot.sendPhoto('%s' % BOTChatIDAPIKey, open('detail_map.png', 'rb'), disable_notification='true')

					# Geocoding of address
					logging.debug("Geocode address")
					url = "".join(["https://maps.googleapis.com/maps/api/geocode/json?address=",
						       address, "&language=de&key=", GoogleAPIKey])
					gcode_result = json.loads(requests.get(url).content)
					logging.debug("Geocoding API return status: %s" % gcode_result['status'])
					logging.debug("Send location via Telegram BOT API")
					bot.sendLocation('%s' % BOTChatIDAPIKey,
							 gcode_result[results][0]['geometry']['location']['lat'],
							 gcode_result[results][0]['geometry']['location']['lng'],
							 disable_notification='true')
			else:
				logging.warning("Invalid Typ: %s", typ)
		except Unauthorized:
			logging.error("Telegram Error: Unauthorized")
			logging.debug("Telegram Error: Unauthorized", exc_info=True)
		except BadRequest:
			logging.error("Telegram Error: BadRequest")
			logging.debug("Telegram Error: BadRequest", exc_info=True)
		except NetworkError:
			logging.error("Telegram Error: NetworkError")
			logging.debug("Telegram Error: NetworkError", exc_info=True)
		except TelegramError:
			logging.error("Telegram Error: TelegramError")
			logging.debug("Telegram Error: TelegramError", exc_info=True)
		########## User Plugin CODE ##########

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
