from .document import Document
from requests import codes
import logging

class Database:

    def __init__(self, server, name):
        self.name = name
        self.server = server
        self.session = server.session
        self.session.add_part_to_prefix(name)

    def exists(self):
        return self.head()

    def head(self):
        """Check existence of a database.

        :param self.name: name of database.
        :return: whether this database exists.
        :rtype: boolean
        """
        r = self.session.head()
        return r.status_code == codes.ok

    def get(self):
        r = self.session.get()
        if r.status_code == codes.ok:
            return r.json()
        else:
            return None

    def put(self):
        r = self.session.put()
        if r.status_code == codes.created:
            return True
        else:
            info = r.json()
            logging.info('Tried to create {0} but {1} happend because {2}'
                         .format(self.name, info['error'], info['reason']))
            return False

    def delete(self):
        r = self.session.delete(self.name)
        if r.status_code == codes.ok:
            return True
        elif r.status_code == codes.bad_request:
            logging.info('Failed attempt to delete database {0}. The request url {1} is not valid.'.format(self.name, r.url)
                         + 'Probably a invalid database name or forgotten document id by accident.')
        elif r.status_code == codes.not_found:
            logging.info('Failed attempt to delete database {0}. It does not exist.'.format(self.name))
        elif r.status_code == codes.unauthorized:
            logging.info('Failed attempt to delete database {0}. CouchDB Server Administrator privileges required.'.format(self.name))
        return False

    def post(self, doc, full_commit=None, batch=None):
        query_params = {}
        if batch is not None:
            query_params['batch'] = batch

        request_headers = {}
        if full_commit is not None:
            request_headers['X-Couch-Full-Commit'] = full_commit

        r = self.session.post(json=doc, params=query_params, headers=request_headers)
        body = r.json()
        if r.status_code == codes.ok:
            return Document(self, body['id'], body['rev'])
        elif r.status_code == codes.created:
            return Document(self, body['id'], body['rev'])
        elif r.status_code == codes.bad_request:
            return False
        elif r.status_code == codes.unauthorized:
            return False
        elif r.status_code == codes.not_found:
            return False
        elif r.status_code == codes.conflict:
            return False

    def query(self, method, params=None):
        response = self.session.get(self.db_url + method, params=params,
                                auth=(self.user, self.password))
        return response.url

    def put_bulk(self, docs):
        response = self.session.post(self.db_url + '_bulk_docs',
                                 json={'docs': docs},
                                 auth=(self.user, self.password))
        return response.json()

    def get_bulk(self, ids):
        str_ids = [str for id in ids]
        response = self.session.post(self.db_url + '_all_docs',
                                 json={'keys': str_ids},
                                 auth=(self.user, self.password))
        return response.json()

