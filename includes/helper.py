#!/usr/bin/python
# -*- coding: cp1252 -*-
#

"""
little Helper functions

@author: 		Bastian Schroll
"""

import logging
import time


def freqToHz(freq):
	"""
	gets a frequency and resolve it in Hz
	
	@type    format: string
	@param   format: Python time Format-String
	
	@return:    Formated Time and/or Date
	@exception: Exception if Error in format
	"""		
def curtime(format="%d.%m.%Y %H:%M:%S"):
	try:
		return time.strftime(format)  
	except:
		logging.warning("error in time-format-string")
		logging.debug("error in time-format-string", exc_info=True)