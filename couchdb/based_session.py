from requests import Session
from urllib.parse import urljoin

class BasedSession(Session):
    def __init__(self, prefix_url):
        self.prefix_url = prefix_url
        super(BasedSession, self).__init__()

    def request(self, method, url=None, *args, **kwargs):
        if url is None:
            url = self.prefix_url
        else:
            url = urljoin(self.prefix_url, url)
        return super(BasedSession, self).request(method, url, *args, **kwargs)

    def add_part_to_prefix(self, url):
        if url is None:
            return
        self.prefix_url = urljoin(self.prefix_url, url)

    def put(self, url=None, data=None, **kwargs):
        return super(BasedSession, self).put(self.add_part_to_prefix(url), data, **kwargs)

    def get(self, url=None, **kwargs):
        return super(BasedSession, self).get(self.add_part_to_prefix(url), **kwargs)

    def options(self, url=None, **kwargs):
        return super(BasedSession, self).options(self.add_part_to_prefix(url), **kwargs)

    def head(self, url=None, **kwargs):
        return super(BasedSession, self).head(self.add_part_to_prefix(url), **kwargs)

    def post(self, url=None, data=None, json=None, **kwargs):
        return super(BasedSession, self).post(self.add_part_to_prefix(url), data, json, **kwargs)

    def patch(self, url=None, data=None, **kwargs):
        return super(BasedSession, self).patch(self.add_part_to_prefix(url), data, **kwargs)

    def delete(self, url=None, **kwargs):
        return super(BasedSession, self).delete(self.add_part_to_prefix(url), **kwargs)
