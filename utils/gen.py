import json

def listToJSON(listForm):
    safe_json = json.dumps(listForm)
    return safe_json
