class Region(object):
    """
    Class for Region methods.
    Used to discover regions for all fabric constructs (images, mappings,
    networks and storage.)
    """
    def __init__(self,
                 region
                 ):
        self.external_region_id = region['externalRegionId']
        self.id = region['id']
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
        return cls(session._request(f'{session.baseurl}{uri}'))

    def describe_by_name(self, session, name):
        uri = f'/iaas/regions/?$filter=(externalRegionId eq \'{name}\')'
        j = session._request(f'{session.baseurl}{uri}')
        return j
