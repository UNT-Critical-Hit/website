import requests
from datetime import datetime
from _utils.db import submit_report
from _utils.CampaignActionRequest import CampaignActionRequest

def submit_player(submission, user, campaign, db):
    url = "https://docs.google.com/forms/d/1Xbl5zCFP8XnTAU7EqVEh2aULOB_ojvuJ6B763XAPc28/formResponse"

    unt_email = ""
    if submission['unt_student'] == 'Yes':
        unt_email = submission['unt_email'] + '@my.unt.edu'

    data = {
    "entry.373645330": submission['name_first'],
    "entry.326653529": submission['name_last'],
    "entry.1089152921": user.id,
    "entry.751573787": user.name,
    "entry.1622039573": submission['ttrpg_experience'],
    "entry.1837363259": unt_email,
    "entry.1106922831": campaign.name,
    "entry.1474493223": "Yes",
    }

    r = requests.post(url, params = data)
    print("Response:", r)
    if r.status_code == 200:
        return True
    else:
        submit_report(db, "submit_player", "Response code: " + str(r.status_code), user)
        return False
    
def send_new_application(submission, user, campaign, db):
    url = "https://api.midnight.wtf/campaigns/apply?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a"

    unt_email = ""
    if submission['unt_student'] == 'Yes':
        unt_email = submission['unt_email'] + '@my.unt.edu'

    data = {
    "campaigns": [
        campaign.name
    ],
    "first_name": submission['name_first'],
    "last_name": submission['name_last'],
    "discord_tag": user.name,
    "discord_id": user.id,
    "unt_email": unt_email
    }

    r = requests.post(url, json=data)
    print("Response:", r)
    if r.status_code == 200:
        return True
    else:
        submit_report(db, "send_new_application", "Response code: " + str(r.status_code), user)
        return False

def submit_dm(submission, user, db):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSeNbRUnipi4PUt5xSakmKEpC0wXIW2-Ns19GffKwzdBfM18KQ/formResponse"

    location = submission['location']
    if location == 'In-person':
        location = submission['location_inperson']
        if location == 'Other':
            location = submission['location_inperson_other']

    date = ""
    day = ""
    if submission['frequency'] == 'Once (one-shot)':
        date = submission['date']
    else:
        day = submission['day']

    playstyle = ""
    if submission['dm_experience'] == 'Yes':
        playstyle = submission['playstyle']

    session_length = ""
    if int(submission['session_length_hours']) == 0:
        session_length = submission['session_length_minutes'] + " minutes"
    elif int(submission['session_length_minutes']) == 0:
        session_length = submission['session_length_hours'] + " hours"
    else:
        session_length = submission['session_length_hours'] + " hours and " + submission['session_length_minutes'] + " minutes"

    unt_email = user.unt_email
    if not unt_email:
        unt_email = "N/A"
    else:
        unt_email += "@my.unt.edu"

    data = {
    "entry.199046626": submission['campaign_name'], # campaign title
    "entry.921050634": submission['name_first'], # first name
    "entry.953372418": submission['name_last'], # last name
    "entry.723836057": user.name, # discord username
    "entry.557094337": user.id, # discord id
    "entry.1040133704": unt_email, # unt email
    "entry.164145856": submission['dm_experience'], # dm experience
    "entry.1654576497": submission['frequency'], # frequency
    "entry.233268853": day, # day
    "entry.1053096750": submission['time'], # time
    "entry.1843167926": date, # date
    "entry.1307001679": session_length, # session length
    "entry.1140668644": submission['min_players'], # minimum players
    "entry.2096421412": submission['max_players'], # maximum players
    "entry.760477997": submission['system'], # system
    "entry.1310138135": submission['desc'], # description
    "entry.1410994733": location, # location
    "entry.1556498857": submission['new_player_friendly'], # new player friendly
    "entry.527869327": playstyle # playstyle
    }

    r = requests.post(url, params = data)
    print("Response:", r)
    if r.status_code == 200:
        return True
    else:
        submit_report(db, "submit_dm", "Response code: " + str(r.status_code), user)
        return False

def send_new_campaign(submission, user, db):
    url = "https://api.midnight.wtf/campaigns/create?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a"

    location = submission['location']
    if location == 'In-person':
        location = submission['location_inperson']
        if location == 'Other':
            location = submission['location_inperson_other']

    date = ""
    day = ""
    if submission['frequency'] == 'Once (one-shot)':
        if type(submission['date']) == datetime:
            date = submission['date'].strftime('%Y-%m-%d')
        else:
            date = submission['date']
    else:
        day = submission['day']

    playstyle = ""
    if submission['dm_experience'] == 'Yes':
        playstyle = submission['playstyle']

    session_length = ""
    if int(submission['session_length_hours']) == 0:
        session_length = submission['session_length_minutes'] + " minutes"
    elif int(submission['session_length_minutes']) == 0:
        session_length = submission['session_length_hours'] + " hours"
    else:
        session_length = submission['session_length_hours'] + " hours and " + submission['session_length_minutes'] + " minutes"

    data = {
    "name": submission['campaign_name'],
    "dm": {
        "first_name": submission['name_first'],
        "last_name": submission['name_last'],
        "discord_tag": user.name,
        "discord_id": user.id,
        "unt_email": submission['unt_email'] + "@my.unt.edu",
        "dm_experience": submission['dm_experience']
    },
    "min_players": submission['min_players'],
    "max_players": submission['max_players'],
    "info_message": submission['desc'],
    "location": location,
    "playstyle": playstyle,
    "session_length": session_length,
    "meeting_frequency": submission['frequency'],
    "meeting_time": submission['time'],
    "meeting_day": day,
    "meeting_date": date,
    "system": submission['system'],
    "new_player_friendly": submission['new_player_friendly']
    }

    r = requests.post(url, json=data)
    print("Response:", r)
    if r.status_code == 200:
        return True
    else:
        submit_report(db, "send_new_campaign", "Response code: " + str(r.status_code), user)
        return False