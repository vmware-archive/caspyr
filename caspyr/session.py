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

    def _request(self, uri, request_method='GET', data=None, **kwargs):
        """
        Credits: Russell Pope
        Generic requestor method for all of the HTTP methods. This gets invoked by pretty much everything in the API.
        You can also use it to do anything not yet implemented in the API.

        :param uri: The complete uri for the requested resource. You should include the leading /
        :param request_method: An HTTP method that is either PUT, POST, PATCH, DELETE or GET
        :param payload: Used to store a resource that is used in either POST or PUT operations
        :param kwargs: Unused currently
        :return: A python dictionary containing the response JSON

        """

        if request_method == "PUT" or "POST" or "PATCH" and data:
            if type(data) == dict:
                data = json.dumps(json)

            r = requests.request(request_method,
                                 url=uri,
                                 headers=self.headers,
                                 json=data)

            if not r.ok:
                raise requests.exceptions.HTTPError('HTTP error. Status code was:', r.status_code, r.content)

            return r.json()

        elif request_method == "GET":
            r = requests.request(request_method,
                                 url=uri,
                                 headers=self.headers)

            if not r.ok:
                uri_code = f'Target uri: {r.uri}, Status Code: {r.status_code}'
                raise requests.exceptions.HTTPError('HTTP error. Status and content:',uri_code , r.content)

            return r.json()

        elif request_method == "DELETE":
            r = requests.request(request_method,
                                 url=uri,
                                 headers=self.headers)

            if not r.ok:
                raise requests.exceptions.HTTPError('HTTP error. Status code was:', r.status_code)

            return r.json()
