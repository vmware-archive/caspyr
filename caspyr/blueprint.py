import requests
import json
import os
import sys

class Blueprint(object):
    def __init__(self, blueprint):
        """
        Class for methods related to Blueprints.
        :method list: Returns the ids of all blueprints.
        :method describe: Returns the full schema of the blueprint.
        :method create: Creates a blueprint, returns an object.
        :method create_from_JSON: Creates a blueprint from JSON, returns an object.
        :method delete: Deletes the blueprint.
        """
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
        data = list()
        j = session._request(f'{session.baseurl}{uri}')
        for i in j['links']:
            i = os.path.split(i)[1]
            data.append(i)
        return data

    @classmethod
    def describe(cls, session, bp):
        uri= f'/blueprint/api/blueprints/{bp}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def create_from_JSON(cls, session, jsonfile):
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
    def list_provider_resources(session):
        uri = '/blueprint/api/provider-resources'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def describe_provider_resources(session, id):
        uri = f'/blueprint/api/provider-resources/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j
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