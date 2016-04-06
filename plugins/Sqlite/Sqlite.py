#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Sqlite-Plugin to dispatch POCSAG - messages to a sqlite database
ZVEI and FMS not implemented yet!

@author: Daniel Klann

@requires: sqlite-Configuration has to be set in the config.ini
@requires: Created Database/Tables, see boswatch.sql
"""

import logging  # Global logger

import sqlite3

from includes import globals  # Global variables

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
# Main function of Sqlite_all-plugin
# will be called by the alarmHandler
#
def run(typ, freq, data):
    """
    This function is the implementation of the Sqlite-Plugin.
    It will store the data to an Sqlite database

    The configuration for the Sqlite-Connection is set in the config.ini.
    For DB- and tablestructure see boswatch.sql

    @type    typ:  string (FMS|ZVEI|POC)
    @param   typ:  Typ of the dataset for sending to BosMon
    @type    data: map of data (structure see interface.txt)
    @param   data: Contains the parameter for dispatch to BosMon.
    @type    freq: string
    @keyword freq: frequency is not used in this plugin

    @requires: Sqlite-Configuration has to be set in the config.ini
    @requires: Created Database/Tables, see boswatch.sql

    @return:    nothing
    """
    try:
        if configHandler.checkConfig("Sqlite"):  # read and debug the config

            try:
                #
                # Connect to Sqlite
                #
                logging.debug("connect to Sqlite")
                dbPath = globals.config.get("Sqlite", "database_path")
                dbName = globals.config.get("Sqlite", "database_name")
                connection = sqlite3.connect("dbPath" + "dbName")
                cursor = connection.cursor()
            except:
                logging.error("cannot connect to Sqlite")
                logging.debug("cannot connect to Sqlite", exc_info=True)
            else:  # Without connection, plugin couldn't work
                try:
                    #
                    # Create and execute SQL-statement
                    #
                    logging.debug("Insert %s", typ)

                    if typ == "POC":
                        # strMsg = data["msg"]
                        # strDescription = data["description"]
                        # strUTFmsg = strMsg.decode('utf-8')
                        # strUTFDescription = strDescription.decode('utf-8')

                        cursor.execute("INSERT INTO " + globals.config.get("Sqlite", "tablePOC") + " (time,ric,function,functionChar,msg,bitrate,description) VALUES (strftime('%Y-%m-%d %H:%M:%S','now'),?,?,?,?,?,?)",
                                       (data["ric"], data["function"], data["functionChar"], data["msg"], data["bitrate"], data["description"]))
                        logging.info("Daten in Sqlite geschrieben")
                    else:
                        logging.warning("Invalid Typ: %s", typ)
                except:
                    logging.error("cannot Insert %s", typ)
                    # logging.error("Nachrichtentext %s", data["msg"])
                    # logging.error("Text in UTF %s", strUTFmsg)
                    # logging.debug("Text in UTF %s", strUTFmsg, exc_info=true)
                    logging.debug("cannot Insert %s", typ, exc_info=True)
                    return

            finally:
                logging.debug("close Sqlite")
                try:
                    connection.commit()
                    cursor.close()
                    connection.close()  # Close connection in every case
                except:
                    pass

    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
