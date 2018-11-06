import requests
import json
import os
import sys

class Deployment(object):
    """
    Classes for Cloud Zone methods.
    """
    def __init__(self,deployment):
        self.id = deployment['id']
        self.name = deployment['name']
        self.description = deployment['description']
        self.template_link = deployment['templateLink']
        self.icon_link = deployment['iconLink']
        self.created_at = deployment['createdAt']
        self.created_by = deployment['createdBy']
        self.updated_at = deployment['updatedAt']
        self.updated_by = deployment['updatedBy']
        self.inputs = deployment['inputs']
        self.resource_links = deployment['resourceLinks']

    @staticmethod
    def list(session):
        uri = '/deployment/api/deployments'
        return session._request(url=f'{session.baseurl}{uri}')['results']

    @staticmethod
    def delete(session, id):
        uri = f'/deployment/api/deployments/{id}'
        session._request(request_method='DELETE', url=f'{session.baseurl}{uri}')

    @staticmethod
    def force_delete(session, id):
        uri = f'/deployment/api/deployments/{id}?forceDelete=true'
        session._request(request_method='DELETE', url=f'{session.baseurl}{uri}')

    @classmethod
    def describe(cls, session, id):
        uri = f'/deployment/api/deployments/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def list_by_project_id(session, id):
        uri = f'/deployment/api/deployments?projects=/provisioning/resources/projects/{id}'
        ids = list()
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            for i in j['results']:
                ids.append(i['id'])
            return ids
        except requests.exceptions.HTTPError as e:
            print(e)
