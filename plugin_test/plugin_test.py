#!/usr/bin/python
# -*- coding: cp1252 -*-

import time
import pluginloader

#create new logger
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#set log string format
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', '%d.%m.%Y %I:%M:%S')

#create a file loger
fh = logging.FileHandler('boswatch.log', 'w')
fh.setLevel(logging.DEBUG) #log level >= Debug
fh.setFormatter(formatter)
logger.addHandler(fh)

#create a display loger
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR) #log level >= Error
ch.setFormatter(formatter)
logger.addHandler(ch)

#https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
#log levels
#----------
#debug - debug messages only for log
#info - only an information
#warning
#error - normal error - program goes further
#exception - error handler in try:exc: into the message
#critical - critical error, program exit


data = {"zvei":"12345"}

while True:
    time.sleep(1)
    logging.info("Alarm!")
    for i in pluginloader.getPlugins():
        logging.debug("Loading plugin " + i["name"])
        plugin = pluginloader.loadPlugin(i)
        plugin.run("zvei","80000000",data)