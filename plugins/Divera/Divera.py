#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Divera-Plugin to send FMS-, ZVEI- and POCSAG - messages to Divera
@author: Marco Grosjohann
@requires: Divera-Configuration has to be set in the config.ini
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
# Main function of Divera-plugin
# will be called by the alarmHandler
#
def run(typ, freq, data):
    """
    This function is the implementation of the Divera-Plugin.
    It will send the data to Divera API
    @type    typ:  string (FMS|ZVEI|POC)
    @param   typ:  Typ of the dataset
    @type    data: map of data (structure see readme.md in plugin folder)
    @param   data: Contains the parameter
    @type    freq: string
    @keyword freq: frequency of the SDR Stick
    @requires:  Divera-Configuration has to be set in the config.ini
    @return:    nothing
    """
    try:
        if configHandler.checkConfig("Divera"):  # read and debug the config

            if typ == "FMS":
                #
                # building message for FMS
                #
                text = globalVars.config.get("Divera", "fms_text")
                title = globalVars.config.get("Divera", "fms_title")
                priority = globalVars.config.get("Divera", "fms_prio")
                vehicle = globalVars.config.get("Divera", "fms_vehicle")

            elif typ == "ZVEI":
                #
                # building message for ZVEI
                #
                text = globalVars.config.get("Divera", "zvei_text")
                title = globalVars.config.get("Divera", "zvei_title")
                priority = globalVars.config.get("Divera","zvei_std_prio")
                ric = globalVars.config.get("Divera","zvei_ric")

            elif typ == "POC":
                #
                # building message for POC
                #
                if data["function"] == '1':
                    priority = globalVars.config.get("Divera", "SubA")
                elif data["function"] == '2':
                    priority = globalVars.config.get("Divera", "SubB")
                elif data["function"] == '3':
                    priority = globalVars.config.get("Divera", "SubC")
                elif data["function"] == '4':
                    priority = globalVars.config.get("Divera", "SubD")
                else:
                    priority = ''
                        
                text = globalVars.config.get("Divera", "poc_text")
                title = globalVars.config.get("Divera", "poc_title")
                ric = globalVars.config.get("Divera", "poc_ric")

            else:
                logging.warning("Invalid type: %s", typ)
                return

        try:
            #
            # Divera-Request
            #
            logging.debug("send Divera for %s", typ)

            # replace the wildcards
            text = wildcardHandler.replaceWildcards(text, data)
            title = wildcardHandler.replaceWildcards(title, data)
            if typ == "FMS":
                vehicle = wildcardHandler.replaceWildcards(vehicle, data)
            else:
                ric = wildcardHandler.replaceWildcards(ric, data)
            
            
            # Logging data to send
            logging.debug("Title   : %s", title)
            if typ == "FMS":
                logging.debug("Vehicle     : %s", vehicle)
            else:
                logging.debug("RIC     : %s", ric)
            logging.debug("Text    : %s", text)
            logging.debug("Priority: %s", priority)
				
            # check priority value
            if (priority != 'false') and (priority != 'true'):
                logging.info("No Priority set for type '%s'! Skipping Divera-Alarm!", typ)
                return

            # Check FMS
            if typ == "FMS":
                if (vehicle == ''):
                    logging.info("No Vehicle set!");
            
            else:
                if (ric == ''):
                    logging.info("No RIC set!");
            
            # start connection to Divera                
            if typ == "FMS":
                # start the connection FMS
                conn = httplib.HTTPSConnection("www.divera247.com:443")
                conn.request("GET", "/api/fms",
                             urllib.urlencode({
                                "accesskey": globalVars.config.get("Divera", "accesskey"),
                                "vehicle_ric": vehicle,
                                "title": title,
                                "text": text,
                                "priority": priority,
                            }))
                            
            else:
            # start connection ZVEI / POC
                conn = httplib.HTTPSConnection("www.divera247.com:443")
                conn.request("GET", "/api/alarm",
                            urllib.urlencode({
                                "accesskey": globalVars.config.get("Divera", "accesskey"),
                                "title": title,
                                "ric": ric,
                                "text": text,
                                "priority": priority,
                            }))

        except:
            logging.error("cannot send Divera request")
            logging.debug("cannot send Divera request", exc_info=True)
            return

        try:
            #
            # check Divera-Response
            #
            response = conn.getresponse()
            if str(response.status) == "200":  # Check Divera Response and print a Log or Error
                logging.debug("Divera response: %s - %s", str(response.status), str(response.reason))
            else:
                logging.warning("Divera response: %s - %s", str(response.status), str(response.reason))
        except:  # otherwise
            logging.error("cannot get Divera response")
            logging.debug("cannot get Divera response", exc_info=True)
            return

        finally:
            logging.debug("close Divera-Connection")
            try:
                request.close()
            except:
                pass

    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
