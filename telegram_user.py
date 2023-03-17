class tg_user(object):
    def __init__(self, uid: int, username: str = None, first_name: str = None, last_name: str = None, user_trust: int = 0, comments: list = None, is_bot: int = 0, lg_code: str = None, admin: int = 0) -> None:
        self.id = uid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.trust_factor = user_trust
        self.comments = comments
        self.is_bot = is_bot
        self.lg_code = lg_code
        self.admin = admin

    def name(self) -> str:
        return self.username

    def uid(self) -> int:
        return self.id

    def getComments(self) -> list:
        return self.comments

    def getTrustfactor(self) -> int:
        return self.trust_factor

    def isAdmin(self) -> bool:
        print(self.id, self.username, "is trying to check adm", self.admin)
        if self.admin == 1:
            return True
        else:
            return False

    def setTrustfactor(self, deltaTrust: int = 0):
        if self.trust_factor != None:
            self.trust_factor += deltaTrust
        else:
            self.trust_factor = deltaTrust
        return self
    def setLgcode(self, text: str = None):
        self.lg_code = text
        return self

