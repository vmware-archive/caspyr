import requests
import json
import os
import sys

class Request(object):
    def __init__(self, request):
        self.request_tracker_link = request['requestTrackerLink']
        self.deployment_name = request['deploymentName']
        self.reason = request['reason']
        self.description = request['description']
        self.plan = request['plan']
        self.destroy = request['destroy']
        self.blueprint_id = request['blueprintId']
        self.inputs = request['inputs']
        self.status = request['status']
        self.project_id = request['projectId']
        self.project_name = request['projectName']
        self.type = request['type']
        self.id = request['id']
        self.self_link = request['selfLink']
        self.created_at = request['createdAt']
        self.created_by = request['createdBy']
        self.updated_at = request['updatedAt']
        self.updated_by = request['updatedBy']
        self.tenants = request['tenants']
        try:
            self.deployment_id = request['deploymentId']
        except KeyError: pass
        try:
            self.failure_message = request['failureMessage']
        except KeyError: pass
        try:
            self.validation_messages = request['validationMessages']
        except KeyError: pass

    @classmethod
    def create(cls, session, name='myapp',reason='', description='', id='9862304f0af67875574edc3216c62', project='25a33c8a-eab8-4a43-88fa-45330e0e68d6'):
        uri = f'/blueprint/api/blueprint-requests'
        body = {
            "deploymentName": name,
            "reason": reason,
            "description": description,
            "projectLink": project,
            "plan": False,
            "destroy": False,
            "blueprintId": id,
            "inputs": {
                "name": name
            }
        }
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, json = body)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)

    @staticmethod
    def list(session):
        uri = f'/blueprint/api/blueprint-requests'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)

    @classmethod
    def describe(cls, session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}'
        try:
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j = r.json()
            return cls(j)
        except requests.exceptions.HTTPError as e:
            print(e)