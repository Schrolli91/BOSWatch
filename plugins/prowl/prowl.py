#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
prowl Plugin to push POCSAG to iOS
https://www.prowlapp.com/

@author: Daniel Klann

@requires: prowl-Configuration has to be set in the config.ini
"""

#
# Imports
#
import logging  # Global logger
from includes import globals  # Global variables

# Helper function, uncomment to use
# from includes.helper import timeHandler
# from includes.helper import wildcardHandler
from includes.helper import configHandler

from includes import pushnotify


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
    @exception: Exception if init has an fatal error so that the plugin couldn't work

    """
    try:
        ########## User onLoad CODE ##########
        pass
    ########## User onLoad CODE ##########
    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
        raise


##
#
# Main function of plugin
# will be called by the alarmHandler
#
def run(typ, freq, data):
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
    try:
        if configHandler.checkConfig("prowl"):  # read and debug the config (let empty if no config used)

            # apikey = globals.config.get("prowl", "APIKey")
            prio = globals.config.getint("prowl", "priority")
            # app_name = globals.config.get("prowl", "appName")

            ########## User Plugin CODE ##########
            if typ == "FMS":
                logging.warning("%s not supported", typ)
            elif typ == "ZVEI":
                logging.warning("%s not supported", typ)
            elif typ == "POC":
                strMsg = data["msg"]
                strDescription = data["description"]
                strUTFmsg = strMsg.decode('utf-8')
                strUTFDescription = strDescription.decode('utf-8')

                #client = pushnotify.get_client('prowl', application='pushnotify examples')
                client = pushnotify.get_client('prowl', application=globals.config.get("prowl", "appName"))
                #client.add_key(apikey)
                client.add_key(globals.config.get("prowl", "APIKey"))

                event = data["functionChar"] + ": " + strUTFDescription + " (" + data["ric"] + ")"
                desc = strUTFmsg

                try:
                    client.notify(desc, event, split=True, kwargs={'priority': prio})
                except pushnotify.exceptions.ApiKeyError:
                    pass
                except:
                    logging.error("pushnotify error")
                    logging.debug("pushnotify error", exc_info=True)
            else:
                logging.warning("Invalid Typ: %s", typ)
            ########## User Plugin CODE ##########

    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
