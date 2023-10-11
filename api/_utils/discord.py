import requests
import json
from _utils.Campaign import Campaign

def get_campaigns():
    resp = requests.get("http://api.midnight.wtf:25713/campaigns?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    campaigns = [generate_struct(campaign, Campaign) for campaign in json.loads(resp.json())]
    return campaigns

def generate_struct(dict_: dict, cls: type):
    obj = cls()
    for key, value in dict_.items():
        setattr(obj, key, value)
    return obj

def get_campaign(id):
    resp = requests.get("http://api.midnight.wtf:25713/campaigns/"+str(id)+"?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    return generate_struct(json.loads(resp.json()), Campaign)