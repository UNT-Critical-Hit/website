import requests
import json
from _utils.Campaign import Campaign
from _utils.User import User
from requests import ConnectTimeout
from _utils.db import submit_report

def get_campaigns(db, user):
    try:
        resp = requests.get("https://api.midnight.wtf/campaigns?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        submit_report(db, "get_campaigns", "Connection to the bot timed out", user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    try:
        campaigns = [generate_struct(campaign, Campaign) for campaign in json.loads(resp.json())]
    except requests.exceptions.JSONDecodeError:
        submit_report(db, "get_campaigns", "The bot returned nothing", user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
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

def get_campaign(id, db, user = None):
    try:
        resp = requests.get("https://api.midnight.wtf/campaigns/"+str(id)+"?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        submit_report(db, "get_campaign", "Connection to the bot timed out", user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    if resp.status_code != 200:
        print("Status code:",resp.status_code)
        submit_report(db, "get_campaign", "Bot returned nothing for campaign " + str(id), user)
        return None, "Campaign not found. Please ensure that you are applying for a valid campaign."
    return generate_struct(json.loads(resp.json()), Campaign), None

def get_user(id, db, user):
    try:
        resp = requests.get("https://api.midnight.wtf/users/"+str(id)+"?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        submit_report(db, "get_user", "Connection to the bot timed out", user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    except requests.exceptions.JSONDecodeError:
        submit_report(db, "get_user", "The bot returned nothing", user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    return generate_struct(json.loads(resp.json()), User), None