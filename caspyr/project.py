import requests
import json
import os
import sys

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
        data = list()
        j = session._request(f'{session.baseurl}{uri}')
        for i in j['content']:
            data.append(i['id'])
        return data

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/projects/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def describe_by_name(cls, session, name):
        j = cls.list(session)
        for i in j:
            d = cls.describe(session, i)
            if d.name.lower() == name.lower():
                print(d.name)
                return d

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/projects/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

    @classmethod
    def removezones(cls, session, id):
        uri = f'/iaas/projects/{id}'
        payload = {}
        payload['zoneAssignmentConfigurations'] = []
        return cls(session._request(f'{session.baseurl}{uri}', request_method='PATCH', payload=payload))



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