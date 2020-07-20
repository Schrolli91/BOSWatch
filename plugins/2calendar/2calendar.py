#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Kalendereinträge für Alarmierungen
Erstellt eine Icalendar (ICS)-Datei, diese kann in Kalender wie Outlook etc. importiert werden.
Aktuell wird jeder Alarm der via Regex dieses Plugin anspricht, in eine "Gesamtdatei" geschrieben. Denkbar wäre aber auch 
für jeden Filter eine seperate Datei anzulegen. 
Auch wird aktuell nur ZVEI, aus mangel an Erfahrung, ausgewertet.
@author: Norbert Jahn
@author: Bastian Schroll
@requires: icalendar https://pypi.org/project/icalendar/
@requires: dateutil https://github.com/dateutil/dateutil/
@requires: pytz https://pypi.org/project/pytz/
"""

import logging # Global logger
import time
import requests
import re
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz 

from includes import globalVars  # Global variables
from includes.helper import configHandler




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
# Main function of Calendar-plugin
# will be called by the alarmHandler
#
def run(typ,freq,data):
	"""
	This function is the implementation of a Calendar-Plugin
	It will write Alarms in an ics-File.
	@type    typ:  string (FMS|ZVEI|POC)
	@param   typ:  Typ of the dataset for sending to BosMon
	@type    data: map of data (structure see readme.md in plugin folder)
	@param   data: Contains the parameter for dispatch to BosMon.
	@type    freq: string
	@keyword freq: frequency is not used in this plugin
	@requires: 
	@return:    nothing
	"""
	try:
		if configHandler.checkConfig("2calendar"): #read and debug the config

			try:
				#
				# Kalender instanzieren
				#
				cal = Calendar()
				cal.add('proid', 'BOS')
				cal.add('version', '2.0')

			except:
				logging.error("Kann Kalender nicht erstellen")
			else: 
				try:
					#
					# Erstelle das Event
					#

					if typ == "ZVEI":
						g = open(globalVars.config.get("2calendar", "filepath2calendar")+'alle.ics','rb')
						gcal = Calendar.from_ical(g.read())

						for component in gcal.walk():

							if component.name == "VEVENT":
								event = Event()
								event.add('summary', component.get('SUMMARY'))
								print(component.get('SUMMARY'))
								event.add('dtstart', component.get('DTSTART'))
								print(component.get('DTSTART').dt)
								event.add('dtend', component.get('dtend'))
								print(component.get('dtend').dt)
								event.add('dtstamp', component.get('dtstamp'))
								print(component.get('dtstamp').dt)
								event.add('location', component.get('location'))
								print(component.get('LOCATION'))
								event['uid'] = component.get('UID')
								cal.add_component(event)

						g.close()


						timestamp = datetime.fromtimestamp(data["timestamp"])
						event = Event()
						event.add('summary', data["description"])        
						event.add('dtstart',timestamp)
						event.add('dtend',timestamp)
						event.add('dtstamp',timestamp)
						event.add('location', data["zvei"])
						event['uid'] = "{0}#{1}".format(timestamp,data["description"])
						cal.add_component(event)
						with open(globalVars.config.get("2calendar", "filepath2calendar")+'alle.ics', 'wb') as f:
							f.write(cal.to_ical())
					else:
						logging.warning("Nicht unterstützter Typ: %s", typ)
				except:
					logging.error("cannot Insert %s", typ)
					logging.debug("cannot Insert %s", typ, exc_info=True)
					return

	except:
		logging.error("unknown error")
		logging.debug("unknown error", exc_info=True)
