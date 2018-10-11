import requests
import json
import sys
import logging

class Session(object):
    """
    Session class for instantiating a logged in session
    for VMware Cloud Services.

    Requires refresh token from VMware Cloud Services portal to instantiate.
    """
    def __init__(self, auth_token, log_level):
        self.token = 'Bearer '+auth_token
        self.headers = {'Content-Type':'application/json','authorization': self.token}
        self.baseurl = 'https://api.mgmt.cloud.vmware.com'
        self.log_level = log_level

    @classmethod
    def login(self, refresh_token, log_level='WARNING'):
            baseurl = 'https://api.mgmt.cloud.vmware.com'
            uri = '/iaas/login'
            headers = {'Content-Type':'application/json'}
            payload = json.dumps({"refreshToken": refresh_token })
            try:
                r = requests.post(f'{baseurl}{uri}', headers = headers, data = payload)
                print('Login successful.')
                auth_token = r.json()['token']
                return self(auth_token, log_level.upper())
            except requests.exceptions.HTTPError as e:
                print(e)
                sys.exit(1)

    def _request(self, url, request_method='GET', payload=None, **kwargs):
        """
        Inspired by the work of Russell Pope.
        :param url: The complete uri for the requested resource. You should include the leading /
        :param request_method: An HTTP method that is either PUT, POST, PATCH, DELETE or GET
        :param payload: Used to store a resource that is used in either POST or PUT operations
        :param kwargs: Unused currently
        :return: A python dictionary containing the response JSON

        """
        numeric_level = getattr(logging, self.log_level, None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % self.log_level)
        logging.basicConfig(level=numeric_level)

        if request_method == "PUT" or "POST" or "PATCH" and payload:
            if type(payload) == dict:
                payload = json.dumps(payload)

            try:
                r = requests.request(request_method,
                                    url=url,
                                    headers=self.headers,
                                    data=payload)

                logging.info(f'{request_method} to {url} with payload {payload}')
                logging.info(f'request response code {r.status_code}')
                logging.info(f'request content {json.dumps(r.json(), indent=2)}')

                r.raise_for_status()
                return r.json()

            except requests.exceptions.HTTPError as e:
                logging.error('request failed with {e}')
                print (e)

        elif request_method == "GET":
            try:
                r = requests.request(request_method,
                                    url=url,
                                    headers=self.headers)
                logging.info(f'{request_method} to {url}')
                logging.info(f'request response code {r.status_code}')
                logging.info(f'request content {r.json}')
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError as e:
                logging.error('request failed with {e}')
                print (e)

        elif request_method == "DELETE":
            try:
                r = requests.request(request_method,
                                    url=url,
                                    headers=self.headers)
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError as e:
                logging.error('request failed with {e}')
                print (e)
