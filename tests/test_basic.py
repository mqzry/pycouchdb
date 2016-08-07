# -*- coding: utf-8 -*-

from .context import couchdb

import unittest
import requests


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_create_db(self):
        server = couchdb.Cloudant(couchdb.auth.user, couchdb.auth.password)
        server.create_db('test')
        assert server.head_db('test')
        server.delete_db('test')

    def test_create_already_existing_db(self):
        server = couchdb.Cloudant(couchdb.auth.user, couchdb.auth.password)
        server.create_db('test')
        assert server.create_db('test')
        server.delete_db('test')


if __name__ == '__main__':
    unittest.main()