from dataclasses import dataclass
from datetime import datetime
import typing
from _utils.User import User
from _utils.db import submit_report
import requests

@dataclass
class CampaignActionRequest():
    first_name: str = ""
    last_name: str = ""
    id: int = 0
    actions: str = ""
    campaign_name: str = ""
    action: str = ""
    reasons: typing.Optional[str] = ""
    elaboration: typing.Optional[str] = ""
    new_player_count: typing.Optional[int] = 0

    def __init__(self, user: User):
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.id = user.id

    def submit(self, campaign, db, user):
        url = "https://api.midnight.wtf/campaigns/{id}/action?auth=1e071fa5-f022-44fc-b884-b5e36bc0c80a".format(id=str(campaign.id))
        data = self.__dict__

        r = requests.post(url, json=data)
        print ("Response:",r)
        if r.status_code == 200:
            return True
        else:
            submit_report(db, "submit_campaign_action_request", "Response code: " + str(r.status_code), user)
            return False
        
    def fill(self, submission):
        pass