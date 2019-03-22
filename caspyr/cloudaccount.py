# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    """
    Abstract Base Class for all Cloud Account classes.
    """

    def __init__(self, cloudaccount):
        self.id = cloudaccount['id']
        self.name = cloudaccount['name']
        self.enabled_region_ids = cloudaccount['enabledRegionIds']
        self.organization = cloudaccount['organizationId']
        self._links = cloudaccount['_links']
        self.custom_properties = cloudaccount['customProperties']
        try:
            self.cloud_account_properties = cloudaccount['cloudAccountProperties']
        except KeyError:
            pass
        try:
            self.type = cloudaccount['type']
        except KeyError:
            pass
        try:
            self.description = cloudaccount['description']
        except KeyError:
            pass

    @classmethod
    @abstractmethod
    def list(self, session, uri):
        """ Returns a list of account ids.
        """
        return (session._request(url=f'{session.baseurl}{uri}'))['content']

    @classmethod
    @abstractmethod
    def describe(cls, session, uri):
        """ Returns the detail of a cloud account.
        """
        return session._request(url=f'{session.baseurl}{uri}')

    @classmethod
    @abstractmethod
    def create(cls, session, uri, payload):
        """ Creates a Cloud Account.
        """
        return session._request(url=f'{session.baseurl}{uri}',
                                request_method='POST',
                                payload=payload
                                )

    @classmethod
    @abstractmethod
    def unregister(cls, session, uri):
        """ Removes the cloud account from Cloud Assembly only,
        leaves it registered in discovery.
        """

        return session._request(url=f'{session.baseurl}{uri}',
                                request_method='DELETE')

    @staticmethod
    @abstractmethod
    def delete(session, uri):
        """ Removes the Cloud Account from discovery, and all other services.
        """
        return session._request(url=f'{session.baseurl}{uri}',
                                request_method='DELETE')

    @staticmethod
    @abstractmethod
    def update(session, id, payload):
        uri = f'/iaas/cloud-accounts/{id}'
        return session._request(url=f'{session.baseurl}{uri}',
                                request_method='PATCH',
                                payload=payload
                                )


class CloudAccount(Base):
    """
    Class for Cloud Account methods.
    """
    def __init__(self, cloudaccount):
        super().__init__(cloudaccount)

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts'
        return super().list(session, uri)

    @classmethod
    def describe(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts/{cloud_account_id}'
        return cls(super().describe(session, uri))

    @classmethod
    def unregister(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts/{cloud_account_id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, cloud_account_id):
        uri = f'/api/cloud-accounts/{cloud_account_id}'
        return super().delete(session, uri)

    @classmethod
    def create(cls):
        pass

    @classmethod
    def update(cls):
        pass


class CloudAccountAws(Base):
    """
    Class for AWS Cloud Account methods.
    """
    def __init__(self, cloudaccount):
        super().__init__(cloudaccount)

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-aws'
        return super().list(session, uri)['content']

    @classmethod
    def describe(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-aws/{cloud_account_id}'
        return cls(super().describe(session, uri))

    @classmethod
    def unregister(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-aws/{cloud_account_id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, cloud_account_id):
        uri = f'/api/cloud-accounts/{cloud_account_id}'
        return super().delete(session, uri)

    @classmethod
    def create(cls,
               session,
               name,
               access_key,
               secret_key,
               regions='us-west-1',
               create_zone=False,
               description=None
               ):
        uri = '/iaas/cloud-accounts-aws'
        payload = {
            "name": name,
            "description": description,
            "accessKeyId": access_key,
            "secretAccessKey": secret_key,
            "regionIds": [regions],
            "createDefaultZones": create_zone
        }
        return cls(super().create(session, uri=uri, payload=payload))

    @classmethod
    def update(cls):
        pass


class CloudAccountAzure(Base):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-azure'
        return super().list(session, uri)['content']

    @classmethod
    def describe(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-azure/{cloud_account_id}'
        return cls(super().describe(session, uri))

    @classmethod
    def unregister(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-azure/{cloud_account_id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, cloud_account_id):
        uri = f'/api/cloud-accounts/{cloud_account_id}'
        return super().delete(session, uri)

    @classmethod
    def create(cls,
               session,
               name,
               subscription_id,
               tenant_id,
               application_id,
               application_key,
               regions='westus',
               create_zone=False,
               description=None
               ):
        payload = {
            "name": name,
            "description": description,
            "subscriptionId": subscription_id,
            "tenantId": tenant_id,
            "clientApplicationId": application_id,
            "clientApplicationSecretKey": application_key,
            "regionIds": [regions],
            "createDefaultZones": create_zone
        }
        uri = '/iaas/cloud-accounts-azure'
        return cls(super().create(session, uri=uri, payload=payload))

    @classmethod
    def update(cls):
        pass


class CloudAccountvSphere(Base):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-vsphere'
        return super().list(session, uri)

    @classmethod
    def describe(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-vsphere/{cloud_account_id}'
        return super().describe(session, uri)

    @classmethod
    def unregister(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-vsphere/{cloud_account_id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, cloud_account_id):
        uri = f'/api/cloud-accounts/{cloud_account_id}'
        return super().delete(session, uri)

    @classmethod
    def create(cls,
               session,
               name,
               fqdn,
               rdc,
               username,
               password,
               datacenter_moid,
               nsx_cloud_account=None,
               description=None
               ):
        """[summary]

        :param session: [description]
        :type session: [type]
        :param name: [description]
        :type name: [type]
        :param fqdn: [description]
        :type fqdn: [type]
        :param rdc: [description]
        :type rdc: [type]
        :param username: [description]
        :type username: [type]
        :param password: [description]
        :type password: [type]
        :param datacenter_moid: [description]
        :type datacenter_moid: [type]
        :param nsx_cloud_account: [description], defaults to None
        :param nsx_cloud_account: [type], optional
        :param description: [description], defaults to None
        :param description: [type], optional
        :return: [description]
        :rtype: [type]
        """

        uri = '/iaas/cloud-accounts-vsphere'
        payload = {
            "name": name,
            "description": description,
            "hostName": fqdn,
            "acceptSelfSignedCertificate": True,
            "associatedCloudAccountIds": nsx_cloud_account,
            "dcid": rdc,
            "username": username,
            "password": password,
            "regionIds": datacenter_moid,
            "createDefaultZones": False
            }
        return cls(super().create(session, uri=uri, payload=payload))

    @classmethod
    def update(cls):
        pass


class CloudAccountNSXT(Base):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-nsx-t'
        return super().list(session, uri)['content']

    @staticmethod
    def describe(session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-nsx-t/{cloud_account_id}'
        return super().describe(session, uri)

    @classmethod
    def unregister(cls, session, cloud_account_id):
        uri = f'/iaas/cloud-accounts-nsx-t/{cloud_account_id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, cloud_account_id):
        uri = f'/api/cloud-accounts/{cloud_account_id}'
        return super().delete(session, uri)

    @classmethod
    def create(cls,
               session,
               name,
               fqdn,
               rdc,
               username,
               password,
               description=None
               ):
        uri = '/iaas/cloud-accounts-nsx-t/'
        payload = {
            "name": name,
            "description": description,
            "hostName": fqdn,
            "acceptSelfSignedCertificate": True,
            "dcid": rdc,
            "username": username,
            "password": password
            }
        return cls(super().create(session, uri=uri, payload=payload))

    @classmethod
    def update(cls):
        pass
