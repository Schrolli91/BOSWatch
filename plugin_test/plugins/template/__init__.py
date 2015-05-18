#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging # Global logger
import globals # Global variables

def run(typ,freq,data):
    logging.debug("Strat Plugin: template")
    try:
        logging.info("ZVEI: %s wurde auf %s empfangen!", data["zvei"],freq)
        logging.debug("try 5/0")
        test = 5/0
    except:
        logging.exception("Error in Template Plugin")