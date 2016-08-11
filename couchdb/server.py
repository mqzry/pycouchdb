from based_session import BasedSession
import logging

class Server:

    def __init__(self, url):
        self.session = BasedSession(url)
        self.session.headers['Accept'] = 'application/json'
        self.cached_dbs = self.get_dbs()

    def __repr__(self):
        return '<CouchDB Server at "{}">'.format(self.session.prefix_url)

    def info(self):
        r = self.session.get(self.url)
        return r.json()

    def get_dbs(self):
        r = self.session.get('_all_dbs')
        return self.dbs

    def head_db(self, db_name):
        """Check existence of a database.

        :param db_name: name of database.
        :return: whether this database exists.
        :rtype: boolean
        """
        r = self.session.head(db_name)
        return r.status_code == requests.codes.ok

    def get_db(self, db_name):
        r = self.session.get(db_name)
        if r.status_code == requests.codes.ok:
            # TODO: Return Database object
            return r.json()
        else:
            return None

    def create_db(self, db_name):
        r = self.session.put(db_name)
        if r.status_code == requests.codes.created:
            # TODO: Return Database object
            return True
        else:
            info = r.json()
            logging.info('Tried to create {0} but {1} happend because {2}'
                         .format(db_name, info.error, info.reason))

    def delete_db(self, db_name):
        r = self.session.delete(db_name)
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
        r = self.session.post('_session', json=payload)
        if r.status_code == requests.codes.ok:
            self.auth.user = r.json().name
            self.auth.roles = r.json().roles
            self.auth.method = 'cookie'
            return True
        elif r.status_code == requests.codes.unauthorized:
            logging.info('Failed attempt to login user {0}. Username or password were not recognized.'.format(user))
            return False

    def logout(self):
        if self.auth is None:
            return
        else:
            r = self.session.delete('_session')
            if r.status_code == requests.codes.ok:
                self.auth = None
            elif r.status_code == requests.codes.unauthorized:
                logging.info('Failed attempt to logout user {0}. User wasn’t authenticated.'.format(self.user))

    def get_user_info(self):
        if self.auth is None:
            return
        else:
            r = self.session.get('_session')
            if r.status_code == requests.codes.ok:
                body = r.json()
                self.auth.user = body.userCtx.name
                self.auth.roles = body.userCtx.roles
                self.auth.method = body.info.authenticated
                self.auth.db = body.info.authentication_db
            elif r.status_code == requests.codes.unauthorized:
                logging.info('Failed attempt to logout user {0}.'.format(self.user),
                             'User wasn’t authenticated.')

    def read_log(self, bytes, offset):
        r = self.session.get('_log',headers={'Accept': 'text/plain'})
        if r.status_code == request.codes.ok:
            return r.text
        elif r.status_code == requests.codes.unauthorized:
            logging.info('Failed attempt read the log of server at {0}.'.format(self.session.prefix_url)
                         + 'CouchDB Server Administrator privileges required.')

    def get_active_tasks(self):
        r = self.session.get('_active_tasks')
        if r.status_code == request.codes.ok:
            return r.json()
        elif r.status_code == requests.codes.unauthorized:
            logging.info('Failed attempt to read the log of server at {0}.'.format(self.session.prefix_url)
                         + 'CouchDB Server Administrator privileges required.')

    def get_membership(self):
        r = self.session.get('_membership')
        return r.json()

    def get_db_updates(self, feed, timeout=None, heartbeat=None):
        payload = {}
        payload['feed'] = feed
        if timeout is not None:
            payload['timeout'] = timeout
        if heartbeat is not None:
            payload['heartbeat'] = heartbeat

        r = self.session.get('_membership', json=payload)

        if r.status_code == request.codes.ok:
            return r.json()
        elif r.status_code == requests.codes.unauthorized:
            logging.info('Failed attempt to retrieve the list of database events of server at {0}.'.format(self.session.prefix_url)
                         + 'CouchDB Server Administrator privileges required.')

    def post_replication(self, source, target, continuous=None, cancel=None,
                         create_target=None, doc_ids=None, proxy=None):
        payload = {}
        payload['source'] = source
        payload['target'] = target
        if continuous is not None:
            payload['continuous'] = continuous
        if cancel is not None:
            payload['cancel'] = cancel
        if create_target is not None:
            payload['create_target'] = create_target
        if doc_ids is not None:
            payload['doc_ids'] = doc_ids
        if proxy is not None:
            payload['proxy'] = proxy
            
        r = self.session.post('_replicate', json=payload)

        if (r.status_code == requests.codes.ok 
            or r.status_code == requests.codes.accepted):
            return r.json();
        if r.status_code == requests.codes.bad_request:
        if r.status_code == requests.codes.unauthorized:
        if r.status_code == requests.codes.not_found: