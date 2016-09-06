from requests import codes

class Document:
    """A document in a CouchDB instance."""
    def __init__(self, database, doc_id, doc_rev):
        self._id = doc_id
        self.db = database
        self.db.session.add_part_to_prefix(doc_id)
        self._rev = doc_rev
        
    def head(self,
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

        req_headers = {'If-None-Matched': self._rev}

        r = self.db.session.head(params=query_params)
        if r.status_code == codes.ok:
            logging.info('Document {0} exists'.format(self._id))
            content_length = int(response.headers['Content-Length'])
            return {'latest_rev': response.headers['ETag'],
                    'content-length': content_length}
        elif r.status_code == codes.not_modified:
            logging.info('Document {0} wasn’t modified since specified revision'.format(self._id))
            return
        elif r.status_code == codes.unauthorized:
            logging.info('Failed attempt to head document {0}. Read privilege required.'.format(self._id))
        elif r.status_code == codes.not_found:
            logging.info('Document {0} not found'.format(self._id))

    def get(self,
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

        req_headers = {'If-None-Matched': self._rev}
        r = self.db.session.get(params=query_params, headers=req_headers)
        
        if r.status_code == codes.ok:
            return r.json()
        elif r.status_code == codes.not_modified:
            logging.info('Document {0} wasn’t modified since specified revision'.format(self._id))
            return
        elif r.status_code == codes.bad_request:
            logging.info('The format of the request or revision {0} is invalid.'.format(self._rev) 
                         + 'Request: {0}'.format(r.request))
            return
        elif r.status_code == codes.unauthorized:
            logging.info('Failed attempt to head document {0}. Read privilege required.'.format(self._id))
            return
        elif r.status_code == codes.not_found:
            logging.info('Document {0} not found'.format(self._id))
            return
 

    def put(self, doc, full_commit=None):
        req_headers = {'If-Match': self._rev}
        if full_commit is not None:
            req_headers['X-Couch-Full-Commit'] = full_commit

        r = self.db.session.post(json=doc, headers=req_headers)

        body = r.json()
        
        return Document(self.db, body.id, body.rev)

    def delete(self, full_commit=None):
        req_headers = {'If-Match': self._rev}

        req_headers = {'If-Match': self._rev}
        if full_commit is not None:
            req_headers['X-Couch-Full-Commit'] = full_commit

        r = self.db.session.delete(headers=req_headers)

        # if r.status_code == codes.ok:

        # elif r.status_code == codes.accepted:
        #     #log
        # elif r.status_code == codes.not_modified:
        #     #log
        # elif r.status_code == codes.unauthorized:
        #     #log
        # elif r.status_code == codes.not_found:
        #     #log
        # elif r.status_code == codes.conflict:
        #     #log
        return r.json().ok

    def copy(self, new_id):
        req_headers = {'If-Match': self._rev, 'Destination': new_id}
        r = self.db.session.copy(headers=req_headers)

    # def head_attachment(self):
    # def get_attachment(self):
    # def put_attachment(self):
    # def post_attachment(self):
    # def delete_attachment(self):
