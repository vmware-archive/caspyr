# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

class DataCollector(object):
    def __init__(self, rdc):
        pass

    @staticmethod
    def list(session):
        uri = '/iaas/api/data-collectors/'
        data = []
        j = session._request(f'{session.baseurl}{uri}')['content']
        for i in j:
            content = {}
            content['id'] = i['dcId']
            content['name'] = i['name']
            data.append(content)
        return data

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/data-collectors/{id}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/data-collectors/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @staticmethod
    def request_otk(session):
        uri = '/api/otk-v3'
        payload = {
                   "url": "https://api.mgmt.cloud.vmware.com",
                   "service": "cloud_assembly"
                   }
        i = session._request(f'{session.baseurl}{uri}',
                             request_method='POST',
                             payload=payload
                             )
        return i['key']
