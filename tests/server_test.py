# -*- coding: utf-8 -*-
from .context import couchdb

import unittest

server = couchdb.Cloudant(couchdb.auth.user, couchdb.auth.password)


class ServerTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_info(self):
        assert server.info['uuid']

    def test_active_tasks(self):
        tasks = server.get_active_tasks()
        assert tasks is not None

    def test_all_dbs(self):
        dbs = server.get_dbs()
        assert dbs[0].name is not None # TODO: look for way to check if variable is a list

    def test_db_updates_longpoll(self):
        db_updates = server.get_db_updates('longpoll')
        assert db_updates is not None

    def test_db_updates_continuous(self):
        raise NotImplementedError

    def test_db_updates_eventsource(self):
        raise NotImplementedError

    def test_membership(self):
        membership = server.get_membership()
        assert membership.all_nodes and membership.cluster_nodes

    def test_log(self):
        log = server.get_log
        assert log is not None

    def test_restart(self):
        result, status = server.restart()
        assert result

    def test_post_replicate(self):
        raise NotImplementedError

    def test_stats(self):
        assert server.stats() is not None

    def test_uuids(self):
        assert len(server.uuids(1)['uuids']) == 1

    def test_login(self):
        raise NotImplementedError

    def test_logout(self):
        raise NotImplementedError

    def test_get_config(self):
        raise NotImplementedError

    def test_put_config(self):
        raise NotImplementedError

    def test_delete_config(self):
        raise NotImplementedError

    def test_put_delete_invariant_config(self):
        section = 'couchdb'
        key = 'database_dir'
        value = server.delete_config(section, key)
        server.put_config(section, key, value)
        last_value = server.get_config(section, key)
        assert value == last_value

    def test_create_db(self):
        db, result = server.create('test')
        assert db.exists

if __name__ == '__main__':
    unittest.main()
