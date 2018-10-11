import requests
import json
import os
import sys

class CloudZone(object):
    """
    Classes for Cloud Zone methods.
    """
    def __init__(self, zone):
        self.tags = zone['tags']
        self.tags_to_match = zone['tagsToMatch']
        self.placement_policy = zone['placementPolicy']
        self.name = zone['name']
        self.id = zone['id']
        self.self_link = zone['selfLink']
        self.updated_at = zone['updatedAt']
        self._links = zone['_links']


    @staticmethod
    def list(session):
        """Takes a single input of your session bearer token"""
        uri = '/iaas/zones/'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/zones/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def create(cls, session, name, region_id, placement_policy = 'DEFAULT', tags = [], tags_to_match = [], description = ''):
        uri = '/iaas/zones/'
        body = {
            "name": name,
            "description": description,
            "regionId": region_id,
            "placementPolicy": placement_policy,
            "tags": tags,
            "tagsToMatch": tags_to_match
        }
        return cls(session._request(f'{session.baseurl}{uri}', request_method='POST', json=body))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/zones/{id}'
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')