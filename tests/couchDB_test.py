# import couchDB
# import auth

# db = couchDB.Cloudant(auth.user, auth.password)

# db.create_db('test')
# db.replicate('library', 'test')
# db.set_current_db('test')
# db.create({'_id': '1', 'key': 'create'})
# db.update({'_id': '1', 'key': 'update'})
# db.get(1)
# docs = [{'_id': str(value), 'key': 'bulk'} for value in range(2, 10)]
# db.put_bulk(docs)
# db.get_bulk([2, 3])
# db.get_all()
# db.delete_db('test')
