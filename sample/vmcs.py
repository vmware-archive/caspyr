"""
Initial structure for classes and functions as they pertain to VMCS automation functions.
"""

import requests
import json
import os
import sys
from abc import ABCMeta, abstractmethod


class Session(object):
    """
    Session class for instantiating a logged in session
    for VMCS.

    Requires refresh token from VMCS portal to instantiate
    """
    def __init__(self, auth_token):
        self.token = 'Bearer '+auth_token
        self.headers = {'Content-Type':'application/json','authorization': self.token}
        self.baseurl = 'https://api.mgmt.cloud.vmware.com'

    @classmethod
    def login(self, refresh_token):
            baseurl = 'https://api.mgmt.cloud.vmware.com'
            uri = '/iaas/login'
            headers = {'Content-Type':'application/json'}
            payload = json.dumps({"refreshToken": refresh_token })
            try:
                r = requests.post(f'{baseurl}{uri}', headers = headers, data = payload)
                print('Login successful.')
                auth_token = r.json()['token']
                return self(auth_token)
            except requests.exceptions.HTTPError as e:
                print(e)
                sys.exit(1)

class Request(object):
    """
    Class for request methods.
    """

    def __init__(self, request):
        self.id = request['id']
        self.deployment_name = request['deploymentName']
        self.deployment_id = request['deploymentId']
        self.description = request['description']
        self.type = request['type']
        self.reason = request['reason']
        self.plan = request['plan']
        self.destroy = request['destroy']
        self.blueprint_id = request['blueprintId']
        self.inputs = request['inputs']
        self.status = request['status']
        self.project_name = request['projectName']
        self.project_id = request['projectId']
        self.created_at = request['createdAt']
        self.created_by = request['createdBy']
        self.updated_at = request['updatedAt']
        self.updated_by = request['updatedBy']
        self.request_tracker_link = request['requestTrackerLink']
        self.flow_id = request['flowId']
        self.flow_execution_id = request['flowExecutionId']
        self.self_link = request['selfLink']
        self.tenants = request['tenants']
        if request['failureMessage']:
            self.failure_message = request['failureMessage']
        if request['validationMessages']:
            self.validation_messages = request['validationMessages']

    @classmethod
    def list(cls, session):
        uri = '/blueprint/api/blueprint-requests/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j['links']:
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @classmethod
    def describe(cls, session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def cancel(session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}?action=cancel'
        try:
            requests.post(f'{session.baseurl}{uri}', headers = session.headers)
        except requests.exceptions.HTTPError as e:
            print(e)
        return


class Blueprint(object):
    """
    Classes for Blueprint methods.

    """
    def __init__(self, blueprint):
        self.name = blueprint['name']
        self.description = blueprint['description']
        self.tags = blueprint['tags']
        self.content = blueprint['content']
        self.valid = blueprint['valid']
        self.validation_messages = blueprint['validationMessages']
        self.status = blueprint['status']
        self.project_id = blueprint['projectId']
        self.project_name = blueprint['projectName']
        self.type = blueprint['type']
        self.id = blueprint['id']
        self.self_link = blueprint['selfLink']
        self.created_at = blueprint['createdAt']
        self.created_by = blueprint['createdBy']
        self.updated_at = blueprint['updatedAt']
        self.updated_by = blueprint['updatedBy']
        self.tenants = blueprint['tenants']


    @staticmethod
    def list(session):
        uri = '/blueprint/api/blueprints/'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            data = list()
            for i in j['links']:
                i = os.path.split(i)[1]
                data.append(i)
            return data
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, bp):
        uri= f'/blueprint/api/blueprints/{bp}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def createFromJSON(cls, session, jsonfile):
        bp = open(jsonfile).read()
        uri= f'/blueprint/api/blueprints'
        try:
            r = requests.post(f'{session.baseurl}{uri}', data = bp, headers = session.headers)
            r.raise_for_status()
            return cls(r.content)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def create(cls, session, bpname, displayname, description, number, raw_data_url):
        uri= f'/blueprint/api/blueprints'
        data = requests.get(raw_data_url)
        data_string = data.text
        jsondata = {}
        jsondata['name'] = bpname
        jsondata['displayName'] = displayname
        jsondata['description']  = description
        jsondata['iteration'] = number
        jsondata['tags'] = []
        jsondata['content'] = data_string
        try:
            r = requests.post(f'{session.baseurl}{uri}', data = json.dumps(jsondata), headers = session.headers)
            r.raise_for_status()
            return cls(r.content)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete(session, id):
        uri= f'/blueprint/api/blueprints/{id}'
        try:
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            return
        except requests.exceptions.HTTPError as e:
            print(e)


class Account(metaclass=ABCMeta):
    """
    Metaclass for Cloud Accounts.
    """

    def __init__(self, cloudaccount):
        self.id = cloudaccount['id']
        self.name = cloudaccount['name']
        self.type = cloudaccount['cloudAccountType']
        self.enabled_region_ids = cloudaccount['enabledRegionIds']
        self.organization = cloudaccount['organizationId']
        self.self_link = cloudaccount['selfLink']
        self._links= cloudaccount['_links']
        self.custom_properties = cloudaccount['customProperties']
        try:
            self.type = cloudaccount['type']
        except KeyError: pass
        try:
            self.description = cloudaccount['description']
        except KeyError: pass

class CloudAccount(Account):
    """
    Class for Cloud Account methods.
    """

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            data = list()
            for i in j['content']:
                data.append(i['id'])
            return data
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/cloud-accounts/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def remove(cls, session, id):
        uri = f'/api/cloud-accounts/{id}'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        return

    @classmethod
    def delete(cls, session, id):
        uri = f'/iaas/cloud-accounts/{id}'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        return


class CloudAccountAws(Account):
    """
    Class for AWS Cloud Account methods.
    """

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-aws'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            data = list()
            for i in j['content']:
                data.append(i['id'])
            return data
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def create(cls, session, name, access_key, secret_key, regions = 'us-west-1', create_zone = False, description = ''):
        print('Creating AWS Cloud Account',name)
        body = {
            "name": name,
            "description": description,
            "accessKeyId": access_key,
            "secretAccessKey": secret_key,
            "regionIds": [regions],
            "createDefaultZones": create_zone
        }
        uri = '/iaas/cloud-accounts-aws'
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = json.dumps(body))
            j=r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def remove(cls, session, id):
        uri = f'/api/cloud-accounts-aws/{id}'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        return

class CloudAccountAzure(Account):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-azure'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j['content']:
            data.append(i)
        return data

    @classmethod
    def create(cls, session, name, subscription_id, tenant_id, application_id, application_key, regions = 'westus', create_zone = False, description = ''):
        body = {
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
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = json.dumps(body))
            r.raise_for_status()
            j=r.json()
            print('Cloud Account',name,'created')
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

class CloudAccountvSphere(Account):

    @classmethod
    def list(cls, session):
        uri = '/iaas/cloud-accounts-vsphere'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            data = list()
            for i in j['content']:
                data.append(i)
            return data
        except requests.exceptions.HTTPError as e:
            print(e)


    @staticmethod
    def createvSphere(session, name, fqdn, rdc, username, password, datacenter_moid, nsx_cloud_account='', description = ''):
        print('Creating vSphere Cloud Account',name)
        body = {
            "name": name,
            "description": description,
            "hostName": fqdn,
            "acceptSelfSignedCertificate": True,
            "linkedCloudAccountLink": nsx_cloud_account,
            "dcid": rdc,
            "username": username,
            "password": password,
            "regionIds": datacenter_moid,
            "createDefaultZones": False
            }
        uri = '/iaas/cloud-accounts-azure'
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = json.dumps(body))
            r.raise_for_status()
            j=r.json()
            print('Cloud Account',name,'created')
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

    @classmethod
    def createNSXT(cls, session, name, fqdn, rdc, username, password, description = ''):
        print('Creating NSX-T Cloud Account',name)
        body = {
            "name": name,
            "description": description,
            "hostName": fqdn,
            "acceptSelfSignedCertificate": True,
            "dcid": rdc,
            "username": username,
            "password": password,
            "createDefaultZones": False
            }
        uri = '/iaas/cloud-accounts-azure'
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = json.dumps(body))
            r.raise_for_status()
            j=r.json()
            print('Cloud Account',name,'created')
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)


class Project(object):
    """
    Class for Project methods
    """

    def __init__(self, project):
        self.administrators = project['administrators']
        self.members = project['members']
        self.zones = project['zones']
        self.name = project['name']
        self.description = project['description']
        self.id = project['id']
        self.self_link = project['selfLink']
        self.organization_id = project['organizationId']
        self._links = project['_links']

    @classmethod
    def list(cls, session):
        uri = '/iaas/projects'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            data = list()
            for i in j['content']:
                data.append(i['id'])
            return data
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/projects/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/projects/{id}'
        try:
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            return
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def removezones(cls, session, id):
        uri = f'/iaas/projects/{id}'
        data = {}
        data['zoneAssignmentConfigurations'] = []
        try:
            r = requests.patch(f'{session.baseurl}{uri}', headers = session.headers, json = data)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def removemembers(cls, session, id):
        uri = f'/iaas/projects/{id}'
        data = {}
        data['members'] = []
        try:
            r = requests.patch(f'{session.baseurl}{uri}', headers = session.headers, json = data)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def removeadmins(cls, session, id):
        uri = f'/iaas/projects/{id}'
        data = {}
        data['administrators'] = []
        try:
            r = requests.patch(f'{session.baseurl}{uri}', headers = session.headers, json = data)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def create(session, name, description):
        uri = '/iaas/projects/'
        data = {
                'name' : name,
                'description' : description,
                }
        print(data)
        r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, json = data)
        if r.status_code == 201:
            content = f'{name} project has been created'
            return print(content)
        else:
            content = f'Error executing: Code {r.status_code}'
            return print(content)

    @staticmethod
    def patch(session, name):
        proj = Project.list(session)
        for i in proj:
            if i['name'] == name:
                v = i['id']
                zone = CloudZone.list(session)[0]['id']
                data = {"zoneAssignmentConfigurations": [
                            {
                            "zoneId": zone,
                            }
                        ]
                        }
                uri = f'/iaas/projects/{v}'
                r = requests.patch(f'{session.baseurl}{uri}', headers = session.headers, json = data)
                print(r.status_code)
                break
        else:
            status = "Unable to find project name"
            return print(status)

    @classmethod
    def patchallzones(cls, session,name):
        ids = []
        zones = CloudZone.list(session)
        for j in zones:
            ids.append({"zoneId": j['id']})
        data = {"zoneAssignmentConfigurations": ids}
        projects = Project.list(session)
        for proj in projects:
            if proj['name'] == name:
                projid = proj['id']
                uri = f'/iaas/projects/{projid}'
                r = requests.patch(f'{session.baseurl}{uri}', headers = session.headers, json = data)
                print(r.status_code)
                return r.status_code
                break
        else:
            print(f'Content not found for name {name}')
            return


class DataCollector(object):
    """
    Classes for Remote Data Collector methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def list(session):
        uri = '/api/data-collector/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        return j

    @staticmethod
    def delete(session, i):
        id = i['dcId']
        uri = f'/api/data-collector/{id}'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        return

class CloudZone(object):
    """
    Classes for Cloud Zone methods.
    """
    def __init__(self, zone):
        self.tags = zone['tags']
        self.tags_to_match = zone['tagsToMatch']
        self.placement_policy = zone['placementPolicy']
        self.name = zone['name']
        self.id = zone['id']
        self.self_link = zone['selfLink']
        self.updated_at = zone['updatedAt']
        self._links = zone['_links']


    @staticmethod
    def list(session):
        """Takes a single input of your session bearer token"""
        uri = '/iaas/zones/'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            r.raise_for_status()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/zones/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            r.raise_for_status()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def create(cls, session, name, region_id, placement_policy = 'DEFAULT', tags = [], tags_to_match = [], description = ''):
        uri = '/iaas/zones/'
        body = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "placementPolicy": placement_policy,
            "tags": tags,
            "tagsToMatch": tags_to_match
        }
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = json.dumps(body))
            r.raise_for_status()
            j=r.json()
            print('Cloud Zone',name,'created')
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/zones/{id}'
        try:
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)

class Deployment(object):
    """
    Classes for Cloud Zone methods.
    """

    @staticmethod
    def list(session):
        uri = '/deployment/api/deployments'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j['results']:
            data.append(i['id'  ])
        return data

    @staticmethod
    def delete(session, id):
        uri = f'/deployment/api/deployments/{id}?forceDelete=true'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)

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


class ProvisioningRegion(object):
    """
    Class for retrieving provisioning regions.
    Used for both NetworkFabric and StorageFabric classes and methods.
    """
    def __init__(self, region):
        self.endpoint_link = region['endpointLink']
        self.region_id = region['regionId']
        self.tenant_links = region['tenantLinks']
        self.version = region['documentVersion']
        self.epoch = region['documentEpoch']
        self.kind = region['documentKind']
        self.self_link = region['documentSelfLink']
        self.updated_at = region['documentUpdateTimeMicros']
        self.id = os.path.split(self.self_link)[1]

    @staticmethod
    def list(session):
        uri = '/provisioning/resources/provisioning-regions/'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            data = list()
            for i in j['documentLinks']:
                i = os.path.split(i)[1]
                data.append(i)
            return data
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, id):
        uri = f'/provisioning/resources/provisioning-regions/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def find_by_region_id(cls, session, region_id):
        try:
            j = cls.list(session)
            for i in j:
                p = cls.describe(session, i)
                if p.region_id == region_id:
                    return p
            else: return
        except requests.exceptions.HTTPError as e:
            print(e)


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
        self.uri = f'/iaas/network-profiles'


    @classmethod
    def list(cls, session):
        uri = '/iaas/network-profile'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        if r.status_code != 200:
            print('Unable to list network profiles, status code',r.status_code)
        else:
            for i in j:
                data.append(i)
        return data

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
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, json = data)
            r.raise_for_status()
            j = r.json
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete(session, id):
        for i in id:
            uri = f'/iaas/network-profiles/{i}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print('Unable to delete network profile',i['name'],'status code',r.status_code)
        return

    @classmethod
    def describe(cls, session, id):
        pass


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

    @staticmethod
    def list(session):
        uri = '/iaas/storage-profiles-azure'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j['content']
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/storage-profiles-azure/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/storage-profiles-azure/{id}'
        try:
            requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        except requests.exceptions.HTTPError as e:
            print(e)
        return

class StorageProfileAWS(StorageProfile):
    def __init__(self, profile):
        pass

    @staticmethod
    def list(session):
        uri = '/iaas/storage-profiles-aws'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete(session, id):
        uri = '/iaas/storage-profiles-aws/{id}'
        try:
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        return

class StorageProfilevSphere(StorageProfile):
    def __init__(self,profile):
        pass

    @staticmethod
    def list_vsphere(session):
        uri = '/iaas/storage-profiles-vsphere'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete_vsphere(session, id):
        uri = f'/iaas/storage-profiles-vsphere/{id}'
        try:
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return

class ImageMapping(object):
    @staticmethod
    def list(session):
        uri = '/iaas/image-profiles'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def delete(session, i):
        uri = f'/iaas/image-profiles/{i}'
        r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        if r.status_code != 200:
            print('Unable to delete image profiles status code',r.status_code)
        return

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
        try:
            #r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, json=data)
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, json = data)
            r.raise_for_status()
            j = r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)


class FlavorMapping(object):
    @staticmethod
    def list(session):
        uri = '/iaas/flavor-profiles'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code != 200:
            print('Unable to list flavor profiles, status code',r.status_code)
        else:
            return j

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/flavor-profiles/{id}'
        r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        if r.status_code != 200:
            print('Unable to delete flavor profiles status code',r.status_code)
        else:
            print('Flavor Profile deleted')

class Org():

    @staticmethod
    def invite(session, org_id, username):
        body = {
            "orgId": org_id,
            "usernames": [
                username
            ],
            "mandatoryOrgRole": "org_member",
            "addOnRoles": [],
            "orgServicesRoles": [
                {
                "serviceName": "VMware Cloud Assembly",
                "serviceType": "EXTERNAL",
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Zy924mE3dwn2ASyVZR0Nn7lupeA_",
                "serviceRolesNames": [
                    "automationservice:user",
                    "automationservice:manager",
                    "automationservice:cloud_admin"
                ]
                },
                {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/ulvqtN4141beCT2oOnbj-wlkzGg_",
                "serviceRolesNames": [
                    "CodeStream:administrator",
                    "CodeStream:viewer",
                    "CodeStream:developer"
                ]
                },
                {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Yw-HyBeQzjCXkL2wQSeGwauJ-mA_",
                "serviceRolesNames": [
                    "catalog:admin",
                    "catalog:user"
                ]
                }
            ]
        }
        uri = f'/csp/gateway/portal/api/orgs/{org_id}/invitations'
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = json.dumps(body))
            r.raise_for_status()
            j=r.json()
            print('User',username,'invited to org',org_id)
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def user_list(session, org_id):
        uri = f'/csp/gateway/portal/api/orgs/{org_id}/users'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j=r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)


class CodeStream(object):
    @staticmethod
    def endpoint_list(session):
        uri = f'/pipeline/api/endpoints'
        try:
            data = list()
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j=r.json()
            print(j)
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return data

    @staticmethod
    def endpoint_delete(session, id):
        pass

    @staticmethod
    def pipeline_list(session):
        pass

    @staticmethod
    def pipeline_delete(session, id):
        pass

    @staticmethod
    def pipeline_execute(session, id):
        pass

    @staticmethod
    def pipeline_cancel(session, id):
        pass

    @staticmethod
    def pipeline_status(session, id):
        pass

class ServiceBroker(object):
    @staticmethod
    def sources_list(session):
        uri = f'/library/api/admin/sources'
        try:
            data = list()
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j=r.json()
            print(j)
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return data

    @staticmethod
    def sources_delete(session, id):
        uri = f'/library/api/admin/sources/{id}'
        try:
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            return
        except requests.exceptions.HTTPError as e:
            print(e)