# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0


import os


class CloudZone(object):
    """
    Classes for Cloud Zone methods.
    """
    def __init__(self, zone):
        try:
            self.tags = zone['tags']
        except KeyError:
            pass
        try:
            self.tags_to_match = zone['tagsToMatch']
        except KeyError:
            pass
        self.placement_policy = zone['placementPolicy']
        self.name = zone['name']
        self.id = zone['id']
        self.updated_at = zone['updatedAt']
        self._links = zone['_links']
        self.region_id = os.path.split(self._links['region']['href'])[1]

    @staticmethod
    def list(session):
        """Takes a single input of your session bearer token"""
        uri = '/iaas/api/zones/'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls,
                 session,
                 id
                 ):
        uri = f'/iaas/api/zones/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def describe_by_name(cls,
                         session,
                         name
                         ):
        uri = f'/iaas/api/zones?$filter=(name eq \'{name}\')'
        return cls(session._request(f'{session.baseurl}{uri}')['content'][0])

    @classmethod
    def create(cls,
               session,
               name,
               region_id,
               placement_policy='DEFAULT',
               tags=[],
               tags_to_match=[],
               description=''
               ):
        uri = '/iaas/api/zones/'
        payload = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "placementPolicy": placement_policy,
            "tags": tags,
            "tagsToMatch": tags_to_match
        }
        return cls(session._request(url=f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/zones/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )
