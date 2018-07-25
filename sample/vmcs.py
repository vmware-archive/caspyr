"""
Initial structure for classes and functions as they pertain to VMCS automation functions.
"""
import requests
import json
import os
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
        p = r.json()
        bps = list()
        table = PrettyTable(['BlueprintID'])
        for i in p['links']:
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
        p = r.json()
        if r.status_code == 403:
            print(f'You do not have sufficient access to org {org} to list its details.')
        else:
            table.add_row([p['name'], p['createdBy'], p['updatedAt']])
        print(table)
        return

    @staticmethod
    def list_detail(session, bps):
        table = PrettyTable(['Name'])
        for bp in bps:
            uri= f'/blueprint/api/blueprints/{bp}'
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            p = r.json()
            print(p['id'])
            """
            if r.status_code == 403:
                print(f'You do not have sufficient access to org {org} to list its details.')
            else:
                table.add_row([p['name']])
        print(table)
        return
        """

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
        p = r.json()
        data = list()
        table = PrettyTable(['RequestID'])
        for i in p['links']:
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
            p = r.json()
            data.append(p)
            table.add_row([p['deploymentId'],p['deploymentName'],p['status']])
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
        p = r.json()
        data = list()
        table = PrettyTable(['CloudAccountID'])
        for i in p['links']:
            i =i.lstrip('/iaas/cloud-accounts')
            accounts.append(i)
            table.add_row([i])
        print(table)
        return data

    @staticmethod
    def delete(session, accounts):
        for account in accounts:
            uri = f'/iaas/cloud-accounts/{account.id}'
            r = requests.delete(f'{session.baseurl}{uri}', headers = session.headers)
            print(r.status_code)
        return

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
        p = r.json()
        data = list()
        for i in p:
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
        uri = '/iaas/zones/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        p = r.json()
        czs = list()
        table = PrettyTable(['BlueprintID'])
        for i in p['links']:
            i =i.lstrip('/blueprint/api/blueprints/')
            bps.append(i)
            table.add_row([i])
        print(table)
        return bps

class CloudZone(object):
    """
    Classes for Cloud Zone methods.
    """
    @staticmethod
    def list(session, pt=False):
        uri = '/iaas/zones/'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        p = r.json()
        data = list()
        table = PrettyTable(['ID','Name'])
        for i in p:
            data.append(i)
            table.add_row([i['id'],i['name']])
        if pt == 'pt':
            print(table)
        return data

class Deployment(object):
    """
    Classes for Cloud Zone methods.
    """

    @staticmethod
    def list(session):
        uri = '/deployment/api/deployments'
        r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
        p = r.json()
        data = list()
        for i in p:
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
        p = r.json()
        data = list()
        if r.status_code != 200:
            print('Unable to list network profiles, status code',r.status_code)
        else:
            print(len(p),'network profiles found')
            for i in p:
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
