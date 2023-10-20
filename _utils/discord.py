import requests
import json
from _utils.Campaign import Campaign
from _utils.User import User
from requests import ConnectTimeout

def get_campaigns():
    try:
        resp = requests.get("https://api.midnight.wtf/campaigns?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    try:
        campaigns = [generate_struct(campaign, Campaign) for campaign in json.loads(resp.json())]
    except requests.exceptions.JSONDecodeError:
        return None, "The bot returned nothing. Please inform an officer that the bot is down."
    campaigns.reverse()
    return campaigns, None

def generate_struct(dict_: dict, cls: type):
    """
    Generates a struct from a dict
    Usage: generate_struct({"name": "test"}, CampaignInfo) --> CampaignInfo(name="test")
    Usage: generate_struct({"name": "test"}, UserInfo) --> UserInfo(name="test")
    :param dict_: The dict to generate from
    :param cls: The class to generate
    :return: The generated struct
    """
    obj = cls()
    for key, value in dict_.items():
        setattr(obj, key, value)
    return obj

def get_campaign(id):
    try:
        resp = requests.get("https://api.midnight.wtf/campaigns/"+str(id)+"?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    return generate_struct(json.loads(resp.json()), Campaign), None

def get_user(id):
    try:
        resp = requests.get("https://api.midnight.wtf/users/"+str(id)+"?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    return generate_struct(json.loads(resp.json()), User), None