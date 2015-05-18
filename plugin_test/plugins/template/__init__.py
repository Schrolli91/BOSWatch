import logging

def run(typ,frequenz,daten):
    logging.debug("Throw Template Plugin")
    try:
        logging.info("ZVEI: %s wurde empfangen!", daten[0])
        logging.debug("try 5/0")
        test = 5/0
    except:
        logging.exception("Error in Template Plugin")