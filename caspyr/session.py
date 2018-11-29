import json
import logging
import os

import requests

logging.basicConfig(level=os.getenv('caspyr_log_level'),
                    format='%(asctime)s %(name)s %(levelname)s %(message)s'
                    )
logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


class Session(object):
    """
    Session class for instantiating a logged in session
    for VMware Cloud Services.

    Requires refresh token from VMware Cloud Services portal to instantiate.
    """
    def __init__(self, auth_token):
        self.token = auth_token
        self.headers = {'Content-Type': 'application/json',
                        'csp-auth-token': self.token}
        self.baseurl = 'https://api.mgmt.cloud.vmware.com'

    @classmethod
    def login(self, refresh_token):
            baseurl = 'https://console.cloud.vmware.com/csp/gateway/am/api'
            uri = f'/auth/api-tokens/authorize?refresh_token={refresh_token}'
            headers = {'Content-Type': 'application/json'}
            payload = {}
            logger.debug(f'POST to: {baseurl}{uri} '
                         f'with headers: {headers} '
                         f'and body: {payload}.'
                         )

            try:
                r = requests.post(f'{baseurl}{uri}',
                                  headers=headers,
                                  data=payload)
                logger.debug(f'Response: {r.json()}')
                r.raise_for_status()
                logger.info('Authenticated successfully.')
                auth_token = r.json()['access_token']
                return self(auth_token)
            except requests.exceptions.HTTPError:
                logger.error('Failed to authenticate.')
                logger.error(f'Error message {r.json()["message"]}',
                             exc_info=False)

    def _request(self,
                 url,
                 request_method='GET',
                 payload=None,
                 **kwargs
                 ):
        """
        Inspired by the work of Russell Pope.
        :param url: The complete uri for the requested resource.
        You must include the leading /
        :param request_method: An HTTP method that one of
        PUT, POST, PATCH, DELETE or GET
        :param payload: Used to store a resource that is used in either
        POST, PATCH or PUT operations
        :param kwargs: Unused currently
        :return: The response JSON
        """

        if request_method in ('PUT', 'POST', 'PATCH') and payload:
            if type(payload) == dict:
                payload = json.dumps(payload)
            try:
                r = requests.request(request_method,
                                     url=url,
                                     headers=self.headers,
                                     data=payload)
                logger.debug(f'{request_method} to {url} '
                             f'with headers {self.headers} '
                             f'and body {payload}.'
                             )
                logger.debug(f'Request response: {r.json()}')
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError:
                logger.error(r.json(),
                             exc_info=False
                             )

        elif request_method == 'GET':
            try:
                r = requests.request(request_method,
                                     url=url,
                                     headers=self.headers)
                logger.debug(f'{request_method} to {url} '
                             f'with headers {self.headers}.'
                             )
                logger.debug(f'Request response: {r.json()}')
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError:
                logger.error(r.json()['message'],
                             exc_info=False
                             )

        elif request_method == 'DELETE':
            try:
                r = requests.request(request_method,
                                     url=url,
                                     headers=self.headers)
                logger.debug(f'{request_method} to {url} '
                             f'with headers {self.headers}.'
                             )
                r.raise_for_status()
                return r.status_code
            except requests.exceptions.HTTPError:
                logger.error(r.json()['message'],
                             exc_info=False
                             )
