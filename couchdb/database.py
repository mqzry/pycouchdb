from requests import Session
import mimetypes
import os
from base64 import b64encode

def handle_codes():
        if response.status_code == requests.codes.not_modified:
            return None
        else:
            response.raise_for_status()

class Database:

    def __init__(self, url, session):
        self.url = url
        self.session = session

    def head(self, docid,
             docrev=None,
             attachments=None,
             att_encoding_info=None,
             atts_since=None,
             conflicts=None,
             deleted_conflicts=None,
             latest=None,
             local_seq=None,
             meta=None,
             open_revs=None,
             rev=None,
             revs=None,
             revs_info=None):

        """Get document from database.

        :param docid: id of document
        :param docrev: rev of current doc
        :param attachments: Includes attachments bodies in response.
        :param att_encoding_info: Includes encoding information in attachment stubs if the particular attachment is compressed. .
        :param atts_since: Includes attachments only since specified revisions. Doesn’t includes attachments for specified revisions.
        :param conflicts: Includes information about conflicts in document. .
        :param deleted_conflicts: Includes information about deleted conflicted revisions. 
        :param latest: Forces retrieving latest “leaf” revision, no matter what rev was requested. 
        :param local_seq: Includes last update sequence number for the document. 
        :param meta: Acts same as specifying all conflicts, deleted_conflicts and open_revs parameters. 
        :param open_revs: Retrieves documents of specified leaf revisions. Additionally, it accepts value as all to return all leaf revisions. Optional
        :param rev: Retrieves document of specified revision. Optional 
        :param revs: Includes list of all known document revisions. 
        :param revs_info: Includes detailed information for all known document revisions.
        :return: The requested doc or None if doc did not get updated.
        """
        query_params = {}
        if attachments is not None: 
            query_params['attachments'] = attachments 
        if att_encoding_info is not None:
            query_params['att_encoding_info'] = att_encoding_info 
        if attachments is not None:
            query_params['atts_since'] = atts_since 
        if conflicts is not None:
            query_params['conflicts'] = conflicts 
        if deleted_conflicts is not None:
            query_params['deleted_conflicts'] = deleted_conflicts
        if latest is not None:
            query_params['latest'] = latest
        if local_seq is not None:
            query_params['local_seq'] = local_seq
        if meta is not None:
            query_params['meta'] = meta
        if open_revs is not None:
            query_params['open_revs'] = open_revs
        if rev is not None:
            query_params['rev'] = rev
        if revs is not None:
            query_params['revs'] = revs
        if revs_info is not None:
            query_params['revs_info'] = revs_info

        req_headers = {}
        if docrev is not None:
            req_headers['If-None-Match'] = '"{}"'.format(docrev)

        response = self.session.head(self.db_url + docid,
                                     params=query_params,
                                     headers=req_headers)
        handle_codes(response)

        content_length = int(response.headers['Content-Length'])
        return {'_rev': response.headers['ETag'],
                'Content-Length': content_length}

    def get(self, docid,
            docrev=None,
            attachments=None,
            att_encoding_info=None,
            atts_since=None,
            conflicts=None,
            deleted_conflicts=None,
            latest=None,
            local_seq=None,
            meta=None,
            open_revs=None,
            rev=None,
            revs=None,
            revs_info=None):
        """Get document from database.

        :param docid: id of document
        :param docrev: rev of current doc
        :param attachments: Includes attachments bodies in response.
        :param att_encoding_info: Includes encoding information in attachment stubs if the particular attachment is compressed. .
        :param atts_since: Includes attachments only since specified revisions. Doesn’t includes attachments for specified revisions.
        :param conflicts: Includes information about conflicts in document. .
        :param deleted_conflicts: Includes information about deleted conflicted revisions. 
        :param latest: Forces retrieving latest “leaf” revision, no matter what rev was requested. 
        :param local_seq: Includes last update sequence number for the document. 
        :param meta: Acts same as specifying all conflicts, deleted_conflicts and open_revs parameters. 
        :param open_revs: Retrieves documents of specified leaf revisions. Additionally, it accepts value as all to return all leaf revisions. Optional
        :param rev: Retrieves document of specified revision. Optional 
        :param revs: Includes list of all known document revisions. 
        :param revs_info: Includes detailed information for all known document revisions.

        :return: The requested document or None if doc did not get updated.
        """

        query_params = {}
        if attachments is not None: 
            query_params['attachments'] = attachments 
        if att_encoding_info is not None:
            query_params['att_encoding_info'] = att_encoding_info 
        if attachments is not None:
            query_params['atts_since'] = atts_since 
        if conflicts is not None:
            query_params['conflicts'] = conflicts 
        if deleted_conflicts is not None:
            query_params['deleted_conflicts'] = deleted_conflicts
        if latest is not None:
            query_params['latest'] = latest
        if local_seq is not None:
            query_params['local_seq'] = local_seq
        if meta is not None:
            query_params['meta'] = meta
        if open_revs is not None:
            query_params['open_revs'] = open_revs
        if rev is not None:
            query_params['rev'] = rev
        if revs is not None:
            query_params['revs'] = revs
        if revs_info is not None:
            query_params['revs_info'] = revs_info

        req_headers = {}
        if docrev is not None:
            req_headers['If-None-Match'] = '"{}"'.format(docrev)

        response = self.session.get(self.db_url + docid,
                                    params=query_params,
                                    headers=req_headers)
        handle_codes(response)
        return response.json()


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
        str_ids = [str for id in ids]
        response = requests.post(self.db_url + '_all_docs',
                                 json={'keys': str_ids},
                                 auth=(self.user, self.password))
        return response.json()

    # def get_all:
    #     return self.query('_all_docs')

    # def add_attachment(doc, attachment_path, name=None, content_type=None):
    #     if attachment_path:
    #         if not name:
    #             name = os.path.basename
    #         if not content_type:
    #             content_type = mimetypes.guess_type[0]
    #         with open(attachment_path, 'rb') as f:
    #             doc['_attachments'] = {}
    #             doc['_attachments'][name] = {
    #                 'content_type': content_type,
    #                 'data': b64encode(f.read()).decode('utf-8')
    #             }
    #     return doc

    # def replicate(self, source, target, params={}):
    #     doc = params
    #     doc['source'] = 'https://{0}:{1}@'.format(self.user, self.password) \
    #                     + self.base_url.split('//')[1] + source
    #     doc['target'] = 'https://{0}:{1}@'.format(self.user, self.password) \
    #                     + self.base_url.split('//')[1] + target
    #     self.set_current_db('_replicator')
    #     return self.create

    # def get_view(self, design_doc, view_name):
    #     response = requests.get(self.db_url + "_design/{0}/_view/{1}".format(design_doc, view_name),
    #                             auth=(self.user, self.password))
    #     return response
