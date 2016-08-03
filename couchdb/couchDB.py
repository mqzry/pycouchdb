# auth info for DB
from requests import Session
import mimetypes
import os
from base64 import b64encode

class Database:
class Document:
class CouchServer:

    def __init__(self, url, user, password):
        self.url = url
        self.session = Session()

    def get(self, db):
        """Get database
        :param db: name of database
        :return: True if authenticated ok
        :rtype: bool
        """
        self.db = db
        self.db_url = self.base_url + db + '/'

    def login(self, user, password):
        self.session.auth = (user, password)

# Documents
    def head(self, docid, docrev=None):
        """Get headers for a document
        :param docid: id of document
        :param docrev: rev of doc that should be used in if-none-matched
        :return: ?
        :rtype: ?
        """
        response = self.session.head(self.db_url + docid,
                                     headers={'If-None-Match': '"{}"'.format(docrev)})
        if response.status_code == 200:
            # Everything went ok
        if response.status_code == 304:
            # Not modified
        if response.status_code == 401:
            # Unauthorized
        if response.status_code == 404:
            # Not Found

        response.headers['_rev'] = response.headers['ETag']
        delete(response.headers['ETag'])

    def get(self, docid, **kwargs):
        """Get document
        :param docid: id of document
        :return: ?
        :rtype: ?
        """
        result = self.session.get(self.db_url + str(id), params=kwargs)
        return result.json()

    def post(self, doc):
        result = requests.post(self.db_url, json=doc,
                               auth=(self.user, self.password))
        return result.json()

    def update(self, doc):
        result = requests.post(self.db_url + str(doc['_id']), json=doc,
                               auth=(self.user, self.password))
        return result.json()

    def query(self, method, params=None):
        response = requests.get(self.db_url + method, params=params,
                                auth=(self.user, self.password))
        return response.url

    def put_bulk(self, docs):
        response = requests.post(self.db_url + '_bulk_docs',
                                 json={'docs': docs},
                                 auth=(self.user, self.password))
        return response.json()

    def get_bulk(self, ids):
        str_ids = [str(id) for id in ids]
        response = requests.post(self.db_url + '_all_docs',
                                 json={'keys': str_ids},
                                 auth=(self.user, self.password))
        return response.json()

    def get_all(self):
        return self.query('_all_docs')

    def add_attachment(doc, attachment_path, name=None, content_type=None):
        if attachment_path:
            if not name:
                name = os.path.basename(attachment_path)
            if not content_type:
                content_type = mimetypes.guess_type(attachment_path)[0]
            with open(attachment_path, 'rb') as f:
                doc['_attachments'] = {}
                doc['_attachments'][name] = {
                    'content_type': content_type,
                    'data': b64encode(f.read()).decode('utf-8')
                }
        return doc

    def replicate(self, source, target, params={}):
        doc = params
        doc['source'] = 'https://{0}:{1}@'.format(self.user, self.password) \
                        + self.base_url.split('//')[1] + source
        doc['target'] = 'https://{0}:{1}@'.format(self.user, self.password) \
                        + self.base_url.split('//')[1] + target
        self.set_current_db('_replicator')
        return self.create(doc)

    def create_db(self, name):
        return requests.put(self.base_url + name, auth=(self.user, self.password))

    def delete_db(self, name):
        return requests.delete(self.base_url + name, auth=(self.user, self.password))

    def get_view(self, design_doc, view_name):
        response = requests.get(self.db_url + "_design/{0}/_view/{1}".format(design_doc, view_name),
                                auth=(self.user, self.password))
        return response
