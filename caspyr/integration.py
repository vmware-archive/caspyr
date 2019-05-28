# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0


class Integration: 
    """
    Class for methods related to Cloud Assembly Integrations.
    :method list: Returns an array of all endpoint resources that are
    which includes Cloud Accounts and Integrations.
    :method delete: Deletes the resource endpoint.
    """
    def __init__(self, integration):
        self.name = integration['name']
        self.id = integration['id']

    @staticmethod
    def list(session):
        """Retrieves list of all resource endpoints.

        :param session: The session object.
        :type session: object
        :return: A list of resource endpoints.
        :rtype: list
        """
        uri = '/provisioning/uerp/resources/endpoints'
        j = session._request(f'{session.baseurl}{uri}')
        endpoints = []
        for i in j['documentLinks']:
            obj = {}
            q = session._request(f'{session.baseurl}/provisioning/uerp/provisioning/mgmt/endpoints{i}')
            obj['name'] = q['name']
            obj['resourceLink'] = i
            obj['id'] = q['id']
            obj['endpointType'] = q['endpointType']
            endpoints.append(obj)
        return endpoints

    @staticmethod
    def delete(session,resourceLink):
        """Deletes a resource endpoint/integration.

        :param session: The session object.
        :type session: object
        :param resourceLink: The resourceLink (URL path) for
        the item in for deletion
        :type id: string
        :return: Success/Failure.
        :rtype: status code
        """
        uri = f'/provisioning/uerp/provisioning/mgmt/endpoints{resourceLink}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE')


class Source: 
    """
    Class for methods related to integration sources.
    :method list: Returns an array of all integration sources from
    bound accounts and integrations.
    :method delete: Deletes an associated integration data source.
    """
    def __init__(self, source):
        self.name = source['name']
        self.id = source['name']

    @staticmethod
    def list(session):
        """Retrieves list of all integration source within a
        Organization

        :param session: The session object.
        :type session: object
        :return: A list of sources.
        :rtype: list
        """
        uri = '/content/api/sources/'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session,id):
        """Deletes source based on a supplied id.

        :param session: The session object.
        :type session: object
        :param id: The ID of an integration source
        :type id: string
        :return: Success/Failure.
        :rtype: status code
        """
        uri = f'/content/api/sources/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

