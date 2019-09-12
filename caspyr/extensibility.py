# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

class Subscription: 
    """
    Class for methods related to Event Broker Subscriptions.
    :method list: Returns an array of all subscriptions that are
    flagged as runnable.
    :method describe: Returns the full schema of the associated
    subscription.
    :method delete: Deletes the subscription.
    """

    def __init__(self, subscription):
        self.name = subscription['name']
        self.id = subscription['id']
        self.type = subscription['type']

    @staticmethod
    def list(session):
        """Retrieves list of all subscriptions that the logged-in
        user has access to.

        :param session: The session object.
        :type session: object
        :return: A list of subscriptions.
        :rtype: list
        """
        uri =f"/event-broker/api/subscriptions?$filter=(type ne 'SUBSCRIBABLE')"
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def describe(session, id):
        """Retrieves the detailed schema of a single 
        subscription that the logged-in user has access to.

        :param session: The session object.
        :type session: object
        :param id: The ID of a subscription
        :type id: string
        :return: A detailed schema of a subscriptions.
        :rtype: list
        """
        uri = f'/event-broker/api/subscriptions/{id}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, id):
        """Deletes an Event Broker subscription based on a supplied
        id.

        :param session: The session object.
        :type session: object
        :param id: The ID of a subscription
        :type id: string
        :return: Success/Failure.
        :rtype: status code
        """
        uri = f'/event-broker/api/subscriptions/{id}'
        return session._request(f'{session.baseurl}{uri}',
                            request_method='DELETE'
                            )

class Action:
    """
    Class for methods related to ABX Actions.
    :method list: Returns the ids for ABX Actions.
    :method describe: Returns the full schema of a single ABX Action.
    :method delete: Deletes an ABX Action.
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
        """Retrieves list of all Actions that the logged-in
        user has access to.

        :param session: The session object.
        :type session: object
        :return: A list of Actions.
        :rtype: list
        """
        uri = '/abx/api/resources/actions/'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def describe(session, selfLink):
        """Retrieves the detailed schema of a single 
        ABX Action that the logged-in user has access to.

        :param session: The session object.
        :type session: object
        :param id: The ID of a ABX Action
        :type id: string
        :return: A detailed schema of a ABX Action.
        :rtype: list
        """
        uri = f'{selfLink}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, selfLink):
        """Deletes an ABX Action based on a supplied
        id.

        :param session: The session object.
        :type session: object
        :param id: The ID of an ABX Action
        :type id: string
        :return: Success/Failure.
        :rtype: status code
        """
        uri = f'{selfLink}'
        return session._request(f'{session.baseurl}{uri}',
                            request_method='DELETE'
                            )