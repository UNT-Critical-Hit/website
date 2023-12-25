from dataclasses import dataclass
from datetime import datetime
import typing

@dataclass
class CampaignActionRequest:
    first_name: str
    last_name: str
    discord_tag: str
    campaign_name: str
    action: str
    reasons: typing.Optional[list[str]]
    elaboration: typing.Optional[str]
    new_player_count: typing.Optional[int]