# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0


class Integration: 
    def __init__(self, integration):
        self.name = integration['name']
        self.id = integration['id']

    @staticmethod
    def list(session):
        uri = '/provisioning/uerp/resources/endpoints?expand'
        j = session._request(f'{session.baseurl}{uri}')
        endpoints = []
        for i in j['documentLinks']:
            obj = {}
            q = session._request(f'{session.baseurl}/provisioning/uerp/provisioning/mgmt/endpoints{i}')
            obj['name'] = q['name']
            obj['id'] = q['id']
            obj['endpointType'] = q['endpointType']
            endpoints.append(obj)
        return endpoints

    @staticmethod
    def delete(session,resourceLink):
        uri = f'/provisioning/uerp/provisioning/mgmt/endpoints{resourceLink}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE')


class Source: 
    def __init__(self, source):
        self.name = source['name']
        self.id = source['name']

    @staticmethod
    def list(session):
        uri = '/content/api/sources/'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session,id):
        uri = f'/content/api/sources/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

