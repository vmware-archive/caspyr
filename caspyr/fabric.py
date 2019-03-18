# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

"""
The Fabric module contains all the classes and methods required to get the
underlying information for creating Image Mappings, Flavor Mappings, Network
Profiles and Storage Profiles.
"""


class Image(object):
    def __init__(self, image):
        try:
            self.os_family = image['osFamily']
        except KeyError:
            pass
        self.external_region_id = image['externalRegionId']
        self.is_private = image['isPrivate']
        self.external_id = image['externalId']
        self.name = image['name']
        self.description = image['description']
        self.id = image['id']
        self.updated_at = image['updatedAt']
        self._links = image['_links']

    @classmethod
    def describe(cls, session, image, region):
        """
        Used to create an instance of the image class. Image details are
        unique by 'region', so the region must be provided.
        :param session: An instance of the Session class.
        :type session: Session
        :param image: The name of the image you want to describe.
        :type image: string
        :param region: The external region id value (friendly name of the
        :type region - eg. westus or us-west-1).
        :return: Returns an instance of the image claass.
        :rtype: Image
        """

        uri = f'/iaas/api/fabric-images?$filter=(name eq \'{image}\') and (externalRegionId eq \'{region}\')'

        j = session._request(f'{session.baseurl}{uri}')['content'][0]
        return cls(j)


class AzureStorageAccount(object):
    """
    The StorageAccountAzure class is a representation of the
    fabric-azure-storage-account API. It is only used when creating
    a storage profile for azure unmanaged disks (see Mapping module).
    """

    def __init(self, account):
        self.type = account["type"]
        self.external_region_id = account["externalRegionId"]
        self.external_id = account["externalId"]
        self.name = account["name"]
        self.id = account["id"]
        self.created_at = account["createdAt"]
        self.updated_at = account["updatedAt"]
        self.organization_id = account["organizationId"]
        self._links = account["_links"]

    @staticmethod
    def list(session):
        """
        Used to list all of the storage accounts associated with Azure
        unmanaged disks.
        :param session: An instance of the Session class.
        :type session: Session
        :return: Returns a list of storage accounts.
        """
        uri = f'/iaas/api/fabric-azure-storage-account'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def describe_by_name(cls, session, name):
        """
        Used to create an instance of the StorageAccountAzure class, after
        finding it by name.
        :param session: An instance of the Session class.
        :type session: Session
        :param name: The name of the unmanaged disk.
        :type name: string
        :return: Returns an instance of the StorageAccountAzure class.
        :rtype: StorageAccountAzure
        """
        j = cls.list(session)
        for i in j:
            if i['name'] == name:
                return cls(i)


class NetworkFabric(object):
    def __init__(self, network):
        self.external_region_id = network['externalRegionId']
        self.name = network['name']
        self.id = network['id']
        self.created_at = network['createdAt']
        self.updated_at = network['updatedAt']
        self.organization_id = network['organizationId']
        self._links = network['_links']
        try:
            self.is_public = network['isPublic']
        except KeyError:
            pass
        try:
            self.is_default = network['isDefault']
        except KeyError:
            pass
        try:
            self.cidr = network['cidr']
        except KeyError:
            pass

    @staticmethod
    def list(session):
        """
        :param session: An instance of the Session class.
        :type session: Session
        :return: [description]
        :rtype: [type]
        """
        uri = f'/iaas/api/fabric-networks'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def list_by_region(cls, session, region="*"):
        uri = f'/iaas/api/fabric-networks?$filter=externalRegionId eq {region}'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def describe_by_name(cls, session, name, region="*"):
        uri = (f'/iaas/api/fabric-networks?$filter=(name eq {name}) and '
               '(externalRegionId eq {region})')
        return cls(session._request(f'{session.baseurl}{uri}')['content'])

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/fabric-networks/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def update(cls, session, id, tags):
        """

        :param session: [description]
        :type session: [type]
        :param id: [description]
        :type id: [type]
        :param tags:
        :return: [description]
        :rtype: [type]
        """
        uri = f'/iaas/api/fabric-network/{id}'
        payload = {
            tags
        }
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='PATCH',
                                    payload=payload
                                    ))


class AwsVolumeType(object):
    pass


class vSphereDatastore(object):
    pass


class vSphereStoragePolicy(object):
    pass


class Flavor(object):
    def __init__(self, flavor):
        pass

    @staticmethod
    def describe(session):
        uri = f'/iaas/api/fabric-flavors'
        print(session._request(f'{session.baseurl}{uri}')['content'][0])
