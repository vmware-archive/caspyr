# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0


from abc import ABCMeta


class StorageProfile(metaclass=ABCMeta):
    """
    Metaclass for common model attributes across AWS/Azure/vSphere
    Storage Profiles.
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
        except KeyError:
            pass
        try:
            self.aws_storage_policies = profile['awsStoragePolicies']
        except KeyError:
            pass
        try:
            self.vsphere_storage_policies = profile['vsphereStoragePolicies']
        except KeyError:
            pass

    @staticmethod
    def list(session):
        uri = '/iaas/api/storage-profiles'
        return session._request(f'{session.baseurl}{uri}')['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/storage-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )


class StorageProfileAzure(StorageProfile):
    def __init__(self, storageprofile):
        super().__init__(storageprofile)

    @staticmethod
    def list(session):
        uri = '/iaas/api/storage-profiles-azure/'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/storage-profiles-azure/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/storage-profiles-azure/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @classmethod
    def create(cls,
               session,
               name,
               region_id,
               policy_name,
               os_disk_caching,
               data_caching,
               storage_account_id=None,
               storage_type=None,
               supports_encryption=False,
               disk_type=None,
               tags=None,
               description=None,
               default_item=True
               ):
        """
        :param name: The name of the Storage Profile.
        :param description: A useful description for the Storage Profile
        :param region_id: Will need to be pulled using
        Region.describe(session, (CloudZone.describe_by_name(session,
                                                             name)['region_id'])['id']
        :param default_item: Whether this should be the default policy used
        when the profile is selected.
        :param storage_type: Can only be managed_disks or False.
        Defaults to None.
        :param storage_account_id: Required for unmanaged disks.
        Defaults to None. Comes from /iaas/api/fabric-azure-storage-accounts
        :param disk_type: Only required for managed_disks. Can be one of
        Standard_LRS or Premium_LRS.
        :param policy_name: The name of the policy within the profile.
        :param tags: A list of tags in the following format:
        [{ "key": "foo", "value": "bar"}]
        """
        uri = f'/iaas/api/storage-profiles-azure/'
        payload = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "azureStoragePolicies": [{
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
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))


class StorageProfileAWS(StorageProfile):
    def __init__(self, storageprofile):
        super().__init__(storageprofile)

    @staticmethod
    def list(session):
        uri = '/iaas/api/storage-profiles-aws/'
        return session._request(f'{session.baseurl}{uri}')['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/storage-profiles-aws/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/storage-profiles-aws/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def create(cls,
               session,
               name,
               region_id,
               policy_name,
               device_type,
               tags=None,
               volume_type=None,
               description=None,
               default_item=True,
               supports_encryption=False
               ):
        '''
        :param name: The name of the Storage Profile.
        :param description: A useful description for the Storage Profile
        :param region_id: Will need to be pulled using
        Region.describe(session, (CloudZone.describe_by_name(session,
                                                             name)['region_id'])['id']
        :param default_item: Whether this should be the default policy used
        when the profile is selected.
        :param supports_encryption: A flag to indicate whether policy supports
        encrypted volumes. Maps to encrypted attribute of the disk in the
        blueprint schema.
        :param device_type: One of EBS or Instance Store.
        :param volume_type: For EBS, one of gp2, io1, sc1, st1 or standard
        (magnetic). For Instance Store this value is not required.
        :param policy_name: The name of the policy within the profile.
        :param tags: A list of tags in the following format:
        [{ "key": "foo", "value": "bar"}]
        '''
        uri = f'/iaas/api/storage-profiles-aws/'
        payload = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "awsStoragePolicies": [{
                "defaultItem": default_item,
                "supportsEncryption": supports_encryption,
                "deviceType": device_type,
                "volumeType": volume_type,
                "name": policy_name,
                "tags": tags
            }]

        }
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))


class StorageProfilevSphere(StorageProfile):
    def __init__(self, storageprofile):
        super().__init__(storageprofile)

    @staticmethod
    def list(session):
        uri = '/iaas/api/storage-profiles-vsphere'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/storage-profiles-vsphere/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )


class ImageMapping(object):
    def __init__(self, mapping):
        self.id = mapping['id']
        self.name = mapping['name']
        self.description = mapping['description']
        self.updated_at = mapping['updatedAt']
        self.organization_id = mapping['organizationId']
        self.external_region_id = mapping['externalRegionId']
        self._links = mapping['_links']
        self.image_mappings = mapping['imageMappings']

    @staticmethod
    def list(session):
        uri = '/iaas/api/image-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    def describe(self, session, id):
        uri = f'/iaas/api/image-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}')['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/image-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @classmethod
    def create(cls,
               session,
               name,
               image_name,
               image_id,
               region_id,
               description=None
               ):
        uri = '/iaas/api/image-profiles'
        payload = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "imageMapping": {
                name: {
                    "id": image_id,
                    "name": image_name
                }
            }
        }
        return (session._request(f'{session.baseurl}{uri}',
                                 request_method='POST',
                                 payload=payload
                                 ))


class Flavor(object):
    def __init__(self, flavor):
        pass

    @staticmethod
    def describe(session):
        uri = f'/iaas/api/flavors/'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def describe_by_name(cls, session, name):
        uri = f'/iaas/api/flavors/'
        j = session._request(f'{session.baseurl}{uri}')['content'][0]
        return cls(j)


class FlavorMapping(object):
    def __init__(self, mapping):
        self.id = mapping['id']
        self.name = mapping['name']
        try:
            self.description = mapping['description']
        except KeyError:
            pass
        self.updated_at = mapping['updatedAt']
        self.organization_id = mapping['organizationId']
        self.external_region_id = mapping['externalRegionId']
        self._links = mapping['_links']
        self.flavor_mappings = mapping['flavorMappings']

    @staticmethod
    def list(session):
        uri = '/iaas/api/flavor-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/flavor-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @classmethod
    def create(cls,
               session,
               name,
               mapping_name,
               region_id,
               flavor_name=None,
               cpuCount=None,
               memoryGb=None,
               memoryMb=None,
               description=None
               ):
        uri = '/iaas/api/flavor-profiles/'
        if memoryGb:
            memoryMb = memoryGb*1024
        payload = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "flavorMapping": {
                mapping_name: {
                    "name": flavor_name,
                    "cpuCount": cpuCount,
                    "memoryMb": memoryMb
                }
            }
        }
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))


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
        self.updated_at = network['updatedAt']
        self.organization_id = network['organizationId']
        self._links = network['_links']

    @classmethod
    def list(cls, session):
        uri = '/iaas/api/network-profiles'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def create(cls,
               session,
               name,
               region_id,
               network_ids,
               isolation_type=None,
               security_group_ids=None,
               isolation_network_domain_id=None,
               isolation_network_domain_cidr=None,
               isolation_ext_net_fabric_id=None,
               isolated_network_cidr_prefix=None,
               description=None,
               tags=None):
        """[summary]
        :param session: [description]
        :type session: [type]
        :param name: [description]
        :type name: [type]
        :param region_id: [description]
        :type region_id: [type]
        :param network_ids: [description]
        :type network_ids: [type]
        :param isolation_type: [description], defaults to None
        :param isolation_type: [type], optional
        :param security_group_ids: [description], defaults to None
        :param security_group_ids: [type], optional
        :param isolation_network_domain_id: [description], defaults to None
        :param isolation_network_domain_id: [type], optional
        :param isolation_network_domain_cidr: [description], defaults to None
        :param isolation_network_domain_cidr: [type], optional
        :param isolation_external_network_fabric_id: [description].
        Defaults to None.
        :param isolation_external_network_fabric_id: [type], optional
        :param isolated_network_cidr_prefix: [description], defaults to None
        :param isolated_network_cidr_prefix: [type], optional
        :param description: [description], defaults to None
        :param description: [type], optional
        :param tags: [description], defaults to None
        :type tags: List, optional
        :return: [description]
        :rtype: [type]
        """
        uri = '/iaas/api/network-profiles'
        payload = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "fabricNetworkIds": network_ids,
            "isolationType": isolation_type,
            "securityGroupIds": security_group_ids,
            "isolationNetworkDomainId": isolation_network_domain_id,
            "isolationNetworkDomainCIDR": isolation_network_domain_cidr,
            "isolationExternalFabricNetworkId": isolation_ext_net_fabric_id,
            "isolatedNetworkCIDRPrefix": isolated_network_cidr_prefix,
            "tags": tags
        }
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/network-profiles/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/network-profiles/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))
