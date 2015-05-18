#!/usr/bin/python
# -*- coding: cp1252 -*-

import time
import pluginloader

import logging
logging.basicConfig(filename='boswatch.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d.%m.%Y %I:%M:%S')

#https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
#log levels
#debug - debug messages only for log
#info - only an information
#warning
#error - normal error - program goes further
#exception - error handler in try:exc: into the message
#critical - big error, program exit

while True:
    time.sleep(1)
    print ("Alarm!")
    logging.info("Alarm!")
    for i in pluginloader.getPlugins():
        logging.debug("Loading plugin " + i["name"])
        plugin = pluginloader.loadPlugin(i)
        plugin.run("zvei","","12345","","")