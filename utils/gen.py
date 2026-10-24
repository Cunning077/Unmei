import json
import sys

def listToJSON(listForm):
    safe_json = json.dumps(listForm)
    return safe_json

def globalQuit():
    raise SystemExit
