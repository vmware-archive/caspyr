import requests
import json
import os
import sys

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

    @staticmethod
    def describe(session, id):
        uri = f'/deployment/api/deployments/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j
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
