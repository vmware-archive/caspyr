import requests
import json
import os
import sys

class Image(object):
    def __init__(self, image):
        try:
            self.os_family=image['osFamily']
        except:
            KeyError
        self.external_region_id=image['externalRegionId']
        self.is_private=image['isPrivate']
        self.external_id=image['externalId']
        self.name=image['name']
        self.description=image['description']
        self.id=image['id']
        self.updated_at=image['updatedAt']
        self._links=image['_links']

    @classmethod
    def describe(cls, session, image, region):
        uri = f'/iaas/fabric-images?$filter=(name eq {image}) and (externalRegionId eq {region})'
        j = session._request(f'{session.baseurl}{uri}')['content'][0]
        return cls(j)