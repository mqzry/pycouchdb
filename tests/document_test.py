import unittest

# class DatabaseTestSuite(unittest.TestCase)

#     def test_create_already_existing_db(self):
#         server.create_db('test')
#         with assert_raises(requests.HTTPError) as cm:
#             server.create_db('test')
#         ex = cm.exception # raised exception is available through exception property of context
#         server.delete_db('test')
#         ok_(ex.response.status_code == 412, 'HTTPError should be 412.')
