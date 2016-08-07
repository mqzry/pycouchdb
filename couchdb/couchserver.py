import requests

def handle_codes():
        if response.status_code == requests.codes.not_modified:
            return None
        else:
            response.raise_for_status()

def add_forward_slash(url):
    if url.endswith('/'):
        return url
    else:
        return url + '/'

class CouchServer:

    def __init__(self, url):
        self.url = add_forward_slash(url)
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'

    def head_db(self, db_name):
        response = self.session.get(self.url + db_name)
        return response.status_code == requests.codes['ok']

    def get_db(self, db_name):
        response = self.session.get(self.url + db_name)
        if response.status_code == requests.codes['ok']:
            return response.json()
        else:
            return None

    def create_db(self, db_name):
        response = self.session.put(self.url + db_name)
        if response.status_code == requests.codes['created']:
            return True
        else: # Log error message of the different status codes here
            response.raise_for_status();

    def delete_db(self, name):
        return self.session.delete(self.url + name)

    def get(self, db):
        """Get database
        :param db: name of database
        :return: True if authenticated ok
        :rtype: bool
        """
        self.db = db
        self.db_url = self.base_url + db + '/'
        return self.session

    def login(self, user, password):
        self.session.auth = (user, password)

    def logout():
        self.session.auth = None;
        # TODO: Improve 
