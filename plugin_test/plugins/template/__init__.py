import logging

def run(typ,time,frequenz,data1,data2,data3):
    logging.debug("Throw Template Plugin")
    try:
        logging.debug("try 5/0")
        test = 5/0
    except:
        logging.exception("Error in Template Plugin")