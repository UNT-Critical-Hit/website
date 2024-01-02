from dataclasses import dataclass
from datetime import datetime
from zenora import OwnUser

@dataclass
class User():
    """
    Holds information for any queried user
    :param id: The user's ID
    :param name: The user's name
    :param discriminator: The user's discriminator
    :param nickname: The user's nickname
    :param officer: Whether the user is an officer
    :param developer: Whether the user is a developer
    :param verified: Whether the user is verified
    :param guest: Whether the user is a guest
    :param player: Whether the user is a player
    :param dm: Whether the user is a DM
    :param banned_player: Whether the user is a banned player
    :param banned_dm: Whether the user is a banned DM
    :param joined: When the user joined
    :param campaigns_player: List of campaigns the user is a player in
    :param campaigns_dm: List of campaigns the user is a DM in
    """

    first_name = ""
    last_name = ""
    unt_student = None
    unt_email = ""

    id: int = 0
    name: str = ""
    discriminator: str = ""
    nickname: str = ""
    officer: bool = False
    developer: bool = False
    verified: bool = False
    guest: bool = False
    player: bool = False
    dm: bool = False
    banned_player: bool = False
    banned_dm: bool = False
    joined: str = ""
    campaigns_player: list[int] = None
    campaigns_dm: list[int] = None

    # Returns None if can join and a string with the reason if they can't
    def can_join(self):
        if not self.joined:
            return "You have not joined the Discord yet! Please click <a href=\"https://discord.gg/9ptD2dr3Yr\">here</a> to join."
        if not self.verified:
            return "You have not been verified in the Discord yet! Please go to the #verification channel and follow the steps to get verified."
        if self.banned_player:
            return "You have been blocked from being a player due to a warning received in the past."
        
    def can_create(self, db):
        if not self.joined:
            return "You have not joined the Discord yet! Please click <a href=\"https://discord.gg/9ptD2dr3Yr\">here</a> to join."
        if not self.verified:
            return "You have not been verified in the Discord yet! Please go to the #verification channel and follow the steps to get verified."
        if self.banned_dm:
            return "You have been blocked from being a Dungeon Master due to a warning received in the past."
        
        return None # remove for release 2
        
        dm_doc = db.collection('documents').document('dungeon-master-agreement').get().to_dict()
        user_doc = db.collection('users').document(str(self.id)).get().to_dict()
        try:
            if user_doc['documents']['dungeon-master-agreement']['signed'] < dm_doc['last_updated']:
                return "There has been an update to the Dungeon Master Agreement which requires you to re-sign it."
        except KeyError:
            return "You have not yet signed the Dungeon Master Agreement."

        return None
    
    def sign_document(self, db, id):
        doc_ref = db.collection('users').document(str(self.id))
        doc = doc_ref.get().to_dict()
        try:
            doc['documents'][id] = {'signed': datetime.now()}
        except KeyError:
            doc['documents'] = {id: {'signed': datetime.now()}}
        doc_ref.set(doc)