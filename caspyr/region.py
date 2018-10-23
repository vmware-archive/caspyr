import requests
import json
import os
import sys

class Region(object):
    """
    Class for Region methods.
    Used to discover regions for all fabric constructs (images, mappings, networks and storage.)
    """
    def _init__(self, region):
        self.external_region_id = region['externalRegionId']
        self.id = region['id']
        self.self_link = region['selfLink']
        self.updated_at = region['updatedAt']
        self._links = region['_links']

    @staticmethod
    def list(session):
        uri = f'/iaas/regions'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/regions/{id}'
        j = session._request(f'{session.baseurl}{uri}')
        return cls(j)

    @classmethod
    def describe_by_name(cls, session, name):
        uri = f'/iaas/regions/?$filter=externalRegionId eq {name}'
        j = session._request(f'{session.baseurl}{uri}')
        return j