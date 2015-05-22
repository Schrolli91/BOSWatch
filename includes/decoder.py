#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

def decode(freq, decoded):
		
	#FMS Decoder Section    
	#check FMS: -> check CRC -> validate -> check double alarm -> log
	if "FMS:" in decoded:   
		logging.debug("recieved FMS")
		from includes.decoders import fms
		fms.decode(freq, decoded)

	#ZVEI Decoder Section
	#check ZVEI: -> validate -> check double alarm -> log     
	if "ZVEI2:" in decoded:
		logging.debug("recieved ZVEI")			
		from includes.decoders import zvei
		zvei.decode(freq, decoded)
		
	#POCSAG Decoder Section
	#check POCSAG -> validate -> check double alarm -> log      
	if "POCSAG" in decoded:
		logging.debug("recieved POCSAG")				
		from includes.decoders import poc
		poc.decode(freq, decoded)
