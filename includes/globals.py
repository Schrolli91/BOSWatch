#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Global variables

@author: Jens Herrmann
@author: Bastian Schroll
"""

# Global variables
config = 0
script_path = ""
log_path = ""

# double alarm
doubleList = []

# pluginLoader
pluginList = {}

# filter
filterList = []

# idDescribing
fmsDescribtionList  = {}
zveiDescribtionList = {}
ricDescribtionList  = {}

# returns the version or build date
# function -> read only in script
def getVers(mode="vers"):
	if mode == "vers":
		return "2.1-dev"
	elif mode == "date":
		return "2015/07/27"
