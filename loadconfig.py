import logging
import json
import os

def load_json_file():

    """Loads file and returns all the data
    
    Returns
    ----------
    A dictionary with all the data from the json config file
    """

    filepath = os.path.dirname(os.path.realpath(__file__)) + "/Config.json"  
    with open(filepath) as f:
        filedata = json.load(f)
    return filedata