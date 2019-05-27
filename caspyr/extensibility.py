# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

class Subscription: 

    def __init__(self, subscription):
        self.name = subscription['name']
        self.id = subscription['id']
        self.type = subscription['type']

    @staticmethod
    def list(session):
        uri ='/event-broker/api/subscriptions/'
        j = session._request(f'{session.baseurl}{uri}')
        subs = []
        for i in j['content']: 
            if i['type'] == 'RUNNABLE':
                print(i['name'])
                subs.append(i)
        return subs

    @staticmethod
    def describe(session, id):
        uri = f'/event-broker/api/subscriptions/{id}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, id):
        uri = f'/event-broker/api/subscriptions/{id}'
        return session._request(f'{session.baseurl}{uri}',
                            request_method='DELETE'
                            )

class Action:
    """
    Class for methods related to Blueprints.
    :method list: Returns the ids extensibility objects.
    :method describe: Returns the full schema of the extensibility object.
    :method delete: Deletes the blueprint.
    """

    def __init__(self, action):
        self.name = action['name']
        self.id = action['id']
        self.runtime = action['runtime']
        self.providers = action['configuration']['const-providers']
        self.projectid = action['projectId']
        self.selfLink = action['selfLink']

    @staticmethod
    def list(session):
        uri = '/abx/api/resources/actions/'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def describe(session, selfLink):
        uri = f'{selfLink}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, selfLink):
        uri = f'{selfLink}'
        return session._request(f'{session.baseurl}{uri}',
                            request_method='DELETE'
                            )