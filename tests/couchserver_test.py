# -*- coding: utf-8 -*-
from .context import couchdb

import unittest
import requests
from nose.tools import *

server = couchdb.Cloudant(couchdb.auth.user, couchdb.auth.password)

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_create_db(self):
        result = server.create_db('test')
        server.delete_db('test')
        assert result

    def test_create_already_existing_db(self):
        server.create_db('test')
        with assert_raises(requests.HTTPError) as cm:
            server.create_db('test')
        ex = cm.exception # raised exception is available through exception property of context
        server.delete_db('test')
        ok_(ex.response.status_code == 412, 'HTTPError should be 412.')

if __name__ == '__main__':
    unittest.main()

