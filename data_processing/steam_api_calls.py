import json

with open(r"apikey.json") as f:
    api_userid = json.load(f)

api_key = api_userid["steam_api_key"]
user_id = api_userid["user_id"]

