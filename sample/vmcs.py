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

class Blueprint(object):
    """
    Classes for Blueprint methods.
    """
    def __init__(self):
        pass

    @staticmethod
    def list(session):
        uri = '/blueprint/api/blueprints/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j['links']:
            i = os.path.split(i)[1]
            data.append(i)
        return data

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
    def detail(session, bp):
        uri= f'/blueprint/api/blueprints/{bp}'
        print(uri)
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
    def delete(session, id):
        uri= f'/blueprint/api/blueprints/{id}'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        return

    @staticmethod
    def request(session):
        uri = '/blueprint/api/blueprint-requests/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j['links']:
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @staticmethod
    def request_detail(session, id):
        #data = list()
        uri = f'/blueprint/api/blueprint-requests/{id}'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        #data.append(j)
        return j

    @staticmethod
    def request_cancel(session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}?action=cancel'
        payload = {}
        try:
            requests.post(f'{session.baseurl}{uri}', headers = session.headers, data = payload)
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        #if r.status_code == 204:
        #    print('Successfully cancelled request')
        #else:
        #    print('Cancellation failed with',r.status_code)
        return

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
        for i in j:
            i = i['selfLink']
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @staticmethod
    def listaws(session):
        uri = '/iaas/cloud-accounts-aws'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j:
            i = i['selfLink']
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @staticmethod
    def listazure(session):
        uri = '/iaas/cloud-accounts-azure'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j:
            i = i['selfLink']
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @staticmethod
    def listvsphere(session):
        uri = '/iaas/cloud-accounts-vsphere'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        data = list()
        for i in j:
            i = i['selfLink']
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @staticmethod
    def delete(session, id):
        uri = f'/api/cloud-accounts/{id}'
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
    def createAzure(session, name, subscription_id, tenant_id, application_id, application_key, regions = 'westus', create_zone = False, description = ''):
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
    def delete(session, id):
        uri = f'/iaas/projects/{id}'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        return

    @staticmethod
    def removezones(session, id):
        uri = f'/iaas/projects/{id}'
        data = {}
        data['zoneAssignmentConfigurations'] = []
        requests.patch(f'{session.baseurl}{uri}', headers = session.headers, json = data)

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

    @staticmethod
    def patchallzones(session,name):
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
        print(len(j),'Data Collectors found')
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
    def __init__(self):
        pass

    @staticmethod
    def list(session):
        """Takes a single input of your session bearer token"""
        uri = '/iaas/zones/'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def create(session, name, region_id, placement_policy = 'DEFAULT', tags = [], tags_to_match = [], description = ''):
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
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/zones/{id}'
        try:
            requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
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
        for i in j['results']:
            data.append(i['id'  ])
        return data

    @staticmethod
    def delete(session, id):
        uri = f'/deployment/api/deployments/{id}'
        requests.delete(f'{session.baseurl}{uri}', headers = session.headers)

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
    def delete(session, id):
        for i in id:
            uri = f'/iaas/network-profiles/{i}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            if r.status_code != 200:
                print('Unable to delete network profile',i['name'],'status code',r.status_code)
        return

class StorageProfile(object):
    @staticmethod
    def list(session):
        uri = '/iaas/storage-profiles'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code != 200:
            print('Unable to list storage profiles, status code',r.status_code)
        return j

    @staticmethod
    def list_azure(session):
        uri = '/iaas/storage-profiles-azure'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code != 200:
            print('Unable to list storage profiles, status code',r.status_code)
        return j

    @staticmethod
    def list_aws(session):
        uri = '/iaas/storage-profiles-aws'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return j

    @staticmethod
    def list_vsphere(session):
        uri = '/iaas/storage-profiles-vsphere'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            j = r.json()
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return j

    @staticmethod
    def delete(session, profiles):
        for i in profiles:
            uri = f'/provisioning/resources/storage-profiles/{i}'
            try:
                requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            except requests.exceptions.HTTPError as e:
                print(e)
                sys.exit(1)

    @staticmethod
    def delete_aws(session, id):
        uri = '/iaas/storage-profiles-aws/{id}'
        try:
            requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return

    @staticmethod
    def delete_azure(session, id):
        uri = f'/iaas/storage-profiles-azure/{id}'
        try:
            requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return

    @staticmethod
    def delete_vsphere(session, id):
        uri = f'/iaas/storage-profiles-vsphere/{id}'
        try:
            requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return

class ImageMapping(object):
    @staticmethod
    def list(session):
        uri = '/iaas/image-profiles'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        j = r.json()
        if r.status_code != 200:
            print('Unable to list image profiles, status code',r.status_code)
        return j

    @staticmethod
    def delete(session, i):
        uri = f'/iaas/image-profiles/{i}'
        r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
        if r.status_code != 200:
            print('Unable to delete image profiles status code',r.status_code)
        return


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
            "mandatoryOrgRole": "org_owner",
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
            #print('User',username,'invited to org',org_id)
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

"""
{
    "orgRoleName": "org_owner",
    "orgRoleNames": [ "" ],
    "serviceRolesDtos": [ {
        "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Zy924mE3dwn2ASyVZR0Nn7lupeA_",
        "serviceRoleNames": [ "automationservice:user","automationservice:manager","automationservice:cloud_admin" ]
    },
    {
        "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/ulvqtN4141beCT2oOnbj-wlkzGg_",
        "serviceRoleNames": ["CodeStream:administrator","CodeStream:viewer","CodeStream:developer"]
    },
    {
        "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Yw-HyBeQzjCXkL2wQSeGwauJ-mA_",
        "serviceRoleNames": ["catalog:admin","catalog:user"]
    } ],
    "usernames": [ "grant.a.orchard@gmail.com" ]
}


 "serviceRolesDtos": [
                {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Zy924mE3dwn2ASyVZR0Nn7lupeA_",
                "serviceRolesNames": ["automationservice:user","automationservice:manager","automationservice:cloud_admin"]
                },
                {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/ulvqtN4141beCT2oOnbj-wlkzGg_",
                "serviceRolesNames": ["CodeStream:administrator","CodeStream:viewer","CodeStream:developer"]
                },
                {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Yw-HyBeQzjCXkL2wQSeGwauJ-mA_",
                "serviceRolesNames": ["catalog:admin","catalog:user"]
                }
            ]
        }
    69016f57-9ebd-4abc-99ee-7492196ee132
}
"""