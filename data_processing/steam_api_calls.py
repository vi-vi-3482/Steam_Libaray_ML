import json

with open(r"apikey.json") as f:
    api_key = json.load(f)
    api_key = api_key["steam_api_key"]


