from requests import Session
from urlparse import urljoin

class BasedSession(Session):
    def __init__(self, prefix_url):
        self.prefix_url = prefix_url
        super(BasedSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(BasedSession, self).request(method, url, *args, **kwargs)