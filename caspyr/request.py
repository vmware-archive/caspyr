import requests
import json
import os
import sys

class Request(object):
    def __init__(self, request):
        self.request_tracker_link = request['requestTrackerLink']
        self.deployment_name = request['deploymentName']
        self.reason = request['reason']
        self.plan = request['plan']
        self.destroy = request['destroy']
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
            self.blueprint_id = request['blueprintId']
        except KeyError: pass
        try:
            self.description = request['description']
        except KeyError: pass
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
        return cls(session._request(f'{session.baseurl}{uri}', method='POST', json=body))

    @classmethod
    def list(cls, session):
        uri = f'/blueprint/api/blueprint-requests'
        j = session._request(f'{session.baseurl}{uri}')
        data = list()
        for i in j['links']:
            i = os.path.split(i)[1]
        return data

    @classmethod
    def describe(cls, session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def cancel(session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}?action=cancel'
        return session._request(f'{session.baseurl}{uri}')

    @classmethod
    def list_incomplete(cls, session):
        r = cls.list(session)
        data = list()
        for i in r:
            d = cls.describe(session, i)
            if d.status == 'STARTED':
                data.append(d.id)
        return data
