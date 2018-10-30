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
        try:
            self.description = project['description']
        except:
            KeyError
        self.id = project['id']
        self.organization_id = project['organizationId']
        self._links = project['_links']

    @classmethod
    def list(cls, session):
        uri = '/iaas/projects'
        return session._request(f'{session.baseurl}{uri}')['content']

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

    @classmethod
    def create(cls, session, name, description=None, administrators=None, members=None, zone_configs=None):
        """
        Creates a new project with the provided parameters.
        :param session: [description]
        :type session: [type]
        :param name: [description]
        :type name: [type]
        :param description: [description], defaults to None
        :param description: [type], optional
        :param administrators: [description], defaults to None
        :param administrators: [type], optional
        :param members: [description], defaults to None
        :param members: [type], optional
        :param zone_configs: Defaults to None.
        [
            {
            "zoneId": "77ee1",
            "priority": 1,
            "maxNumberInstances": 50
            }
        ]
        :param zone_configs: List of objects, optional.
        :return: [description]
        :rtype: [type]
        """

        uri = '/iaas/projects/'
        payload = {
                "name" : name,
                "description" : description,
                "administrators" : administrators,
                "members" : members,
                "zoneAssignmentConfigurations": zone_configs
                }
        return cls(session._request(f'{session.baseurl}{uri}', request_method='POST', payload=payload))