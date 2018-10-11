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
        self.description = profile['description']
        self.id = profile['id']
        self.self_link = profile['selfLink']
        self.updated_at = profile['updatedAt']
        self.organization_id = profile['organizationId']
        self._links = profile['_links']
        try:
            self.azure_storage_policies = profile['azureStoragePolicies']
        except KeyError: pass
        try:
            self.aws_storage_policies = profile['azureStoragePolicies']
        except KeyError: pass
        try:
            self.vsphere_storage_policies = profile['azureStoragePolicies']
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
        return session._request(f'{session.baseurl}{uri}', method='DELETE')

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
        return session._request(f'{session.baseurl}{uri}', method='DELETE')

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
        return session._request(f'{session.baseurl}{uri}', method='DELETE')


class ImageMapping(object):
    @staticmethod
    def list(session):
        uri = '/iaas/image-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, i):
        uri = f'/iaas/image-profiles/{i}'
        return session._request(f'{session.baseurl}{uri}', method='DELETE')

    @staticmethod
    def create(session, name="Ubuntu", image="Canonical:UbuntuServer:16.04-LTS:latest", region="dev azure / westus", description=None):
        #uri = '/iaas/image-profiles'
        uri = f'/iaas/fabric-images?$filter=name eq {image}'
        data = [{
            "imageMappings" : {
                "mapping" : {
                    f"{name}" : {
                        "externalRegionId" : f"{region}",
                        "name" : f"{image}",
                        "description" : f"{description}",
                    }
                }
            }
        }]
        return session._request(f'{session.baseurl}{uri}', method='POST', json=data)


class FlavorMapping(object):
    @staticmethod
    def list(session):
        uri = '/iaas/flavor-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/flavor-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}', method='DELETE')

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
    def find_by_name(cls, session):
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
        To get the region info you need, First off, determine the Cloud Account that has the networks you want to add to your network profile.
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