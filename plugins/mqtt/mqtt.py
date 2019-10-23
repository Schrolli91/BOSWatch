#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
MQTT-Plugin to send FMS-, ZVEI- and POCSAG - messages to a MQTT-Broker
@author: Marco Grosjohann
@requires: MQTT-Configuration has to be set in the config.ini and library paho-mqtt is required
Installation: 
    sudo apt-get install python-pip
    sudo apt-get install python3-pip

    sudo pip install paho-mqtt (Python 2.x)
    sudo pip3 install paho-mqtt (Python 3.x)
"""

import logging  # Global logger
import paho.mqtt.client as mqtt #import the client
from includes import globalVars  # Global variables

# from includes.helper import timeHandler
from includes.helper import configHandler
from includes.helper import wildcardHandler

def isSignal(poc_id):
    """
    @type    poc_id: string
    @param   poc_id: POCSAG Ric

    @requires:  Configuration has to be set in the config.ini

    @return:    True if the Ric is Signal, other False
    @exception: none
    """
    # If RIC is Signal return True, else False
    if globalVars.config.get("POC", "netIdent_ric"):
        if poc_id in globalVars.config.get("POC", "netIdent_ric"):
            logging.info("RIC %s is net ident", poc_id)
            return True
        else:
            logging.info("RIC %s is no net ident", poc_id)
            return False



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
        if configHandler.checkConfig("mqtt"):  # read and debug the config

            if typ == "FMS":
                #
                # building message for FMS
                #
                message = globalVars.config.get("mqtt", "fms_message")

            elif typ == "ZVEI":
                #
                # building message for ZVEI
                #
                message = globalVars.config.get("mqtt", "zvei_message")

            elif typ == "POC":
                if isSignal(data["ric"]):
                    return
                #
                # building message for POC
                #
                message = globalVars.config.get("mqtt", "poc_message")

            else:
                logging.warning("Invalid type: %s", typ)
                return

            try:
                #
                # MQTT-Request
                #
                logging.debug("send MQTT for %s", typ)

                # replace the wildcards
                message = wildcardHandler.replaceWildcards(message, data)
                topic = globalVars.config.get("mqtt", "topic")

                # Logging data to send
                logging.debug("Topic   : %s", topic)
                logging.debug("Message : %s", message)

                # start the connection
                client = mqtt.Client()
                client.connect(globalVars.config.get("mqtt", "broker_address"))
                client.publish(topic, message)

            except:
                logging.error("Error sending Data to MQTT")
                logging.debug("Error sending Data to MQTT", exc_info=True)

    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
