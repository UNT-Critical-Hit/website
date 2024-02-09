import requests
import json
from _utils.Campaign import Campaign
from _utils.User import User
from requests import ConnectTimeout
from _utils.db import submit_report
from zenora import OwnUser
from firebase_admin import firestore

def get_campaigns_by_id(db: firestore.client, user: OwnUser, ids: list):
    try:
        resp = requests.get("https://api.midnight.wtf/campaigns/getmany/" + str(ids) + "?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        submit_report(db, "get_campaigns_by_id", "Connection to the bot timed out", user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    try:
        campaigns = [generate_struct(campaign, Campaign) for campaign in json.loads(resp.json())]
    except requests.exceptions.JSONDecodeError:
        submit_report(db, "get_campaigns", "The bot returned nothing", user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    return campaigns, None

def get_campaigns(db: firestore.client, user: OwnUser):
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

def get_campaign(id: int, db: firestore.client, user: OwnUser = None):
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

def get_user(id: int, db: firestore.client, current_user: OwnUser):
    try:
        resp = requests.get("https://api.midnight.wtf/users/"+str(id)+"?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a")
    except ConnectTimeout:
        submit_report(db, "get_user", "Connection to the bot timed out", current_user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    except requests.exceptions.JSONDecodeError:
        submit_report(db, "get_user", "The bot returned nothing", current_user)
        return None, "Connection to the bot timed out. Please inform an officer that the bot is down."
    except Exception as ex:
        submit_report(db, "get_user", "Unknown error: {0}".format(ex.__name__))
        return None, "An unknown error occured."
    return generate_struct(json.loads(resp.json()), User), None

def create_user(id: int, db: firestore.client, user: User):
    url = "https://api.midnight.wtf/users/{id}/update?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a".format(id=id)
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'id': user.id,
        'unt_email': user.unt_email,
        'unt_student': user.unt_student
    }
    r = requests.post(url, json=data)
    print("Response:", r)
    if r.status_code == 200:
        return True
    else:
        submit_report(db, "update_user", "Response code: " + str(r.status_code), user)
        return False

def update_user(id: int, db: firestore.client, user: User):
    url = "https://api.midnight.wtf/users/{id}/update?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a".format(id=id)
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'id': user.id,
        'unt_email': user.unt_email,
        'unt_student': user.unt_student
    }
    r = requests.post(url, json=data)
    print("Response:", r)
    if r.status_code == 200:
        return True
    else:
        submit_report(db, "update_user", "Response code: " + str(r.status_code), user)
        return False