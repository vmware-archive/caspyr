import unittest
import os
from requests import HTTPError
import json

api_token=os.getenv('api_token')

class Hands_On_Labs(unittest.TestCase):
    '''
    This set of tests checks all the functions we need to standup HOL-1902-03,
    and the subsequent cleanup once a user finishes their session.
    '''

    def setUp(self, api_token=api_token):
        from caspyr import Session
        self.session = Session.login(refresh_token=api_token)

        details = '../secrets.json'
        with open(details) as f:
            data = json.load(f)
            for i in data:
                if i['token']==api_token:
                    self.aws_access_key = i["aws_access_key"]
                    self.aws_secret_key = i["aws_secret_key"]
                    self.azure_subscription_id = i["azure_subscription_id"]
                    self.azure_tenant_id = i["azure_tenant_id"]
                    self.azure_application_id = i["azure_application_id"]
                    self.azure_application_key = i["azure_application_key"]
                    self.aws_cloud_account_name = i["aws_cloud_account_name"]
                    self.aws_region = i["aws_region"]
                    self.aws_cloud_zone_name = i["aws_cloud_zone_name"]
                    self.aws_image_name = i["aws_image_name"]
                    self.azure_cloud_account_name = i["azure_cloud_account_name"]
                    self.azure_region = i["azure_region"]
                    self.azure_cloud_zone_name = i["azure_cloud_zone_name"]
                    self.azure_image_name = i["azure_image_name"]
                    self.image_mapping_name = i["image_mapping_name"]
            f.closed

    def test_01_session_object_for_attributes_on_successful_login(self):
        '''
        Story: User logs in with a valid API token.
        An instance of the session class is created, including the following attributes:
        token
        baseurl
        headers
        log_level
        '''
        self.assertIsInstance(self.session.token, str)
        self.assertEqual(self.session.baseurl, 'https://api.mgmt.cloud.vmware.com')
        self.assertTrue(self.session.headers['authorization'])

    def test_02_exception_raised_on_failed_login(self):
        '''
        Story: User logs in with an invalid API token.
        Ensure that a HTTPError is raised in response.
        '''
        from caspyr import Session
        with self.assertRaises(HTTPError):
            self.session = Session.login(refresh_token='12345')

    def test_03_aws_cloud_account_create(self):
        '''
        Story: AWS Cloud Account is created with provided credentials, resulting in an
        instance of the CloudAccount class. Class object is validated for expected
        attributed.
        '''
        from caspyr import CloudAccountAws
        self.aws_account=CloudAccountAws.create(self.session, name='HOL Test AWS Account', access_key=self.aws_access_key, secret_key=self.aws_secret_key, regions = 'ap-southeast-2', create_zone = False, description = 'Created as part of the test framework for caspyr.')
        self.assertTrue(self.aws_account.id)
        self.assertTrue(self.aws_account.name)
        self.assertTrue(self.aws_account.enabled_region_ids)
        self.assertTrue(self.aws_account.organization)
        self.assertTrue(self.aws_account._links)
        self.assertTrue(self.aws_account.custom_properties)

    def test_04_aws_cloud_account_list(self):
        from caspyr import CloudAccountAws
        self.aws_accounts=CloudAccountAws.list(self.session)
        self.assertIsInstance(self.aws_accounts, list)

    def test_05_aws_cloud_account_describe(self):
        from caspyr import CloudAccountAws
        self.aws_account=CloudAccountAws.describe(self.session, CloudAccountAws.list(self.session)[0]['id'])
        self.assertTrue(self.aws_account.id)
        self.assertTrue(self.aws_account.name)
        self.assertTrue(self.aws_account.enabled_region_ids)
        self.assertTrue(self.aws_account.organization)
        self.assertTrue(self.aws_account._links)
        self.assertTrue(self.aws_account.custom_properties)

    def test_06_cloud_account_azure_create(self):
        '''
        Story: AWS Cloud Account is created with provided credentials, resulting in an
        instance of the CloudAccount class. Class object is validated for expected
        attributed.
        '''
        from caspyr import CloudAccountAzure
        self.azure_account=CloudAccountAzure.create(self.session, name='HOL Test Azure Account', subscription_id=self.azure_subscription_id, tenant_id=self.azure_tenant_id, application_id=self.azure_application_id, application_key=self.azure_application_key, regions = 'westus', create_zone = False, description = 'Created as part of the caspyr test suite.')
        self.assertTrue(self.azure_account.id)
        self.assertTrue(self.azure_account.name)
        self.assertTrue(self.azure_account.enabled_region_ids)
        self.assertTrue(self.azure_account.organization)
        self.assertTrue(self.azure_account._links)
        self.assertTrue(self.azure_account.custom_properties)

    def test_07_cloud_account_azure_list(self):
        from caspyr import CloudAccountAzure
        self.azure_accounts=CloudAccountAzure.list(self.session)
        self.assertIsInstance(self.azure_accounts, list)

    def test_08_cloud_account_azure_describe(self):
        from caspyr import CloudAccountAzure
        self.azure_account=CloudAccountAzure.describe(self.session, CloudAccountAzure.list(self.session)[0]['id'])
        self.assertTrue(self.azure_account.id)
        self.assertTrue(self.azure_account.name)
        self.assertTrue(self.azure_account.enabled_region_ids)
        self.assertTrue(self.azure_account.organization)
        self.assertTrue(self.azure_account._links)
        self.assertTrue(self.azure_account.custom_properties)

    def test_09_create_cloud_zone_aws(self):
        from caspyr import CloudAccountAws, CloudZone
        self.aws_account=CloudAccountAws.describe(self.session, CloudAccountAws.list(self.session)[0]['id'])
        self.region=os.path.split(self.aws_account._links['regions']['hrefs'][0])[1]
        self.aws_cloudzone=CloudZone.create(self.session, name=self.aws_cloud_zone_name, region_id=self.region, tags_to_match=[{"key": "platform", "value": "aws"}], description='Created as part of the test framework for caspyr.')
        self.assertIs(type(self.aws_cloudzone), CloudZone)
        self.assertIsInstance(self.aws_cloudzone.id, str)
        self.assertIsInstance(self.aws_cloudzone.tags_to_match, list)
        self.assertIsInstance(self.aws_cloudzone.placement_policy, str)
        self.assertIsInstance(self.aws_cloudzone.name, str)
        self.assertIsInstance(self.aws_cloudzone.updated_at, str)
        self.assertIsInstance(self.aws_cloudzone._links, object)

    def test_10_create_cloud_zone_azure(self):
        from caspyr import CloudAccountAzure, CloudZone
        self.aws_account=CloudAccountAzure.describe(self.session, CloudAccountAzure.list(self.session)[0]['id'])
        self.region=os.path.split(self.aws_account._links['regions']['hrefs'][0])[1]
        self.aws_cloudzone=CloudZone.create(self.session, name=self.azure_cloud_zone_name, region_id=self.region, tags_to_match=[{"key": "platform", "value": "azure"}], description='Created as part of the test framework for caspyr.')
        self.assertIs(type(self.aws_cloudzone), CloudZone)
        self.assertIsInstance(self.aws_cloudzone.id, str)
        self.assertIsInstance(self.aws_cloudzone.tags_to_match, list)
        self.assertIsInstance(self.aws_cloudzone.placement_policy, str)
        self.assertIsInstance(self.aws_cloudzone.name, str)
        self.assertIsInstance(self.aws_cloudzone.updated_at, str)
        self.assertIsInstance(self.aws_cloudzone._links, object)

    def test_cloud_zone_describe_by_name(self):
        from caspyr import CloudZone
        self.cloudzone=CloudZone.describe_by_name(self.session, "'caspyr testing aws cloud zone'")
        self.assertIs(type(self.cloudzone), CloudZone)
        self.assertIsInstance(self.cloudzone.id, str)
        self.assertIsInstance(self.cloudzone.tags_to_match, list)
        self.assertIsInstance(self.cloudzone.placement_policy, str)
        self.assertIsInstance(self.cloudzone.name, str)
        self.assertIsInstance(self.cloudzone.updated_at, str)
        self.assertIsInstance(self.cloudzone._links, object)

    def test_11_image_describe(self):
        from caspyr import Image
        self.image_aws=Image.describe(self.session, image='Canonical:UbuntuServer:16.04-LTS:latest', region='westus')
        self.assertIs(type(self.image_aws), Image)
        self.assertIsInstance(self.image_aws.os_family, str)
        self.assertIsInstance(self.image_aws.external_region_id, str)
        self.assertIsInstance(self.image_aws.is_private, bool)
        self.assertIsInstance(self.image_aws.external_id, str)
        self.assertIsInstance(self.image_aws.name, str)
        self.assertIsInstance(self.image_aws.description, str)
        self.assertIsInstance(self.image_aws.id, str)
        self.assertIsInstance(self.image_aws.updated_at, str)
        self.assertIsInstance(self.image_aws._links, object)

    def test_12_image_profile_create(self):
        from caspyr import Image, ImageMapping, CloudZone, Region
        self.cloudzone_aws=CloudZone.describe_by_name(self.session, self.aws_cloud_zone_name)
        self.region_aws=Region.describe(self.session, self.cloudzone_aws.region_id)
        self.image_aws=Image.describe(self.session, image=self.aws_image_name, region=self.region_aws.external_region_id)

        self.cloudzone_azure=CloudZone.describe_by_name(self.session, self.azure_cloud_zone_name)
        self.region_azure=Region.describe(self.session, self.cloudzone_azure.region_id)
        self.image_azure=Image.describe(self.session, image=self.azure_image_name, region=self.region_azure.external_region_id)

        self.image_mapping_aws=ImageMapping.create(self.session, name=self.image_mapping_name, image_name=self.image_aws.name, image_id=self.image_aws.id, region_id=self.region_aws.id, description=None)
        self.image_mapping_azure=ImageMapping.create(self.session, name=self.image_mapping_name, image_name=self.image_azure.name, image_id=self.image_azure.id, region_id=self.region_azure.id, description=None)

        self.assertIsInstance(self.image_mapping_aws, dict)
        self.assertIsInstance(self.image_mapping_azure, dict)

    def test_create_flavor_mapping(self):
        pass

    def test_create_storage_mapping(self):
        pass

    def test_create_network_mapping(self):
        pass

    def test_create_networks(self):
        pass

    def test_create_project(self):
        pass

    def test_create_blueprint(self):
        pass

    def test_create_deployment_azure(self):
        pass

    def test_create_deployment_aws(self):
        pass

    def check_in_progress_deployments(self):
        pass

    def test_03_deployment_list(self):
        '''
        Story: A user performs Deployment.list(bearer).
        The response should contain a list of all deployments.
        '''
        from caspyr import Deployment
        self.deployments = Deployment.list(self.session)
        self.assertIsInstance(self.deployments, list)

    def test_cancel_in_progress_deployments(self):
        pass

    def test_delete_deployments(self):
        pass

    def test_image_profile_delete(self):
        from caspyr import ImageMapping
        for i in ImageMapping.list(self.session):
            self.assertEqual(ImageMapping.delete(self.session, i['id']), 200)
        self.assertEqual(len(ImageMapping.list(self.session)), 0)

    def test_cloud_zone_delete(self):
        from caspyr import CloudZone
        self.cloud_zones=CloudZone.list(self.session)
        for i in self.cloud_zones:
            self.assertEqual(CloudZone.delete(self.session, i['id']), 200)

    def test_06_aws_cloud_account_unregister_and_delete(self):
        from caspyr import CloudAccount, CloudAccountAws
        self.aws_account=CloudAccountAws.describe(self.session, CloudAccountAws.list(self.session)[0]['id'])
        self.assertEqual(CloudAccountAws.unregister(self.session, self.aws_account.id), 200)
        self.assertEqual(CloudAccount.delete(self.session, self.aws_account.id), 200)

    def test_06_cloud_account_azure_unregister_and_delete(self):
        from caspyr import CloudAccount, CloudAccountAzure
        self.azure_account=CloudAccountAzure.describe(self.session, CloudAccountAzure.list(self.session)[0]['id'])
        self.assertEqual(CloudAccountAzure.unregister(self.session, self.azure_account.id), 200)
        self.assertEqual(CloudAccount.delete(self.session, self.azure_account.id), 200)

if __name__ == '__main__':
    unittest.main(warnings='ignore')