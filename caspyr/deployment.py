# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0


class Deployment(object):
    """
    Classes for Cloud Zone methods.
    """
    def __init__(self,
                 deployment):
        self.id = deployment['id']
        self.name = deployment['name']
        self.description = deployment['description']
        self.blueprint_id = deployment['blueprintId']
        # self.icon_link = deployment['iconLink']
        self.created_at = deployment['createdAt']
        self.created_by = deployment['createdBy']
        self.updated_at = deployment['lastUpdatedAt']
        self.updated_by = deployment['lastUpdatedBy']
        self.inputs = deployment['inputs']
        # self.resource_links = deployment['resourceLinks']

    @staticmethod
    def list(session):
        uri = '/deployment/api/deployments'
        return session._request(url=f'{session.baseurl}{uri}')['content']

    @staticmethod
    def delete(session, id):
        uri = f'/deployment/api/deployments/{id}'
        session._request(request_method='DELETE',
                         url=f'{session.baseurl}{uri}')

    @staticmethod
    def force_delete(session, id):
        uri = f'/deployment/api/deployments/{id}?forceDelete=true'
        session._request(request_method='DELETE',
                         url=f'{session.baseurl}{uri}')

    @classmethod
    def describe(cls, session, id):
        uri = f'/deployment/api/deployments/{id}'
        return cls(session._request(url=f'{session.baseurl}{uri}'))

    @staticmethod
    def list_by_project_id(session, id):
        uri = (f'/deployment/api/deployments'
               '?projects=/provisioning/resources/projects/{id}')
        ids = {}
        j = session._request(url=f'{session.baseurl}{uri}')['content']
        for i in j:
            ids['id'] = i['id']
            ids['name'] = i['name']
        return ids

    @staticmethod
    def check_status(session, id):
        uri = f'/deployment/api/deployments/{id}/events'
        stat = {}
        j = session._request(url=f'{session.baseurl}{uri}')['content'][0]
        for i in j:
            stat['status'] = j['status']
            if stat['status'] == "FAILED":
                stat['statusMessage'] = j['details']
        return stat
