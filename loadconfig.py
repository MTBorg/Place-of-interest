import logging
import json
import os

def load_json_file():

    """Loads file and returns all the data
    
    Returns
    ----------
    A dictionary with all the data from the json config file
    """
    dirname = os.path.dirname(__file__)
    logging.info("dirname %s", dirname)
    if (dirname == ""): #If the script is run from the same folder we don't want to prepend "/" (as it would result in searching the root)
        filepath = "Config.json"
    else:
        filepath = dirname + "/Config.json"
    logging.info("Reading file %s", filepath)
    with open(filepath) as f:
        filedata = json.load(f)
    return filedata