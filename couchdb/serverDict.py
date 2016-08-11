from server import Server


class ServerDict(Server):
    #  Emulating a container
    def __len__(self):
        return len(self.get_dbs())

    def __length_hint__(self):
        return len(self.dbs)

    def __contains__(self, key):
        return self.exists(key)

    def __delitem__(self, key):
        result = self.delete_db(key)
        if not result:
            raise Exception('Deletion failed. Check the logs.')

    def __iter__(self):
        return iter(self.get_dbs())

    def __getitem__(self, key):
        if key in self.dbs or self.exists(key):
            return self.get_db(key)
        else:
            raise KeyError
