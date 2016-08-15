from requests import Session
from urlparse import urljoin

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
    	self.prefix_url = urljoin(self.prefix_url, url)