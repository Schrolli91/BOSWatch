#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Search for decode string and call the right decoder function

@author: Jens Herrmann

@requires: none
"""

import logging # Global logger

def decode(freq, decoded):
	"""
	Search for decode string and call the right decoder function

	@type    freq: string
	@param   freq: frequency of the SDR Stick
	@type    decoded: string
	@param   decoded: RAW Information from Multimon-NG

	@return:    nothing
	@exception: Exception if decoder file call failed
	"""
	try:
		# FMS Decoder Section
		# check FMS: -> check CRC -> validate -> check double alarm -> log
		if "FMS:" in decoded:
			logging.debug("received FMS")
			from includes.decoders import fms
			fms.decode(freq, decoded)

		# ZVEI Decoder Section
		# check ZVEI: -> validate -> check double alarm -> log
		elif "ZVEI2:" in decoded:
			logging.debug("received ZVEI")
			from includes.decoders import zvei
			zvei.decode(freq, decoded)

		# POCSAG Decoder Section
		# check POCSAG -> validate -> check double alarm -> log
		elif "POCSAG512:" in decoded or "POCSAG1200:" in decoded or "POCSAG2400:" in decoded:
			logging.debug("received POCSAG")
			from includes.decoders import poc
			poc.decode(freq, decoded)

	except:
		logging.exception("cannot start decoder")
