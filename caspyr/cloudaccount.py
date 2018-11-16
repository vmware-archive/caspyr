import requests
import json
import os
import sys
from abc import ABCMeta, abstractmethod, ABC
import logging

logger = logging.getLogger('caspyr.__name__')


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
        self.cloud_account_properties = cloudaccount['cloudAccountProperties']
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
        """
        Returns a list of account ids.
        """
        return (session._request(url=f'{session.baseurl}{uri}'))['content']

    @classmethod
    @abstractmethod
    def describe(cls, session, uri):
        """
        Returns the detail of a cloud account.
        """
        return (session._request(url=f'{session.baseurl}{uri}'))

    @classmethod
    @abstractmethod
    def create(cls, session, uri, payload):
        """
        Creates a Cloud Account.
        """
        return session._request(url=f'{session.baseurl}{uri}',
                                request_method='POST',
                                payload=payload
                                )

    @classmethod
    @abstractmethod
    def unregister(cls, session, uri):
        """
        Removes the cloud account from cloud assembly only,
        leaves it registered in discovery.
        """
        return session._request(url=f'{session.baseurl}{uri}',
                                request_method='DELETE')

    @staticmethod
    @abstractmethod
    def delete(session, uri):
        """
        Removes the cloud account from discovery, and all other services.
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
    def describe(cls, session, id):
        uri = f'/iaas/cloud-accounts/{id}'
        return cls(super().describe(session, uri))

    @classmethod
    def unregister(cls, session, id):
        uri = f'/iaas/cloud-accounts/{id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, id):
        uri = f'/api/cloud-accounts/{id}'
        return super().delete(session, uri)

    @classmethod
    def create(cls):
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
    def describe(cls, session, id):
        uri = f'/iaas/cloud-accounts-aws/{id}'
        return cls(super().describe(session, uri))

    @classmethod
    def unregister(cls, session, id):
        uri = f'/iaas/cloud-accounts-aws/{id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, id):
        uri = f'/api/cloud-accounts/{id}'
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


class CloudAccountAzure(Base):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-azure'
        return super().list(session, uri)['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/cloud-accounts-azure/{id}'
        return cls(super().describe(session, uri))

    @classmethod
    def unregister(cls, session, id):
        uri = f'/iaas/cloud-accounts-azure/{id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, id):
        uri = f'/api/cloud-accounts/{id}'
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


class CloudAccountvSphere(Base):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-vsphere'
        return super().list(session, uri)

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/cloud-accounts-vsphere/{id}'
        return super().describe(session, uri)

    @classmethod
    def unregister(cls, session, id):
        uri = f'/iaas/cloud-accounts-vsphere/{id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, id):
        uri = f'/api/cloud-accounts/{id}'
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


class CloudAccountNSXT(Base):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-nsx-t'
        return super().list(session, uri)['content']

    @staticmethod
    def describe(session, id):
        uri = f'/iaas/cloud-accounts-nsx-t/{id}'
        return super().describe(session, uri)

    @classmethod
    def unregister(cls, session, id):
        uri = f'/iaas/cloud-accounts-nsx-t/{id}'
        return super().unregister(session, uri)

    @classmethod
    def delete(cls, session, id):
        uri = f'/api/cloud-accounts/{id}'
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
