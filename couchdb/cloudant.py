from .server import Server

class Cloudant(Server):

    def __init__(self, user, password):
        super().__init__('https://{}.cloudant.com/'.format(user))
        self.login(user, password)
