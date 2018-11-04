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

        self.aws_cloud_account_name = "trading aws"
        self.aws_region = "us-west-1"
        self.aws_cloud_zone_name = "dev aws"
        self.aws_image_name = "ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-20171026.1"
        self.aws_network_profile_name = "trading aws network profile"
        self.aws_storage_profile_name = "trading aws storage profile"
        self.aws_storage_policy_name = "gp2"
        self.aws_flavor_name = "t2.small"
        self.aws_storage_device_type = "ebs"
        self.aws_storage_volume_type = "gp2"

        self.azure_cloud_account_name = "trading azure"
        self.azure_region = "westus"
        self.azure_cloud_zone_name = "dev azure"
        self.azure_image_name = "Canonical:UbuntuServer:16.04-LTS:latest"
        self.azure_network_profile_name = "trading azure network profile"
        self.azure_storage_profile_name = "trading azure storage profile"
        self.azure_storage_policy_name = "standard lrs"
        self.azure_storage_storage_type = "managed_disks"
        self.azure_storage_disk_type = "standard_lrs"
        self.azure_flavor_name = "Standard_B2s"
        self.azure_storage_os_disk_caching = "read_only"
        self.azure_storage_data_caching = "read_only"

        self.image_mapping_name = "ubuntu"
        self.flavor_mapping_name = "small"
        self.network_profile_tags = [{ "key": "env", "value": "dev" }]
        self.storage_policy_tags = [{ "key": "performance", "value": "standard"}]
        self.project_name = "trading"

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
            f.closed
    """
    def tearDown(self, api_token=api_token):
        from caspyr import Session, Request, Deployment, Blueprint
        from caspyr import NetworkProfile
        from caspyr import StorageProfileAWS, StorageProfileAzure, StorageProfilevSphere
        from caspyr import ImageMapping, FlavorMapping
        from caspyr import Project
        from caspyr import CloudZone
        from caspyr import CloudAccount, CloudAccountAws, CloudAccountAzure

        self.session = Session.login(refresh_token=api_token)

        Request.list
    """

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

    """
    Cloud Account Tests
    """

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
        Story: Azure Cloud Account is created with provided credentials, resulting in an
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

    """
    Cloud Zone Tests
    """
    def test_09_create_cloud_zone_aws(self):
        from caspyr import CloudAccountAws, CloudZone
        self.aws_account=CloudAccountAws.describe(self.session, CloudAccountAws.list(self.session)[0]['id'])
        self.region=os.path.split(self.aws_account._links['regions']['hrefs'][0])[1]
        self.aws_cloudzone=CloudZone.create(self.session, name=self.aws_cloud_zone_name, region_id=self.region, tags_to_match=[{"key": "platform", "value": "aws"}], description='Created as part of the test framework for caspyr.')
        self.assertIsInstance(self.aws_cloudzone, CloudZone)
        self.assertIsInstance(self.aws_cloudzone.id, str)
        self.assertIsInstance(self.aws_cloudzone.region_id, str)
        self.assertIsInstance(self.aws_cloudzone.tags_to_match, list)
        self.assertIsInstance(self.aws_cloudzone.placement_policy, str)
        self.assertIsInstance(self.aws_cloudzone.name, str)
        self.assertIsInstance(self.aws_cloudzone.updated_at, str)
        self.assertIsInstance(self.aws_cloudzone._links, object)

    def test_10_create_cloud_zone_azure(self):
        from caspyr import CloudAccountAzure, CloudZone
        self.azure_account=CloudAccountAzure.describe(self.session, CloudAccountAzure.list(self.session)[0]['id'])
        self.region=os.path.split(self.azure_account._links['regions']['hrefs'][0])[1]
        self.azure_cloudzone=CloudZone.create(self.session, name=self.azure_cloud_zone_name, region_id=self.region, tags_to_match=[{"key": "platform", "value": "azure"}], description='Created as part of the test framework for caspyr.')
        self.assertIsInstance(self.azure_cloudzone, CloudZone)
        self.assertIsInstance(self.azure_cloudzone.id, str)
        self.assertIsInstance(self.azure_cloudzone.region_id, str)
        self.assertIsInstance(self.azure_cloudzone.tags_to_match, list)
        self.assertIsInstance(self.azure_cloudzone.placement_policy, str)
        self.assertIsInstance(self.azure_cloudzone.name, str)
        self.assertIsInstance(self.azure_cloudzone.updated_at, str)
        self.assertIsInstance(self.azure_cloudzone._links, object)

    def test_11_cloud_zone_describe_by_name(self):
        from caspyr import CloudZone
        self.cloudzone=CloudZone.describe_by_name(self.session, self.aws_cloud_zone_name)
        self.assertIsInstance(self.cloudzone, CloudZone)
        self.assertIsInstance(self.cloudzone.id, str)
        self.assertIsInstance(self.cloudzone.tags_to_match, list)
        self.assertIsInstance(self.cloudzone.placement_policy, str)
        self.assertIsInstance(self.cloudzone.name, str)
        self.assertIsInstance(self.cloudzone.updated_at, str)
        self.assertIsInstance(self.cloudzone._links, object)

    """
    Mapping Tests
    """

    def test_12_image_describe(self):
        from caspyr import Image
        self.image_aws=Image.describe(self.session, image='Canonical:UbuntuServer:16.04-LTS:latest', region='westus')
        self.assertIsInstance(self.image_aws, Image)
        self.assertIsInstance(self.image_aws.os_family, str)
        self.assertIsInstance(self.image_aws.external_region_id, str)
        self.assertIsInstance(self.image_aws.is_private, bool)
        self.assertIsInstance(self.image_aws.external_id, str)
        self.assertIsInstance(self.image_aws.name, str)
        self.assertIsInstance(self.image_aws.description, str)
        self.assertIsInstance(self.image_aws.id, str)
        self.assertIsInstance(self.image_aws.updated_at, str)
        self.assertIsInstance(self.image_aws._links, object)

    def test_13_image_profile_create_aws(self):
        from caspyr import Image, ImageMapping, CloudZone, Region
        self.cloudzone_aws=CloudZone.describe_by_name(self.session, self.aws_cloud_zone_name)
        self.region_aws=Region.describe(self.session, self.cloudzone_aws.region_id)
        self.image_aws=Image.describe(self.session, image=self.aws_image_name, region=self.region_aws.external_region_id)
        self.image_mapping_aws=ImageMapping.create(self.session, name=self.image_mapping_name, image_name=self.image_aws.name, image_id=self.image_aws.id, region_id=self.region_aws.id, description=None)
        self.assertIsInstance(self.image_mapping_aws, dict)

    def test_14_image_profile_create_azure(self):
        from caspyr import Image, ImageMapping, CloudZone, Region
        self.cloudzone_azure=CloudZone.describe_by_name(self.session, self.azure_cloud_zone_name)
        self.region_azure=Region.describe(self.session, self.cloudzone_azure.region_id)
        self.image_azure=Image.describe(self.session, image=self.azure_image_name, region=self.region_azure.external_region_id)
        self.image_mapping_azure=ImageMapping.create(self.session, name=self.image_mapping_name, image_name=self.image_azure.name, image_id=self.image_azure.id, region_id=self.region_azure.id, description=None)
        self.assertIsInstance(self.image_mapping_azure, dict)

    def test_15_create_flavor_mapping_aws(self):
        from caspyr import FlavorMapping, CloudZone
        self.cloudzone_aws=CloudZone.describe_by_name(self.session, self.aws_cloud_zone_name)
        self.flavor_mapping=FlavorMapping.create(self.session, self.flavor_mapping_name, description="Ubuntu image mapping.", region_id=self.cloudzone_aws.region_id, mapping_name=self.flavor_mapping_name, flavor_name=self.aws_flavor_name)
        self.assertIsInstance(self.flavor_mapping, FlavorMapping)
        self.assertIsInstance(self.flavor_mapping.id, str)
        self.assertIsInstance(self.flavor_mapping.description, str)
        self.assertIsInstance(self.flavor_mapping.updated_at, str)
        self.assertIsInstance(self.flavor_mapping.organization_id, str)
        self.assertIsInstance(self.flavor_mapping.external_region_id, str)
        self.assertIsInstance(self.flavor_mapping.name, str)
        self.assertIsInstance(self.flavor_mapping._links, object)
        self.assertIsInstance(self.flavor_mapping.flavor_mappings, object)

    def test_16_create_flavor_mapping_azure(self):
        from caspyr import FlavorMapping, CloudZone
        self.cloudzone_azure=CloudZone.describe_by_name(self.session, self.azure_cloud_zone_name)
        self.flavor_mapping=FlavorMapping.create(self.session, self.flavor_mapping_name, description="Ubuntu image mapping.", region_id=self.cloudzone_azure.region_id, mapping_name=self.flavor_mapping_name, flavor_name=self.azure_flavor_name)
        self.assertIsInstance(self.flavor_mapping, FlavorMapping)
        self.assertIsInstance(self.flavor_mapping.id, str)
        self.assertIsInstance(self.flavor_mapping.description, str)
        self.assertIsInstance(self.flavor_mapping.updated_at, str)
        self.assertIsInstance(self.flavor_mapping.organization_id, str)
        self.assertIsInstance(self.flavor_mapping.external_region_id, str)
        self.assertIsInstance(self.flavor_mapping.name, str)
        self.assertIsInstance(self.flavor_mapping._links, object)
        self.assertIsInstance(self.flavor_mapping.flavor_mappings, object)

    def test_17_create_storage_profile_aws(self):
        from caspyr import CloudZone, StorageProfileAWS
        self.cloudzone_aws=CloudZone.describe_by_name(self.session, self.aws_cloud_zone_name)
        self.storage_profile=StorageProfileAWS.create(self.session,
                                                      name = self.aws_storage_profile_name,
                                                      region_id = self.cloudzone_aws.region_id,
                                                      policy_name = self.aws_storage_policy_name,
                                                      device_type = self.aws_storage_device_type,
                                                      volume_type = self.aws_storage_volume_type,
                                                      tags = self.storage_policy_tags
                                                      )
        self.assertIsInstance(self.storage_profile, StorageProfileAWS)

    def test_18_create_storage_profile_azure(self):
        from caspyr import CloudZone, StorageProfileAzure
        self.cloudzone_azure=CloudZone.describe_by_name(self.session, self.azure_cloud_zone_name)
        self.storage_profile=StorageProfileAzure.create(self.session,
                                                        name = self.azure_storage_profile_name,
                                                        region_id = self.cloudzone_azure.region_id,
                                                        policy_name = self.azure_storage_policy_name,
                                                        storage_type = self.azure_storage_storage_type,
                                                        disk_type = self.azure_storage_disk_type,
                                                        os_disk_caching = self.azure_storage_os_disk_caching,
                                                        data_caching = self.azure_storage_data_caching,
                                                        tags = self.storage_policy_tags
                                                        )
        self.assertIsInstance(self.storage_profile, StorageProfileAzure)

    def test_19_create_network_profile_aws(self):
        from caspyr import CloudZone, NetworkFabric, NetworkProfile
        self.cloudzone_aws=CloudZone.describe_by_name(self.session, self.aws_cloud_zone_name)
        self.networks = []
        for i in NetworkFabric.list(self.session):
            self.networks.append(i['id'])
        self.network_profile = NetworkProfile.create(self.session,
                                                     region_id = self.cloudzone_aws.region_id,
                                                     name = self.aws_network_profile_name,
                                                     network_ids = self.networks
                                                    )
        self.assertIsInstance(self.network_profile, NetworkProfile)

    def test_20_create_network_profile_azure(self):
        from caspyr import CloudZone, NetworkFabric, NetworkProfile
        self.cloudzone_azure=CloudZone.describe_by_name(self.session, self.azure_cloud_zone_name)
        self.networks = []
        for i in NetworkFabric.list(self.session):
            self.networks.append(i['id'])
        self.network_profile = NetworkProfile.create(self.session,
                                                     region_id = self.cloudzone_azure.region_id,
                                                     name = self.aws_network_profile_name,
                                                     network_ids = self.networks
                                                    )
        self.assertIsInstance(self.network_profile, NetworkProfile)

    def test_21_create_project(self):
        from caspyr import CloudZone, Project
        self.cloudzone_aws = CloudZone.describe_by_name(self.session, self.aws_cloud_zone_name)
        self.cloudzone_azure = CloudZone.describe_by_name(self.session, self.azure_cloud_zone_name)
        self.project = Project.create(self.session,
                                      name = self.project_name,
                                      zone_configs = [{"zoneId": self.cloudzone_aws.id, "priority": 1, "maxNumberInstances": None}, {"zoneId": self.cloudzone_azure.id, "priority": 2, "maxNumberInstances": None}]
                                      )
        self.assertIsInstance(self.project, Project)


    """
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

    """

if __name__ == '__main__':
    unittest.main(warnings='ignore')