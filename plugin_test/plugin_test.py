#!/usr/bin/python
# -*- coding: cp1252 -*-

import time
import pluginloader

while True:
    time.sleep(1)
    print ("Alarm!")
    for i in pluginloader.getPlugins():
        print("Loading plugin " + i["name"])
        plugin = pluginloader.loadPlugin(i)
        plugin.run()