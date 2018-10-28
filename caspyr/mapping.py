import requests
import json
import os
import sys
from abc import ABCMeta, abstractmethod, ABC

class StorageProfile(metaclass=ABCMeta):
    """
    Metaclass for common model attributes across AWS/Azure/vSphere Storage Profiles.
    """
    def __init__(self, profile):
        self.external_region_id = profile['externalRegionId']
        self.name = profile['name']
        try:
            self.description = profile['description']
        except:
            KeyError
        self.id = profile['id']
        self.updated_at = profile['updatedAt']
        self.organization_id = profile['organizationId']
        try:
            self.azure_storage_policies = profile['azureStoragePolicies']
        except KeyError: pass
        try:
            self.aws_storage_policies = profile['awsStoragePolicies']
        except KeyError: pass
        try:
            self.vsphere_storage_policies = profile['vsphereStoragePolicies']
        except KeyError: pass

class StorageProfileAzure(StorageProfile):
    def __init__(self, storageprofile):
        super().__init__(storageprofile)

    @staticmethod
    def list(session):
        uri = '/iaas/storage-profiles-azure'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/storage-profiles-azure/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/storage-profiles-azure/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

    @classmethod
    def create(cls, session, name, region_id, policy_name, os_disk_caching, data_caching, storage_account_id=None, storage_type=None, supports_encryption=False, disk_type=None, tags=None, description=None, default_item=True, ):
        """
        :param name: The name of the Storage Profile.
        :param description: A useful description for the Storage Profile
        :param region_id: Will need to be pulled using Region.describe(session, (CloudZone.describe_by_name(session, name)['region_id'])['id']
        :param default_item: Whether this should be the default policy used when the profile is selected.
        :param storage_type: Can only be managed_disks or False. Defaults to None.
        :param storage_account_id: Required for unmanaged disks. Defaults to None. Comes from /iaas/fabric-azure-storage-accounts
        :param disk_type: Only required for managed_disks. Can be one of Standard_LRS or Premium_LRS.
        :param policy_name: The name of the policy within the profile.
        :param tags: A list of tags in the following format - [{ "key": "foo", "value": "bar"}]
        """
        uri = f'/iaas/storage-profiles-azure/'
        payload = {
            "name" : name,
            "description" : description,
            "regionId" : region_id,
            "azureStoragePolicies" : [{
                "storageAccountId": storage_account_id,
                "storageType": storage_type,
                "defaultItem": default_item,
                "supportsEncryption": supports_encryption,
                "diskType": disk_type,
                "osDiskCaching": os_disk_caching,
                "dataCaching": data_caching,
                "name": policy_name,
                "tags": tags
            }]

        }
        return cls(session._request(f'{session.baseurl}{uri}', request_method='POST', payload=payload))

class StorageProfileAWS(StorageProfile):
    def __init__(self, storageprofile):
        super().__init__(storageprofile)

    @staticmethod
    def list(session):
        uri = '/iaas/storage-profiles-aws'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, id):
        uri = '/iaas/storage-profiles-aws/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/storage-profiles-aws/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def create(cls, session, name, region_id, policy_name, device_type, tags= None, volume_type=None, description=None, default_item=True, supports_encryption=False):
        '''
        :param name: The name of the Storage Profile.
        :param description: A useful description for the Storage Profile
        :param region_id: Will need to be pulled using Region.describe(session, (CloudZone.describe_by_name(session, name)['region_id'])['id']
        :param default_item: Whether this should be the default policy used when the profile is selected.
        :param supports_encryption: A flag to indicate whether policy supports encrypted volumes. Maps to encrypted attribute of the disk in the blueprint schema.
        :param device_type: One of EBS or Instance Store.
        :param volume_type: For EBS, one of gp2, io1, sc1, st1 or standard (magnetic). For Instance Store this value is not required.
        :param policy_name: The name of the policy within the profile.
        :param tags: A list of tags in the following format - [{ "key": "foo", "value": "bar"}]
        '''
        uri = f'/iaas/storage-profiles-aws/'
        payload = {
            "name" : name,
            "description" : description,
            "regionId" : region_id,
            "awsStoragePolicies" : [{
                "defaultItem": default_item,
                "supportsEncryption": supports_encryption,
                "deviceType": device_type,
                "volumeType": volume_type,
                "name": policy_name,
                "tags": tags
            }]

        }
        return cls(session._request(f'{session.baseurl}{uri}', request_method='POST', payload=payload))

class StorageProfilevSphere(StorageProfile):
    def __init__(self, storageprofile):
        super().__init__(storageprofile)

    @staticmethod
    def list(session):
        uri = '/iaas/storage-profiles-vsphere'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/storage-profiles-vsphere/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

class ImageMapping(object):
    def __init__(self, mapping):
        self.id=mapping['id']
        self.name=mapping['name']
        self.description=mapping['description']
        self.updated_at=mapping['updatedAt']
        self.organization_id=mapping['organizationId']
        self.external_region_id=mapping['externalRegionId']
        self._links=mapping['_links']
        self.image_mappings=mapping['imageMappings']

    @staticmethod
    def list(session):
        uri = '/iaas/image-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    def describe(self, session, id):
        uri = f'/iaas/image-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}')['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/image-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

    @classmethod
    def create(cls, session, name, image_name, image_id, region_id, description=None):
        uri = '/iaas/image-profiles'
        payload = {
            "name": f"{name}",
            "description": f"{description}",
            "regionId": f"{region_id}",
            "imageMapping": {
                f"{name}": {
                    "id": f"{image_id}",
                    "name": f"{image_name}"
                }
            }
        }
        return (session._request(f'{session.baseurl}{uri}', request_method='POST', payload=payload))

class Flavor(object):
    def __init__(self, flavor):
        pass

    @staticmethod
    def describe(session):
        uri = f'/iaas/flavors/'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def describe_by_name(cls, session, name):
        uri = f'/iaas/flavors/'
        j = session._request(f'{session.baseurl}{uri}')['content'][0]
        return cls(j)

class FlavorMapping(object):
    def __init__(self, mapping):
        self.id=mapping['id']
        self.name=mapping['name']
        try:
            self.description=mapping['description']
        except:
            KeyError
        self.updated_at=mapping['updatedAt']
        self.organization_id=mapping['organizationId']
        self.external_region_id=mapping['externalRegionId']
        self._links=mapping['_links']
        self.image_mappings=mapping['flavorMappings']

    @staticmethod
    def list(session):
        uri = '/iaas/flavor-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/flavor-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

    @classmethod
    def create(cls, session, name, mapping_name, region_id, flavor_name=None, cpuCount=None, memoryGb=None, memoryMb=None, description=None):
        uri='/iaas/flavor-profiles/'
        if memoryGb:
            memoryMb=memoryGb*1024
        payload = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "flavorMapping": {
                mapping_name: {
                    "id": flavor_name,
                    "cpuCount": cpuCount,
                    "memoryMb": memoryMb
                }
            }
        }
        return cls(session._request(f'{session.baseurl}{uri}', request_method='POST', payload=payload))

class NetworkFabric(object):
    """

    """
    def __init__(self, network):
        self.external_region_id = network['externalRegionId']
        self.name = network['name']
        self.id = network['id']
        self.self_link = network['selfLink']
        self.created_at = network['createdAt']
        self.updated_at = network['updatedAt']
        self.organization_id = network['organizationId']
        self._links = network['_links']
        try:
            self.is_public = network['isPublic']
        except KeyError: pass
        try:
            self.is_default = network['isDefault']
        except KeyError: pass
        try:
            self.cidr = network['cidr']
        except KeyError: pass

    @staticmethod
    def list(session):
        uri = '/iaas/fabric-networks'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            data = list()
            for i in j['content']:
                data.append({i['externalRegionId'], i['name'], i['id']})
            return data
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def list_for_region(session, region="*"):
        uri = f'/iaas/fabric-networks?$filter=externalRegionId eq {region}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            data = list()
            for i in j['content']:
                data.append({i['externalRegionId'], i['name'], i['id']})
            return data
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/fabric-networks/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe_by_name(cls, session):
        pass

class NetworkProfile(object):
    """
    Class for Network Profile methods.
    """

    def __init__(self, network):
        self.external_region_id = network['externalRegionId']
        self.isolation_type = network['isolationType']
        self.tags = network['tags']
        self.name = network['name']
        self.id = network['id']
        self.self_link = network['selfLink']
        self.updated_at = network['updatedAt']
        self.organization_id = network['organizationId']
        self._links = network['_links']

    @classmethod
    def list(cls, session):
        uri = '/iaas/network-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def create(cls, session, name, region, networks=[], tags=[]):
        """
        This method requires you to peel the onion a bit.
        It is worth noting that network profiles are scoped to a given region.
        To get the region info you need, first off determine the Cloud Account that has the networks you want to add to your network profile.
        Perform a CloudAccount.describe(session, id) against that account, and return the cls.enabled_region_ids.
        Use the enabled_region_id value for the region you want to configure networks for.
        :param session: type: object. Generated from Session.login(token).
        :param name: type: string. The desired name of the network profile.
        :param networks: type: array. A list of networks and their ids can be found using NetworkFabric.list_for_region(session, region). The region itself can be found by CloudAccount.describe
        :param region: type:string. The id is generated from ProvisioningRegion.find_by_region_id(session, )
        :returns: this is a description of what is returned
        :raises keyError: raises an exception
        """
        uri = '/iaas/network-profiles'
        data = {
            "name": name,
            "regionId": region,
            "fabricNetworkIds" : networks,
            "tags": tags
        }
        return session._request(f'{session.baseurl}{uri}', request_method='POST', json=data)


    @staticmethod
    def delete(session, id):
        uri = f'/iaas/network-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/network-profiles/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

class Network(object):
    def __init__(self, network):
        pass

    @staticmethod
    def list(session):
        uri = f'/iaas/networks'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/networks/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/networks/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')