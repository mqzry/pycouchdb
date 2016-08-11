import requests

def handle_codes():
        if r.status_code == requests.codes.not_modified:
            return None
        else:
            r.raise_for_status()