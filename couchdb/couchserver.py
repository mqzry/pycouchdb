import requests
import logging

def handle_codes():
        if r.status_code == requests.codes.not_modified:
            return None
        else:
            r.raise_for_status()

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
        r = self.session.get(self.url + db_name)
        return r.status_code == requests.codes.ok

    def get_db(self, db_name):
        r = self.session.get(self.url + db_name)
        if r.status_code == requests.codes.ok:
            # TODO: Return Database object
            return r.json()
        else:
            return None

    def create_db(self, db_name):
        r = self.session.put(self.url + db_name)
        if r.status_code == requests.codes.created:
            # TODO: Return Database object
            return True
        else:
            info = r.json()
            logging.info('Tried to create {0} but {1} happend because {2}'
                         .format(db_name, info.error, info.reason))

    def delete_db(self, db_name):
        r = self.session.delete(self.url + db_name)
        if r.status_code == requests.codes.ok:
            return True
        elif r.status_code == requests.codes.bad_request:
            logging.info('Failed attempt to delete database {0}. The request url {1} is not valid.'.format(db_name, r.url)
                         + 'Probably a invalid database name or forgotten document id by accident.')
        elif r.status_code == requests.codes.not_found:
            logging.info('Failed attempt to delete database {0}. It does not exist.'.format(db_name))
        elif r.status_code == requests.codes.unauthorized:
            logging.info('Failed attempt to delete database {0}. CouchDB Server Administrator privileges required.'.format(db_name))
        return False

    def login(self, user, password):
        ''' Login to the server. Save the cookie token in the session.
        The redirect parameter called next is not supported.'''

        payload = {'name': user, 'password': password}
        r = self.session.post(self.url + '_session', json=payload)
        if r.status_code == requests.codes.ok:
            self.user = r.json().name
            self.user_roles = r.json().roles
            return True
        elif r.status_code == requests.codes.unauthorized:
            logging.info('Failed attempt to login user {0}. Username or password were not recognized.'.format(user))
            return False


    def logout():
        if self.user is None:
            return
        else:
            r = self.session.delete(self.url + '_session', json=payload)
            if r.status_code == requests.codes.ok:
                self.user = None
                self.user_roles = None
            elif r.status_code == requests.codes.unauthorized:
                logging.info('Failed attempt to logout user {0}. User wasn’t authenticated.'.format(self.user))
