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
        self.session = Session.login(refresh_token=api_token)

    def test_01_session_object_for_attributes_on_successful_login(self):
        '''
        Story: User logs in with a valid API token.
        An instance of the session class is created, including the following
        attributes:
        token
        baseurl
        authorization headers (csp-auth-token)
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
        self.assertTrue(self.session.headers['Authorization'])

    def test_02_exception_raised_on_failed_login(self):
        '''
        Story: User logs in with an invalid API token.
        Ensure that a HTTPError is raised in response.
        '''
        from caspyr import Session
        with self.assertRaises(HTTPError):
            self.session = Session.login(refresh_token='invalid_token')


class Blueprint_tests(unittest.TestCase):
    '''
    This set of tests checks the Blueprint class methods.
    '''

    def setUp(self):
        from caspyr import Session
        api_token = os.getenv('api_token')
        self.session = Session.login(refresh_token=api_token)

    def test_01_blueprint_get_returns_list(self):
        '''
        Story: User attempts Blueprint.list(session) and expects a
        list of blueprints in return.
        '''
        from caspyr import Blueprint
        self.assertIsInstance(Blueprint.list(self.session),
                              list
                              )

    @unittest.skip("not ready")
    def test_02_blueprint_create_returns_object(self):
        '''Story:
        User attempts to create a blueprint (Blueprint.create) and expects an
        object in response.
        '''
        from caspyr import Blueprint

        self.blueprint = Blueprint.create(self.session,
                                          project_id='0af2ca6c-aa99-4826-8911-0298a31fc2a4',
                                          bp_name='caspyr',
                                          description='Blueprint for caspyr tests',
                                          version='1',
                                          content=('formatVersion: 1\n'
                                                   'inputs: {}\n'
                                                   'resources:\n'
                                                   'Cloud_Machine_1:\n'
                                                   '  type: Cloud.Machine\n'
                                                   '  properties:\n'
                                                   '  image: ubuntu\n'
                                                   '  flavor: small\n'
                                                   )
                                          )
        self.assertIsInstance(self.blueprint,
                              Blueprint
                              )

    @unittest.skip("under development")
    def test_02_blueprint_describe_returns_object(self):
        '''
        Story: User attempts Blueprint.describe(session) and expects an
        instance of a Blueprint class to be returned, containing the following
        attributes:
        name
        description
        tags
        content
        valid
        validationMessages
        status
        projectId
        projectName
        type
        id
        selfLink
        createdAt
        createdBy
        updatedAt
        updatedBy
        '''
        from caspyr import Blueprint
        bp = Blueprint.list(self.session)[0]
        self.blueprint = Blueprint.describe(self.session, bp['id'])
        self.assertIsInstance(self.blueprint,
                              Blueprint
                              )
        self.assertIsInstance(self.blueprint.id,
                              str
                              )
        self.assertIsInstance(self.blueprint.name,
                              str
                              )
        self.assertIsInstance(self.blueprint.description,
                              str
                              )
        self.assertIsInstance(self.blueprint.tags,
                              list
                              )
        self.assertIsInstance(self.blueprint.content,
                              str
                              )
        self.assertIsInstance(self.blueprint.valid,
                              bool
                              )
        self.assertIsInstance(self.blueprint.validation_messages,
                              list
                              )
        self.assertIsInstance(self.blueprint.status,
                              str
                              )
        self.assertIsInstance(self.blueprint.project_id,
                              str
                              )
        self.assertIsInstance(self.blueprint.project_name,
                              str
                              )
        self.assertIsInstance(self.blueprint.type,
                              str
                              )
        self.assertIsInstance(self.blueprint.id,
                              str
                              )
        self.assertIsInstance(self.blueprint.self_link,
                              str
                              )
        self.assertIsInstance(self.blueprint.created_at,
                              str
                              )
        self.assertIsInstance(self.blueprint.created_by,
                              str
                              )
        self.assertIsInstance(self.blueprint.updated_at,
                              str
                              )
        self.assertIsInstance(self.blueprint.updated_by,
                              str
                              )

if __name__ == '__main__':
    unittest.main(warnings='ignore')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
