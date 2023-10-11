class User:
    def __init__(self, _id: int = 0, name: str = "", discriminator: str = "", nickname: str = "", is_officer: bool = False, is_developer: bool = False, campaigns_player: List[str] = [], campaigns_dm: List[str] = []):
        self.id = _id
        self.name = name
        self.discriminator = discriminator
        self.nickname = nickname
        self.is_officer = is_officer
        self.is_developer = is_developer
        self.campaigns_player = campaigns_player
        self.campaigns_dm = campaigns_dm