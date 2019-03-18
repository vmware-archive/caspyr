# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

import os


class Request:
    def __init__(self, request):
        try:
            self.request_tracker_link = request['requestTrackerLink']
        except KeyError:
            pass
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
        try:
            self.tenants = request['tenants']
        except KeyError:
            pass
        try:
            self.blueprint_id = request['blueprintId']
        except KeyError:
            pass
        try:
            self.description = request['description']
        except KeyError:
            pass
        try:
            self.deployment_id = request['deploymentId']
        except KeyError:
            pass
        try:
            self.failure_message = request['failureMessage']
        except KeyError:
            pass
        try:
            self.validation_messages = request['validationMessages']
        except KeyError:
            pass

    @classmethod
    def list(cls, session):
        uri = f'/blueprint/api/blueprint-requests/'
        j = session._request(f'{session.baseurl}{uri}')['links']
        data = []
        for i in j:
            i = os.path.split(i)[1]
            data.append({"id": i})
        return data

    @classmethod
    def describe(cls,
                 session,
                 id
                 ):
        uri = f'/blueprint/api/blueprint-requests/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def cancel(session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}?action=cancel'
        return session._request(f'{session.baseurl}{uri}')

    @classmethod
    def list_incomplete(cls,
                        session):
        r = cls.list(session)
        data = []
        for i in r:
            d = cls.describe(session, i['id'])
            if d.status == 'STARTED':
                data.append({"id": d.id})
        return data
