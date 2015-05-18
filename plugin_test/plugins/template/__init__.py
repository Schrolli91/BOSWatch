import logging

def run(typ,freq,data):
    logging.debug("Throw Template Plugin")
    try:
        logging.info("ZVEI: %s wurde auf %s empfangen!", data["zvei"],freq)
        logging.debug("try 5/0")
        test = 5/0
    except:
        logging.exception("Error in Template Plugin")