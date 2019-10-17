#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Pushover-Plugin to send FMS-, ZVEI- and POCSAG - messages to Pushover Clients

@author: Ricardo Krippner

@requires: Pushover-Configuration has to be set in the config.ini
"""

import logging  # Global logger
import httplib  # for the HTTP request
import urllib
from includes import globalVars  # Global variables

# from includes.helper import timeHandler
from includes.helper import configHandler
from includes.helper import wildcardHandler


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
# Main function of Pushover-plugin
# will be called by the alarmHandler
#
def run(typ, freq, data):
    """
    This function is the implementation of the Pushover-Plugin.
    It will send the data to Pushover API

    @type    typ:  string (FMS|ZVEI|POC)
    @param   typ:  Typ of the dataset
    @type    data: map of data (structure see readme.md in plugin folder)
    @param   data: Contains the parameter
    @type    freq: string
    @keyword freq: frequency of the SDR Stick

    @requires:  Pushover-Configuration has to be set in the config.ini

    @return:    nothing
    """
    try:
        if configHandler.checkConfig("Pushover"):  # read and debug the config

            if typ == "FMS":
                #
                # building message for FMS
                #

                message = globalVars.config.get("Pushover", "fms_message")
                title = globalVars.config.get("Pushover", "fms_title")
                priority = globalVars.config.get("Pushover", "fms_prio")
                logging.debug("Sending message: %s", message)

            elif typ == "ZVEI":
                #
                # building message for ZVEI
                #
                if globalVars.config.get("Pushover", "zvei_sep_prio") == '1':
			if data["zvei"] in globalVars.config.get("Pushover", "zvei_prio2"):
				priority = '2'
			elif data["zvei"] in globalVars.config.get("Pushover","zvei_prio1"):
				priority = '1'
			elif data["zvei"] in globalVars.config.get("Pushover","zvei_prio0"):
				priority = '0'
			else:
				priority = '-1'
		else:
			priority = globalVars.config.get("Pushover","zvei_std_prio")

                message = globalVars.config.get("Pushover", "zvei_message")
                title = globalVars.config.get("Pushover", "zvei_title")
                logging.debug("Sending message: %s", message)

            elif typ == "POC":

                #
                # Pushover-Request
                #
                logging.debug("send Pushover for %s", typ)
                if globalVars.config.get("Pushover", "poc_spec_ric") == '0':
			if data["function"] == '1':
                        	priority = globalVars.config.get("Pushover", "SubA")
                    	elif data["function"] == '2':
                        	priority = globalVars.config.get("Pushover", "SubB")
                    	elif data["function"] == '3':
	                        priority = globalVars.config.get("Pushover", "SubC")
        	        elif data["function"] == '4':
                	        priority = globalVars.config.get("Pushover", "SubD")
                    	else:
                        	priority = 0
                else:
                    	if data["ric"] in globalVars.config.get("Pushover", "poc_prio2"):
                        	priority = 2
			elif data["ric"] in globalVars.config.get("Pushover","poc_prio1"):
			        priority = 1
                    	elif data["ric"] in globalVars.config.get("Pushover","poc_prio0"):
			        priority = 0
			else:
				priority = -1
                        
                message = globalVars.config.get("Pushover", "poc_message")
                title = globalVars.config.get("Pushover", "poc_title")

            else:
                logging.warning("Invalid type: %s", typ)

            try:
                # replace the wildcards
                message = wildcardHandler.replaceWildcards(message, data)
                title = wildcardHandler.replaceWildcards(title, data)
                sound = globalVars.config.get("Pushover", "sound")
                # set Default-Sound
                if not sound:
                        sound = "pushover"

                # start the connection
                conn = httplib.HTTPSConnection("api.pushover.net:443")
                conn.request("POST", "/1/messages.json",
                             urllib.urlencode({
                                 "token": globalVars.config.get("Pushover", "api_key"),
                                 "user": globalVars.config.get("Pushover", "user_key"),
                                 "message": message,
                                 "html": globalVars.config.get("Pushover", "html"),
                                 "title": title,
                                 "sound": sound,
                                 "priority": priority,
                                 "retry": globalVars.config.get("Pushover", "retry"),
                                 "expire": globalVars.config.get("Pushover", "expire")
                             }), {"Content-type": "application/x-www-form-urlencoded"})

            except:
                logging.error("cannot send Pushover request")
                logging.debug("cannot send Pushover request", exc_info=True)
                return

            try:
                #
                # check Pushover-Response
                #
                response = conn.getresponse()
                if str(response.status) == "200":  # Check Pushover Response and print a Log or Error
                    logging.debug("Pushover response: %s - %s", str(response.status), str(response.reason))
                else:
                    logging.warning("Pushover response: %s - %s", str(response.status), str(response.reason))
            except:  # otherwise
                logging.error("cannot get Pushover response")
                logging.debug("cannot get Pushover response", exc_info=True)
                return

            finally:
                logging.debug("close Pushover-Connection")
                try:
                    request.close()
                except:
                    pass

    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
