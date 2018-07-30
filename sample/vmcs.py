"""Initial structure for classes and functions as they pertain to VMCS automation functions."""
import requests
import json
import os
import sys
from prettytable import PrettyTable


class Session(object):
    """
    Session class for instantiating a logged in session
    for VMCS.

    Requires refresh token from VMCS portal to instantiate
    """
    def __init__(self, auth_token):
        self.token = 'Bearer '+auth_token
        self.headers = {'Content-Type':'application/json','authorization': self.token}
        self.baseurl = 'https://www.mgmt.cloud.vmware.com'

    @classmethod
    def login(self, refresh_token):
            baseurl = 'https://www.mgmt.cloud.vmware.com'
            uri = '/iaas/login'
            headers = {'Content-Type':'application/json'}
            payload = json.dumps({"refreshToken": refresh_token })
            r = requests.post(f'{baseurl}{uri}', headers = headers, data = payload)
            if r.status_code != 200:
                print(f'Unsuccessful Login Attempt. Error code {r.status_code}')
            else:
                print('Login successful. ')
                auth_token = r.json()['token']
                return self(auth_token)

class Blueprint(object):
    """
    Classes for Blueprint methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def list(session, pt=False):
        uri = '/blueprint/api/blueprints/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        bps = list()
        table = PrettyTable(['BlueprintID'])
        for i in j['links']:
            i = os.path.split(i)[1]
            bps.append(i)
            table.add_row([i])
        if pt == 'pt':
            print(table)
        return bps

    @staticmethod
    def describe(session, bp):
        table = PrettyTable(['Name', 'CreatedBy', 'LastUpdated'])
        uri= f'/blueprint/api/blueprints/{bp}'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code == 403:
            print(f'You do not have sufficient access to org to list its details.')
        else:
            table.add_row([j['name'], j['createdBy'], j['updatedAt']])
        print(table)
        return j

    @staticmethod
    def list_detail(session, bps):
        for i in bps:
            uri= f'/blueprint/api/blueprints/{i}'
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            return j


    @staticmethod
    def createFromJSON(session, jsonfile):
        bp = open(jsonfile).read()
        uri= f'/blueprint/api/blueprints'
        r = requests.post(f'{session.baseurl}{uri}', data = bp, headers = session.headers)
        print(r.status_code)
        return r

    @staticmethod
    def create(session, bpname, displayname, description, number, raw_data_url):
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
        r = requests.post(f'{session.baseurl}{uri}', data = json.dumps(jsondata), headers = session.headers)
        if r.status_code != 201:
            print("BP Format Error - Check Content and resubmit")
        else:
            print(jsondata['displayName'] + " has been created")
        return r.content

    @staticmethod
    def delete(session, bps):
        print(bps)
        for bp in bps:
            uri= f'/blueprint/api/blueprints/{bp}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            print(r.status_code)
        return

    @staticmethod
    def request(session):
        uri = '/blueprint/api/blueprint-requests/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        table = PrettyTable(['RequestID'])
        for i in j['links']:
            i = os.path.split(i)[1]
            #n = n.lstrip('/blueprint/api/blueprint-request')
            data.append(i)
            table.add_row([i])
        print(table)
        return data

    @staticmethod
    def request_detail(session, bp_requests):
        data = list()
        table = PrettyTable(['DeploymentId', 'DeploymentName', 'Status'])
        for i in bp_requests:
            uri = f'/blueprint/api/blueprint-requests/{i}'
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            data.append(j)
            table.add_row([j['deploymentId'],j['deploymentName'],j['status']])
        print(table)
        return data

    @staticmethod
    def request_cancel(session, ids):
        for i in ids:
            uri = f'/blueprint/api/blueprint-requests/{i}?action=cancel'
            payload = {}
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = payload)
            if r.status_code == 204:
                print('Successfully cancelled request')
            else:
                print('Cancellation failed with',r.status_code)

class CloudAccount(object):
    """
    Classes for Cloud Account methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def list(session):
        uri = '/iaas/cloud-accounts'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        table = PrettyTable(['CloudAccountID'])
        for i in j:
            i =i['selfLink'].lstrip('/iaas/cloud-accounts')
            data.append(i)
            table.add_row([i])
        print(table)
        return data

    @staticmethod
    def delete(session, accounts):
        for account in accounts:
            uri = f'/iaas/cloud-accounts/{account}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            print(r.status_code)
        return

    @staticmethod
    def createAWS(session, name, access_key, secret_key, regions = 'us-west-1', create_zone = False, description = ''):
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
            print('Cloud Account',name,'created')
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def createAzure(session, name, subscription_id, tenant_id, application_id, application_key, regions = 'West US', create_zone = False, description = ''):
        print('Creating Azure Cloud Account',name)
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
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

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

    @staticmethod
    def createNSXT(session, name, fqdn, rdc, username, password, description = ''):
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
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)


class Project(object):
    """
    Class for Project methods"
    """

    def __init__(self):
        pass

    @staticmethod
    def list(session):
        uri = '/iaas/projects'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j:
            data.append(i)
        return data

    @staticmethod
    def delete(session, projects):
        data = list()
        for i in projects:
            id = i['id']
            uri = f'/iaas/projects/{id}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            data.append({'id':id,'response':r.status_code})
        return data


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
        print(len(j),'Data Collectors found')
        return j

    @staticmethod
    def delete(session, collectors):
        data = list()
        for i in collectors:
            id = i['dcId']
            uri = f'/api/data-collector/{id}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print("Unable to delete data collector",i['name'],"status code",r.status_code)
            else:
                print("Deleted data collector",i['name'])
                data.append(i)
            return data

class CloudZone(object):
    """
    Classes for Cloud Zone methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def list(session, pt=False):
        """Takes a single input of your session bearer token"""
        uri = '/iaas/zones/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        table = PrettyTable(['ID','Name'])
        for i in j:
            data.append(i)
            table.add_row([i['id'],i['name']])
        if pt == 'pt':
            print(table)
        return data

    @staticmethod
    def create(session, name, region_id, placement_policy = 'DEFAULT', tags = [], tags_to_match = [], description = ''):
        uri = '/iaas/zones'
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
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)


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
        for i in j:
            data.append(i)
        return data

    @staticmethod
    def delete(session, deployments):
        for i in deployments:
            id = i['id']
            uri = f'/deployment/api/deployments/{id}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print("Unable to delete",i['name'],"status code",r.status_code)
            else:
                print("Deleted deployment",i['name'])

class NetworkProfile(object):
    """
    Class for Network Profile methods.
    """

    @staticmethod
    def list(session):
        uri = '/iaas/network-profiles'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        if r.status_code != 200:
            print('Unable to list network profiles, status code',r.status_code)
        else:
            print(len(j),'network profiles found')
            for i in j:
                data.append(i)
        return data

    @staticmethod
    def delete(session, network_profiles):
        data = list()
        for i in network_profiles:
            id = i['id']
            uri = f'/iaas/network-profiles/{id}'
            print(uri)
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print('Unable to delete network profile',i['name'],'status code',r.status_code)
            else:
                data.append(i['name'])
        print(len(data),'networks deleted')
        return data

class StorageProfile(object):
    @staticmethod
    def list(session):
        uri = '/provisioning/resources/storage-profiles'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        if r.status_code != 200:
            print('Unable to list storage profiles, status code',r.status_code)
        else:
            print(len(j['documentLinks']),'storage profiles found')
            for i in j['documentLinks']:
                i = os.path.split(i)[1]
                data.append(i)
        return data

    @staticmethod
    def delete(session, profiles):
        for i in profiles:
            uri = f'/provisioning/resources/storage-profiles/{i}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print('Unable to delete storage profile',i,'status code',r.status_code)
            else:
                print('Storage Profile',i,'deleted')

class ImageMapping(object):
    @staticmethod
    def list(session):
        uri = '/provisioning/mgmt/image-profiles'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code != 200:
            print('Unable to list image profiles, status code',r.status_code)
        else:
            print(j['totalCount'],'image profiles found (each profile may contain many maps)')
        return j

    @staticmethod
    def delete(session, mappings):
        for i in mappings['documentLinks']:
            uri = f'{i}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print('Unable to delete image profiles status code',r.status_code)
            else:
                print('Image Profile deleted')

class FlavorMapping(object):
    @staticmethod
    def list(session):
        uri = '/iaas/flavor-profiles'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code != 200:
            print('Unable to list network profiles, status code',r.status_code)
        else:
            return j

    @staticmethod
    def delete(session, mappings):
        for i in mappings:
            id = i['id']
            uri = f'/iaas/flavor-profiles/{id}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print('Unable to delete flavor profiles status code',r.status_code)
            else:
                print('Flavor Profile deleted')
