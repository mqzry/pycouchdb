import couchDB


class Cloudant(couchDB.CouchDB):

    def __init__(self, user, password):
        super().__init__('https://{}.cloudant.com/'.format(user), user, password)
