import requests
import json
import sys

class Session(object):
    """
    Session class for instantiating a logged in session
    for VMware Cloud Services.

    Requires refresh token from VMware Cloud Services portal to instantiate.
    """
    def __init__(self, auth_token):
        self.token = 'Bearer '+auth_token
        self.headers = {'Content-Type':'application/json','authorization': self.token}
        self.baseurl = 'https://api.mgmt.cloud.vmware.com'

    @classmethod
    def login(self, refresh_token):
            baseurl = 'https://api.mgmt.cloud.vmware.com'
            uri = '/iaas/login'
            headers = {'Content-Type':'application/json'}
            payload = json.dumps({"refreshToken": refresh_token })
            try:
                r = requests.post(f'{baseurl}{uri}', headers = headers, data = payload)
                print('Login successful.')
                auth_token = r.json()['token']
                return self(auth_token)
            except requests.exceptions.HTTPError as e:
                print(e)
                sys.exit(1)

    @classmethod
    def _request(cls, session):
        pass
