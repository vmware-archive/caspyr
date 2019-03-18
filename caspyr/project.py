# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0


class Project(object):
    """
    Class for Project methods
    """

    def __init__(self, project):
        try:
            self.administrators = project['administrators']
        except KeyError:
            pass
        try:
            self.members = project['members']
        except KeyError:
            pass
        try:
            self.zones = project['zones']
        except KeyError:
            pass
        self.name = project['name']
        try:
            self.description = project['description']
        except KeyError:
            pass
        self.id = project['id']
        self.organization_id = project['organizationId']
        self._links = project['_links']

    @classmethod
    def list(cls, session):
        uri = '/iaas/api/projects'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/projects/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @classmethod
    def find_by_name(cls, session, name):
        j = cls.list(session)
        for i in j:
            d = cls.describe(session, i['id'])
            if d.name.lower() == name.lower():
                return d

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/projects/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @classmethod
    def removezones(cls,
                    session,
                    id
                    ):
        uri = f'/iaas/api/projects/{id}'
        payload = {}
        payload['zoneAssignmentConfigurations'] = []
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='PATCH',
                                    payload=payload
                                    ))

    @classmethod
    def removemembers(cls,
                      session,
                      id):
        uri = f'/iaas/api/projects/{id}'
        payload = {}
        payload['members'] = []
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='PATCH',
                                    payload=payload
                                    ))

    @classmethod
    def removeadmins(cls, session, id):
        uri = f'/iaas/api/projects/{id}'
        payload = {}
        payload['administrators'] = []
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='PATCH',
                                    payload=payload
                                    ))

    @classmethod
    def create(cls,
               session,
               name,
               description=None,
               administrators=None,
               members=None,
               zone_configs=None
               ):
        """
        Creates a new project with the provided parameters.
        :param session: [description]
        :type session: [type]
        :param name: [description]
        :type name: [type]
        :param description: [description], defaults to None
        :param description: [type], optional
        :param administrators: [description], defaults to None
        :param administrators: [type], optional
        :param members: [description], defaults to None
        :param members: [type], optional
        :param zone_configs: Defaults to None.
        [
            {
            "zoneId": "77ee1",
            "priority": 1,
            "maxNumberInstances": 50
            }
        ]
        :param zone_configs: List of objects, optional.
        :return: [description]
        :rtype: [type]
        """

        uri = '/iaas/api/projects/'
        payload = {
                "name": name,
                "description": description,
                "administrators": administrators,
                "members": members,
                "zoneAssignmentConfigurations": zone_configs
                }
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))
