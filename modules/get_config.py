import json

# * ====== CONFIG ====== *
def read_json(file) -> dict:
    # doc: This function read the config.json file:    
    f = open(file)
    config = json.load(f)
    return config