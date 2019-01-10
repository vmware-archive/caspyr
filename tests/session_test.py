import unittest
import os
from requests import HTTPError
import json


class Session_tests(unittest.TestCase):
    '''
    This set of tests checks the Session class constructor.
    '''

    def setUp(self):
        from caspyr import Session
        api_token = os.getenv('api_token')
        print(api_token)
        self.session = Session.login(refresh_token=api_token)

    def test_01_session_object_for_attributes_on_successful_login(self):
        '''
        Story: User logs in with a valid API token.
        An instance of the session class is created, including the following
        attributes:
        token
        baseurl
        authorization headers
        '''

        self.assertIsInstance(self.session,
                              object
                              )
        self.assertIsInstance(self.session.token,
                              str
                              )
        self.assertEqual(self.session.baseurl,
                         'https://api.mgmt.cloud.vmware.com'
                         )
        self.assertTrue(self.session.headers['csp-auth-token'])

    def test_02_exception_raised_on_failed_login(self):
        '''
        Story: User logs in with an invalid API token.
        Ensure that a HTTPError is raised in response.
        '''
        from caspyr import Session
        with self.assertRaises(HTTPError):
            self.session = Session.login(refresh_token='12345')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
