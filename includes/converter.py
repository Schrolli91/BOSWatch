#!/usr/bin/python
# -*- coding: cp1252 -*-
#

"""
convert frequency to Hz

@author: 		Bastian Schroll
"""

import logging

def freqToHz(freq):
	"""
	gets a frequency and resolve it in Hz
	
	@type    freq: string
	@param   freq: frequency of the SDR Stick
	
	@return:    frequency in Hz
	@exception: Exception if Error by recalc
	"""
	try:
		freq = freq.replace("k","e3").replace("M","e6")
		# freq has to be interpreted as float first...
		# otherwise you will get the error: an invalid literal for int() with base 10
		return int(float(freq))
	except:
		logging.exception("Error in freqToHz()")